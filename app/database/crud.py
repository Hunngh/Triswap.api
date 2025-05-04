from sqlalchemy.orm import Session
from app import models

#通过account查询用户
def get_user_by_account(db: Session, account: str):
    return db.query(models.UserInfo).filter(models.UserInfo.account == account).first()

#获取关注信息
def get_follow(db: Session, user_id: int, opposite_id: int):
    return db.query(models.FollowInfo).filter(
        models.FollowInfo.user_id == user_id,
        models.FollowInfo.opposite_id == opposite_id
    ).first()

#通过id查询个人信息
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.UserInfo).filter(models.UserInfo.user_id == user_id).first()