"""
API中间件模块
提供请求日志、性能监控、CORS处理等跨切关注功能
"""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse

import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 生成请求ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # 记录请求开始时间
        start_time = time.time()

        # 记录请求信息
        logger.info(
            f"请求开始 [{request_id}] {request.method} {request.url} "
            f"- 客户端: {request.client.host if request.client else 'unknown'} "
            f"- User-Agent: {request.headers.get('user-agent', 'unknown')}"
        )

        # 执行请求
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"请求异常 [{request_id}] {request.method} {request.url}: {e}", exc_info=True)
            raise

        # 计算处理时间
        process_time = time.time() - start_time

        # 记录响应信息
        logger.info(
            f"请求完成 [{request_id}] {request.method} {request.url} "
            f"- 状态码: {response.status_code} "
            f"- 处理时间: {process_time:.3f}s "
            f"- 响应大小: {self._get_response_size(response)}"
        )

        # 添加响应头
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.3f}"

        return response

    def _get_response_size(self, response: Response) -> int:
        """获取响应大小"""
        try:
            if hasattr(response, 'body'):
                return len(response.body)
            return 0
        except:
            return 0


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """安全头中间件"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # 添加安全头
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'"
        )

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """简单的速率限制中间件"""

    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls  # 允许的请求次数
        self.period = period  # 时间窗口（秒）
        self.clients = {}  # 存储客户端请求记录

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 获取客户端标识
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        # 清理过期的记录
        self._cleanup_expired_records(current_time)

        # 检查速率限制
        if not self._is_allowed(client_ip, current_time):
            from app.api.exceptions import RateLimitError
            raise RateLimitError(
                f"请求过于频繁，请在 {self.period} 秒后重试",
                client_ip=client_ip,
                current_requests=len(self.clients.get(client_ip, [])),
                max_requests=self.calls,
                period=self.period
            )

        # 记录请求
        if client_ip not in self.clients:
            self.clients[client_ip] = []
        self.clients[client_ip].append(current_time)

        response = await call_next(request)
        return response

    def _cleanup_expired_records(self, current_time: float):
        """清理过期的请求记录"""
        for client_ip, requests in list(self.clients.items()):
            # 保留在时间窗口内的记录
            self.clients[client_ip] = [
                req_time for req_time in requests
                if current_time - req_time <= self.period
            ]

        # 清空空列表
        self.clients = {
            client_ip: requests
            for client_ip, requests in self.clients.items()
            if requests
        }

    def _is_allowed(self, client_ip: str, current_time: float) -> bool:
        """检查是否允许请求"""
        if client_ip not in self.clients:
            return True

        # 检查时间窗口内的请求数量
        recent_requests = [
            req_time for req_time in self.clients[client_ip]
            if current_time - req_time <= self.period
        ]

        return len(recent_requests) <= self.calls


class CompressionMiddleware(BaseHTTPMiddleware):
    """响应压缩中间件"""

    def __init__(self, app, minimum_size: int = 1024):
        super().__init__(app)
        self.minimum_size = minimum_size  # 最小压缩大小

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # 检查是否需要压缩
        if self._should_compress(request, response):
            # 注意：实际压缩实现需要根据项目需求来定
            # 这里只是设置压缩相关的头
            response.headers["Content-Encoding"] = "gzip"

        return response

    def _should_compress(self, request: Request, response: Response) -> bool:
        """判断是否应该压缩响应"""
        # 检查客户端是否支持gzip
        accept_encoding = request.headers.get("accept-encoding", "")
        if "gzip" not in accept_encoding.lower():
            return False

        # 检查响应类型
        content_type = response.headers.get("content-type", "")
        compressible_types = [
            "application/json",
            "text/html",
            "text/css",
            "text/javascript",
            "application/javascript",
            "text/xml",
            "application/xml"
        ]

        if not any(content_type.startswith(ct) for ct in compressible_types):
            return False

        # 检查响应大小（这里简化处理）
        return True


class APIVersionMiddleware(BaseHTTPMiddleware):
    """API版本控制中间件"""

    def __init__(self, app, current_version: str = "v1"):
        super().__init__(app)
        self.current_version = current_version
        self.supported_versions = ["v1"]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 从请求头或URL中获取版本信息
        requested_version = self._get_requested_version(request)

        # 验证版本
        if requested_version and requested_version not in self.supported_versions:
            from app.api.exceptions import ValidationError
            raise ValidationError(
                f"不支持的API版本: {requested_version}",
                field="api_version",
                value=requested_version
            )

        # 设置响应头
        response = await call_next(request)
        response.headers["API-Version"] = self.current_version

        return response

    def _get_requested_version(self, request: Request) -> str:
        """从请求中获取API版本"""
        # 优先从URL路径获取
        path_parts = request.url.path.split('/')
        if len(path_parts) >= 2 and path_parts[1] in self.supported_versions:
            return path_parts[1]

        # 从请求头获取
        return request.headers.get("API-Version", "")