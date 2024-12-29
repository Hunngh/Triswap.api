#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:user_router.py
# author:软件2202 曹凛然
# datetime:2024/12/29 14:58
# software: PyCharm

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User
from app.services.user_service import get_user_by_id

router = APIRouter()

@router.get("/api/users/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
