"""
OpenAPI配置和文档生成模块
提供详细的API文档配置和自定义文档生成功能
"""

from typing import Dict, Any
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.core.config import settings


def custom_openapi(app: FastAPI) -> Dict[str, Any]:
    """
    自定义OpenAPI配置
    提供更详细的API文档信息
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="""
        # 小遥搜索API

        跨平台本地文件智能搜索服务，提供强大的文件搜索、AI查询理解和隐私保护功能。

        ## 主要功能

        ### 🔍 智能语义搜索
        - **向量搜索**: 基于BGE模型的中文语义理解
        - **混合搜索**: 结合向量搜索和传统文本搜索
        - **多模态支持**: 文本、图像、音频文件搜索
        - **相关性排序**: 智能相关性评分和结果排序

        ### 📁 文件管理
        - **文件索引**: 自动文件发现和索引建立
        - **元数据提取**: 文件内容分析和元数据提取
        - **预览功能**: 文件内容快速预览
        - **批量操作**: 支持批量文件处理

        ### 🤖 AI驱动查询
        - **自然语言理解**: 支持自然语言查询
        - **查询扩展**: 自动查询词扩展和同义词处理
        - **意图识别**: 查询意图智能识别
        - **个性化推荐**: 基于用户行为的搜索推荐

        ### 🔒 安全与隐私
        - **本地部署**: 数据完全本地存储和处理
        - **用户认证**: JWT令牌认证机制
        - **访问控制**: 细粒度权限控制
        - **审计日志**: 完整的操作审计记录

        ## 技术架构

        ### 后端技术栈
        - **FastAPI**: 高性能异步Web框架
        - **SQLAlchemy**: ORM数据库操作
        - **BGE**: 中文语义向量模型
        - **Whoosh**: 全文搜索引擎
        - **Faiss**: 向量相似度搜索
        - **Whisper**: 音频转文字
        - **CLIP**: 图文多模态理解

        ### 数据存储
        - **SQLite**: 轻量级关系数据库
        - **向量索引**: Faiss向量存储
        - **倒排索引**: Whoosh文本索引

        ## API使用指南

        ### 认证方式
        API使用JWT Bearer Token进行认证：
        ```
        Authorization: Bearer <your_token>
        ```

        ### 响应格式
        所有API响应都遵循统一格式：
        ```json
        {
            "code": 200,
            "message": "success",
            "data": {},
            "timestamp": "2023-12-07T10:30:00Z"
        }
        ```

        ### 错误处理
        错误响应包含详细的错误信息：
        ```json
        {
            "detail": "错误描述",
            "error_code": "ERROR_CODE",
            "details": {},
            "timestamp": "2023-12-07T10:30:00Z"
        }
        ```

        ### 分页查询
        列表接口支持分页查询：
        ```
        GET /api/v1/search?page=1&size=20
        ```

        ## 开发指南

        ### 环境要求
        - Python 3.8+
        - 8GB+ RAM
        - 足够的存储空间用于索引

        ### 快速开始
        1. 安装依赖: `pip install -r requirements.txt`
        2. 初始化数据库: `python database_cli.py init`
        3. 启动服务: `python main.py`
        4. 访问文档: `http://localhost:8000/api/v1/docs`

        ### 配置说明
        详细配置请参考 `.env` 文件或环境变量设置。

        ## 许可证
        MIT License - 详见 [LICENSE](https://opensource.org/licenses/MIT) 文件

        ## 支持与反馈
        - GitHub: https://github.com/xiaoyaosearch
        - Email: support@xiaoyao.local
        - 文档: https://docs.xiaoyao.local
        """,
        routes=app.routes,
        servers=[
            {
                "url": f"http://localhost:{settings.PORT}{settings.API_V1_STR}",
                "description": "开发环境"
            },
            {
                "url": f"https://api.xiaoyao.local{settings.API_V1_STR}",
                "description": "生产环境"
            }
        ],
        contact={
            "name": "小遥搜索开发团队",
            "url": "https://github.com/xiaoyaosearch",
            "email": "support@xiaoyao.com"
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        }
    )

    # 添加自定义标签
    openapi_schema["tags"] = [
        {
            "name": "认证",
            "description": "用户认证和授权相关接口"
        },
        {
            "name": "搜索",
            "description": "文件搜索和查询相关接口"
        },
        {
            "name": "文件管理",
            "description": "文件管理和操作相关接口"
        },
        {
            "name": "目录管理",
            "description": "目录扫描和管理相关接口"
        },
        {
            "name": "用户管理",
            "description": "用户信息管理相关接口"
        },
        {
            "name": "系统管理",
            "description": "系统配置和状态管理接口"
        },
        {
            "name": "健康检查",
            "description": "系统健康检查和监控接口"
        }
    ]

    # 添加安全方案
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT Bearer Token认证"
        }
    }

    # 添加全局安全要求（可选）
    openapi_schema["security"] = [
        {"BearerAuth": []}
    ]

    # 添加示例
    openapi_schema["components"]["examples"] = {
        "SearchRequest": {
            "summary": "搜索请求示例",
            "value": {
                "query": "人工智能发展趋势",
                "type": "document",
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "size": 20,
                "page": 1
            }
        },
        "UserLogin": {
            "summary": "用户登录示例",
            "value": {
                "username": "admin",
                "password": "password123"
            }
        },
        "ErrorResponse": {
            "summary": "错误响应示例",
            "value": {
                "detail": "用户名或密码错误",
                "error_code": "AUTHENTICATION_ERROR",
                "timestamp": "2023-12-07T10:30:00Z"
            }
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


def setup_custom_openapi(app: FastAPI) -> None:
    """
    设置自定义OpenAPI配置
    """
    app.openapi = lambda: custom_openapi(app)


# 文档生成配置
DOCUMENTATION_CONFIG = {
    "swagger_ui_parameters": {
        "deepLinking": True,
        "displayRequestDuration": True,
        "docExpansion": "none",
        "operationsSorter": "alpha",
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "tryItOutEnabled": True
    },
    "redoc_parameters": {
        "hideHostname": True,
        "hideDownloadButton": False,
        "expandResponses": "200",
        "requiredPropsFirst": True
    }
}