"""
Modulo de Beneficiários
"""

from datetime import datetime
from typing import List, Union

import pandas as pd

from ans_wrapper.download_utils import parse_url_links, download_and_extract_csv
from ans_wrapper.enums import BRAZILIAN_STATE_CODES, STATE_CODES

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/"


class Beneficiarios:
    ENDPOINT = "informacoes_consolidadas_de_beneficiarios-024/"
    __BENEFICIARIOS_URL = BASE_URL + ENDPOINT
    FILENAME = "pda-024-icb-{state_sigla}-{year}_{month}.zip"

    def __init__(self):
        self.available_months = self._fetch_available_months()


    @property
    def date_range(self):
        """Range of available data"""
        if not self.available_months:
            return "No data available"

        start = (datetime.strptime(self.available_months[0], "%Y%m")
                         .strftime("%b %Y"))

        end = (datetime.strptime(self.available_months[-1], "%Y%m")
                       .strftime("%b %Y"))

        return f"data available from {start} to {end}"


    @property
    def info(self) -> str:
        return (
            f"Beneficiários data available:\n"
            f"📅 {self.date_range}\n"
            f"📦 {len(self.available_months)} months available\n"
            f"🔗 Source: {self.__BENEFICIARIOS_URL}"
        )


    # Main function of this class
    # TODO: Work in Progress, concat can be more efficient
    def build_dataset(
        self,
        states: Union[STATE_CODES, List[STATE_CODES]],
        target_date: str = None,
        start=None,
        end=None,
    ) -> pd.DataFrame:
        """Create a dataset using customized configs."""
        # 1. CHECKS ---------------
        # Checking date args
        if ((target_date and (start or end)) or 
            (not target_date and not (start and end))):
            raise ValueError(
                "provide either `target_date` or both `start` and `end`, not both."
            )

        # checking states
        if isinstance(states, str):
            states = [states]

        for state in states:
            if state not in BRAZILIAN_STATE_CODES:
                raise ValueError(
                    f"invalid state: {state}, allowed states are: {BRAZILIAN_STATE_CODES}"
                )

        # Creating a list of dates
        dates = [target_date] if target_date else generate_month_range(start, end)

        # 2. DOWNLOADING ---------------
        print(dates, states)
        csv_paths = self.download_raw_data(states, dates)
        # combined_df_path = concat_datasets(csv_paths)
        # df = pd.read_csv(combined_df_path, delimiter=";")
        # print(df.head())
        print(csv_paths)
        concat_csv_files(
            csv_paths=csv_paths,
            output_path="combined.csv",
        )


    def download_raw_data(self, states: list, dates: list) -> str:
        """Download raw, unaltered datasets from the ANS server"""
        file_paths = []
        for state in states:
            for date in dates:
                year, month = date[:4], date[4:]
                cur_file_name = self.FILENAME.format(
                    state_sigla=state, year=year, month=month
                )
                cur_file_path = date + "/" + cur_file_name
                file_paths.append(cur_file_path)

        csv_paths = []
        for urls in file_paths:
            cur_url = self.__BENEFICIARIOS_URL + urls
            print(cur_url)
            csv_path = download_and_extract_csv(cur_url)
            csv_paths.append(csv_path)

        return csv_paths


    def _fetch_available_months(self) -> List[str]:
        """
        Fetches the list of available months from the beneficiários folder.

        Returns:
                List[str]: A sorted list of strings in the format 'YYYYMM',
                                   representing each available monthly folder on the server.
        """
        # Fetching the page data
        list_of_links = parse_url_links(self.__BENEFICIARIOS_URL)

        # Parsing and cleaning links
        list_of_dates = []
        for link in list_of_links:
            href = link["href"]
            # if it's a folder and name starts with a 6-digit date
            if href.endswith("/") and href[:6].isdigit():
                list_of_dates.append(href.strip("/"))

        return list_of_dates


from dateutil.relativedelta import relativedelta


def generate_month_range(start: str, end: str) -> list[str]:
    """Generates a range of dates with monthly frequency."""
    start_date = datetime.strptime(start, "%Y%m")
    end_date = datetime.strptime(end, "%Y%m")

    date_range = []
    cur = start_date

    while cur <= end_date:
        date_range.append(cur.strftime("%Y%m"))
        cur += relativedelta(months=1)

    return date_range


# ------------------------------------------------------------------------------

# Not Being Used
def concat_datasets(list_of_datasets):
    output_file = "combined_dataset.csv"
    first_chunk = True  # Track if it's the first chunk being written

    for file_path in list_of_datasets:
        print(f"Processing {file_path}...")

        for chunk in pd.read_csv(file_path, chunksize=100_000):
            mode = "w" if first_chunk else "a"
            chunk.to_csv(
                output_file, mode=mode, header=first_chunk, index=False
            )
            first_chunk = False

import pandas as pd

def concat_csv_files(csv_paths, output_path, chunksize=100_000):
    """
    Concatenate multiple large CSV files with ';' as delimiter.
    Works efficiently in chunks to avoid memory issues.
    """
    header_written = False

    with open(output_path, "w", encoding="utf-8", newline="") as f_out:
        for path in csv_paths:
            try:
                for chunk in pd.read_csv(
                    path,
                    sep=";",                # ✅ use semicolon
                    chunksize=chunksize,     # ✅ read in small chunks
                    low_memory=False,
                    encoding="utf-8",
                    on_bad_lines="skip"      # ✅ skip malformed rows
                ):
                    chunk.to_csv(
                        f_out,
                        sep=";",              # ✅ keep same delimiter
                        index=False,
                        header=not header_written,
                        mode="a"
                    )
                    header_written = True
            except Exception as e:
                print(f"⚠️ Skipping {path} due to error: {e}")
    
    return str(output_path)
