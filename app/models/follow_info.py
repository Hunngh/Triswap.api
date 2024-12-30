from sqlalchemy import Column, String, DateTime, Integer
from app.database.database import Base

class FollowInfo(Base):
    __tablename__ = "follow_info"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    opposite_id = Column(Integer, primary_key=True, autoincrement=True)
    follow_date = Column(DateTime, nullable=False)
