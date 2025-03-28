import io
import asyncio
from typing import List, Optional
import requests
import pandas as pd
from datetime import datetime
from .zip_processor import ZipProcessor

from services.web.scraper import ScraperService

class FileService:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.zip_processor = ZipProcessor(db_manager)
        self.scraper_service = ScraperService(db_manager)

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

    def _get_cricinfo_key(self, row) -> int:
        """Get the cricinfo key from either key_cricinfo_2 or key_cricinfo."""
        for key in ['key_cricinfo_2', 'key_cricinfo']:
            if not pd.isna(row[key]):
                return int(row[key])
        return 0

    async def process_players_url(self) -> Optional[List[int]]:
        try:
            players_url = "https://www.cricsheet.org/register/people.csv"

            players_response = requests.get(players_url)
            players_response.raise_for_status()
            
            # Read CSV data into pandas DataFrame
            players_df = pd.read_csv(io.StringIO(players_response.text))

            players_count = await self.db_manager.get_players_count()

            if players_count == len(players_df):
                print("No new players to process")
                return None

            # Process players in smaller batches of 20
            batch_size = 20
            total_processed = 0
            for i in range(0, len(players_df), batch_size):
                batch = players_df.iloc[i:i + batch_size]
                tasks = []
                for _, row in batch.iterrows():
                    identifier = row['identifier']
                    key_cricinfo = self._get_cricinfo_key(row)
                    
                    async def process_player(identifier=identifier, key_cricinfo=key_cricinfo):
                        try:
                            if await self.db_manager.player_exists(identifier):
                                print(f"Player {identifier} already exists in db")
                                return False

                            if key_cricinfo:
                                player_data = await self.scraper_service.scrape_player_data(identifier, key_cricinfo)
                                return await self.db_manager.add_player(identifier, player_data)
                            else:
                                print(f"No key_cricinfo for player {identifier}")
                                return False
                        except Exception as e:
                            print(f"Error processing player {identifier}: {e}")
                            return False

                    tasks.append(process_player())
                
                if tasks:
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    successful = sum(1 for r in results if r is True)
                    total_processed += successful
                    print(f"Processed batch {i//batch_size + 1}: {successful}/{len(tasks)} players added successfully")
                    print(f"Total processed: {total_processed} players")
                    
                    # Add a small delay between batches to prevent overwhelming the database
                    if i + batch_size < len(players_df):
                        await asyncio.sleep(0.5)

            print(f"Finished processing players. Total added: {total_processed}")
            return list(range(total_processed))

        except requests.RequestException as e:
            print(f"Error downloading file: {e}")
            return None

        except Exception as e:
            print(f"Error processing players: {e}")
            return None