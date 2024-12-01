from sqlalchemy import Boolean, Integer, String, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import ForeignKey

from domains.base import Base

class Delivery(Base):
    __tablename__ = 'stg_deliveries'

    # Composite primary key fields
    match_id = Column(Integer, ForeignKey('stg_matches.match_id'), primary_key=True)
    inning = Column(Integer, primary_key=True)
    over = Column(String, primary_key=True)
    ball = Column(Integer, primary_key=True)


    # Other fields
    batting_team = Column(String)
    batter = Column(String)
    bowler = Column(String)
    runs_total = Column(Integer)
    runs_batter = Column(Integer)
    runs_extras = Column(Integer)
    non_striker = Column(String)
    
    # Wicket related fields
    is_wicket = Column(Boolean)
    wicket_type = Column(String)
    player_dismissed = Column(String)
    fielders = Column(JSONB)
    
    # Extras related fields
    wide_runs = Column(Integer)
    noball_runs = Column(Integer)
    bye_runs = Column(Integer)
    legbye_runs = Column(Integer)

    def __init__(self, match_id, inning, over, ball, batting_team, batter, bowler, runs_total, runs_batter, runs_extras, non_striker, is_wicket, wicket_type, player_dismissed, fielders, wide_runs, noball_runs, bye_runs, legbye_runs):
        self.match_id = match_id
        self.inning = inning
        self.over = over
        self.ball = ball
        self.batting_team = batting_team
        self.batter = batter
        self.bowler = bowler
        self.runs_total = runs_total
        self.runs_batter = runs_batter
        self.runs_extras = runs_extras
        self.non_striker = non_striker
        self.is_wicket = is_wicket
        self.wicket_type = wicket_type
        self.player_dismissed = player_dismissed
        self.fielders = fielders
        self.wide_runs = wide_runs
        self.noball_runs = noball_runs
        self.bye_runs = bye_runs
        self.legbye_runs = legbye_runs

    def __repr__(self):
        return f"<Deliveries(match_id={self.match_id}, inning={self.inning}, over={self.over}, ball={self.ball})>"
