from sqlalchemy import Column, Integer, JSON, String, ForeignKey
from domains.base import Base

class Match(Base):
    __tablename__ = 'stg_matches'
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

    For more details, please visit: https://creativecommons.org/licenses/by-nc-sa/4.0/
    """

    match_id = Column(Integer, ForeignKey('raw_matches.match_id'), primary_key=True)
    series_name = Column(String)
    match_num = Column(Integer)
    match_stage = Column(String)
    match_type = Column(String)
    match_type_num = Column(Integer)
    team_type = Column(String)
    format = Column(String)
    season = Column(Integer)
    player_of_match = Column(String)
    match_dates = Column(JSON)
    num_days = Column(Integer)
    venue = Column(String)
    toss_winner = Column(String)
    toss_decision = Column(String)
    outcome = Column(String)
    team1 = Column(String)
    team2 = Column(String)
    winner = Column(String)
    win_by_wickets = Column(Integer)
    win_by_runs = Column(Integer)
    win_by_innings = Column(Integer)

    def __init__(self, match_id, series_name, match_num, match_stage, match_type, match_type_num, team_type, format, season, player_of_match, match_dates, num_days, venue, toss_winner, toss_decision, outcome, team1, team2, winner, win_by_wickets, win_by_runs, win_by_innings):
        self.match_id = match_id
        self.series_name = series_name
        self.match_num = match_num
        self.match_stage = match_stage
        self.match_type = match_type
        self.match_type_num = match_type_num
        self.team_type = team_type
        self.format = format
        self.season = season
        self.player_of_match = player_of_match
        self.match_dates = match_dates
        self.num_days = num_days
        self.venue = venue
        self.toss_winner = toss_winner
        self.toss_decision = toss_decision
        self.outcome = outcome
        self.team1 = team1
        self.team2 = team2
        self.winner = winner
        self.win_by_wickets = win_by_wickets
        self.win_by_runs = win_by_runs
        self.win_by_innings = win_by_innings

    def __repr__(self):
        return f'<MatchInfo(match_id={self.match_id}, series_name={self.series_name}, match_num={self.match_num}, match_stage={self.match_stage}, match_type={self.match_type}, match_type_num={self.match_type_num}, team_type={self.team_type}, format={self.format}, season={self.season}, player_of_match={self.player_of_match}, match_dates={self.match_dates}, num_days={self.num_days}, venue={self.venue}, toss_winner={self.toss_winner}, toss_decision={self.toss_decision}, outcome={self.outcome}, team1={self.team1}, team2={self.team2}, winner={self.winner}, win_by_wickets={self.win_by_wickets}, win_by_runs={self.win_by_runs}, win_by_innings={self.win_by_innings})>'