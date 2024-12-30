from sqlalchemy import Column, String, DateTime, Integer
from app.database.database import Base

class SkillLike(Base):
    __tablename__ = "skill_like"

    like_id = Column(String(36), primary_key=True, nullable=False)
    skill_id = Column(String(36), nullable=False)
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    like_date = Column(DateTime, nullable=False)
