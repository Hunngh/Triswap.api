from sqlalchemy.orm import Session
<<<<<<< HEAD
from app.models.user_info import UserInfo
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.models.admin_account import AdminAccount
from datetime import timedelta
import uuid
=======
>>>>>>> cccce800dfa82433453291a2f1d589b414d701f9
from fastapi import HTTPException
from app.models.user_info import UserInfo  # 用户模型
from uuid import uuid4


<<<<<<< HEAD
def register_user(account: str, email: str, password: str, db: Session):
    """用户注册"""
    # 检查用户名或邮箱是否已存在
    if db.query(UserInfo).filter((UserInfo.account == account) | (UserInfo.email == email)).first():
        raise HTTPException(status_code=400, detail="Account or email already registered")

    # 创建新用户
    new_user = UserInfo(
        user_id=str(uuid.uuid4()),
=======
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
>>>>>>> cccce800dfa82433453291a2f1d589b414d701f9
        account=account,
        password=password,  # 注意：这里未加密，需要在实际项目中实现加密
        email=email,
        status="active"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
<<<<<<< HEAD
    return new_user


def authenticate_user(account: str, password: str, db: Session):
    """验证用户登录"""
    user = db.query(UserInfo).filter(UserInfo.account == account).first()
    if not user or not verify_password(password, user.password):
        return None
    return user
=======
    return {"message": "User registered successfully", "user_id": new_user.user_id}
>>>>>>> cccce800dfa82433453291a2f1d589b414d701f9


def login_user(account: str, password: str, db: Session):
    """用户登录服务"""
    user = db.query(UserInfo).filter(UserInfo.account == account).first()
    if not user:
<<<<<<< HEAD
        raise HTTPException(status_code=401, detail="Invalid account or password")
    access_token = create_access_token(data={"sub": user.account}, expires_delta=timedelta(days=1))
    return {"access_token": access_token, "token_type": "bearer"}


def admin_login(account: str, password: str, db: Session):
    """管理员登录"""
    admin =db.query(AdminAccount).filter(AdminAccount.account == account).first()
    if admin and admin.password == password:
        return admin
    else:
        return None
    
    '''这个文件应该合并到user_service.py中,其中管理员的登录和管理员对用户的管理应该单独新建一个service文件'''
=======
        raise HTTPException(status_code=404, detail="Account does not exist")
    if user.password != password:  # 注意：实际项目中需要对密码加密后验证
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {
        "user_id": user.user_id,
        "account": user.account,
        "email": user.email,
        "status": user.status
    }
>>>>>>> cccce800dfa82433453291a2f1d589b414d701f9
