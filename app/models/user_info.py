# 用户信息模型
from datetime import date

from sqlalchemy import Column, String, Enum, Date, Integer, Text
from app.database.database import Base

class UserInfo(Base):
    __tablename__ = "user_info"

    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    account = Column(String(50))
    password = Column(String(255), nullable=False)
    avator = Column(String(255))  # 用户头像链接
    gender = Column(Enum("male", "female", "other"))
    birth = Column(Date)
    school = Column(String(100))
    profile = Column(Text)  # 用户简介
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(11))
    status = Column(Enum("active", "inactive"))
    created = Column(Date, default=date.today, nullable=False)