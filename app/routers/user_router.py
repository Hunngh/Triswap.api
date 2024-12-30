#此路由用于完成涉及用户的所有操作

'''
    需要完成以下功能：
    1.用户查找其他用户信息
    2.用户关注其他用户
    3.用户修改个人信息
    4.用户修改密码
    5.用户登录
    6.用户注册
    7.用户发布帖子
    8.用户发布评论
    9.用户点赞评论
    10.用户收藏帖子
    11.用户收藏评论
    12.用户获取个人信息

'''






from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user_info import UserInfo
# from app.services.user_service import get_user_by_account
from app.services.user_service import register_user, login_user
from pydantic import BaseModel

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
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("api/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """用户登录路由"""
    return login_user(request.email, request.password, db)

#用户注册
class RegisterRequest(BaseModel):
    password: str
    email: str

@router.post("api/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册路由"""
    return register_user(request.email, request.password, db)

#用户更改个人信息

#用户修改密码


#用户查找其他用户信息


#用户关注其他用户


