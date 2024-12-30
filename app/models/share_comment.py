from sqlalchemy import Column, String, Text, DateTime, Integer
from app.database.database import Base

class ShareComment(Base):
    __tablename__ = "share_comment"

    comment_id = Column(String(36), primary_key=True, nullable=False)
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    comment_content = Column(Text, nullable=False)
    parent_id = Column(String(36), nullable=True)
    share_id = Column(String(36), nullable=False)
    comment_date = Column(DateTime, nullable=False)
