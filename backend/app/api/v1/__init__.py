"""
API v1 路由包
"""

from fastapi import APIRouter

from app.api.v1.endpoints import search, files, directories, users, settings

api_router = APIRouter()

# 包含所有端点路由
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(directories.router, prefix="/directories", tags=["directories"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])