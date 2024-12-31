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
import json
from datetime import date, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import crud

from app.database.database import get_db
from app.services.user_service import FollowService, UserService, SkillService, LikeService, FavoriteService, \
    CommentService, ShareService
from app.models.user_info import UserInfo
from app.services.user_service import register_user, login_user
from pydantic import BaseModel

router = APIRouter()


#用户登录
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    user_id: int
    email: str
    status: str

@router.post("/api/login", response_model=LoginResponse)
def login_route(login_request: LoginRequest, db: Session = Depends(get_db)):

    # 调用服务层的登录逻辑
    user = login_user(login_request.email, login_request.password, db)

    # 返回登录成功的信息
    return user

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
        from_attributes = True

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
        from_attributes = True

@router.get("/api/users/{user_id}", response_model=UserResponse)
def get_user_info(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.get_user_by_id(user_id)  # 调用 service 层方法
    return db_user

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
        from_attributes = True

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
        from_attributes = True


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
        from_attributes = True

@router.post("/api/follow", response_model=FollowResponse)
def follow_user(follow_request: FollowRequest, db: Session = Depends(get_db)):
    user_id = 1  # 假设当前用户的 user_id 是 1，可以通过登录系统获取
    opposite_id = follow_request.opposite_id

    # 使用FollowService来处理关注逻辑
    follow_service = FollowService(db)
    follow_info = follow_service.follow_user(user_id, opposite_id)

    return follow_info

#用户发布技能交换
class SkillPostRequest(BaseModel):
    user_id: int
    content: dict
    skill_type: str

class SkillResponse(BaseModel):
    skill_id: int
    user_id: int
    content: dict  # 返回 JSON 对象
    skill_type: str
    likes: int
    comment_count: int
    skill_date: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        # 将 content 从字符串解析为 JSON
        data = super().from_orm(obj)
        data.content = json.loads(obj.content)
        return data

@router.post("/api/skills", response_model=SkillResponse)
def post_skill(
    skill_request: SkillPostRequest,
    db: Session = Depends(get_db)
):
    user_id = skill_request.user_id
    skill_service = SkillService(db)
    return skill_service.create_skill(user_id, skill_request.dict())



# 发布分享帖子
class SharePostRequest(BaseModel):
    content: str

class ShareResponse(BaseModel):
    share_id: int
    user_id: int
    content: str
    likes: int
    comment_count: int
    share_date: datetime

    class Config:
        from_attributes = True

@router.post("/api/shares", response_model=ShareResponse)
def post_share(share_request: SharePostRequest, db: Session = Depends(get_db)):
    user_id = 1  # 这里应该从token中获取当前用户ID
    share_service = ShareService(db)
    return share_service.create_share(user_id, share_request.dict())

# 发布评论
class CommentRequest(BaseModel):
    content: str
    parent_id: Optional[int] = None

@router.post("/api/skills/{skill_id}/comments")
def comment_skill(skill_id: int, comment_request: CommentRequest, db: Session = Depends(get_db)):
    user_id = 1  # 这里应该从token中获取当前用户ID
    comment_service = CommentService(db)
    return comment_service.create_skill_comment(
        user_id,
        skill_id,
        comment_request.content,
        comment_request.parent_id
    )

# 点赞帖子
@router.post("/api/skills/{skill_id}/like")
def like_skill(skill_id: int, db: Session = Depends(get_db)):
    user_id = 1  # 这里应该从token中获取当前用户ID
    like_service = LikeService(db)
    return like_service.like_skill(user_id, skill_id)

# 收藏帖子
@router.post("/api/skills/{skill_id}/favorite")
def favorite_skill(skill_id: int, db: Session = Depends(get_db)):
    user_id = 1  # 这里应该从token中获取当前用户ID
    favorite_service = FavoriteService(db)
    return favorite_service.favorite_skill(user_id, skill_id)

# 获取用户发布的技能帖子列表
@router.get("/api/users/{user_id}/skills")
def get_user_skills(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    skill_service = SkillService(db)
    return skill_service.get_user_skills(user_id, skip, limit)

# 获取用户的收藏列表
@router.get("/api/users/{user_id}/favorites")
def get_user_favorites(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    favorite_service = FavoriteService(db)
    return favorite_service.get_user_favorites(user_id, skip, limit)

