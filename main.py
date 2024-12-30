from fastapi import FastAPI
from app.routers import user_router
from app.database.database import Base, engine, get_db

# 初始化数据库
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Triswap API", description="API for Triswap application", version="0.1.0")

# 注册路由
app.include_router(user_router.router)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MySQL!"}
