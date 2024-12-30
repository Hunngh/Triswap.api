
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
import datetime
from sqlalchemy.orm import Session
from app.models.user_info import UserInfo
from app import models
from app.database import  crud
from sqlalchemy.orm import Session
from fastapi import HTTPException

#删除用户


#更新用户个人信息
class UserService:
    def __init__(self, db: Session):
        self.db = db

    #更新用户个人资料
    def update_user_info(self, user_id: int, user_update_request: dict):
        # 获取用户信息
        db_user = self.db.query(models.UserInfo).filter(models.UserInfo.user_id == user_id).first()

        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # 更新用户信息
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

    # 更新用户密码
    def update_user_password(self, user_id: int, old_password: str, new_password: str):
        # 获取用户
        db_user = self.db.query(models.UserInfo).filter(models.UserInfo.user_id == user_id).first()

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
    user = db.query(UserInfo).filter(UserInfo.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="账号不存在")
    if user.password != password:  # 注意：实际项目中需要对密码加密后验证
        raise HTTPException(status_code=401, detail="密码错误")
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



#用户发表评论，或者回复评论

