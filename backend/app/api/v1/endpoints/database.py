"""
数据库管理API端点
提供数据库健康检查、备份恢复、连接状态查询等功能
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel

from app.core.database import (
    backup_database,
    check_db_health,
    cleanup_old_backups,
    get_db_info,
    list_backups,
    restore_database,
)
from app.core.config import settings
from app.api.deps import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic模型定义
class DatabaseHealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str

class DatabaseInfoResponse(BaseModel):
    database_type: str
    database_path: Optional[str] = None
    file_size_bytes: Optional[int] = None
    file_size_mb: Optional[float] = None
    tables_count: Optional[int] = None
    connection_pool: dict
    error: Optional[str] = None

class BackupResponse(BaseModel):
    success: bool
    message: str
    backup_path: Optional[str] = None
    error: Optional[str] = None

class BackupInfo(BaseModel):
    filename: str
    path: str
    size_bytes: int
    size_mb: float
    created_at: str
    modified_at: str

class BackupListResponse(BaseModel):
    success: bool
    backups: List[BackupInfo]
    count: int
    error: Optional[str] = None

class RestoreRequest(BaseModel):
    backup_path: str

class RestoreResponse(BaseModel):
    success: bool
    message: str
    error: Optional[str] = None

class CleanupResponse(BaseModel):
    success: bool
    message: str
    deleted_count: int
    error: Optional[str] = None


@router.get("/health", response_model=DatabaseHealthResponse)
async def get_database_health(current_user: User = Depends(get_current_user)):
    """
    获取数据库健康状态

    Returns:
        DatabaseHealthResponse: 数据库健康状态信息
    """
    try:
        health_info = check_db_health()
        return DatabaseHealthResponse(**health_info)
    except Exception as e:
        logger.error(f"获取数据库健康状态失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取数据库健康状态失败: {str(e)}")


@router.get("/info", response_model=DatabaseInfoResponse)
async def get_database_info(current_user: User = Depends(get_current_user)):
    """
    获取数据库详细信息

    Returns:
        DatabaseInfoResponse: 数据库详细信息
    """
    try:
        db_info = get_db_info()
        return DatabaseInfoResponse(**db_info)
    except Exception as e:
        logger.error(f"获取数据库信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取数据库信息失败: {str(e)}")


@router.post("/backup", response_model=BackupResponse)
async def create_database_backup(
    background_tasks: BackgroundTasks,
    backup_dir: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    创建数据库备份

    Args:
        backup_dir: 备份目录路径（可选）

    Returns:
        BackupResponse: 备份结果
    """
    try:
        # 在后台任务中执行备份
        def backup_task():
            try:
                backup_path = backup_database(backup_dir)
                logger.info(f"数据库备份成功: {backup_path}")
                return backup_path
            except Exception as e:
                logger.error(f"数据库备份失败: {e}")
                raise

        # 异步执行备份
        backup_path = backup_database(backup_dir)

        return BackupResponse(
            success=True,
            message="数据库备份创建成功",
            backup_path=backup_path
        )
    except Exception as e:
        logger.error(f"创建数据库备份失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建数据库备份失败: {str(e)}")


@router.get("/backups", response_model=BackupListResponse)
async def list_database_backups(
    backup_dir: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    列出所有数据库备份文件

    Args:
        backup_dir: 备份目录路径（可选）

    Returns:
        BackupListResponse: 备份文件列表
    """
    try:
        backups = list_backups(backup_dir)
        backup_info_list = [BackupInfo(**backup) for backup in backups]

        return BackupListResponse(
            success=True,
            backups=backup_info_list,
            count=len(backup_info_list)
        )
    except Exception as e:
        logger.error(f"列出备份文件失败: {e}")
        raise HTTPException(status_code=500, detail=f"列出备份文件失败: {str(e)}")


@router.post("/restore", response_model=RestoreResponse)
async def restore_database_from_backup(
    request: RestoreRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """
    从备份恢复数据库

    Args:
        request: 恢复请求参数

    Returns:
        RestoreResponse: 恢复结果
    """
    try:
        # 验证备份文件是否存在
        import os
        if not os.path.exists(request.backup_path):
            raise HTTPException(status_code=404, detail=f"备份文件不存在: {request.backup_path}")

        # 在后台任务中执行恢复
        def restore_task():
            try:
                restore_database(request.backup_path)
                logger.info(f"数据库恢复成功: {request.backup_path}")
            except Exception as e:
                logger.error(f"数据库恢复失败: {e}")
                raise

        # 同步执行恢复（因为这是一个关键操作）
        restore_database(request.backup_path)

        return RestoreResponse(
            success=True,
            message=f"数据库已从 {request.backup_path} 恢复成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"恢复数据库失败: {e}")
        raise HTTPException(status_code=500, detail=f"恢复数据库失败: {str(e)}")


@router.delete("/backups/cleanup", response_model=CleanupResponse)
async def cleanup_old_database_backups(
    keep_count: int = 5,
    backup_dir: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    清理旧的数据库备份文件

    Args:
        keep_count: 保留的备份数量
        backup_dir: 备份目录路径（可选）

    Returns:
        CleanupResponse: 清理结果
    """
    try:
        if keep_count < 1:
            raise HTTPException(status_code=400, detail="保留数量必须大于0")

        deleted_count = cleanup_old_backups(backup_dir, keep_count)

        return CleanupResponse(
            success=True,
            message=f"旧备份清理完成，保留了最新的 {keep_count} 个备份",
            deleted_count=deleted_count
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"清理旧备份失败: {e}")
        raise HTTPException(status_code=500, detail=f"清理旧备份失败: {str(e)}")


@router.post("/vacuum")
async def vacuum_database(current_user: User = Depends(get_current_user)):
    """
    清理数据库碎片，优化数据库文件大小
    仅适用于SQLite数据库

    Returns:
        dict: 清理结果
    """
    try:
        if "sqlite" not in settings.DATABASE_URL:
            raise HTTPException(status_code=400, detail="当前仅支持SQLite数据库清理")

        from app.core.database import engine
        from sqlalchemy import text

        with engine.connect() as conn:
            # 执行VACUUM命令清理数据库
            conn.execute(text("VACUUM"))
            conn.commit()

        logger.info("数据库VACUUM清理完成")

        return {
            "success": True,
            "message": "数据库清理完成",
            "operation": "VACUUM"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"数据库清理失败: {e}")
        raise HTTPException(status_code=500, detail=f"数据库清理失败: {str(e)}")


@router.post("/analyze")
async def analyze_database(current_user: User = Depends(get_current_user)):
    """
    分析数据库统计信息，优化查询性能
    仅适用于SQLite数据库

    Returns:
        dict: 分析结果
    """
    try:
        if "sqlite" not in settings.DATABASE_URL:
            raise HTTPException(status_code=400, detail="当前仅支持SQLite数据库分析")

        from app.core.database import engine
        from sqlalchemy import text

        with engine.connect() as conn:
            # 执行ANALYZE命令更新统计信息
            conn.execute(text("ANALYZE"))
            conn.commit()

        logger.info("数据库ANALYZE分析完成")

        return {
            "success": True,
            "message": "数据库分析完成，查询优化信息已更新",
            "operation": "ANALYZE"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"数据库分析失败: {e}")
        raise HTTPException(status_code=500, detail=f"数据库分析失败: {str(e)}")


@router.get("/stats")
async def get_database_statistics(current_user: User = Depends(get_current_user)):
    """
    获取数据库统计信息

    Returns:
        dict: 数据库统计信息
    """
    try:
        from app.core.database import engine, get_db_session
        from sqlalchemy import text

        stats = {}

        with engine.connect() as conn:
            if "sqlite" in settings.DATABASE_URL:
                # SQLite统计信息
                # 获取表信息
                result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                tables = [row[0] for row in result.fetchall()]

                stats["tables"] = {}
                total_records = 0

                for table in tables:
                    try:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        count = result.fetchone()[0]
                        stats["tables"][table] = count
                        total_records += count
                    except Exception as e:
                        logger.warning(f"获取表 {table} 记录数失败: {e}")
                        stats["tables"][table] = -1

                stats["total_records"] = total_records
                stats["table_count"] = len(tables)

                # 获取数据库页面信息
                try:
                    result = conn.execute(text("PRAGMA page_count"))
                    page_count = result.fetchone()[0]

                    result = conn.execute(text("PRAGMA page_size"))
                    page_size = result.fetchone()[0]

                    stats["database_size_bytes"] = page_count * page_size
                    stats["database_size_mb"] = round(stats["database_size_bytes"] / (1024 * 1024), 2)
                except Exception as e:
                    logger.warning(f"获取数据库大小信息失败: {e}")

        # 使用ORM获取特定模型统计
        with get_db_session() as db:
            try:
                from app.models.user import User
                from app.models.file import File
                from app.models.directory import Directory
                from app.models.search_history import SearchHistory

                stats["users_count"] = db.query(User).count()
                stats["files_count"] = db.query(File).count()
                stats["directories_count"] = db.query(Directory).count()
                stats["search_history_count"] = db.query(SearchHistory).count()

                # 获取文件类型统计
                file_type_result = db.execute(text("""
                    SELECT file_type, COUNT(*) as count
                    FROM files
                    WHERE file_type IS NOT NULL
                    GROUP BY file_type
                    ORDER BY count DESC
                """))
                stats["file_types"] = dict(file_type_result.fetchall())

            except Exception as e:
                logger.warning(f"获取ORM模型统计失败: {e}")

        return {
            "success": True,
            "stats": stats,
            "timestamp": "2024-01-01T00:00:00Z"  # 实际应该使用真实时间戳
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取数据库统计信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取数据库统计信息失败: {str(e)}")