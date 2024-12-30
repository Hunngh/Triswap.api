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
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import crud

from app.database.database import get_db
from app.services.user_service import FollowService, UserService
from app.models.user_info import UserInfo
from app.services.user_service import register_user, login_user
from pydantic import BaseModel

router = APIRouter()


#用户登录
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/api/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """用户登录路由"""
    return login_user(request.email, request.password, db)

#用户注册
class RegisterRequest(BaseModel):
    password: str
    email: str

@router.post("/api/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册路由"""
    return register_user(request.email, request.password, db)

#用户更改个人信息
class UserUpdateRequest(BaseModel):
    avator: Optional[str] = None  # 头像链接
    gender: Optional[str] = None  # 性别
    birth: Optional[date] = None  # 生日
    school: Optional[str] = None  # 学校
    profile: Optional[str] = None  # 个人简介
    phone: Optional[str] = None  # 手机号码
    status: Optional[str] = None  # 用户状态

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    user_id: int
    account: str
    avator: Optional[str]
    gender: Optional[str]
    birth: Optional[date]
    school: Optional[str]
    profile: Optional[str]
    email: str
    phone: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True

@router.put("/api/users/{user_id}", response_model=UserResponse)
def update_user_info(user_id: int, user_update_request: UserUpdateRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)

    # 将请求体转为字典格式传入 service 层
    updated_user = user_service.update_user_info(user_id, user_update_request.dict(exclude_unset=True))

    return updated_user
#用户修改密码
class PasswordUpdateRequest(BaseModel):
    old_password: str
    new_password: str

class UserResponse(BaseModel):
    user_id: int
    account: str
    password: str  # 在实际情况中，我们通常不会返回密码，示范时可以返回
    email: str

    class Config:
        orm_mode = True

@router.put("/api/users/{user_id}/change-password", response_model=UserResponse)
def change_password(user_id: int, password_update_request: PasswordUpdateRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)

    # 调用 service 层修改密码
    updated_user = user_service.update_user_password(
        user_id=user_id,
        old_password=password_update_request.old_password,
        new_password=password_update_request.new_password
    )

    return updated_user

#用户查找其他用户信息
class UserResponse(BaseModel):
    user_id: int
    account: str
    avator: Optional[str]
    gender: Optional[str]
    birth: Optional[str]  # 更改为字符串类型以返回日期格式
    school: Optional[str]
    profile: Optional[str]
    email: str
    phone: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True


@router.get("/api/users/{account}", response_model=UserResponse)
def get_user_by_account(account: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_account(db, account=account)
    if db_user is None:
        raise HTTPException(status_code=404, detail="没有找到对应的用户")

    # 将 birth 转换为字符串格式，以便返回 JSON
    if db_user.birth:
        db_user.birth = db_user.birth.strftime('%Y-%m-%d')  # 格式化日期为字符串

    return db_user

#用户关注其他用户
class FollowRequest(BaseModel):
    opposite_id: int

class FollowResponse(BaseModel):
    user_id: int
    opposite_id: int
    follow_date: str

    class Config:
        orm_mode = True

@router.post("/api/follow", response_model=FollowResponse)
def follow_user(follow_request: FollowRequest, db: Session = Depends(get_db)):
    user_id = 1  # 假设当前用户的 user_id 是 1，可以通过登录系统获取
    opposite_id = follow_request.opposite_id

    # 使用FollowService来处理关注逻辑
    follow_service = FollowService(db)
    follow_info = follow_service.follow_user(user_id, opposite_id)

    return follow_info
