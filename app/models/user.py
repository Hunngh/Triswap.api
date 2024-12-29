#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:user.py
# author:软件2202 曹凛然
# datetime:2024/12/5 21:27
# software: PyCharm

# 用户模型
from sqlalchemy import Column, String, Enum, Date
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, index=True)
    account = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(11), nullable=True)
    avator = Column(String(255), nullable=True)  # 用户头像链接
    profile = Column(String, nullable=True)  # 用户简介
    gender = Column(Enum("male", "female", "other"), nullable=True)
    birth = Column(Date, nullable=True)
