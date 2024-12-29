#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:main.py.py
# author:软件2202 曹凛然
# datetime:2024/12/29 14:54
# software: PyCharm

from fastapi import FastAPI
from app.routers import auth_router
from app.database.database import Base, engine
from app.database.database import get_db

# 初始化数据库
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 注册路由
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MySQL!"}
