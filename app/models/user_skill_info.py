from sqlalchemy import Column, DateTime, Integer, ForeignKey, PrimaryKeyConstraint
from app.database.database import Base

class UserSkillInfo(Base):
    __tablename__ = "user_skill_info"

    user_id = Column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    opposite_id = Column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skill_info.skill_id"), nullable=False)
    is_finished = Column(Integer, default=0)
    date = Column(DateTime, nullable=False)

    # 复合主键
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "skill_id", "opposite_id"),
    )