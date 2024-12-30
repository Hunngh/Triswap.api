
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



from sqlalchemy.orm import Session
from app.models.user_info import UserInfo
from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import uuid4

#删除用户


#更新用户个人资料


#更新用户密码


#用户注册
def register_user(email: str, password: str, db: Session):
    """用户注册服务"""
    # 检查账户或邮箱是否已存在
    if db.query(UserInfo).filter(UserInfo.email == email).first():
        raise HTTPException(status_code=400, detail="账号已经存在")

    # 创建新用户
    new_user = UserInfo(
        user_id=str(uuid4()),
        password=password,  # 注意：这里未加密，需要在实际项目中实现加密
        email=email,
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



#用户发布技能帖子，或者分享帖子



#用户发表评论，或者回复评论

