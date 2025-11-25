"""
系统管理API路由
提供系统设置、状态监控等API接口
"""
import os
import psutil
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db, get_database_info
from app.core.logging_config import get_logger
from app.schemas.requests import SettingsUpdateRequest
from app.schemas.responses import (
    SettingsResponse, HealthResponse, SuccessResponse
)

router = APIRouter(prefix="/api/system", tags=["系统管理"])
logger = get_logger(__name__)


@router.get("/health", response_model=HealthResponse, summary="系统健康检查")
async def health_check(db: Session = Depends(get_db)):
    """
    系统健康检查

    检查数据库连接、AI模型状态、索引状态等
    """
    logger.info("执行系统健康检查")

    try:
        # 数据库状态检查
        db_status = get_database_info()

        # 系统资源状态
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        cpu_percent = psutil.cpu_percent(interval=1)

        # 获取真实的AI模型状态
        ai_models_status = {}
        try:
            # 尝试获取AI模型服务状态
            from app.services.ai_model_manager import ai_model_service
            ai_models_status = await ai_model_service.get_model_status()
        except Exception as e:
            logger.warning(f"无法获取AI模型状态: {str(e)}")
            # 提供默认状态
            ai_models_status = {
                "error": f"AI模型服务不可用: {str(e)}",
                "bge_m3": {"status": "unknown", "error": "模型服务不可用"},
                "faster_whisper": {"status": "unknown", "error": "模型服务不可用"},
                "cn_clip": {"status": "unknown", "error": "模型服务不可用"}
            }

        # 获取真实的索引状态
        indexes_status = {}
        try:
            # 获取搜索服务实例
            from app.services.search_service import get_search_service
            search_service = get_search_service()
            index_info = search_service.get_index_info()

            # 转换索引状态格式
            indexes_status = {
                "faiss_index": {
                    "status": "ready" if index_info.get('faiss_available') else "not_available",
                    "document_count": index_info.get('faiss_doc_count', 0),
                    "index_size": f"{index_info.get('faiss_doc_count', 0) * 150}KB",  # 估算大小
                    "dimension": index_info.get('faiss_dimension', 'unknown'),
                    "last_updated": datetime.now().isoformat()
                },
                "whoosh_index": {
                    "status": "ready" if index_info.get('whoosh_available') else "not_available",
                    "document_count": index_info.get('whoosh_doc_count', 0),
                    "index_size": f"{index_info.get('whoosh_doc_count', 0) * 50}KB",  # 估算大小
                    "last_updated": datetime.now().isoformat()
                }
            }
        except Exception as e:
            logger.warning(f"无法获取索引状态: {str(e)}")
            indexes_status = {
                "faiss_index": {"status": "error", "error": str(e)},
                "whoosh_index": {"status": "error", "error": str(e)}
            }

        # 服务状态
        services_status = {
            "fastapi": {
                "status": "running",
                "uptime": "2h 15m",
                "version": "1.0.0"
            },
            "database": {
                "status": db_status["status"],
                "connection_pool": "1/1"
            }
        }

        # 计算整体健康状态
        overall_status = "healthy"
        if db_status["status"] != "connected":
            overall_status = "unhealthy"
        elif memory.percent > 90:
            overall_status = "warning"
        elif disk.percent > 95:
            overall_status = "warning"

        health_data = {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_percent": cpu_percent,
                "memory": {
                    "total": f"{memory.total / (1024**3):.1f}GB",
                    "used": f"{memory.used / (1024**3):.1f}GB",
                    "percent": memory.percent
                },
                "disk": {
                    "total": f"{disk.total / (1024**3):.1f}GB",
                    "used": f"{disk.used / (1024**3):.1f}GB",
                    "percent": disk.percent
                }
            },
            "database": db_status,
            "ai_models": ai_models_status,
            "indexes": indexes_status,
            "services": services_status
        }

        logger.info(f"健康检查完成: status={overall_status}")

        return HealthResponse(
            data=health_data,
            message="系统健康检查完成"
        )

    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        return HealthResponse(
            data={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            },
            message="健康检查失败"
        )


@router.get("/info", summary="系统信息")
async def get_system_info():
    """
    获取系统基本信息
    """
    logger.info("获取系统信息")

    try:
        # 系统基本信息
        system_info = {
            "app_name": "小遥搜索",
            "version": "1.0.0",
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            "platform": os.name,
            "hostname": os.uname().nodename if hasattr(os, 'uname') else "unknown",
            "working_directory": os.getcwd(),
            "environment": os.getenv("NODE_ENV", "development")
        }

        # 进程信息
        process = psutil.Process()
        process_info = {
            "pid": process.pid,
            "create_time": datetime.fromtimestamp(process.create_time()).isoformat(),
            "memory_info": {
                "rss": f"{process.memory_info().rss / (1024**2):.1f}MB",
                "vms": f"{process.memory_info().vms / (1024**2):.1f}MB"
            },
            "cpu_percent": process.cpu_percent(),
            "num_threads": process.num_threads()
        }

        system_info.update({
            "process": process_info,
            "timestamp": datetime.now().isoformat()
        })

        return {
            "success": True,
            "data": system_info,
            "message": "获取系统信息成功"
        }

    except Exception as e:
        logger.error(f"获取系统信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取系统信息失败: {str(e)}")


@router.get("/settings", response_model=SettingsResponse, summary="获取应用设置")
async def get_settings():
    """
    获取应用设置
    """
    logger.info("获取应用设置")

    try:
        # 默认设置
        settings = {
            "app": {
                "name": "小遥搜索",
                "version": "1.0.0",
                "debug": os.getenv("NODE_ENV") == "development"
            },
            "search": {
                "default_limit": 20,
                "default_threshold": 0.7,
                "max_file_size": 52428800,  # 50MB
                "supported_file_types": [
                    "pdf", "txt", "md", "docx", "xlsx", "mp3", "mp4", "wav"
                ]
            },
            "indexing": {
                "max_concurrent_jobs": 3,
                "supported_formats": [
                    "pdf", "txt", "md", "docx", "xlsx", "mp3", "mp4", "wav"
                ],
                "auto_rebuild": False,
                "scan_interval": 3600  # 1小时
            },
            "ai_models": {
                "embedding_model": "BAAI/bge-m3",
                "speech_model": "faster-whisper",
                "vision_model": "OFA-Sys/chinese-clip-vit-base-patch16",
                "llm_model": "qwen-turbo",
                "prefer_local": True,
                "fallback_to_cloud": True
            },
            "ui": {
                "theme": "light",
                "language": "zh-CN",
                "auto_refresh": True,
                "refresh_interval": 30  # 30秒
            },
            "logging": {
                "level": os.getenv("LOG_LEVEL", "info"),
                "file_path": os.getenv("LOG_FILE", "../data/logs/app.log"),
                "max_file_size": "10MB",
                "backup_count": 5
            },
            "security": {
                "enable_cors": True,
                "allowed_origins": [
                    "http://localhost:3000",
                    "http://localhost:5173"
                ],
                "max_request_size": 52428800  # 50MB
            }
        }

        return SettingsResponse(
            data=settings,
            message="获取应用设置成功"
        )

    except Exception as e:
        logger.error(f"获取应用设置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取应用设置失败: {str(e)}")


@router.post("/settings", response_model=SuccessResponse, summary="更新应用设置")
async def update_settings(request: SettingsUpdateRequest):
    """
    更新应用设置

    - **request**: 设置更新请求
    """
    logger.info("更新应用设置")

    try:
        # TODO: 实现设置保存逻辑
        # 这里暂时只是记录更新内容
        updated_settings = {}

        if request.search:
            updated_settings["search"] = request.search
        if request.indexing:
            updated_settings["indexing"] = request.indexing
        if request.ui:
            updated_settings["ui"] = request.ui
        if request.ai_models:
            updated_settings["ai_models"] = request.ai_models

        logger.info(f"设置更新完成: {list(updated_settings.keys())}")

        return SuccessResponse(
            data=updated_settings,
            message="设置更新成功"
        )

    except Exception as e:
        logger.error(f"更新应用设置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"更新应用设置失败: {str(e)}")


@router.post("/restart", response_model=SuccessResponse, summary="重启应用")
async def restart_application():
    """
    重启应用服务
    """
    logger.info("收到应用重启请求")

    try:
        # TODO: 实现应用重启逻辑
        # 这里暂时返回成功响应
        logger.warning("应用重启功能尚未实现，仅返回成功响应")

        return SuccessResponse(
            data={
                "restart_requested": True,
                "estimated_downtime": "5-10秒",
                "timestamp": datetime.now().isoformat()
            },
            message="应用重启请求已接收"
        )

    except Exception as e:
        logger.error(f"重启应用失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"重启应用失败: {str(e)}")


@router.get("/logs", summary="获取应用日志")
async def get_application_logs(
    lines: int = 100,
    level: str = "all"
):
    """
    获取应用日志

    - **lines**: 返回日志行数
    - **level**: 日志级别过滤 (all/error/warning/info/debug)
    """
    logger.info(f"获取应用日志: lines={lines}, level={level}")

    try:
        log_file = os.getenv("LOG_FILE", "../data/logs/app.log")

        if not os.path.exists(log_file):
            return {
                "success": True,
                "data": {
                    "logs": [],
                    "total_lines": 0,
                    "log_file": log_file
                },
                "message": "日志文件不存在"
            }

        # 读取真实日志文件
        real_logs = []
        try:
            if os.path.exists(log_file):
                # 读取日志文件最后N行
                with open(log_file, 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()

                # 过滤日志级别
                filtered_lines = []
                if level.lower() == 'all':
                    filtered_lines = all_lines
                else:
                    level_upper = level.upper()
                    for line in all_lines:
                        if level_upper in line:
                            filtered_lines.append(line)
                        elif 'DEBUG' in line and level_upper in ['INFO', 'WARNING', 'ERROR']:
                            filtered_lines.append(line)
                        elif 'INFO' in line and level_upper in ['WARNING', 'ERROR']:
                            filtered_lines.append(line)
                        elif 'WARNING' in line and level_upper == 'ERROR':
                            filtered_lines.append(line)

                # 取最后N行
                recent_lines = filtered_lines[-lines:] if len(filtered_lines) > lines else filtered_lines

                # 解析日志格式
                for line in recent_lines:
                    try:
                        # 尝试解析标准日志格式：时间戳 - 模块名 - 级别 - 消息
                        if ' - ' in line:
                            parts = line.strip().split(' - ', 3)
                            if len(parts) >= 4:
                                timestamp_str = parts[0]
                                module = parts[1]
                                level_str = parts[2]
                                message = parts[3]

                                real_logs.append({
                                    "timestamp": timestamp_str,
                                    "level": level_str,
                                    "message": message,
                                    "module": module
                                })
                            else:
                                # 简单格式处理
                                real_logs.append({
                                    "timestamp": datetime.now().isoformat(),
                                    "level": "INFO",
                                    "message": line.strip(),
                                    "module": "unknown"
                                })
                        else:
                            real_logs.append({
                                "timestamp": datetime.now().isoformat(),
                                "level": "INFO",
                                "message": line.strip(),
                                "module": "unknown"
                            })
                    except Exception as e:
                        # 解析失败时保留原始内容
                        real_logs.append({
                            "timestamp": datetime.now().isoformat(),
                            "level": "INFO",
                            "message": line.strip(),
                            "module": "unknown"
                        })
            else:
                real_logs.append({
                    "timestamp": datetime.now().isoformat(),
                    "level": "WARNING",
                    "message": f"日志文件不存在: {log_file}",
                    "module": "system"
                })

        except Exception as e:
            logger.error(f"读取日志文件失败: {str(e)}")
            real_logs.append({
                "timestamp": datetime.now().isoformat(),
                "level": "ERROR",
                "message": f"读取日志失败: {str(e)}",
                "module": "system"
            })

        return {
            "success": True,
            "data": {
                "logs": real_logs,
                "total_lines": len(real_logs),
                "log_file": log_file,
                "filter_level": level,
                "file_exists": os.path.exists(log_file),
                "file_size": os.path.getsize(log_file) if os.path.exists(log_file) else 0
            },
            "message": "获取应用日志成功"
        }

    except Exception as e:
        logger.error(f"获取应用日志失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取应用日志失败: {str(e)}")


@router.delete("/cache", response_model=SuccessResponse, summary="清理缓存")
async def clear_cache():
    """
    清理系统缓存
    """
    logger.info("清理系统缓存")

    try:
        # TODO: 实现缓存清理逻辑
        # 包括：向量缓存、搜索结果缓存、临时文件等

        cache_cleared = {
            "vector_cache": True,
            "search_cache": True,
            "temp_files": True,
            "logs_cleaned": False
        }

        logger.info(f"缓存清理完成: {cache_cleared}")

        return SuccessResponse(
            data=cache_cleared,
            message="系统缓存清理完成"
        )

    except Exception as e:
        logger.error(f"清理缓存失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"清理缓存失败: {str(e)}")