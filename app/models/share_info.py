from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, PrimaryKeyConstraint
from app.database.database import Base

class ShareInfo(Base):
    __tablename__ = "share_info"

    share_id = Column(Integer, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user_info.user_id"), nullable=False)
    share_content = Column(String(255), nullable=False)
    share_likes = Column(Integer, default=0, nullable=False)
    share_date = Column(DateTime, nullable=False)
    share_comment_count = Column(Integer, default=0, nullable=False)

    # 复合主键
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "share_id"),
    )