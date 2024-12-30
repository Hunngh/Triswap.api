from sqlalchemy import Column, String, Text, Boolean, DateTime
from app.database.database import Base

class ChatInfo(Base):
    __tablename__ = "chat_info"

    chat_id = Column(String(36), primary_key=True, nullable=False)
    user_id = Column(String(36), nullable=False)
    opposite_id = Column(String(36), nullable=False)
    chat_content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    chat_date = Column(DateTime, nullable=False)
