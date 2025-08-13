"""
Modulo de Beneficiários
"""

from datetime import datetime
from typing import List, Literal, Union

import pandas as pd
import requests

from ans_wrapper.beneficiarios_utils import parse_url_links
from ans_wrapper.download_utils import download_and_extract_csv
from ans_wrapper.enums import BRAZILIAN_STATE_CODES, STATE_CODES

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/"


class Beneficiarios:
    ENDPOINT = "informacoes_consolidadas_de_beneficiarios-024/"
    BENEFICIARIOS_URL = BASE_URL + ENDPOINT
    FILENAME = "pda-024-icb-{state_sigla}-{year}_{month}.zip"

    def __init__(self):
        self.available_months = self._fetch_available_months()

    @property
    def date_range(self):
        """Range of available data"""
        if not self.available_months:
            return "No data available"

        start = datetime.strptime(self.available_months[0], "%Y%m").strftime(
            "%b %Y"
        )

        end = datetime.strptime(self.available_months[-1], "%Y%m").strftime(
            "%b %Y"
        )

        return f"data available from {start} to {end}"

    @property
    def info(self) -> str:
        return (
            f"Beneficiários data available:\n"
            f"📅 {self.date_range}\n"
            f"📦 {len(self.available_months)} months available\n"
            f"🔗 Source: {self.BENEFICIARIOS_URL}"
        )

    def build_dataset(
        self,
        states: Union[STATE_CODES, List[STATE_CODES]],
        target_date: str = None,
        start=None,
        end=None,
    ) -> pd.DataFrame:
        """Create a dataset using customized configs."""
        # Checking date args
        if target_date and (start or end):
            raise ValueError(
                "provide either `target_date` or both `start` and `end`, not both."
            )
        if not target_date and not (start and end):
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

        dates = target_date if target_date else generate_month_range(start, end)

        csv_paths = self.download_raw_data(states, dates)
        print(csv_paths)
        print(dates, states)

    def download_raw_data(self, states: list, dates: list):
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
            cur_url = self.BENEFICIARIOS_URL + urls
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
        list_of_links = parse_url_links(self.BENEFICIARIOS_URL)

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


if __name__ == "__main__":
    bf = Beneficiarios()
    # print(bf.info)
    # print(bf.date_range)
    # bf.download_raw_data(["AC", "AM"], ["202401", "202404"])
    # bf.build_dataset(states = ["AC", "AM"], start="202305", end="202412")
    bf.build_dataset(states=["AC", "CE"], start="202401", end="202402")
