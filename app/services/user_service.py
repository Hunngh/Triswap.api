#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:user_service.py
# author:软件2202 曹凛然
# datetime:2024/12/29 15:59
# software: PyCharm

from sqlalchemy.orm import Session
from app.models.user_info import User

def get_user_by_id(user_id: str, db: Session):
    return db.query(User).filter(User.user_id == user_id).first()
