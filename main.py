from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from app.routers import user_router, admin_router
from app.database.database import Base, engine, get_db

# 初始化数据库
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Triswap API", description="API for Triswap application", version="0.1.0")

# 挂载静态文件目录
app.mount("/uploaded_images", StaticFiles(directory="uploaded_images"), name="uploaded_images")

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://120.46.200.190"],  # 允许的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许的 HTTP 头
)

# 注册路由
app.include_router(user_router.router)
app.include_router(admin_router.router)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MySQL!"}
