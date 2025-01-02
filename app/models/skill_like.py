from sqlalchemy import Column, DateTime, Integer, PrimaryKeyConstraint, ForeignKey
from app.database.database import Base

class SkillLike(Base):
    __tablename__ = "skill_like"

    like_id = Column(Integer, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("share_info.share_id"), nullable=False)
    like_date = Column(DateTime, nullable=False)

    # 复合主键
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "skill_id", "like_id"),
    )