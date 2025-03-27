import io
import asyncio
from typing import List, Optional
import requests
import pandas as pd
from datetime import datetime
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

    async def process_players_url(self) -> Optional[List[int]]:
        try:
            players_url = "https://www.cricsheet.org/register/people.csv"
            names_url = "https://www.cricsheet.org/register/names.csv"

            players_response = requests.get(players_url)
            names_response = requests.get(names_url)

            players_response.raise_for_status()
            names_response.raise_for_status()
            
            # Read CSV data into pandas DataFrame
            players_df = pd.read_csv(io.StringIO(players_response.text))
            names_df = pd.read_csv(io.StringIO(names_response.text))

            players_df = players_df.merge(names_df, on='identifier', how='left', suffixes=('', '_complete'))

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
                    try:
                        task = self.db_manager.add_player(row['identifier'], row)
                        tasks.append(task)
                    except Exception as e:
                        print(f"Error creating task for player {row['identifier']}: {e}")
                
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