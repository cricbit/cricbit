from sqlalchemy import Column, Integer, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RawDBaseMatch(Base):
    __tablename__ = 'raw_base_matches'
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

    match_id = Column(Integer, primary_key=True)
    match_data = Column(JSON)
    deliveries = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now())

    def __init__(self, match_id, match_data, deliveries):
        self.match_id = match_id
        self.match_data = match_data
        self.deliveries = deliveries

    def __repr__(self):
        return f'<RawDBTMatch(match_id={self.match_id}, created_at={self.created_at})>'


class RawDBTMatch(Base):
    __tablename__ = 'raw_matches'
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

    match_id = Column(Integer, ForeignKey('dbt.raw_base_matches.match_id'), primary_key=True)
    match_data = Column(JSON)
    deliveries = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now())

    def __init__(self, match_id, match_data, deliveries):
        self.match_id = match_id
        self.match_data = match_data
        self.deliveries = deliveries

    def __repr__(self):
        return f'<RawDBTMatch(match_id={self.match_id}, created_at={self.created_at})>'

