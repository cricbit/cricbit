import io
import json
import os
import requests
import sqlalchemy

from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from blob import upload_matches_zip, read_file

# Load environment variables
load_dotenv()

DB_HOST = os.environ['HOSTNAME']
DB_NAME = os.environ['DATABASE']
DB_USER = os.environ['USER']
DB_PASSWORD = os.environ['PASSWORD']
MATCHES_DIR = 'data/matches/'

class DatabaseManager:
    """Handles all database-related operations."""
    def __init__(self, user, password, host, dbname):
        self.engine = sqlalchemy.create_engine(f"postgresql://{user}:{password}@{host}/{dbname}")

        with self.engine.connect() as connection:
            connection.execute(text('''
                DROP TABLE IF EXISTS raw_match_info CASCADE;
                CREATE TABLE IF NOT EXISTS raw_match_info (
                    match_id INTEGER PRIMARY KEY,
                    match_data JSONB,
                    deliveries JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            connection.commit()
        
    @contextmanager
    def session_scope(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def insert_file_data(self, json_path):
        match_data = read_file(json_path)
        match_id = os.path.basename(json_path).split('.')[0]
        print(f"Processing match {match_id}")
        try:
            with self.session_scope() as session:
                session.execute(text('''
                    INSERT INTO raw_match_info (match_id, match_data, deliveries)
                VALUES (:match_id, :match_data, :deliveries)
            '''),
            {'match_id': match_id, 'match_data': json.dumps(match_data['info']), 'deliveries': json.dumps(match_data['innings'])})
        except IntegrityError:
            print(f"Match with ID {match_id} already exists in the database.")
            return
        
class MatchDataManager:
    """Handles downloading and loading match data files."""
    def __init__(self, db_manager, matches_dir=MATCHES_DIR):
        self.db_manager = db_manager
        self.matches_dir = matches_dir

    def download_and_extract_matches(self, matches_url):
        response = requests.get(matches_url)
        zip_file = io.BytesIO(response.content)
        uploaded_file_urls = upload_matches_zip(zip_file)
        return uploaded_file_urls

    def load_files_to_db(self, file_urls):
        file_urls = file_urls[:2]

        with ThreadPoolExecutor() as executor:
            batch_size = 10  # Adjust this value based on your needs
            for i in range(0, len(file_urls), batch_size):
                batch = file_urls[i:i+batch_size]
                futures = [executor.submit(self.db_manager.insert_file_data, file) for file in batch]
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        print(f"Error processing file: {e}")

def main(url):
    if url:
        db_manager = DatabaseManager(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
        # match_data_manager = MatchDataManager(db_manager)

        # # Download matches and process data
        # file_urls = match_data_manager.download_and_extract_matches(url)
        # match_data_manager.load_files_to_db(file_urls)

        db_manager.insert_file_data('https://unheoqy7ylzzj6ao.public.blob.vercel-storage.com/data/1227593.json')

        return {
            'statusCode': 200,
            'body': 'Matches downloaded and data loaded successfully.'
        }
    else:
        return {
            'statusCode': 400,
            'body': 'URL not provided.'
        }

if __name__ == '__main__':
    main('https://cricsheet.org/downloads/bwt_male_json.zip')