from sqlalchemy import Column, String, Text, DateTime, Integer
from app.database.database import Base

class Notification(Base):
    __tablename__ = "notification"

    notification_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    notification_content = Column(Text, nullable=False)
    notification_date = Column(DateTime, nullable=False)
