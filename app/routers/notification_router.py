'''
    此文件用于定义通知相关的路由
    需要完成以下功能：
    1.验证账户是否是管理员
    2.获取所有已发布的通知
    3.发布新通知
    4.删除已发布的通知

'''


# 导入依赖
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import notification
from app.services.notification_service import verify_admin_permission,publish_notification,get_notification_list,delete_notification
from app.database.database import get_db
# 创建路由
router = APIRouter()

# 获取所有已发布的通知
@router.get("/notifications")
async def get_notifications(db: Session = Depends(get_db)):
        # 获取所有已发布的通知
        notifications = get_notification_list(db)
        return {"notifications": notifications}

# 发布新通知
@router.post("/notifications")
async def publish_new_notification(title: str, content: str, db: Session = Depends(get_db)):
        # 发布新通知
        notification = publish_notification(db, title, content)
        return {"notification": notification}

# 删除已发布的通知
@router.delete("/notifications/{notification_id}")
async def delete_notification_by_id(notification_id: int, db: Session = Depends(get_db)):
        # 删除已发布的通知
        delete_notification(db, notification_id)
        return {"message": "Notification deleted successfully"}