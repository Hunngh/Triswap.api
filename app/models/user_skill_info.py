from sqlalchemy import Column, String, Boolean, DateTime
from app.database.database import Base

class UserSkillInfo(Base):
    __tablename__ = "user_skill_info"

    user_id = Column(String(36), primary_key=True, nullable=False)
    opposite_id = Column(String(36), primary_key=True, nullable=False)
    skill_id = Column(String(36), primary_key=True, nullable=False)
    is_finished = Column(Boolean, nullable=False, default=False)
    date = Column(DateTime, nullable=False)
