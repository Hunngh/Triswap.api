from sqlalchemy import Column, String, Integer, DateTime, Text
from app.database.database import Base

class ShareInfo(Base):
    __tablename__ = "share_info"

    share_id = Column(String(36), primary_key=True, nullable=False)
    user_id = Column(String(36), nullable=False)
    share_content = Column(Text, nullable=False)
    share_likes = Column(Integer, default=0)
    share_date = Column(DateTime, nullable=False)
    share_comment_count = Column(Integer, default=0)
