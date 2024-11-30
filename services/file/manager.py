import io
from typing import List, Optional
import requests
from .zip_processor import ZipProcessor

class FileService:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.zip_processor = ZipProcessor(db_manager)

    async def process_matches_url(self, url: str) -> Optional[List[int]]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            zip_file = io.BytesIO(response.content)
            return await self.zip_processor.process_zip(zip_file)
        except requests.RequestException as e:
            print(f"Error downloading file: {e}")
            return None
        except Exception as e:
            print(f"Error processing matches: {e}")
            return None
