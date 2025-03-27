from typing import Optional, Dict
import requests

from domains.player_info import PlayerInfo

class ScraperService:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.url = "http://core.espnuk.org/v2/sports/cricket/athletes/"

    async def scrape_player_data(self, player_id: str, cricinfo_id: int) -> Optional[Dict]:
        try:
            response = requests.get(self.url + str(cricinfo_id))

            data = response.json()

            batting_styles = []
            bowling_styles = []
            styles = data['styles']
            for style in styles:
                if style['type'] == 'batting':
                    batting_styles.append(style['description'])
                if style['type'] == 'bowling':
                    bowling_styles.append(style['description'])

            national_team = requests.get(data['team']['$ref']).json()['name']

            player_data = {
                'name': data['name'],
                'dob': data['dateOfBirth'],
                'batting_styles': batting_styles,
                'bowling_styles': bowling_styles,
                'playing_role': data['position']['name'],
                'image_url': data['headshot']['href'],
                'is_active': data['isActive'],
                'gender': data['gender'],
                'national_team': national_team,
            }

            await self.db_manager.upsert_player(player_id, player_data)

            return player_data
        except Exception as e:
            print(f"Error scraping player {player_id}: {e}")
            return None


