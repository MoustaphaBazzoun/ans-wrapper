"""download financial data of any healthcare company registered in ANS .

This module provides functionality to download and process financial statements
from the Brazilian National Health Agency (ANS). It provides two statements:
Balance sheets and income statements.
"""

from typing import List, Optional, Union

import pandas as pd

from ans_wrapper.utils import download_and_extract_csv, DownloadError

# Base URL for ANS open data portal
BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/"

# Example URL format:
# "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2021/4T2021.zip"


class DemonstracoesContabeis:
    """A class to download and process financial statements from ANS.

    This class provides methods to download quarterly financial data for health
    plan operators and filter the data by specific companies using ANS codes.
    """

    ENDPOINT: str = "demonstracoes_contabeis/"
    DEM_CONTABEIS_ENDPOINT: str = BASE_URL + ENDPOINT
    FILENAME: str = "{quarter}T{year}.zip"

    def get_info(
        self,
        quarters: Union[str, List[str]],
        company: Optional[Union[str, int, List[Union[str, int]]]] = None,
    ) -> pd.DataFrame:
        """
        Download and filter financial data for specified companies and quarters.

        This method downloads CSV files for the specified quarters, combines them,
        and optionally filters by company ANS codes. The data is expected to have
        a 'REG_ANS' column containing the ANS registration codes.

        Args:
            quarters: Quarter(s) in format "1T2024", "2T2023", etc. Can be a single
                     string or a list of strings.
            company: ANS code(s) to filter by. Can be a single code (str/int) or a
                    list of codes. If None, returns the full dataset for all companies.

        Returns:
            pd.DataFrame: Filtered financial data with columns including REG_ANS

        Raises:
            ValueError: If quarter format is invalid, no data could be downloaded,
                       REG_ANS column is missing, or company codes are not found
            Exception: If CSV reading or processing fails
        """
        # Parse quarters parameter to ensure it's a list
        if isinstance(quarters, str):
            quarters_list = [quarters]
        else:
            quarters_list = quarters

        # Parse company parameter and convert to integers
        company_list = None
        if company is not None:
            if isinstance(company, (str, int)):
                company_list = [int(company)]
            else:
                # Convert all elements to integers
                company_list = [int(c) for c in company]

        # Download CSV files for each quarter
        csv_paths = []
        for quarter in quarters_list:
            # Extract year and quarter number from format like "1T2024"
            if "T" not in quarter:
                raise ValueError(
                    f"Invalid quarter format: {quarter}. Expected format: '1T2024'"
                )

            quarter_num, year = quarter.split("T")
            filename = self.FILENAME.format(quarter=quarter_num, year=year) 
            request_url = (
                self.DEM_CONTABEIS_ENDPOINT + str(year) + "/" + filename
            )

            try:
                csv_path = download_and_extract_csv(request_url)
                csv_paths.append(csv_path)
            except Exception as e:
                raise DownloadError(f"Failed to download data for {quarter}: {e}") # NOTE: Maybe raise exception and interrupt function here...

        if not csv_paths:
            raise ValueError(
                "No data could be downloaded for the specified quarters"
            )

        # Load and combine all CSV files
        dataframes = []
        for csv_path in csv_paths:
            try:
                # Use semicolon separator and handle quoted values
                df = pd.read_csv(csv_path, sep=";", quotechar='"')
                dataframes.append(df)
            except Exception as e:
                print(f"Failed to read CSV file {csv_path}: {e}")
                continue

        if not dataframes:
            raise ValueError("No CSV files could be successfully read")

        # Combine all dataframes
        combined_df = pd.concat(dataframes, ignore_index=True)

        # Filter by company codes if specified
        if company_list is not None:
            if "REG_ANS" not in combined_df.columns:
                raise ValueError("REG_ANS column not found in the dataset")

            # NOTE: IDK, I'm adding this just in case REG_ANS is not an integer
            combined_df["REG_ANS"] = combined_df["REG_ANS"].astype(int)

            # Check if all the company codes the user wants are in the dataset
            available_codes = combined_df["REG_ANS"].unique()
            missing_codes = [
                code for code in company_list if code not in available_codes
            ]

            if missing_codes:
                raise ValueError(
                    f"Company code(s) not found in dataset: {missing_codes}"
                )

            filtered_df = combined_df[combined_df["REG_ANS"].isin(company_list)]

            if filtered_df.empty:
                print(f"Warning: No data found for companies {company_list}")

            return filtered_df

        return combined_df

