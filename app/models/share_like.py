from sqlalchemy import Column, String, DateTime, Integer
from app.database.database import Base

class ShareLike(Base):
    __tablename__ = "share_like"

    like_id = Column(String(36), primary_key=True, nullable=False)
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    share_id = Column(String(36), nullable=False)
    like_date = Column(DateTime, nullable=False)
