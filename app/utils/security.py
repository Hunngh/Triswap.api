#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:security.py
# author:软件2202 曹凛然
# datetime:2024/12/29 14:56
# software: PyCharm

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """加密密码"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

