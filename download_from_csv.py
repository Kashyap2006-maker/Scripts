import pandas as pd
import requests
import os
from urllib.parse import urlparse


def download_files_from_csv(csv_path, url_col, name_col, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {csv_path} -> {e}")
        return
    for index, row in df.iterrows():
        url = row[url_col]
        filename_base = str(row[name_col]).strip()
        if pd.isna(url):
            continue
        try:
            parsed_url = urlparse(url)
            extension = os.path.splitext(parsed_url.path)[1]
            full_filename = f"{filename_base}{extension}"
            save_path = os.path.join(output_folder, full_filename)
            response = requests.get(url, stream=True, timeout=10)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Successfully downloaded: {save_path}")
            else:
                print(f"Failed to download {url}: Status {response.status_code}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")


# --- Configuration ---
# Set your input and output root folders
INPUT_ROOT = "input_root"  # Change as needed
OUTPUT_ROOT = "output_root"  # Change as needed
LINK_COLUMN = 'Link'       # The column header containing the URL
NAME_COLUMN = 'FileName'   # The column header for the new filename

def process_all_csvs(input_root, output_root, url_col, name_col):
    for current_dir, dirs, files in os.walk(input_root):
        rel_dir = os.path.relpath(current_dir, input_root)
        output_dir = os.path.join(output_root, rel_dir)
        for file in files:
            if file.lower().endswith('.csv'):
                csv_path = os.path.join(current_dir, file)
                print(f"Processing CSV: {csv_path}")
                download_files_from_csv(csv_path, url_col, name_col, output_dir)

if __name__ == "__main__":
    process_all_csvs(
        input_root=INPUT_ROOT,
        output_root=OUTPUT_ROOT,
        url_col=LINK_COLUMN,
        name_col=NAME_COLUMN
    )