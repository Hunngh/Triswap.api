from sqlalchemy import Column, DateTime, Integer, ForeignKey, PrimaryKeyConstraint
from app.database.database import Base

class ShareLike(Base):
    __tablename__ = "share_like"

    like_id = Column(Integer, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    share_id = Column(Integer, ForeignKey("share_info.share_id"), nullable=False)
    like_date = Column(DateTime, nullable=False)

    # 复合主键
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "share_id", "like_date"),
    )