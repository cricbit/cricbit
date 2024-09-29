from sqlalchemy import Column, Integer, String, ForeignKey

from domains.base import Base

class PlayingXI(Base):
    __tablename__ = 'playing_xi'
    __license__ = """
    This data is provided under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) license.

    You are free to:
    - Share: copy and redistribute the material in any medium or format
    - Adapt: remix, transform, and build upon the material

    Under the following terms:
    - Attribution: You must give appropriate credit to Cricsheet (https://cricsheet.org/), 
      provide a link to the license, and indicate if changes were made.
    - NonCommercial: You may not use the material for commercial purposes.
    - ShareAlike: If you remix, transform, or build upon the material, you must distribute 
      your contributions under the same license as the original.
    """

    match_id = Column(Integer, ForeignKey('match_details.match_id'), primary_key=True)
    player_id = Column(String, primary_key=True)
    player_name = Column(String)
    team_name = Column(String)

    def __init__(self, match_id, player_id, player_name, team_name):
        self.match_id = match_id
        self.player_id = player_id
        self.player_name = player_name
        self.team_name = team_name

    def __repr__(self):
        return f"<PlayingXI(match_id={self.match_id}, player_id={self.player_id}, player_name={self.player_name}, team_name={self.team_name})>"
