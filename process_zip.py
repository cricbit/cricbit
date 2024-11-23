import json
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

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(set_redis, filename.split('.')[0], json.loads(content)) 
                   for filename, content in json_files.items()]
        
        match_ids = [filename.split('.')[0] for filename in json_files.keys()]
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f'An error occurred: {exc}')
    
    return match_ids
