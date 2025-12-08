"""
API路由包初始化
导出所有API路由模块
"""

from app.api.search import router as search_router
from app.api.index import router as index_router
from app.api.config import router as config_router
from app.api.system import router as system_router
from app.api.realtime_msg import router as realtime_msg_router

__all__ = [
    "search_router",
    "index_router",
    "config_router",
    "system_router",
    "realtime_msg_router"
]