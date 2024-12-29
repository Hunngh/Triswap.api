#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:jwt.py
# author:软件2202 曹凛然
# datetime:2024/12/29 14:57
# software: PyCharm

from datetime import datetime, timedelta
import jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    """生成 JWT 令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
