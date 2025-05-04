from sqlalchemy import Column, Text, DateTime, Integer, ForeignKey, PrimaryKeyConstraint
from app.database.database import Base

class SkillComment(Base):
    __tablename__ = "skill_comment"

    comment_id = Column(Integer, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    comment_content = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey("share_comment.comment_id"))
    skill_id = Column(Integer, ForeignKey("share_info.share_id"), nullable=False)
    comment_date = Column(DateTime, nullable=False)

    # 复合主键
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "comment_id", "skill_id"),
    )