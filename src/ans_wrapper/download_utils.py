import requests

TEST_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/informacoes_consolidadas_de_beneficiarios-024/202505/pda-024-icb-AC-2025_05.zip"


def download_archive(url):
    """Faz o download de um arquivo da web"""
    response = requests.get(url)
    response.raise_for_status()


import os

import requests


def download_zip(url, output_dir="ans_downloads"):
    """Download a ZIP file from the web and save it locally in 'ans_downloads' folder."""
    os.makedirs(output_dir, exist_ok=True)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    filename = url.split("/")[-1]
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"ZIP file saved at: {filepath}")
    return filepath


print("inicio")
download_zip(TEST_URL)
print("fimm")
