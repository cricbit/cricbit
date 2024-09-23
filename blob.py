import os
import requests
import zipfile
import re

from concurrent.futures import ThreadPoolExecutor, as_completed

BLOB_READ_WRITE_TOKEN = os.environ['BLOB_READ_WRITE_TOKEN']
VERCEL_API_URL = "https://blob.vercel-storage.com"

def zip_to_json_files(zip_path: str) -> dict:
    result = {}
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for info in zip_ref.infolist():
            filename = info.filename
            if re.search(r'json$', filename):
                content = zip_ref.read(filename).decode('utf-8')
                result[filename] = content
    return result

def put(pathname: str, body: str) -> dict:
    headers = {
        "access": "public",
        "authorization": f"Bearer {BLOB_READ_WRITE_TOKEN}",
        "x-api-version": "4",
        "x-add-random-suffix": "false"
    }
    _resp = requests.put(f"{VERCEL_API_URL}/{pathname}", data=body, headers=headers)
    return _resp.json()

def upload_matches_zip(zip_path: str) -> list:
    json_files = zip_to_json_files(zip_path)
    uploaded_file_urls = []

    with ThreadPoolExecutor() as executor:
        future_to_filename = {executor.submit(put, f"data/{filename}", content): filename
                              for filename, content in json_files.items()}
        
        for future in as_completed(future_to_filename):
            filename = future_to_filename[future]
            try:
                result = future.result()
                uploaded_file_urls.append(result)
            except Exception as exc:
                print(f'{filename} generated an exception: {exc}')

    return uploaded_file_urls

def read_file(file_url: str) -> str:
    headers = {
        "access": "public",
        "authorization": f"Bearer {BLOB_READ_WRITE_TOKEN}",
        "x-api-version": "4",
    }
    _resp = requests.get(f"{file_url}", headers=headers)
    return _resp.json()
