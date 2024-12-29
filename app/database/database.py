#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:database.py
# author:软件2202 曹凛然
# datetime:2024/12/29 14:52
# software: PyCharm

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL 数据库配置
DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/your_database_name"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



