"""
小遥搜索后端应用入口点
提供完整的FastAPI应用结构，支持依赖注入、中间件和生命周期管理
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import init_db
from app.core.openapi import setup_custom_openapi, DOCUMENTATION_CONFIG
from app.api.v1 import api_router
from app.api.middleware import (
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    CompressionMiddleware,
    APIVersionMiddleware
)
from app.api.exceptions import (
    XiaoyaoSearchException,
    xiaoyao_search_exception_handler,
    http_exception_handler,
    general_exception_handler
)

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    应用生命周期管理
    """
    # 启动时执行
    logger.info("正在启动小遥搜索API服务...")

    try:
        # 初始化数据库
        init_db()
        logger.info("数据库初始化完成")

        # 这里可以添加其他启动时的初始化逻辑
        # 例如：加载AI模型、初始化缓存等

        logger.info("小遥搜索API服务启动完成")

    except Exception as e:
        logger.error(f"应用启动失败: {e}")
        raise

    yield

    # 关闭时执行
    logger.info("正在关闭小遥搜索API服务...")

    # 这里可以添加清理逻辑
    # 例如：关闭数据库连接、保存状态等

    logger.info("小遥搜索API服务已关闭")


def create_application() -> FastAPI:
    """
    创建FastAPI应用实例，配置中间件、路由和事件处理器
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="""
        小遥搜索API - 跨平台本地文件智能搜索服务

        ## 功能特性
        - 🔍 智能语义搜索
        - 📁 多模态文件支持
        - 🤖 AI驱动查询理解
        - 🔒 隐私保护优先
        - 🚀 高性能索引
        - 📊 实时统计分析

        ## 技术栈
        - FastAPI + SQLAlchemy + Pydantic
        - SQLite + Faiss + Whoosh
        - 机器学习：BGE + Whisper + CLIP
        """,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan,

        # API配置
        contact={
            "name": "小遥搜索开发团队",
            "url": "https://github.com/xiaoyaosearch",
            "email": "support@xiaoyao.local"
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        },

        # 文档配置
        servers=[
            {
                "url": f"http://localhost:{settings.PORT}{settings.API_V1_STR}",
                "description": "开发环境"
            }
        ]
    )

    # 设置自定义OpenAPI配置
    setup_custom_openapi(app)

    # 配置Swagger UI参数
    app.swagger_ui_parameters = DOCUMENTATION_CONFIG["swagger_ui_parameters"]

    # 添加自定义中间件（按顺序很重要）
    # 1. API版本控制
    app.add_middleware(APIVersionMiddleware, current_version="v1")

    # 2. 请求日志记录
    app.add_middleware(RequestLoggingMiddleware)

    # 3. 安全头处理
    app.add_middleware(SecurityHeadersMiddleware)

    # 4. 速率限制
    app.add_middleware(RateLimitMiddleware, calls=100, period=60)

    # 5. 响应压缩
    app.add_middleware(CompressionMiddleware, minimum_size=1024)

    # 6. CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count", "X-Page-Count", "X-Request-ID", "X-Process-Time"]
    )

    # 7. 受信任主机中间件（生产环境）
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["localhost", "127.0.0.1", "*.xiaoyao.local"]
        )

    # 8. 全局异常处理器
    app.add_exception_handler(XiaoyaoSearchException, xiaoyao_search_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # 健康检查端点（在API路由之前）
    @app.get("/")
    async def root():
        """根路径健康检查"""
        return {
            "message": "小遥搜索API服务运行中",
            "version": settings.VERSION,
            "status": "healthy",
            "docs_url": f"{settings.API_V1_STR}/docs",
            "api_version": "v1"
        }

    @app.get("/health")
    async def health_check():
        """详细健康检查"""
        from app.core.database import check_db_health

        db_health = check_db_health()

        return {
            "status": "healthy" if db_health["status"] == "healthy" else "degraded",
            "version": settings.VERSION,
            "database": db_health["status"],
            "timestamp": db_health["timestamp"],
            "environment": "development" if settings.DEBUG else "production"
        }

    # 包含API路由
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


# 创建应用实例
app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
        use_colors=True
    )