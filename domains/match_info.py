from sqlalchemy import Column, Integer, JSON, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# this table is to be created in the dbt schema 

class MatchInfo(Base):
    __tablename__ = 'match_info'
    __table_args__ = {'schema': 'dbt'}
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

    match_id = Column(Integer, primary_key=True, description="Unique identifier for each match")
    series_name = Column(String, description="Name of the series or tournament")
    match_num = Column(Integer, description="Match number within the series")
    match_stage = Column(String, description="Stage of the match (e.g., group, knockout)")
    match_type = Column(String, description="Type of match (e.g., T20, ODI, Test)")
    match_type_num = Column(Integer, description="Number associated with the match type")
    team_type = Column(String, description="Type of teams playing (e.g., international, club)")
    format = Column(String, description="Format of the match")
    season = Column(Integer, description="Season in which the match was played")
    player_of_match = Column(String, description="Player of the match")
    match_dates = Column(JSON, description="Dates and times of the match")
    num_days = Column(Integer, description="Number of days the match lasted")
    venue = Column(String, description="Venue of the match")
    toss_winner = Column(String, description="Team that won the toss")
    toss_decision = Column(String, description="Decision made by the toss winner")
    outcome = Column(String, description="Outcome of the match")
    team1 = Column(String, description="First team playing in the match")
    team2 = Column(String, description="Second team playing in the match")
    winner = Column(String, description="Team that won the match")
    win_by_wickets = Column(Integer, description="Wickets by which the winning team won")
    win_by_runs = Column(Integer, description="Runs by which the winning team won")
    win_by_innings = Column(Integer, description="Innings by which the winning team won")

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