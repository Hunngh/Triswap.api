
'''api的启动文件'''



from fastapi import FastAPI
from app.routers import user_router
from app.database.database import Base, engine
from app.database.database import get_db

# 初始化数据库
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 注册路由
app.include_router(user_router.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MySQL!"}
