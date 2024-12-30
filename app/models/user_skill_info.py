from sqlalchemy import Column, String, Boolean, DateTime, Integer
from app.database.database import Base

class UserSkillInfo(Base):
    __tablename__ = "user_skill_info"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    opposite_id = Column(Integer, primary_key=True, autoincrement=True)
    skill_id = Column(String(36), primary_key=True, nullable=False)
    is_finished = Column(Boolean, nullable=False, default=False)
    date = Column(DateTime, nullable=False)
