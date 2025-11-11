#!/usr/bin/env python3
"""
数据库管理脚本
"""

import click
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import init_db, drop_db
from app.core.index_manager import IndexManager
from app.core.config import settings
from init_db import create_default_user, create_default_settings, create_index_status, setup_directories


@click.group()
def cli():
    """数据库管理命令行工具"""
    pass


@cli.command()
def init():
    """初始化数据库"""
    try:
        print("🚀 开始初始化数据库...")

        # 创建必要的目录
        setup_directories()

        # 创建数据库表
        print("📊 创建数据库表...")
        init_db()

        # 创建默认用户和设置
        from app.core.database import SessionLocal
        global SessionLocal
        SessionLocal = SessionLocal

        print("👤 创建默认用户...")
        user = create_default_user()

        print("⚙️ 创建默认设置...")
        create_default_settings(user.id)

        print("📈 创建索引状态...")
        create_index_status(user.id)

        print("\n✅ 数据库初始化完成！")

    except Exception as e:
        print(f"❌ 初始化失败: {str(e)}")
        sys.exit(1)


@cli.command()
def reset():
    """重置数据库"""
    if click.confirm("确定要重置数据库吗？这将删除所有数据！"):
        try:
            print("🗑️ 正在删除数据库...")
            drop_db()

            print("🔄 重新初始化数据库...")
            init()

        except Exception as e:
            print(f"❌ 重置失败: {str(e)}")
            sys.exit(1)


@cli.command()
@click.option("--path", default=settings.INDEX_DIR, help="索引目录路径")
def index_stats(path):
    """显示索引统计信息"""
    try:
        print(f"📈 索引统计信息: {path}")

        index_manager = IndexManager(path)
        stats = index_manager.get_stats()

        print(f"向量索引大小: {stats['vector_index_size']} 个向量")
        print(f"全文索引大小: {stats['text_index_size']} 个文档")
        print(f"索引目录: {stats['index_directory']}")

    except Exception as e:
        print(f"❌ 获取统计信息失败: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--path", default=settings.INDEX_DIR, help="索引目录路径")
def index_rebuild(path):
    """重建索引"""
    if click.confirm("确定要重建索引吗？这可能需要一些时间。"):
        try:
            print(f"🔄 正在重建索引: {path}")

            index_manager = IndexManager(path)
            index_manager.rebuild_index()

            print("✅ 索引重建完成！")

        except Exception as e:
            print(f"❌ 重建索引失败: {str(e)}")
            sys.exit(1)


@cli.command()
def check():
    """检查数据库状态"""
    try:
        print("🔍 检查数据库状态...")

        from app.core.database import SessionLocal
        from app.models.user import User
        from app.models.file import File
        from app.models.directory import Directory
        from app.models.search_history import SearchHistory

        db = SessionLocal()

        # 检查各种表的记录数
        user_count = db.query(User).count()
        file_count = db.query(File).count()
        directory_count = db.query(Directory).count()
        search_count = db.query(SearchHistory).count()

        print(f"👤 用户数量: {user_count}")
        print(f"📁 文件数量: {file_count}")
        print("📂 索引目录:")
        directories = db.query(Directory).all()
        for directory in directories:
            print(f"   - {directory.name}: {directory.path} ({directory.file_count} 个文件, {directory.indexed_count} 个已索引)")
        print(f"🔍 搜索历史: {search_count} 条记录")

        # 检查索引状态
        if os.path.exists(settings.INDEX_DIR):
            try:
                index_manager = IndexManager(settings.INDEX_DIR)
                stats = index_manager.get_stats()
                print(f"📈 索引统计:")
                print(f"   - 向量索引: {stats['vector_index_size']} 个向量")
                print(f"   - 全文索引: {stats['text_index_size']} 个文档")
            except Exception as e:
                print(f"❌ 索引检查失败: {str(e)}")
        else:
            print("⚠️  索引目录不存在")

        print("✅ 数据库状态检查完成！")

    except Exception as e:
        print(f"❌ 检查失败: {str(e)}")
        sys.exit(1)
    finally:
        if 'db' in locals():
            db.close()


@cli.command()
def test_db():
    """运行数据库测试"""
    try:
        print("🧪 运行数据库测试...")

        # 运行pytest测试
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/test_database.py",
            "-v",
            "--tb=short"
        ], capture_output=True, text=True)

        print(result.stdout)
        if result.stderr:
            print("错误输出:")
            print(result.stderr)

        if result.returncode == 0:
            print("✅ 数据库测试通过！")
        else:
            print("❌ 数据库测试失败！")
            sys.exit(1)

    except Exception as e:
        print(f"❌ 运行测试失败: {str(e)}")
        sys.exit(1)


@cli.command()
def test_index():
    """运行索引测试"""
    try:
        print("🧪 运行索引测试...")

        # 运行pytest测试
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/test_index_manager.py",
            "-v",
            "--tb=short"
        ], capture_output=True, text=True)

        print(result.stdout)
        if result.stderr:
            print("错误输出:")
            print(result.stderr)

        if result.returncode == 0:
            print("✅ 索引测试通过！")
        else:
            print("❌ 索引测试失败！")
            sys.exit(1)

    except Exception as e:
        print(f"❌ 运行测试失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    cli()