"""
Collection of download utils to help download,
extract and manipulate zip files and project folders
"""

import os
import zipfile
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from tqdm import tqdm


class DownloadError(Exception):
    pass


# Download Utils ----------


def download_zip(url: str, output_dir="ans_downloads") -> str:
    """
    Download a ZIP file from the web and save it locally in the specified folder.

    Returns:
        str: Full path to the downloaded ZIP file.
    """
    # create directory if it doesn't exist yet
    os.makedirs(output_dir, exist_ok=True)

    # getting the name of the zip file
    filename = url.split("/")[-1]
    # the path where are storing this zip
    filepath = os.path.join(output_dir, filename)

    # downloading the zip file
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))

    # saving it
    with open(filepath, "wb") as f, tqdm(
        total=total_size, unit="B", unit_scale=True, desc=filename
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))

    print(f"ZIP file saved at: {filepath}")
    return filepath


def extract_csv(zip_path, temp_extract_dir="ans_downloads") -> str:
    """
    Extracts the first CSV file from a ZIP archive to a temporary directory.

    Returns:
        str: Full path to the extracted CSV file.

    Raises:
        ValueError: If no CSV is found in the archive.
    """
    os.makedirs(temp_extract_dir, exist_ok=True)

    # From the given zip path. we list all the files inside it and get the csv
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_contents = zip_ref.namelist()
        csv_files = [f for f in zip_contents if f.lower().endswith(".csv")]

        # Raise error if there are no csv files in the zip
        if not csv_files:
            raise ValueError("No CSV file found in the ZIP archive.")

        # There will be only one csv in the list, so we can get it with:
        csv_filename = csv_files[0]

        # TODO: implement try-error here.
        zip_ref.extract(csv_filename, temp_extract_dir)

    extracted_csv_path = os.path.join(temp_extract_dir, csv_filename)
    print(f"CSV extracted: {extracted_csv_path}")

    # removing the zip file
    os.remove(zip_path)

    return extracted_csv_path


def download_and_extract_csv(url):
    zip_file_path = download_zip(url)
    csv_file_path = extract_csv(zip_file_path)
    return csv_file_path


def parse_url_links(url: str) -> list:
    """Parse the paths of a given url"""
    # This returns a html file inside a string
    response = requests.get(url)

    # Parsing the html
    soup = BeautifulSoup(response.content, "html.parser")

    # Parsing all the links
    links = soup.find_all("a")

    return links


# General Utils ----------


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
                    sep=";",
                    chunksize=chunksize,
                    low_memory=False,
                    encoding="utf-8",
                    on_bad_lines="skip",
                ):
                    chunk.to_csv(
                        f_out,
                        sep=";",
                        index=False,
                        header=not header_written,
                        mode="a",
                    )
                    header_written = True
            except Exception as e:
                print(f"Skipping {path} due to error: {e}")

    return str(output_path)
