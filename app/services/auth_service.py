from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user_info import UserInfo  # 用户模型
from uuid import uuid4


def register_user(account: str, password: str, email: str, db: Session):
    """用户注册服务"""
    # 检查账户或邮箱是否已存在
    if db.query(UserInfo).filter(UserInfo.account == account).first():
        raise HTTPException(status_code=400, detail="Account already exists")
    if db.query(UserInfo).filter(UserInfo.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # 创建新用户
    new_user = UserInfo(
        user_id=str(uuid4()),
        account=account,
        password=password,  # 注意：这里未加密，需要在实际项目中实现加密
        email=email,
        status="active"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.user_id}


def login_user(account: str, password: str, db: Session):
    """用户登录服务"""
    user = db.query(UserInfo).filter(UserInfo.account == account).first()
    if not user:
        raise HTTPException(status_code=404, detail="Account does not exist")
    if user.password != password:  # 注意：实际项目中需要对密码加密后验证
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {
        "user_id": user.user_id,
        "account": user.account,
        "email": user.email,
        "status": user.status
    }
