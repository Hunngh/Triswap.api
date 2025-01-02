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
import base64
import json
import os
import random
from datetime import date, datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.sql import crud

from app.database.database import get_db
from app.models import ShareInfo, SkillLike, UserSkillInfo, SkillComment, ShareComment
from app.models.skill_info import SkillInfo
from app.services.user_service import FollowService, UserService, SkillService, LikeService,  \
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
    account: Optional[str] = None  # 用户名字段
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

UPLOAD_AVATARS_FOLDER = "uploaded_images/avatars"
os.makedirs(UPLOAD_AVATARS_FOLDER, exist_ok=True)

class AvatarUpdateRequest(BaseModel):
    avatar_base64: str

# 更新其他用户信息接口
@router.put("/api/users/{user_id}/info")
async def update_user_info(
    user_id: int,
    user_data: UserUpdateRequest,  # 使用更新后的 Pydantic 模型
    db: Session = Depends(get_db)
):
    try:
        # 转换请求体为字典，并排除未设置的字段
        update_data = user_data.dict(exclude_unset=True)

        # 检查是否有更新内容
        if not update_data:
            raise HTTPException(status_code=400, detail="没有提供更新内容")

        # 更新数据库中的用户信息
        user_service = UserService(db)
        updated_user = user_service.update_user_info(user_id, update_data)

        if not updated_user:
            raise HTTPException(status_code=404, detail="用户未找到")

        return {"message": "User information updated successfully", "user": updated_user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/users/{user_id}/avatar")
async def upload_user_avatar(
    user_id: int,
    avatar_data: AvatarUpdateRequest,  # 使用 Pydantic 模型解析请求体
    db: Session = Depends(get_db)
):
    try:
        avatar_base64 = avatar_data.avatar_base64
        # 解码 Base64 并保存头像
        image_data = base64.b64decode(avatar_base64)
        image_filename = f"user_{user_id}_avatar_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        image_path = os.path.join(UPLOAD_AVATARS_FOLDER, image_filename)

        with open(image_path, "wb") as f:
            f.write(image_data)

        # 拼接完整 URL
        avatar_url = f"http://120.46.200.190:5500/{UPLOAD_AVATARS_FOLDER}/{image_filename}"

        # 更新数据库中的头像 URL
        user_service = UserService(db)
        updated_user = user_service.update_user_info(user_id, {"avator": avatar_url})

        return {"message": "Avatar updated successfully", "avatar_url": avatar_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

#用户主页显示
@router.get("/api/skills/{user_id}", summary="获取用户发布的所有帖子")
async def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    """
    根据 user_id 查询该用户发布的所有帖子
    """
    # 检查用户是否存在
    user = db.query(UserInfo).filter(UserInfo.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 查询该用户的所有帖子
    posts = (
        db.query(SkillInfo)
        .filter(SkillInfo.user_id == user_id)
        .order_by(SkillInfo.skill_date.desc())
        .all()
    )

    # 返回帖子信息
    return {
        "user": {
            "user_id": user.user_id,
            "account": user.account,
            "avator": user.avator,
            "email": user.email,
            "profile": user.profile,
        },
        "posts": [
            {
                "skill_id": post.skill_id,
                "skill_content": post.skill_content,
                "skill_likes": post.skill_likes,
                "skill_date": post.skill_date,
                "skill_comment_count": post.skill_comment_count,
            }
            for post in posts
        ],
    }


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
UPLOAD_FOLDER = "uploaded_images"  # 定义图片上传文件夹
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 如果文件夹不存在，则创建

class SkillPost(BaseModel):
    user_id: int
    skill_content: dict  # 处理包含文本和Base64图片的JSON
    skill_date: datetime

@router.post("/api/skills")
async def create_skill_post(skill: SkillPost, db: Session = Depends(get_db)):
    try:
        # 保存图片到文件夹并获取URL
        images = skill.skill_content.get("images", [])
        saved_image_urls = []

        for idx, image_base64 in enumerate(images):
            image_data = base64.b64decode(image_base64)
            image_filename = f"user_{skill.user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{idx}.jpg"
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            with open(image_path, "wb") as f:
                f.write(image_data)

            # 拼接完整URL
            full_url = f"http://120.46.200.190:5500/{UPLOAD_FOLDER}/{image_filename}"  # 替换为你的服务器地址
            saved_image_urls.append(full_url)

        # 更新 skill_content 字段为文本和图片URL的组合
        skill_content = {
            "content": skill.skill_content.get("content", ""),
            "images": saved_image_urls
        }

        # 创建新的技能帖子
        new_skill = SkillInfo(
            user_id=skill.user_id,
            skill_content=json.dumps(skill_content),  # 转换为JSON字符串保存
            skill_date=skill.skill_date
        )
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)

        return {"message": "Skill post created successfully", "data": new_skill}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 首页帖子列表显示
@router.get("/api/skill_posts")
async def get_all_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = (
        db.query(SkillInfo)
        .order_by(SkillInfo.skill_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    result = []
    for post in posts:
        skill_content = json.loads(post.skill_content)  # 假设 skill_content 是 JSON 格式
        result.append({
            "skill_id": post.skill_id,
            "user_id": post.user_id,
            "content": skill_content.get("content", ""),
            "image": skill_content.get("images", [None])[0],  # 第一张图片
            "skill_likes": post.skill_likes,
            "skill_date": post.skill_date,
            "skill_comment_count": post.skill_comment_count,
        })

    # 随机打乱帖子顺序
    random.shuffle(result)

    return {"posts": result}

#获取帖子详细信息
@router.get("/api/skill_posts/{skill_id}")
async def get_post_detail(skill_id: int, db: Session = Depends(get_db)):
    post = db.query(SkillInfo).filter(SkillInfo.skill_id == skill_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="帖子未找到")

    skill_content = json.loads(post.skill_content)  # 假设 skill_content 是 JSON 格式

    return {
        "skill_id": post.skill_id,
        "user_id": post.user_id,
        "content": skill_content.get("content", ""),
        "images": skill_content.get("images", []),
        "skill_likes": post.skill_likes,
        "skill_date": post.skill_date,
        "skill_comment_count": post.skill_comment_count,
    }


# 点赞技能交换帖子
#查询是否点赞
@router.get("/api/skill_likes")
async def check_like_status(skill_id: int, user_id: int, db: Session = Depends(get_db)):
    is_liked = (
        db.query(SkillLike)
        .filter(SkillLike.skill_id == skill_id, SkillLike.user_id == user_id)
        .first()
    )
    return {"is_liked": is_liked is not None}

#更改点赞状态
# @router.post("/api/skill_likes")
# async def like_skill(skill_like: SkillLike, db: Session = Depends(get_db)):
#     existing_like = (
#         db.query(SkillLike)
#         .filter(SkillLike.skill_id == skill_like.skill_id, SkillLike.user_id == skill_like.user_id)
#         .first()
#     )
#     if existing_like:
#         raise HTTPException(status_code=400, detail="已经点赞过")
#
#     new_like = SkillLike(
#         user_id=skill_like.user_id,
#         skill_id=skill_like.skill_id,
#         like_date=datetime.now(),
#     )
#     db.add(new_like)
#
#     # 更新 SkillInfo 的点赞数量
#     skill = db.query(SkillInfo).filter(SkillInfo.skill_id == skill_like.skill_id).first()
#     if skill:
#         skill.skill_likes += 1
#
#     db.commit()
#     return {"message": "点赞成功"}
#
# @router.delete("/api/skill_likes")
# async def unlike_skill(skill_id: int, user_id: int, db: Session = Depends(get_db)):
#     existing_like = (
#         db.query(SkillLike)
#         .filter(SkillLike.skill_id == skill_id, SkillLike.user_id == user_id)
#         .first()
#     )
#     if not existing_like:
#         raise HTTPException(status_code=400, detail="尚未点赞")
#
#     db.delete(existing_like)
#
#     # 更新 SkillInfo 的点赞数量
#     skill = db.query(SkillInfo).filter(SkillInfo.skill_id == skill_id).first()
#     if skill:
#         skill.skill_likes -= 1
#
#     db.commit()
#     return {"message": "取消点赞成功"}


# 确定交换关系请求模型
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
    skill_id = exchange_request.skill_id
    opposite_id = exchange_request.opposite_id
    user_id = exchange_request.user_id

    # 校验：确保发帖人和发起交换人不是同一个人
    skill_info = db.query(SkillInfo).filter(SkillInfo.skill_id == skill_id).first()
    if not skill_info:
        raise HTTPException(status_code=404, detail="技能帖子不存在")

    if skill_info.user_id == user_id:
        raise HTTPException(status_code=400, detail="无法与自己确定技能交换关系")

    # 检查是否已存在已确定的交换关系
    existing_exchange = (
        db.query(UserSkillInfo)
        .filter(UserSkillInfo.skill_id == skill_id, UserSkillInfo.is_finished == 0)
        .first()
    )
    if existing_exchange:
        raise HTTPException(
            status_code=400,
            detail="帖子已经确定技能交换关系",
        )

    # 检查是否已存在相同的交换关系
    user_existing_exchange = (
        db.query(UserSkillInfo)
        .filter(
            UserSkillInfo.user_id == user_id,
            UserSkillInfo.skill_id == skill_id,
            UserSkillInfo.opposite_id == opposite_id,
        )
        .first()
    )
    if user_existing_exchange:
        raise HTTPException(status_code=400, detail="你已与该用户存在交换关系")

    # 创建新的交换关系
    new_exchange = UserSkillInfo(
        user_id=user_id,
        opposite_id=opposite_id,
        skill_id=skill_id,
        is_finished=0,  # 初始状态为未完成
        date=datetime.now(),
    )
    db.add(new_exchange)
    db.commit()
    db.refresh(new_exchange)

    return {
        "message": "交换请求已创建",
        "user_id": new_exchange.user_id,
        "opposite_id": new_exchange.opposite_id,
        "skill_id": new_exchange.skill_id,
        "is_finished": new_exchange.is_finished,  # 状态
        "date": new_exchange.date,  # 时间戳
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

#技能交换评论
# 评论响应模型
class SkillCommentResponse(BaseModel):
    comment_id: int
    user_id: int
    account: str
    avatar: str = None  # 用户头像
    content: str
    date: datetime

#添加技能交换评论
class CommentRequest(BaseModel):
    user_id: int
    skill_id: int
    comment_content: str
    parent_id: Optional[int] = None

# 添加评论接口
@router.post("/api/skills/{skill_id}/comments")
def add_comment(skill_id: int, comment_request: CommentRequest, db: Session = Depends(get_db)):
    """
    添加评论接口
    """
    # 检查帖子是否存在
    skill_post = db.query(SkillInfo).filter(SkillInfo.skill_id == skill_id).first()
    if not skill_post:
        raise HTTPException(status_code=404, detail="帖子不存在")

    # 创建评论记录
    new_comment = SkillComment(
        user_id=comment_request.user_id,
        skill_id=skill_id,
        comment_content=comment_request.comment_content,
        parent_id=comment_request.parent_id,  # 默认为空值
        comment_date=datetime.now()
    )

    db.add(new_comment)

    # 更新 skill_comment_count 字段
    skill_post.skill_comment_count += 1  # 评论数加 1
    db.commit()
    db.refresh(new_comment)

    return {
        "message": "评论添加成功",
        "comment_id": new_comment.comment_id,
        "user_id": new_comment.user_id,
        "content": new_comment.comment_content,
        "date": new_comment.comment_date,
    }

# 评论响应模型
class CommentResponse(BaseModel):
    comment_id: int
    user_id: int
    account: str
    avatar: Optional[str] = None
    content: str
    date: datetime

# 获取评论列表接口
@router.get("/api/skills/{skill_id}/comments", response_model=List[CommentResponse])
def get_comments(skill_id: int, db: Session = Depends(get_db)):
    """
    获取帖子评论列表接口
    """
    # 检查帖子是否存在
    skill_post = db.query(SkillInfo).filter(SkillInfo.skill_id == skill_id).first()
    if not skill_post:
        raise HTTPException(status_code=404, detail="帖子不存在")

    # 获取评论列表
    comments = (
        db.query(SkillComment, UserInfo)
        .join(UserInfo, SkillComment.user_id == UserInfo.user_id)
        .filter(SkillComment.skill_id == skill_id)
        .order_by(SkillComment.comment_date.asc())
        .all()
    )

    # 格式化评论数据
    result = []
    for comment, user in comments:
        result.append({
            "comment_id": comment.comment_id,
            "user_id": comment.user_id,
            "account": user.account,
            "avatar": user.avator,
            "content": comment.comment_content,
            "date": comment.comment_date,
        })

    return result

# 创建分享帖子
class SharePost(BaseModel):
    user_id: int
    share_content: dict  # 处理包含文本和Base64图片的JSON
    share_date: datetime

@router.post("/api/shares")
async def create_share_post(share: SharePost, db: Session = Depends(get_db)):
    try:
        # 保存图片到文件夹并获取URL
        images = share.share_content.get("images", [])
        saved_image_urls = []

        for idx, image_base64 in enumerate(images):
            image_data = base64.b64decode(image_base64)
            image_filename = f"user_{share.user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{idx}.jpg"
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            with open(image_path, "wb") as f:
                f.write(image_data)

            # 拼接完整URL
            full_url = f"http://120.46.200.190:5500/{UPLOAD_FOLDER}/{image_filename}"  # 替换为你的服务器地址
            saved_image_urls.append(full_url)

        # 更新 share_content 字段为文本和图片URL的组合
        share_content = {
            "content": share.share_content.get("content", ""),
            "images": saved_image_urls
        }

        # 创建新的经验分享帖子
        new_share = ShareInfo(
            user_id=share.user_id,
            share_content=json.dumps(share_content),  # 转换为JSON字符串保存
            share_date=share.share_date  # 确保字段名正确
        )
        db.add(new_share)
        db.commit()
        db.refresh(new_share)

        return {"message": "Share post created successfully", "data": new_share}
    except Exception as e:
        print(f"Error creating share post: {e}")  # 打印具体错误
        raise HTTPException(status_code=500, detail="Error creating share post.")

# 分享帖子列表显示
@router.get("/api/share_posts")
async def get_all_share_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = (
        db.query(ShareInfo)
        .order_by(ShareInfo.share_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    result = []
    for post in posts:
        share_content = json.loads(post.share_content)  # 假设 share_content 是 JSON 格式
        result.append({
            "share_id": post.share_id,
            "user_id": post.user_id,
            "content": share_content.get("content", ""),
            "image": share_content.get("images", [None])[0],  # 第一张图片
            "share_likes": post.share_likes,
            "share_date": post.share_date,
            "share_comment_count": post.share_comment_count,
        })
    return {"posts": result}

# 获取分享帖详细信息
@router.get("/api/share_posts/{share_id}")
async def get_share_post_detail(share_id: int, db: Session = Depends(get_db)):
    """
    获取分享帖详细信息
    """
    # 查询帖子是否存在
    post = db.query(ShareInfo).filter(ShareInfo.share_id == share_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="帖子未找到")

    # 假设 share_content 是 JSON 格式
    share_content = json.loads(post.share_content)

    return {
        "share_id": post.share_id,
        "user_id": post.user_id,
        "content": share_content.get("content", ""),
        "images": share_content.get("images", []),
        "share_likes": post.share_likes,
        "share_date": post.share_date,
        "share_comment_count": post.share_comment_count,
    }


# 经验分享评论响应模型
class ShareCommentResponse(BaseModel):
    comment_id: int
    user_id: int
    account: str
    avatar: str = None  # 用户头像
    content: str
    date: datetime

# 添加经验分享评论请求模型
class ShareCommentRequest(BaseModel):
    user_id: int
    share_id: int
    comment_content: str
    parent_id: Optional[int] = None

# 添加评论接口
@router.post("/api/shares/{share_id}/comments")
def add_share_comment(share_id: int, comment_request: ShareCommentRequest, db: Session = Depends(get_db)):
    """
    添加经验分享评论接口
    """
    # 检查帖子是否存在
    share_post = db.query(ShareInfo).filter(ShareInfo.share_id == share_id).first()
    if not share_post:
        raise HTTPException(status_code=404, detail="帖子不存在")

    # 创建评论记录
    new_comment = ShareComment(
        user_id=comment_request.user_id,
        share_id=share_id,
        comment_content=comment_request.comment_content,
        parent_id=comment_request.parent_id,  # 默认为空值
        comment_date=datetime.now()
    )

    db.add(new_comment)

    # 更新 share_comment_count 字段
    share_post.share_comment_count += 1  # 评论数加 1
    db.commit()
    db.refresh(new_comment)

    return {
        "message": "评论添加成功",
        "comment_id": new_comment.comment_id,
        "user_id": new_comment.user_id,
        "content": new_comment.comment_content,
        "date": new_comment.comment_date,
    }

# 获取经验分享评论列表接口
@router.get("/api/shares/{share_id}/comments", response_model=List[ShareCommentResponse])
def get_share_comments(share_id: int, db: Session = Depends(get_db)):
    """
    获取经验分享帖子评论列表接口
    """
    # 检查帖子是否存在
    share_post = db.query(ShareInfo).filter(ShareInfo.share_id == share_id).first()
    if not share_post:
        raise HTTPException(status_code=404, detail="帖子不存在")

    # 获取评论列表
    comments = (
        db.query(ShareComment, UserInfo)
        .join(UserInfo, ShareComment.user_id == UserInfo.user_id)
        .filter(ShareComment.share_id == share_id)
        .order_by(ShareComment.comment_date.asc())
        .all()
    )

    # 格式化评论数据
    result = []
    for comment, user in comments:
        result.append({
            "comment_id": comment.comment_id,
            "user_id": comment.user_id,
            "account": user.account,
            "avatar": user.avator,
            "content": comment.comment_content,
            "date": comment.comment_date,
        })

    return result
