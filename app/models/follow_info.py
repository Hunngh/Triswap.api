from sqlalchemy import Column, DateTime, Integer, ForeignKey, PrimaryKeyConstraint
from app.database.database import Base

class FollowInfo(Base):
    __tablename__ = "follow_info"

    user_id = Column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    opposite_id = Column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    follow_date = Column(DateTime, nullable=False)

    # 复合主键
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "opposite_id"),
    )