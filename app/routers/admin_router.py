'''
    此文档完成管理员路由
    需要完成以下功能：
    1. 管理员登录
    2. 管理员查询所有用户信息
    3. 管理员查询单个用户信息
    4. 管理员修改用户信息
    5. 管理员删除用户信息


'''



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# from app.services.admin_service import admin_login
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
        return {"message": "Admin logged in successfully", "admin_id": result.account}
    else:
        raise HTTPException(status_code=401, detail="Incorrect account or password")
