from sqlalchemy import Column, String, DateTime
from app.database.database import Base

class FollowInfo(Base):
    __tablename__ = "follow_info"

    user_id = Column(String(36), primary_key=True, nullable=False)
    opposite_id = Column(String(36), primary_key=True, nullable=False)
    follow_date = Column(DateTime, nullable=False)
