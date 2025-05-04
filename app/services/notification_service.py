'''
    此文档完成通知的服务层代码
    主要功能：
    1. 验证管理员权限
    2.发布通知
    3.获取通知列表
    4.删除通知

'''


# 导入依赖库
from app.models.notification import Notification
from app.models.admin_account import AdminAccount
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime


#验证管理员权限
def verify_admin_permission(db: Session, admin:str,password: str):
    admin_account = db.query(AdminAccount).filter(AdminAccount.username == admin).first()
    if not admin_account:
        raise HTTPException(status_code=401, detail="管理员不存在")
    if not admin_account.verify_password(password):
        raise HTTPException(status_code=401, detail="密码错误")
    return True

#发布通知
def publish_notification(db: Session, title: str, content: str):
    notification=Notification(notification_content=title+"@#"+content+"@#",notification_date=datetime.datetime.now())
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


#获取通知列表
def get_notification_list(db: Session):
    notifications = db.query(Notification).all()
    return notifications


#删除通知
def delete_notification(db: Session, id: int):
    notification = db.query(Notification).filter(Notification.id == id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="通知不存在")

    db.delete(notification)
    db.commit()