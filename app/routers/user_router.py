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
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import crud

from app.database.database import get_db
from app.services.user_service import FollowService, UserService, SkillService, LikeService, FavoriteService, \
    CommentService, ShareService,MessageService
from app.models.user_info import UserInfo
from app.services.user_service import register_user, login_user,create_exchange
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
    skill_content: dict
    skill_type: str

class SkillResponse(BaseModel):
    skill_id: int
    user_id: int
    skill_content: dict  # JSON 对象
    skill_type: str
    skill_likes: int
    skill_comment_count: int
    skill_date: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        # 将 content 从字符串解析为 JSON
        data = super().from_orm(obj)
        data.content = json.loads(obj.content)
        return data

@router.get("/api/skills", response_model=List[SkillResponse])
def get_skills(db: Session = Depends(get_db)):
    skill_service = SkillService(db)
    return skill_service.get_all_skills()

@router.post("/api/skills", response_model=SkillResponse)
def post_skill(skill_request: SkillPostRequest, db: Session = Depends(get_db)):
    user_id = skill_request.user_id
    skill_service = SkillService(db)
    return skill_service.create_skill(user_id, skill_request.dict())



# 发布分享帖子
class SharePostRequest(BaseModel):
    user_id: int
    share_content: dict  # JSON 格式的帖子内容
    share_date: datetime

class ShareResponse(BaseModel):
    share_id: int
    user_id: int
    share_content: dict  # JSON 格式的帖子内容
    share_likes: int
    share_comment_count: int
    share_date: datetime

    class Config:
        from_attributes = True

@router.get("/api/shares", response_model=List[ShareResponse])
def get_shares(db: Session = Depends(get_db)):
    share_service = ShareService(db)
    return share_service.get_all_shares()

@router.post("/api/shares", response_model=ShareResponse)
def post_share(share_request: SharePostRequest, db: Session = Depends(get_db)):
    user_id = share_request.user_id
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

# 点赞技能交换帖子
@router.post("/api/skills/{skill_id}/like")
def like_skill(skill_id: int, db: Session = Depends(get_db)):
    user_id = 1  # 这里应该从token中获取当前用户ID
    like_service = LikeService(db)
    return like_service.like_skill(user_id, skill_id)







# 确定交换关系
class ExchangeRequest(BaseModel):
    skill_id: int
    opposite_id: int  # 对方用户ID
    user_id: int  # 用户 ID

@router.post("/api/skills/{skill_id}/exchange")
def create_exchange(exchange_request: ExchangeRequest, db: Session = Depends(get_db)):
    """
    创建交换请求
    - skill_id: 相关技能的ID
    - opposite_id: 对方用户的ID
    """
    # 提取请求数据
    skill_id = exchange_request.skill_id
    opposite_id = exchange_request.opposite_id

    # 调用服务层的 create_exchange 函数
    exchange_record = create_exchange(db, exchange_request.user_id, skill_id, opposite_id)
    
    return {
        "message": "交换请求已创建",
        "user_id": exchange_record.user_id,
        "opposite_id": opposite_id,
        "skill_id": skill_id,
        "is_finished": exchange_record.is_finished,  # 状态
        "date": exchange_record.date  # 时间戳
    }

# routers/user_router.py

class MesssageRequest(BaseModel):
    content: str
    receiver_id: int
    user_id: int  # 这里可以省略，直接从 JWT 或上下文获取

@router.post("/api/send_message")
def send_message(message_request: MesssageRequest, db: Session = Depends(get_db)):
    """发送消息"""
    message_service = MessageService(db)

    # 使用请求体中的数据发送消息
    new_message = message_service.create_message(
        user_id=message_request.user_id,  # 发件人ID
        opposite_id=message_request.receiver_id,  # 收件人ID
        content=message_request.content  # 消息内容
    )

    return {
        "message": "消息发送成功",
        "message_id": new_message.chat_id,  
        "content": new_message.chat_content,
        "chat_date": new_message.chat_date,
        "is_read": new_message.is_read
    }
