"""Main Module to download financial data via ANS codes."""

from typing import List, Union, Optional
import pandas as pd

from ans_wrapper.download_utils import download_and_extract_csv

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/"

# "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2021/4T2021.zip"

class DemonstracoesContabeis:
    ENDPOINT = "demonstracoes_contabeis/"
    DEM_CONTABEIS_ENDPOINT = BASE_URL + ENDPOINT
    FILENAME = "{quarter}T{year}.zip"

    def download_info(self,
                      year=None,
                      quarter=None):
        """Download Financial Info for a given quarter"""

        filename = self.FILENAME.format(quarter=quarter, year=year)

        request_url = self.DEM_CONTABEIS_ENDPOINT + str(year) + "/" + filename

        download_and_extract_csv(request_url)

    def get_info(self, 
                 quarters: Union[str, List[str]],
                 company: Optional[Union[str, int, List[Union[str, int]]]] = None) -> pd.DataFrame:
        """
        Download and filter financial data for specified companies and quarters.
        
        Args:
            quarters: Quarter(s) in format "1T2024", "2T2023", etc.
            company: ANS code(s) to filter by (str, int, or list). If None, returns full dataset.
            
        Returns:
            pd.DataFrame: Filtered financial data
        """
        # Parse quarters parameter to ensure it's a list
        if isinstance(quarters, str):
            quarters_list = [quarters]
        else:
            quarters_list = quarters
        
        # Parse company parameter and convert to integers
        if company is None:
            company_list = None
        elif isinstance(company, (str, int)):
            company_list = [int(company)]
        else:
            # Convert all elements to integers
            company_list = [int(c) for c in company]
        
        # Download CSV files for each quarter
        csv_paths = []
        for quarter in quarters_list:
            # Extract year and quarter number from format like "1T2024"
            if 'T' not in quarter:
                raise ValueError(f"Invalid quarter format: {quarter}. Expected format: '1T2024'")
            
            quarter_num, year = quarter.split('T')
            filename = self.FILENAME.format(quarter=quarter_num, year=year)
            request_url = self.DEM_CONTABEIS_ENDPOINT + str(year) + "/" + filename
            
            try:
                csv_path = download_and_extract_csv(request_url)
                csv_paths.append(csv_path)
            except Exception as e:
                print(f"Failed to download data for {quarter}: {e}")
                continue
        
        if not csv_paths:
            raise ValueError("No data could be downloaded for the specified quarters")
        
        # Load and combine all CSV files
        dataframes = []
        for csv_path in csv_paths:
            # Use semicolon separator and handle quoted values
            df = pd.read_csv(csv_path, sep=';', quotechar='"')
            dataframes.append(df)
        
        # Combine all dataframes
        combined_df = pd.concat(dataframes, ignore_index=True)
        
        # Filter by company codes if specified
        if company_list is not None:
            if 'REG_ANS' not in combined_df.columns:
                raise ValueError("REG_ANS column not found in the dataset")
            
            # idk, I'm adding this just in case REG_ANS is not an integer
            combined_df['REG_ANS'] = combined_df['REG_ANS'].astype(int)

            # Check if all the company codes the user wants are on the dataset
            missing_codes = [code for code in company_list
                             if code not in combined_df['REG_ANS'].unique()]

            if missing_codes:
                raise ValueError(f"Company code(s) not found in dataset: {missing_codes}")

            filtered_df = combined_df[combined_df['REG_ANS'].isin(company_list)]
            
            if filtered_df.empty:
                print(f"Warning: No data found for companies {company_list}")
            
            return filtered_df
        
        return combined_df
    

if __name__ == "__main__":
    dem = DemonstracoesContabeis()

    # Example usage of get_info function
    # Get full dataset for specific quarters
    df_full = dem.get_info(quarters="1T2025", company=None)
    print("Full dataset shape:", df_full.shape)
    print("Columns:", list(df_full.columns))
    
    # Get filtered dataset for specific companies (using real company codes)
    # Can use strings, integers, or mixed
    df_filtered = dem.get_info(quarters="1T2025", company=["477", 515])
    print("Filtered dataset shape:", df_filtered.shape)




