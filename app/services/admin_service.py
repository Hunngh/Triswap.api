'''
    需要完成以下功能：
    1. 管理员登录
    2. 管理员查询所有用户信息
    3. 管理员查询单个用户信息
    4. 管理员修改用户信息
    5. 管理员删除用户信息

'''
from sqlalchemy.orm import Session
from app.models.admin_account import AdminAccount
from app.models.user_info import UserInfo
from sqlalchemy.orm import Session
from fastapi import HTTPException


#管理员登录
def admin_login(account:str, password:str, db:Session):
    '''管理员登录'''
    admin=db.query(AdminAccount).filter(AdminAccount.account==account, AdminAccount.password==password).first()
    if not admin:
        raise HTTPException(status_code=401, detail="账号或密码错误")
    return admin

#管理员查询所有用户信息
def get_all_user_info(db:Session):
    '''管理员查询所有用户信息'''
    user_info=db.query(UserInfo).all()
    return user_info

#管理员查询单个用户信息
def get_user_info(account:str, db:Session):
    '''管理员查询单个用户信息'''
    user_info=db.query(UserInfo).filter(UserInfo.account==account).first()
    if not user_info:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user_info

#管理员修改用户状态
def modify_user_status(account:str, status:str, db:Session):
    '''管理员修改用户状态'''
    user_info=db.query(UserInfo).filter(UserInfo.account==account).first()
    if not user_info:
        raise HTTPException(status_code=404, detail="用户不存在")
    user_info.status=status
    db.commit()
    return user_info

#管理员删除用户信息
def delete_user_info(account:str, db:Session):
    '''管理员删除用户信息'''
    user_info=db.query(UserInfo).filter(UserInfo.account==account).first()
    if not user_info:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.delete(user_info)
    db.commit()
    return user_info
