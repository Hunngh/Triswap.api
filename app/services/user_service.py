
from sqlalchemy.orm import Session
from app.models.user_info import UserInfo


#根据用户名获取用户记录
def get_user_by_account(account: str, db: Session):
    return db.query(UserInfo).filter(UserInfo.account == account).first()

#直接获取所有用户记录
def get_users(db: Session):
    return db.query(UserInfo).all()

#创建用户


#删除用户


#更新用户个人资料


#更新用户密码


#用户注册


#用户登录


#用户关注其他用户



#用户发布技能帖子，或者分享帖子



#用户发表评论，或者回复评论

