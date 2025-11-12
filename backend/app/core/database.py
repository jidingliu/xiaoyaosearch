"""
数据库连接和会话管理
支持连接池、健康检查和备份恢复功能
"""

import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Generator, Optional

from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool, StaticPool

from app.core.config import settings

logger = logging.getLogger(__name__)

# 数据库连接配置
def create_database_engine() -> Engine:
    """创建数据库引擎，支持连接池配置"""
    engine_kwargs = {
        "echo": settings.DB_ECHO,
        "future": True,  # 使用SQLAlchemy 2.0风格
    }

    if "sqlite" in settings.DATABASE_URL:
        # SQLite特定配置
        engine_kwargs.update({
            "connect_args": {
                "check_same_thread": False,
                "timeout": settings.SQLITE_TIMEOUT,
                "isolation_level": settings.SQLITE_ISOLATION_LEVEL,
            },
            "poolclass": StaticPool,
            "pool_pre_ping": True,  # 连接健康检查
        })
    else:
        # 其他数据库的连接池配置
        engine_kwargs.update({
            "poolclass": QueuePool,
            "pool_size": settings.DB_POOL_SIZE,
            "max_overflow": settings.DB_MAX_OVERFLOW,
            "pool_timeout": settings.DB_POOL_TIMEOUT,
            "pool_recycle": settings.DB_POOL_RECYCLE,
            "pool_pre_ping": True,
        })

    engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

    # 添加连接事件监听器
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if "sqlite" in settings.DATABASE_URL:
            cursor = dbapi_connection.cursor()
            # 启用WAL模式提高并发性能
            cursor.execute("PRAGMA journal_mode=WAL")
            # 启用外键约束
            cursor.execute("PRAGMA foreign_keys=ON")
            # 优化SQLite性能
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.execute("PRAGMA cache_size=10000")
            cursor.execute("PRAGMA temp_store=MEMORY")
            cursor.execute("PRAGMA mmap_size=268435456")  # 256MB
            cursor.close()

    @event.listens_for(engine, "checkout")
    def receive_checkout(dbapi_connection, connection_record, connection_proxy):
        """连接检出时的日志记录"""
        logger.debug("数据库连接已检出")

    @event.listens_for(engine, "checkin")
    def receive_checkin(dbapi_connection, connection_record):
        """连接检入时的日志记录"""
        logger.debug("数据库连接已检入")

    return engine

# 创建数据库引擎
engine = create_database_engine()

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True  # 使用SQLAlchemy 2.0风格
)

# 创建基类
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话，支持自动错误处理和重试

    Yields:
        Session: 数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"数据库会话错误: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def get_db_session() -> Session:
    """
    获取数据库会话实例，用于非依赖注入场景

    Returns:
        Session: 数据库会话
    """
    return SessionLocal()


def init_db() -> None:
    """
    初始化数据库
    创建所有表并设置默认数据
    """
    try:
        logger.info("开始初始化数据库...")

        # 创建所有表
        Base.metadata.create_all(bind=engine)

        # 创建默认用户（如果不存在）
        from app.models.user import User
        from app.models.settings import Settings, IndexStatus

        with SessionLocal() as db:
            # 检查是否已有用户
            user_count = db.query(User).count()
            if user_count == 0:
                # 创建默认用户
                default_user = User(
                    id="default-user-001",
                    username="默认用户",
                    email="user@xiaoyao.local",
                    is_active=True,
                    preferences='{"theme": "light", "language": "zh-CN"}'
                )
                db.add(default_user)
                db.flush()

                # 创建默认设置
                default_settings = [
                    Settings(
                        id="default-search-001",
                        user_id=default_user.id,
                        category="search",
                        key="search_mode",
                        value="hybrid",
                        value_type="string",
                        default_value="hybrid",
                        description="搜索模式：hybrid（混合）、vector（向量）、text（全文）"
                    ),
                    Settings(
                        id="default-search-002",
                        user_id=default_user.id,
                        category="search",
                        key="results_per_page",
                        value="20",
                        value_type="integer",
                        default_value="20",
                        description="每页显示的搜索结果数量"
                    ),
                    Settings(
                        id="default-index-001",
                        user_id=default_user.id,
                        category="index",
                        key="auto_scan",
                        value="true",
                        value_type="boolean",
                        default_value="true",
                        description="是否自动扫描文件变化"
                    ),
                    Settings(
                        id="default-ai-001",
                        user_id=default_user.id,
                        category="ai",
                        key="ai_mode",
                        value="local",
                        value_type="string",
                        default_value="local",
                        description="AI模式：local（本地）、cloud（云端）"
                    )
                ]

                for setting in default_settings:
                    db.add(setting)

                # 创建索引状态记录
                index_status = IndexStatus(
                    id="default-index-status-001",
                    user_id=default_user.id,
                    status="idle",
                    progress=0,
                    total_files=0,
                    indexed_files=0,
                    total_size=0,
                    vector_index_version=1,
                    text_index_version=1,
                    avg_search_time=0.0
                )
                db.add(index_status)

                db.commit()
                logger.info(f"默认用户已创建: {default_user.username}")
            else:
                logger.info(f"数据库已包含 {user_count} 个用户，跳过默认用户创建")

        logger.info("数据库初始化完成")

    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise


def drop_db() -> None:
    """
    删除所有表（危险操作，仅用于开发环境）
    """
    try:
        logger.warning("开始删除所有数据库表...")
        Base.metadata.drop_all(bind=engine)
        logger.warning("所有数据库表已删除")
    except Exception as e:
        logger.error(f"删除数据库表失败: {e}")
        raise


def check_db_health() -> dict:
    """
    检查数据库连接健康状态

    Returns:
        dict: 健康状态信息
    """
    try:
        with engine.connect() as conn:
            # 执行简单查询测试连接
            result = conn.execute(text("SELECT 1"))
            result.fetchone()

        return {
            "status": "healthy",
            "message": "数据库连接正常",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"数据库健康检查失败: {e}")
        return {
            "status": "unhealthy",
            "message": f"数据库连接异常: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


def get_db_info() -> dict:
    """
    获取数据库信息

    Returns:
        dict: 数据库信息
    """
    try:
        with engine.connect() as conn:
            if "sqlite" in settings.DATABASE_URL:
                # SQLite特定信息
                result = conn.execute(text("PRAGMA database_list"))
                db_info = result.fetchall()

                result = conn.execute(text("PRAGMA table_info"))
                tables = result.fetchall()

                # 获取数据库文件大小
                db_path = settings.DATABASE_URL.replace("sqlite:///", "")
                file_size = 0
                if os.path.exists(db_path):
                    file_size = os.path.getsize(db_path)

                return {
                    "database_type": "SQLite",
                    "database_path": db_path,
                    "file_size_bytes": file_size,
                    "file_size_mb": round(file_size / (1024 * 1024), 2),
                    "tables_count": len(set(table[1] for table in tables)),
                    "connection_pool": {
                        "pool_size": "StaticPool",
                        "checked_out": engine.pool.checkedout() if hasattr(engine.pool, 'checkedout') else "N/A"
                    }
                }
            else:
                # 其他数据库信息
                return {
                    "database_type": "Other",
                    "connection_pool": {
                        "size": engine.pool.size(),
                        "checked_in": engine.pool.checkedin(),
                        "checked_out": engine.pool.checkedout(),
                        "overflow": engine.pool.overflow()
                    }
                }
    except Exception as e:
        logger.error(f"获取数据库信息失败: {e}")
        return {"error": str(e)}


def backup_database(backup_dir: Optional[str] = None) -> str:
    """
    备份数据库

    Args:
        backup_dir: 备份目录，默认为 ./data/backups

    Returns:
        str: 备份文件路径
    """
    if "sqlite" not in settings.DATABASE_URL:
        raise ValueError("当前仅支持SQLite数据库备份")

    try:
        # 确保备份目录存在
        if backup_dir is None:
            backup_dir = os.path.join(settings.DATA_DIR, "backups")

        Path(backup_dir).mkdir(parents=True, exist_ok=True)

        # 生成备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        db_filename = os.path.basename(db_path)
        backup_filename = f"{db_filename}.backup_{timestamp}"
        backup_path = os.path.join(backup_dir, backup_filename)

        # 执行备份
        shutil.copy2(db_path, backup_path)

        logger.info(f"数据库已备份到: {backup_path}")
        return backup_path

    except Exception as e:
        logger.error(f"数据库备份失败: {e}")
        raise


def restore_database(backup_path: str) -> None:
    """
    从备份恢复数据库

    Args:
        backup_path: 备份文件路径
    """
    if "sqlite" not in settings.DATABASE_URL:
        raise ValueError("当前仅支持SQLite数据库恢复")

    try:
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"备份文件不存在: {backup_path}")

        db_path = settings.DATABASE_URL.replace("sqlite:///", "")

        # 创建当前数据库的备份（以防恢复失败）
        current_backup = backup_database()

        try:
            # 执行恢复
            shutil.copy2(backup_path, db_path)
            logger.info(f"数据库已从 {backup_path} 恢复")

        except Exception as e:
            # 恢复失败，回滚到当前备份
            shutil.copy2(current_backup, db_path)
            logger.error(f"数据库恢复失败，已回滚到当前状态: {e}")
            raise

    except Exception as e:
        logger.error(f"数据库恢复失败: {e}")
        raise


def list_backups(backup_dir: Optional[str] = None) -> list:
    """
    列出所有备份文件

    Args:
        backup_dir: 备份目录，默认为 ./data/backups

    Returns:
        list: 备份文件信息列表
    """
    try:
        if backup_dir is None:
            backup_dir = os.path.join(settings.DATA_DIR, "backups")

        backup_files = []
        if os.path.exists(backup_dir):
            for filename in os.listdir(backup_dir):
                if filename.endswith(('.backup_', '.db')):
                    file_path = os.path.join(backup_dir, filename)
                    stat = os.stat(file_path)
                    backup_files.append({
                        "filename": filename,
                        "path": file_path,
                        "size_bytes": stat.st_size,
                        "size_mb": round(stat.st_size / (1024 * 1024), 2),
                        "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })

        # 按修改时间倒序排列
        backup_files.sort(key=lambda x: x["modified_at"], reverse=True)
        return backup_files

    except Exception as e:
        logger.error(f"列出备份文件失败: {e}")
        return []


def cleanup_old_backups(backup_dir: Optional[str] = None, keep_count: int = 5) -> int:
    """
    清理旧备份文件，保留最新的几个

    Args:
        backup_dir: 备份目录，默认为 ./data/backups
        keep_count: 保留的备份数量

    Returns:
        int: 删除的文件数量
    """
    try:
        backups = list_backups(backup_dir)

        if len(backups) <= keep_count:
            return 0

        # 删除最旧的备份
        old_backups = backups[keep_count:]
        deleted_count = 0

        for backup in old_backups:
            try:
                os.remove(backup["path"])
                deleted_count += 1
                logger.info(f"已删除旧备份: {backup['filename']}")
            except Exception as e:
                logger.warning(f"删除备份文件失败 {backup['filename']}: {e}")

        return deleted_count

    except Exception as e:
        logger.error(f"清理旧备份失败: {e}")
        return 0