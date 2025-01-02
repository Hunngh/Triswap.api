
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
    13.用户通过帖子确定和谁交换
'''


from datetime import datetime
import json
from typing import Optional
from sqlalchemy.orm import Session

from app.models.share_info import ShareInfo
from app.models.share_like import ShareLike
from app.models.skill_info import SkillInfo
from app.models.skill_like import SkillLike
from app.models.user_info import UserInfo
from app import models
from app.database import  crud
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user_skill_info import UserSkillInfo

#删除用户


class UserService:
    def __init__(self, db: Session):
        self.db = db

    # 更新用户个人信息
    def update_user_info(self, user_id: int, user_update_request: dict):
        db_user = self.db.query(UserInfo).filter(UserInfo.user_id == user_id).first()

        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # 更新用户信息
        if user_update_request.get("account"):
            db_user.account = user_update_request["account"]
        if user_update_request.get("avator"):
            db_user.avator = user_update_request["avator"]
        if user_update_request.get("gender"):
            db_user.gender = user_update_request["gender"]
        if user_update_request.get("birth"):
            db_user.birth = user_update_request["birth"]
        if user_update_request.get("school"):
            db_user.school = user_update_request["school"]
        if user_update_request.get("profile"):
            db_user.profile = user_update_request["profile"]
        if user_update_request.get("phone"):
            db_user.phone = user_update_request["phone"]
        if user_update_request.get("status"):
            db_user.status = user_update_request["status"]

        # 提交更新
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    # 获取用户个人信息
    def get_user_by_id(self, user_id: int):
        db_user = self.db.query(UserInfo).filter(UserInfo.user_id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


    # 更新用户密码
    def update_user_password(self, user_id: int, old_password: str, new_password: str):
        # 获取用户
        db_user = self.db.query(UserInfo).filter(UserInfo.user_id == user_id).first()

        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # 验证旧密码
        if db_user.password != old_password:
            raise HTTPException(status_code=400, detail="Old password is incorrect")

        # 更新密码
        db_user.password = new_password  # 在生产环境中，应该加密新密码
        self.db.commit()
        self.db.refresh(db_user)

        return db_user


#用户注册
def register_user(email: str, password: str, db: Session):
    """用户注册服务"""
    # 检查账户或邮箱是否已存在
    if db.query(UserInfo).filter(UserInfo.email == email).first():
        raise HTTPException(status_code=400, detail="账号已经存在")

    # 创建新用户
    new_user = UserInfo(
        password=password,  # 注意：这里未加密，需要在实际项目中实现加密
        email=email,
        account=email,
        status="active"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.user_id}

#用户登录
def login_user(email: str, password: str, db: Session):
    """用户登录服务"""
    # 查询用户信息
    user = db.query(UserInfo).filter(UserInfo.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="账号不存在")

    # 验证密码是否正确
    if user.password != password:  # 明文密码直接对比
        raise HTTPException(status_code=401, detail="密码错误")

    # 检查用户状态（如果需要）
    if user.status != "active":
        raise HTTPException(status_code=403, detail="账号被禁用")

    # 返回用户的基本信息
    return {
        "user_id": user.user_id,
        "email": user.email,
        "status": user.status
    }



#用户关注其他用户
class FollowService:
    def __init__(self, db: Session):
        self.db = db

    def follow_user(self, user_id: int, opposite_id: int):
        # 检查用户是否已经关注了对方
        db_follow = crud.get_follow(self.db, user_id, opposite_id)
        if db_follow:
            raise HTTPException(status_code=400, detail="You are already following this user")

        # 创建关注记录
        follow_info = models.FollowInfo(
            user_id=user_id,
            opposite_id=opposite_id,
            follow_date=datetime.now()
        )
        self.db.add(follow_info)
        self.db.commit()
        self.db.refresh(follow_info)

        return follow_info


#用户发布技能帖子，或者分享帖子
class SkillService:
    def __init__(self, db: Session):
        self.db = db

    def create_skill(self, user_id: int, skill_data: dict):
        # 将 JSON 对象序列化为字符串
        skill_data["content"] = json.dumps(skill_data["content"])
        new_skill = SkillInfo(user_id=user_id, **skill_data)
        self.db.add(new_skill)
        self.db.commit()
        self.db.refresh(new_skill)
        # 返回新创建的技能交换帖
        new_skill.content = json.loads(new_skill.content)  # 返回时反序列化为 JSON
        return new_skill

    def get_all_skills(self):
        # 查询技能交换帖子并排序
        skills = self.db.query(SkillInfo).order_by(SkillInfo.skill_date.desc()).all()
        for skill in skills:
            try:
                skill.skill_content = json.loads(skill.skill_content)
            except json.JSONDecodeError:
                raise ValueError(f"Content字段格式错误: {skill.skill_content}")
        return skills


class ShareService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_shares(self):
        """获取所有经验分享帖子"""
        shares = self.db.query(ShareInfo).all()
        for share in shares:
            # 将 share_content 转换为字典
            try:
                share.share_content = json.loads(share.share_content)
            except json.JSONDecodeError:
                raise ValueError("分享帖内容 JSON 格式错误")
        return shares

    def create_share(self, user_id: int, share_data: dict):
        # 将 JSON 数据存储为字符串
        share_content = json.dumps(share_data['share_content'])
        share_date = share_data['share_date']

        new_share = ShareInfo(
            user_id=user_id,
            share_content=share_content,
            share_date=share_date,
            share_likes=0,
            share_comment_count=0,
        )
        self.db.add(new_share)
        self.db.commit()
        self.db.refresh(new_share)

        # 返回新增的分享帖
        return new_share

    def get_all_shares(self):
        """获取所有经验分享帖子并按发布时间排序"""
        # 查询所有分享帖，按日期降序排列
        shares = self.db.query(ShareInfo).order_by(ShareInfo.share_date.desc()).all()

        # 将每个分享帖的内容从 JSON 格式的字符串解析为字典
        for share in shares:
            try:
                share.share_content = json.loads(share.share_content)
            except json.JSONDecodeError:
                raise ValueError(f"Content字段格式错误: {share.share_content}")

        return shares


#用户点赞
class LikeService:
    def __init__(self, db: Session):
        self.db = db

    def like_skill(self, user_id: int, skill_id: int):
        """技能帖子点赞/取消点赞"""
        # 检查是否已经点赞
        existing_like = self.db.query(SkillLike).filter(
            SkillLike.user_id == user_id,
            SkillLike.skill_id == skill_id
        ).first()

        skill = self.db.query(SkillInfo).filter(SkillInfo.skill_id == skill_id).first()
        if not skill:
            raise HTTPException(status_code=404, detail="帖子不存在")

        if existing_like:
            # 取消点赞
            self.db.delete(existing_like)
            skill.skill_likes -= 1
            message = "取消点赞成功"
        else:
            # 添加点赞
            new_like = SkillLike(
                user_id=user_id,
                skill_id=skill_id,
                like_date=datetime.now()
            )
            self.db.add(new_like)
            skill.skill_likes += 1
            message = "点赞成功"

        self.db.commit()
        return {"message": message}

    def like_share(self, user_id: int, share_id: int):
        """分享帖子点赞/取消点赞"""
        existing_like = self.db.query(ShareLike).filter(
            ShareLike.user_id == user_id,
            ShareLike.share_id == share_id
        ).first()

        share = self.db.query(ShareInfo).filter(ShareInfo.share_id == share_id).first()
        if not share:
            raise HTTPException(status_code=404, detail="帖子不存在")

        if existing_like:
            # 取消点赞
            self.db.delete(existing_like)
            share.share_likes -= 1
            message = "取消点赞成功"
        else:
            # 添加点赞
            new_like = ShareLike(
                user_id=user_id,
                share_id=share_id,
                like_date=datetime.now()
            )
            self.db.add(new_like)
            share.share_likes += 1
            message = "点赞成功"

        self.db.commit()
        return {"message": message}



#用户发表评论，或者回复评论
class CommentService:
    def __init__(self, db: Session):
        self.db = db

    def create_share_comment(self, user_id: int, share_id: int, content: str, parent_id: Optional[int] = None):
        """创建分享评论"""
        new_comment = models.ShareComment(
            user_id=user_id,
            share_id=share_id,
            comment_content=content,
            parent_id=parent_id,
            comment_date=datetime.now()
        )
        self.db.add(new_comment)

        # 更新帖子的评论数
        share = self.db.query(models.ShareInfo).filter(models.ShareInfo.share_id == share_id).first()
        share.share_comment_count += 1

        self.db.commit()
        self.db.refresh(new_comment)
        return new_comment

    def create_skill_comment(self, user_id: int, skill_id: int, content: str, parent_id: Optional[int] = None):
        """创建技能评论"""
        new_comment = models.SkillComment(
            user_id=user_id,
            skill_id=skill_id,
            comment_content=content,
            parent_id=parent_id,
            comment_date=datetime.now()
        )
        self.db.add(new_comment)

        # 更新技能帖子的评论数
        skill = self.db.query(models.SkillInfo).filter(models.SkillInfo.skill_id == skill_id).first()
        skill.skill_comment_count += 1

        self.db.commit()
        self.db.refresh(new_comment)
        return new_comment




#用户通过帖子确定和谁交换
#需要获得帖子的id，以及对方的id，然后判断是否已经交换过，如果没有交换过，则创建新的交换记录
def create_exchange(db: Session, user_id: int, skill_id: int, opposite_id: int):
    # 检查是否已经交换过
    is_exchange = db.query(UserSkillInfo.is_finished).filter(
        UserSkillInfo.is_finished == 1, 
        UserSkillInfo.user_id == user_id, 
        UserSkillInfo.skill_id == skill_id, 
        UserSkillInfo.opposite_id == opposite_id
    ).first()
    if is_exchange:
        raise HTTPException(status_code=400, detail="have already exchanged with this user")
    # 创建交换记录
    new_exchange = UserSkillInfo(
        user_id=user_id,
        skill_id=skill_id,
        opposite_id=opposite_id,
        is_finished=1,
        exchange_date=datetime.now()
    )
    db.add(new_exchange)
    db.commit()
    db.refresh(new_exchange)
    return new_exchange


#用户可以和其他用户发送消息
class MessageService:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, user_id: int, opposite_id: int, content: str):
        """创建私信"""
        new_message = models.ChatInfo(
            user_id=user_id,
            opposite_id=opposite_id,
            chat_content=content,
            chat_date=datetime.now(),
            is_read=0
        )
        self.db.add(new_message)
        self.db.commit()
        self.db.refresh(new_message)
        return new_message

    def get_user_messages(self, user_id: int, skip: int = 0, limit: int = 10):
        """获取用户的私信列表"""
        return self.db.query(models.ChatInfo)\
            .filter(models.ChatInfo.user_id == user_id)\
            .order_by(models.ChatInfo.chat_date.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    def get_unread_message_count(self, user_id: int):
        """获取未读私信数量"""
        return self.db.query(models.ChatInfo)\
            .filter(models.ChatInfo.user_id == user_id, models.ChatInfo.is_read == 0)\
            .count()

    def read_message(self, user_id: int, message_id: int):
        """标记私信为已读"""
        message = self.db.query(models.ChatInfo).filter(models.ChatInfo.chat_id == message_id).first()
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        if message.user_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        message.is_read = 1
        self.db.commit()
        return message
    


