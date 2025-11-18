from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import time
import os
import base64
import logging
from datetime import datetime
from contextlib import asynccontextmanager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    logger.info("小遥搜索服务启动中...")
    yield
    # 关闭时执行
    logger.info("小遥搜索服务关闭中...")

app = FastAPI(
    title="小遥搜索 API",
    description="多模态AI智能搜索桌面应用后端",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS中间件，支持Electron跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Electron渲染进程地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查
@app.get("/api/system/health")
async def health_check():
    """
    系统健康检查
    """
    try:
        return {
            "success": True,
            "data": {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            }
        }
    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        return {
            "success": False,
            "data": {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        }

# 启动服务
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True
    )