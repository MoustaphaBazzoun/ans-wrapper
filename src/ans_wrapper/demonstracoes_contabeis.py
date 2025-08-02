
BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/"

# "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2021/4T2021.zip"

class DemonstracoesContabeis:
    ENDPOINT = "demonstracoes_contabeis/"
    DEM_CONTABEIS_ENDPOINT = BASE_URL + ENDPOINT

    FILENAME = "pda-024-icb-{state_sigla}-{year}_{month}.zip"
    FILENAME = "{quarter}T{year}.zip"

    def download_info(self,
                      ans_code=None,
                      year=None,
                      quarter=None):
        """Download Financial Info for a given ANS code"""

        filename = self.FILENAME.format(quarter=quarter, year=year)
        request_url = self.DEM_CONTABEIS_ENDPOINT + str(year) + filename





