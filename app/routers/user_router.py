#此路由用于获取用户信息，或者修改用户信息

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user_info import User
from app.services.user_service import get_user_by_account

router = APIRouter()

#管理员获取用户信息
@router.get("/api/users/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = get_user_by_account(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#管理员获取所有用户信息
@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

#修改用户状态


#用户登录


#用户注册

#用户更改个人信息

#用户修改密码


#用户查找其他用户信息


#用户关注其他用户


