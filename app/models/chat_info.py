from sqlalchemy import Column, Text, DateTime, Integer, ForeignKey, PrimaryKeyConstraint
from app.database.database import Base

class ChatInfo(Base):
    __tablename__ = "chat_info"

    chat_id = Column(Integer, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    opposite_id = Column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    chat_content = Column(Text, nullable=False)
    is_read = Column(Integer, default=0, nullable=False)
    chat_date = Column(DateTime, nullable=False)

    # 复合主键
    __table_args__ = (
        PrimaryKeyConstraint("chat_id", "user_id", "opposite_id"),
    )