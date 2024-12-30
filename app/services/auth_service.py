#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:auth_service.py
# author:软件2202 曹凛然
# datetime:2024/12/5 21:31
# software: PyCharm

# 用户认证服务
from sqlalchemy.orm import Session
from app.models.user_info import User
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.models.admin_account import Admin
from datetime import timedelta
import uuid
from fastapi import HTTPException


def register_user(account: str, email: str, password: str, db: Session):
    """用户注册"""
    # 检查用户名或邮箱是否已存在
    if db.query(User).filter((User.account == account) | (User.email == email)).first():
        raise HTTPException(status_code=400, detail="Account or email already registered")

    # 创建新用户
    new_user = User(
        user_id=str(uuid.uuid4()),
        account=account,
        email=email,
        password=hash_password(password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(account: str, password: str, db: Session):
    """验证用户登录"""
    user = db.query(User).filter(User.account == account).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


def login_user(account: str, password: str, db: Session):
    """用户登录"""
    user = authenticate_user(account, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid account or password")
    access_token = create_access_token(data={"sub": user.account}, expires_delta=timedelta(days=1))
    return {"access_token": access_token, "token_type": "bearer"}


def admin_login(account: str, password: str, db: Session):
    """管理员登录"""
    admin =db.query(Admin).filter(Admin.account == account).first()
    if admin and admin.password == password:
        return admin
    else:
        return None