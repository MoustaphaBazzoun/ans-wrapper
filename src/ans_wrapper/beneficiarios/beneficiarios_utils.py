import requests
from bs4 import BeautifulSoup

# TODO: maybe remove this in future updates?
BENEFICIARIOS_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/informacoes_consolidadas_de_beneficiarios-024/"

def parse_url_links(url: str) -> list:
    """Parse the paths of a given url"""
    # This returns a html file inside a string
    response = requests.get(url)

    # Parsing the html
    soup = BeautifulSoup(response.content, "html.parser")

    # Parsing all the links
    links = soup.find_all("a")

    return links


def get_link_type():
    raise NotImplementedError("This function is deprecated, might be removed in future updates.")


def download_zip(file_url: str):
    """Download the zipfile"""
    raise NotImplementedError("This function is deprecated, might be removed in future updates.")

