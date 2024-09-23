import io
import json
import os
import re
import requests
import sqlalchemy
import zipfile

from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

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
        with open(json_path, 'r') as file:
            match_data = json.loads(file.read())
            match_id = os.path.basename(json_path).split('.')[0]
            try:
                with self.session_scope() as session:
                    session.execute(text('''
                        INSERT INTO raw_match_info (match_id, match_data, deliveries)
                        VALUES (:match_id, :match_data, :deliveries)
                    '''), {'match_id': match_id, 'match_data': json.dumps(match_data['info']), 'deliveries': json.dumps(match_data['innings'])})
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
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            for info in zip_ref.infolist():
                filename = info.filename
                if re.search(r'json$', filename):
                    zip_ref.extract(info, self.matches_dir)

    def load_files_to_db(self):
        files = os.listdir(self.matches_dir)
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.db_manager.insert_file_data, os.path.join(self.matches_dir, file)) for file in files]
            for future in futures:
                future.result()

def main(url):
    if url:
        db_manager = DatabaseManager(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
        match_data_manager = MatchDataManager(db_manager)

        # Download matches and process data
        match_data_manager.download_and_extract_matches(url)
        match_data_manager.load_files_to_db()

        return {
            'statusCode': 200,
            'body': 'Matches downloaded and data loaded successfully.'
        }
    else:
        return {
            'statusCode': 400,
            'body': 'URL not provided.'
        }
