"""Collection of download utils to help download, extract and manipulate zip files and project folders"""

import os
import shutil
import zipfile

import requests


def download_zip(url, output_dir="ans_downloads"):
    """
    Download a ZIP file from the web and save it locally in the specified folder.

    Returns:
        str: Full path to the downloaded ZIP file.
    """
    os.makedirs(output_dir, exist_ok=True)

    filename = url.split("/")[-1]
    filepath = os.path.join(output_dir, filename)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(filepath, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"ZIP file saved at: {filepath}")
    return filepath


def extract_csv(zip_path, temp_extract_dir="temp_extract"):
    """
    Extracts the first CSV file from a ZIP archive to a temporary directory.

    Returns:
        str: Full path to the extracted CSV file.

    Raises:
        ValueError: If no CSV is found in the archive.
    """
    os.makedirs(temp_extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_contents = zip_ref.namelist()
        csv_files = [f for f in zip_contents if f.lower().endswith(".csv")]

        if not csv_files:
            raise ValueError("No CSV file found in the ZIP archive.")

        csv_filename = csv_files[0]
        zip_ref.extract(csv_filename, temp_extract_dir)

    extracted_csv_path = os.path.join(temp_extract_dir, csv_filename)
    print(f"CSV extracted: {extracted_csv_path}")
    return extracted_csv_path


def move_and_cleanup(csv_path, final_dir="ans_datasets", cleanup_dirs=None):
    """
    Moves the CSV to a final directory and deletes any specified folders/files.

    Returns:
        str: Final path to the moved CSV file.
    """
    os.makedirs(final_dir, exist_ok=True)
    final_csv_path = os.path.join(final_dir, os.path.basename(csv_path))
    shutil.move(csv_path, final_csv_path)

    if cleanup_dirs:
        for path in cleanup_dirs:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

    print(f"Final CSV location: {final_csv_path}")
    return final_csv_path
