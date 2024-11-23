import json
import os
import re
import zipfile

from concurrent.futures import ThreadPoolExecutor, as_completed

from redis_resource import set_redis

def zip_to_json_files(zip_path: str) -> dict:
    result = {}
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for info in zip_ref.infolist():
            filename = info.filename
            if re.search(r'json$', filename):
                content = zip_ref.read(filename).decode('utf-8')
                result[filename] = content
    return result

def upload_matches_zip(zip_path: str) -> list:
    json_files = zip_to_json_files(zip_path)

    match_ids = [filename.split('.')[0] for filename in json_files.keys()]
    for match_id, content in zip(match_ids, json_files.values()):
        try:
            set_redis(match_id, json.loads(content))
        except Exception as exc:
            print(f'An error occurred: {exc}')
    
    return match_ids
