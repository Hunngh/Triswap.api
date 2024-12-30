from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.services.auth_service import register_user, login_user
from app.database.database import get_db

router = APIRouter()

# 用户注册请求模型
class RegisterRequest(BaseModel):
    account: str
    password: str
    email: EmailStr

# 用户登录请求模型
class LoginRequest(BaseModel):
    account: str
    password: str

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册路由"""
    return register_user(request.account, request.password, request.email, db)

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """用户登录路由"""
    return login_user(request.account, request.password, db)

'''这个文件应该合并到user_router.py中'''