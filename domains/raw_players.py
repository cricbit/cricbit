from sqlalchemy import Column, String, DateTime, Integer
from domains.base import Base

class RawPlayer(Base):
    __tablename__ = 'raw_players'

    player_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    cricinfo_id = Column(Integer, nullable=True, unique=True)