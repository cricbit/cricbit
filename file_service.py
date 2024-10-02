import io
import requests

from process_zip import upload_matches_zip

MATCHES_DIR = 'data/matches/'

class MatchDataManager:
    """Handles downloading and loading match data files."""

    def __init__(self, matches_dir=MATCHES_DIR):
        self.matches_dir = matches_dir

    def download_and_extract_matches(self, matches_url):
        response = requests.get(matches_url)
        zip_file = io.BytesIO(response.content)
        match_ids = upload_matches_zip(zip_file)
        return match_ids

async def extract_files(url):
    match_data_manager = MatchDataManager()

    match_ids = match_data_manager.download_and_extract_matches(url)

    return match_ids
