"""
API异常处理模块
定义自定义异常类和全局异常处理器
"""

import logging
from typing import Any, Dict, Optional

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


class XiaoyaoSearchException(Exception):
    """小遥搜索基础异常类"""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class ValidationError(XiaoyaoSearchException):
    """数据验证异常"""

    def __init__(self, message: str, field: Optional[str] = None, value: Optional[Any] = None):
        details = {}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = str(value)

        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class AuthenticationError(XiaoyaoSearchException):
    """认证异常"""

    def __init__(self, message: str = "认证失败"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class AuthorizationError(XiaoyaoSearchException):
    """授权异常"""

    def __init__(self, message: str = "权限不足"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=status.HTTP_403_FORBIDDEN
        )


class NotFoundError(XiaoyaoSearchException):
    """资源未找到异常"""

    def __init__(self, message: str, resource_type: Optional[str] = None, resource_id: Optional[str] = None):
        details = {}
        if resource_type:
            details["resource_type"] = resource_type
        if resource_id:
            details["resource_id"] = resource_id

        super().__init__(
            message=message,
            error_code="NOT_FOUND_ERROR",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )


class ConflictError(XiaoyaoSearchException):
    """资源冲突异常"""

    def __init__(self, message: str, conflict_field: Optional[str] = None):
        details = {}
        if conflict_field:
            details["conflict_field"] = conflict_field

        super().__init__(
            message=message,
            error_code="CONFLICT_ERROR",
            status_code=status.HTTP_409_CONFLICT,
            details=details
        )


class DatabaseError(XiaoyaoSearchException):
    """数据库操作异常"""

    def __init__(self, message: str, operation: Optional[str] = None):
        details = {}
        if operation:
            details["operation"] = operation

        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class SearchError(XiaoyaoSearchException):
    """搜索操作异常"""

    def __init__(self, message: str, query: Optional[str] = None):
        details = {}
        if query:
            details["query"] = query

        super().__init__(
            message=message,
            error_code="SEARCH_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class FileOperationError(XiaoyaoSearchException):
    """文件操作异常"""

    def __init__(self, message: str, file_path: Optional[str] = None, operation: Optional[str] = None):
        details = {}
        if file_path:
            details["file_path"] = file_path
        if operation:
            details["operation"] = operation

        super().__init__(
            message=message,
            error_code="FILE_OPERATION_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class RateLimitError(XiaoyaoSearchException):
    """速率限制异常"""

    def __init__(self, message: str, client_ip: Optional[str] = None, current_requests: Optional[int] = None, max_requests: Optional[int] = None, period: Optional[int] = None):
        details = {}
        if client_ip:
            details["client_ip"] = client_ip
        if current_requests is not None:
            details["current_requests"] = current_requests
        if max_requests is not None:
            details["max_requests"] = max_requests
        if period is not None:
            details["period"] = period

        super().__init__(
            message=message,
            error_code="RATE_LIMIT_ERROR",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details=details
        )


def create_error_response(
    status_code: int,
    message: str,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None
) -> JSONResponse:
    """
    创建标准错误响应
    """
    from datetime import datetime

    if not timestamp:
        timestamp = datetime.now().isoformat()

    content = {
        "detail": message,
        "timestamp": timestamp
    }

    if error_code:
        content["error_code"] = error_code

    if details:
        content["details"] = details

    return JSONResponse(
        status_code=status_code,
        content=content
    )


# 异常处理器
async def xiaoyao_search_exception_handler(request: Request, exc: XiaoyaoSearchException):
    """处理小遥搜索自定义异常"""
    logger.error(f"小遥搜索异常: {exc}", exc_info=True)

    return create_error_response(
        status_code=exc.status_code,
        message=exc.message,
        error_code=exc.error_code,
        details=exc.details
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理请求验证异常"""
    logger.warning(f"请求验证失败: {exc}")

    # 提取验证错误详情
    details = {}
    errors = []

    for error in exc.errors():
        error_detail = {
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        }
        if "input" in error:
            error_detail["input"] = str(error["input"])
        errors.append(error_detail)

    details["errors"] = errors

    return create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="请求参数验证失败",
        error_code="VALIDATION_ERROR",
        details=details
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """处理HTTP异常"""
    logger.warning(f"HTTP异常: {exc.status_code} - {exc.detail}")

    return create_error_response(
        status_code=exc.status_code,
        message=str(exc.detail),
        error_code="HTTP_ERROR"
    )


async def general_exception_handler(request: Request, exc: Exception):
    """处理通用异常"""
    logger.error(f"未处理的异常: {exc}", exc_info=True)

    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="服务器内部错误",
        error_code="INTERNAL_SERVER_ERROR"
    )