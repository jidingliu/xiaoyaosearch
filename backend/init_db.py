#!/usr/bin/env python3
"""
数据库初始化脚本
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import init_db, get_db
from app.models.user import User
from app.models.settings import Settings, IndexStatus
from app.core.config import settings
import uuid
from datetime import datetime


def create_default_user():
    """创建默认用户"""
    from sqlalchemy.orm import Session

    db = SessionLocal()
    try:
        # 检查是否已有用户
        existing_user = db.query(User).first()
        if existing_user:
            print(f"用户已存在: {existing_user.username}")
            return existing_user

        # 创建新用户
        user = User(
            id=str(uuid.uuid4()),
            username="默认用户",
            created_at=datetime.now(),
            last_login=datetime.now(),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"创建默认用户: {user.username} (ID: {user.id})")
        return user

    finally:
        db.close()


def create_default_settings(user_id: str):
    """创建默认设置"""
    from sqlalchemy.orm import Session

    db = SessionLocal()
    try:
        default_settings = [
            # 搜索设置
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "search",
                "key": "search_mode",
                "value": "hybrid",
                "value_type": "string",
                "default_value": "hybrid",
                "description": "搜索模式"
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "search",
                "key": "results_per_page",
                "value": "20",
                "value_type": "integer",
                "default_value": "20",
                "description": "每页显示结果数"
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "search",
                "key": "auto_suggestions",
                "value": "true",
                "value_type": "boolean",
                "default_value": "true",
                "description": "自动搜索建议"
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "search",
                "key": "search_history_enabled",
                "value": "true",
                "value_type": "boolean",
                "default_value": "true",
                "description": "搜索历史记录"
            },

            # 索引设置
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "index",
                "key": "index_update_frequency",
                "value": "realtime",
                "value_type": "string",
                "default_value": "realtime",
                "description": "索引更新频率"
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "index",
                "key": "max_file_size",
                "value": str(settings.MAX_FILE_SIZE),
                "value_type": "integer",
                "default_value": str(settings.MAX_FILE_SIZE),
                "description": "最大文件大小"
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "index",
                "key": "supported_file_types",
                "value": str(settings.SUPPORTED_FILE_TYPES),
                "value_type": "json",
                "default_value": str(settings.SUPPORTED_FILE_TYPES),
                "description": "支持的文件类型"
            },

            # AI设置
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "ai",
                "key": "ai_mode",
                "value": "local",
                "value_type": "string",
                "default_value": "local",
                "description": "AI运行模式"
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "ai",
                "key": "gpu_acceleration",
                "value": "true",
                "value_type": "boolean",
                "default_value": "true",
                "description": "GPU加速"
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "ai",
                "key": "embedding_model",
                "value": settings.EMBEDDING_MODEL,
                "value_type": "string",
                "default_value": settings.EMBEDDING_MODEL,
                "description": "嵌入模型"
            },

            # 界面设置
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "ui",
                "key": "theme",
                "value": "light",
                "value_type": "string",
                "default_value": "light",
                "description": "界面主题"
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "ui",
                "key": "language",
                "value": "zh-CN",
                "value_type": "string",
                "default_value": "zh-CN",
                "description": "界面语言"
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "ui",
                "key": "font_size",
                "value": "14",
                "value_type": "integer",
                "default_value": "14",
                "description": "字体大小"
            },

            # 性能设置
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "performance",
                "key": "max_memory_usage",
                "value": "2048",
                "value_type": "integer",
                "default_value": "2048",
                "description": "最大内存使用量(MB)"
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "category": "performance",
                "key": "max_concurrent_tasks",
                "value": "4",
                "value_type": "integer",
                "default_value": "4",
                "description": "最大并发任务数"
            }
        ]

        for setting_data in default_settings:
            setting = Settings(**setting_data)
            db.add(setting)

        db.commit()
        print(f"创建默认设置: {len(default_settings)} 项")

    finally:
        db.close()


def create_index_status(user_id: str):
    """创建索引状态记录"""
    from sqlalchemy.orm import Session

    db = SessionLocal()
    try:
        index_status = IndexStatus(
            id=str(uuid.uuid4()),
            user_id=user_id,
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
        print("创建索引状态记录")

    finally:
        db.close()


def setup_directories():
    """创建必要的目录"""
    directories = [
        settings.DATA_DIR,
        settings.UPLOAD_DIR,
        settings.MODELS_DIR,
        settings.CACHE_DIR,
        settings.INDEX_DIR,
        "./logs"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"创建目录: {directory}")


def main():
    """主函数"""
    print("🚀 初始化小遥搜索数据库...")

    try:
        # 创建必要的目录
        setup_directories()

        # 初始化数据库表
        print("📊 创建数据库表...")
        init_db()

        # 获取数据库会话
        from app.core.database import SessionLocal
        global SessionLocal
        SessionLocal = SessionLocal

        # 创建默认用户
        print("👤 创建默认用户...")
        user = create_default_user()

        # 创建默认设置
        print("⚙️ 创建默认设置...")
        create_default_settings(user.id)

        # 创建索引状态
        print("📈 创建索引状态...")
        create_index_status(user.id)

        print("\n✅ 数据库初始化完成！")
        print(f"   用户ID: {user.id}")
        print(f"   用户名: {user.username}")
        print(f"   数据库: {settings.DATABASE_URL}")

    except Exception as e:
        print(f"❌ 初始化失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()