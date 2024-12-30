# 用户信息模型
from sqlalchemy import Column, String, Enum, Date, Integer
from app.database.database import Base

class UserInfo(Base):
    __tablename__ = "user_info"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    avator = Column(String(255), nullable=True)  # 用户头像链接
    gender = Column(Enum("male", "female", "other"), nullable=True)
    birth = Column(Date, nullable=True)
    school = Column(String(100), nullable=True)
    profile = Column(String, nullable=True)  # 用户简介
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(11), nullable=True)
    status = Column(Enum("active", "inactive"), nullable=True)