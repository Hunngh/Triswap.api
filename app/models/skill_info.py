from sqlalchemy import Column, String, Integer, Date, Text
from app.database.database import Base

class SkillInfo(Base):
    __tablename__ = "skill_info"

    skill_id = Column(String(36), primary_key=True, nullable=False)
    user_id = Column(String(36), nullable=False)
    skill_likes = Column(Integer, default=0)
    skill_type = Column(String(50), nullable=False)
    skill_date = Column(Date, nullable=False)
    skill_content = Column(Text, nullable=False)
    skill_comment_count = Column(Integer, default=0)
