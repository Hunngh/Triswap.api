from sqlalchemy import Column, String, Text, DateTime
from app.database.database import Base

class SkillComment(Base):
    __tablename__ = "skill_comment"

    comment_id = Column(String(36), primary_key=True, nullable=False)
    user_id = Column(String(36), nullable=False)
    comment_content = Column(Text, nullable=False)
    parent_id = Column(String(36), nullable=True)
    skill_id = Column(String(36), nullable=False)
    comment_date = Column(DateTime, nullable=False)
