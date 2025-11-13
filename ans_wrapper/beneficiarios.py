"""
Modulo de Beneficiários
"""

from datetime import datetime
from typing import List, Union

import pandas as pd

from ans_wrapper.utils import parse_url_links, download_and_extract_csv
from ans_wrapper.enums import BRAZILIAN_STATE_CODES, STATE_CODES

from utils import generate_month_range, concat_csv_files


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


    def build_dataset(
            self,
            states: Union[STATE_CODES, List[STATE_CODES]],
            target_date: str = None,
            start=None,
            end=None,
            output_name="resulting_dataset",
            in_chunks=False,
            chunk_size=100_000
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
        csv_paths = self.download_raw_data(states, dates)

        concat_csv_files(
            csv_paths=csv_paths,
            output_path=output_name,
        )

        if in_chunks:
            return pd.read_csv(output_name, chunksize=chunk_size, delimiter=";") 
        else:
            return pd.read_csv(output_name, delimiter=";") 


    def download_raw_data(
            self,
            states: STATE_CODES | list[STATE_CODES], 
            dates: str | list[str]
            ) -> str:
        """
        Download raw, unaltered datasets from the ANS server

        Args:
            states: A list of state codes.
            dates: List of dates in the "YYYYMM" format.
        
        Returns:
            str: The path to the downloaded csv files.
        
        """
        # Checking argument types first
        if isinstance(states, str): states = [states]
        if isinstance(dates, str): dates = [dates]

        # Forming urls
        file_paths = []
        for state in states:
            for date in dates:
                year, month = date[:4], date[4:]
                cur_file_name = self.FILENAME.format(
                    state_sigla=state, year=year, month=month
                )
                cur_file_path = date + "/" + cur_file_name
                file_paths.append(cur_file_path)

        # Downloading CSVs
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

