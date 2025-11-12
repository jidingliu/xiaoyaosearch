"""
API依赖注入模块
提供FastAPI依赖注入功能，包括数据库会话、用户认证、权限控制等
"""

import logging
from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.services.user_service import UserService

logger = logging.getLogger(__name__)

# HTTP Bearer认证方案
security = HTTPBearer(auto_error=False)


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    获取当前用户（可选）
    如果没有认证信息，返回None
    """
    if not credentials:
        return None

    try:
        user_service = UserService(db)
        user = await user_service.get_user_by_token(credentials.credentials)
        return user
    except Exception as e:
        logger.warning(f"用户认证失败: {e}")
        return None


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前用户（必需）
    如果没有认证信息或认证失败，抛出异常
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证信息",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_service = UserService(db)
        user = await user_service.get_user_by_token(credentials.credentials)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证信息",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="用户账户已被禁用",
            )

        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"用户认证异常: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证失败",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    获取当前活跃用户
    验证用户是否处于活跃状态
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账户已被禁用"
        )
    return current_user


class PermissionChecker:
    """权限检查器"""

    def __init__(self, required_permissions: list[str]):
        self.required_permissions = required_permissions

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        """
        检查用户是否具有所需权限
        """
        # TODO: 实现基于角色的权限控制系统
        # 当前简单实现：检查用户是否活跃
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )

        return current_user


# 依赖注入快捷方式
CurrentUser = Depends(get_current_user)
CurrentUserOptional = Depends(get_current_user_optional)
ActiveUser = Depends(get_current_active_user)


# 权限依赖
RequireAdmin = PermissionChecker(["admin"])
RequireUser = PermissionChecker(["user"])


def get_pagination_params(
    page: int = 1,
    size: int = 20,
    max_size: int = 100
) -> dict:
    """
    获取分页参数并进行验证
    """
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="页码必须大于0"
        )

    if size < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="页面大小必须大于0"
        )

    if size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"页面大小不能超过{max_size}"
        )

    offset = (page - 1) * size

    return {
        "page": page,
        "size": size,
        "offset": offset,
        "limit": size
    }


def get_search_params(
    q: Optional[str] = None,
    file_type: Optional[str] = None,
    sort_by: Optional[str] = "relevance",
    sort_order: Optional[str] = "desc"
) -> dict:
    """
    获取搜索参数并进行验证
    """
    if q and len(q.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="搜索查询不能为空"
        )

    if len(q) > 1000 if q else False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="搜索查询过长，最多1000个字符"
        )

    # 验证排序参数
    valid_sort_by = ["relevance", "date", "name", "size"]
    if sort_by and sort_by not in valid_sort_by:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的排序字段，支持的选项: {', '.join(valid_sort_by)}"
        )

    # 验证排序方向
    valid_sort_order = ["asc", "desc"]
    if sort_order and sort_order not in valid_sort_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的排序方向，支持的选项: {', '.join(valid_sort_order)}"
        )

    return {
        "query": q.strip() if q else None,
        "file_type": file_type,
        "sort_by": sort_by,
        "sort_order": sort_order
    }


def validate_file_path(file_path: str) -> str:
    """
    验证文件路径安全性
    """
    if not file_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件路径不能为空"
        )

    # 检查路径遍历攻击
    if ".." in file_path or file_path.startswith("/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的文件路径"
        )

    return file_path


def get_database_session(
    db: Session = Depends(get_db)
) -> Session:
    """
    获取数据库会话的依赖注入
    自动处理事务和异常
    """
    try:
        return db
    except Exception as e:
        logger.error(f"获取数据库会话失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="数据库连接失败"
        )