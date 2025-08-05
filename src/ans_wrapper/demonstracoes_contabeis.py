"""Main Module to download financial data via ANS codes."""

from ans_wrapper.download_utils import download_and_extract_csv

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/"

# "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2021/4T2021.zip"

class DemonstracoesContabeis:
    ENDPOINT = "demonstracoes_contabeis/"
    DEM_CONTABEIS_ENDPOINT = BASE_URL + ENDPOINT

    FILENAME = "pda-024-icb-{state_sigla}-{year}_{month}.zip"
    FILENAME = "{quarter}T{year}.zip"

    def download_info(self,
                      year=None,
                      quarter=None):
        """Download Financial Info for a given quarter"""

        filename = self.FILENAME.format(quarter=quarter, year=year)

        request_url = self.DEM_CONTABEIS_ENDPOINT + str(year) + "/" + filename

        download_and_extract_csv(request_url)

    



if __name__ == "__main__":
    dem = DemonstracoesContabeis()

    df = dem.download_info(
        ans_code=None,
        year="2025",
        quarter="1"
    )




