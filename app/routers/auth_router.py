from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.auth_service import register_user, login_user
from app.database.database import get_db
from pydantic import BaseModel

router = APIRouter()

# 请求模型
class RegisterRequest(BaseModel):
    account: str
    email: str
    password: str

class LoginRequest(BaseModel):
    account: str
    password: str

@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """注册用户"""
    user = register_user(request.account, request.email, request.password, db)
    return {"message": "User registered successfully", "user_id": user.user_id}

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """登录用户"""
    return login_user(request.account, request.password, db)


'''这个文件应该合并到user_router.py中'''