from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.auth_service import admin_login
from app.database.database import get_db
from pydantic import BaseModel

router = APIRouter()

# 请求模型
class AdminLoginRequest(BaseModel):
    account: str
    password: str

@router.post("/api/admin/login")
async def admin_login_route(request: AdminLoginRequest, db: Session = Depends(get_db)):
    """管理员登录"""
    result = admin_login(request.account, request.password, db)
    if result is not None:
        return {"message": "Admin logged in successfully", "admin_id": result.admin_id}
    else:
        raise HTTPException(status_code=401, detail="Incorrect account or password")
