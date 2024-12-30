from sqlalchemy import Column, String, Text, DateTime
from app.database.database import Base

class Notification(Base):
    __tablename__ = "notification"

    notification_id = Column(String(36), primary_key=True, nullable=False)
    notification_content = Column(Text, nullable=False)
    notification_date = Column(DateTime, nullable=False)
