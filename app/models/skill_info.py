from sqlalchemy import Column, String, Integer, PrimaryKeyConstraint, DateTime, ForeignKey
from app.database.database import Base

class SkillInfo(Base):
    __tablename__ = "skill_info"

    share_id = Column(Integer, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    share_content = Column(String(255), nullable=False)
    skill_likes = Column(Integer, default=0, nullable=False)
    skill_type = Column(String(50))
    skill_date = Column(DateTime, nullable=False)
    skill_comment_count = Column(Integer, default=0, nullable=False)

    # 复合主键
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "skill_id"),
    )