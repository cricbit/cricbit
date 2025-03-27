from sqlalchemy import Column, String, DateTime, Boolean, ARRAY
from datetime import datetime

from domains.base import Base


class PlayerInfo(Base):
    __tablename__ = 'player_info'

    player_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    dob = Column(DateTime, nullable=True)
    gender = Column(String, nullable=True)
    batting_styles = Column(ARRAY(String), nullable=True)
    bowling_styles = Column(ARRAY(String), nullable=True)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    national_team = Column(String, nullable=True)
    playing_role = Column(String, nullable=True)

    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerInfo':
        processed_data = data.copy()
        
        # Handle date conversion
        if 'dob' in processed_data and processed_data['dob']:
            try:
                # Handle different date formats
                if isinstance(processed_data['dob'], str):
                    # Try different date formats
                    for fmt in ['%Y-%m-%dT%H:%MZ', '%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d']:
                        try:
                            processed_data['dob'] = datetime.strptime(processed_data['dob'], fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        processed_data['dob'] = None
            except Exception:
                processed_data['dob'] = None
        
        return cls(**processed_data)