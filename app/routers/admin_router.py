'''
    此文档完成管理员路由
    需要完成以下功能：
    1. 管理员登录
    2. 管理员查询所有用户信息
    3. 管理员查询单个用户信息
    4. 管理员修改用户信息
    5. 管理员删除用户信息
'''

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.services.admin_service import admin_login,get_all_user_info,get_user_info
from app.services.admin_service import modify_user_status,delete_user_info
from app.database.database import get_db
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt

# 配置密钥和算法
SECRET_KEY = "wtffish"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 定义 create_access_token 函数
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter()

# 请求模型
class AdminLoginRequest(BaseModel):
    account: str
    password: str

# 管理员登录
@router.post("/api/admin/login")
async def admin_login_route(request: AdminLoginRequest, response: Response, db: Session = Depends(get_db)):
    """管理员登录"""
    admin = admin_login(request.account, request.password, db)
    if admin is not None:
        access_token = create_access_token(data={"sub": admin.account})
        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)

        return {"message": "Admin logged in successfully", "admin_account": admin.account}
    else:
        raise HTTPException(status_code=401, detail="Incorrect account or password")

# 管理员查询所有用户信息
@router.get("/api/admin/users")
async def admin_get_users_route(response: Response, db: Session = Depends(get_db)):
    """管理员查询所有用户信息"""
    users=get_all_user_info(db)
    return {"message": "All users information", "users": users}


# 管理员查询单个用户信息
@router.get("/api/admin/users/{user_id}")
async def admin_get_user_route(user_id: int, db: Session = Depends(get_db)):
    """管理员查询单个用户信息"""
    user=get_user_info(user_id, db)
    if user is not None:
        return {"message": "User information", "user": user}
    else:
        raise HTTPException(status_code=404, detail="User not found")


# 管理员修改用户状态
@router.put("/api/admin/users/{user_id}")
async def admin_modify_user_status_route(user_id: int, status: str, db: Session = Depends(get_db)):
    """管理员修改用户状态"""
    modify_user_status(user_id, status, db)
    return {"message": "User status modified successfully"}

# 管理员删除用户信息
@router.delete("/api/admin/users/{user_id}")
async def admin_delete_user_route(user_id: int, db: Session = Depends(get_db)):
    """管理员删除用户信息"""
    delete_user_info(user_id, db)
    return {"message": "User deleted successfully"}