#!/usr/bin/env python3
"""
数据库管理命令行工具
提供数据库备份、恢复、清理等操作的CLI接口
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.database import (
    backup_database,
    restore_database,
    list_backups,
    cleanup_old_backups,
    check_db_health,
    get_db_info,
    init_db,
    drop_db,
)
from app.core.config import settings


def format_size(size_bytes):
    """格式化文件大小显示"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def format_timestamp(timestamp_str):
    """格式化时间戳显示"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str


def cmd_backup(args):
    """创建数据库备份"""
    try:
        backup_path = backup_database(args.backup_dir)
        print(f"✅ 数据库备份成功")
        print(f"📁 备份路径: {backup_path}")

        # 显示备份文件大小
        if os.path.exists(backup_path):
            size = os.path.getsize(backup_path)
            print(f"📊 文件大小: {format_size(size)}")

    except Exception as e:
        print(f"❌ 备份失败: {e}")
        sys.exit(1)


def cmd_restore(args):
    """恢复数据库"""
    try:
        # 确认操作
        if not args.force:
            answer = input(f"⚠️  确定要从 {args.backup_path} 恢复数据库吗？这将覆盖当前数据 (y/N): ")
            if answer.lower() not in ['y', 'yes']:
                print("❌ 恢复操作已取消")
                return

        print("🔄 开始恢复数据库...")
        restore_database(args.backup_path)
        print("✅ 数据库恢复成功")

    except Exception as e:
        print(f"❌ 恢复失败: {e}")
        sys.exit(1)


def cmd_list(args):
    """列出备份文件"""
    try:
        backups = list_backups(args.backup_dir)

        if not backups:
            print("📭 没有找到备份文件")
            return

        print(f"📋 找到 {len(backups)} 个备份文件:")
        print("-" * 80)
        print(f"{'文件名':<30} {'大小':<10} {'创建时间':<20} {'修改时间':<20}")
        print("-" * 80)

        for backup in backups:
            size_str = format_size(backup['size_bytes'])
            created_str = format_timestamp(backup['created_at'])
            modified_str = format_timestamp(backup['modified_at'])

            print(f"{backup['filename']:<30} {size_str:<10} {created_str:<20} {modified_str:<20}")

        print("-" * 80)

        # 计算总大小
        total_size = sum(b['size_bytes'] for b in backups)
        print(f"💾 总计: {format_size(total_size)}")

    except Exception as e:
        print(f"❌ 列出备份失败: {e}")
        sys.exit(1)


def cmd_cleanup(args):
    """清理旧备份"""
    try:
        # 首先列出当前备份
        backups = list_backups(args.backup_dir)
        if not backups:
            print("📭 没有找到备份文件，无需清理")
            return

        print(f"📋 当前有 {len(backups)} 个备份文件")

        # 确认操作
        if not args.force:
            answer = input(f"⚠️  确定要清理旧备份，只保留最新的 {args.keep_count} 个吗 (y/N): ")
            if answer.lower() not in ['y', 'yes']:
                print("❌ 清理操作已取消")
                return

        print("🧹 开始清理旧备份...")
        deleted_count = cleanup_old_backups(args.backup_dir, args.keep_count)

        if deleted_count > 0:
            print(f"✅ 清理完成，删除了 {deleted_count} 个旧备份")
        else:
            print("ℹ️  没有需要清理的备份文件")

    except Exception as e:
        print(f"❌ 清理失败: {e}")
        sys.exit(1)


def cmd_health(args):
    """检查数据库健康状态"""
    try:
        health = check_db_health()

        if health['status'] == 'healthy':
            print("✅ 数据库连接正常")
            print(f"🕐 检查时间: {format_timestamp(health['timestamp'])}")
        else:
            print("❌ 数据库连接异常")
            print(f"🚨 错误信息: {health['message']}")
            print(f"🕐 检查时间: {format_timestamp(health['timestamp'])}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        sys.exit(1)


def cmd_info(args):
    """显示数据库信息"""
    try:
        info = get_db_info()

        if 'error' in info:
            print(f"❌ 获取数据库信息失败: {info['error']}")
            sys.exit(1)

        print("📊 数据库信息:")
        print("-" * 40)
        print(f"数据库类型: {info['database_type']}")

        if info['database_type'] == 'SQLite':
            print(f"数据库路径: {info['database_path']}")
            print(f"文件大小: {format_size(info['file_size_bytes'])}")
            print(f"表数量: {info['tables_count']}")

        print(f"连接池类型: {info['connection_pool']['pool_size']}")
        if 'checked_out' in info['connection_pool']:
            print(f"活跃连接: {info['connection_pool']['checked_out']}")

    except Exception as e:
        print(f"❌ 获取数据库信息失败: {e}")
        sys.exit(1)


def cmd_init(args):
    """初始化数据库"""
    try:
        # 确认操作
        if not args.force:
            answer = input("⚠️  确定要初始化数据库吗？这将创建所有表和默认数据 (y/N): ")
            if answer.lower() not in ['y', 'yes']:
                print("❌ 初始化操作已取消")
                return

        print("🚀 开始初始化数据库...")
        init_db()
        print("✅ 数据库初始化成功")

    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)


def cmd_drop(args):
    """删除数据库（危险操作）"""
    try:
        # 双重确认
        if not args.force:
            answer1 = input("⚠️  确定要删除数据库吗？这将删除所有数据 (y/N): ")
            if answer1.lower() not in ['y', 'yes']:
                print("❌ 删除操作已取消")
                return

            answer2 = input("🚨 再次确认：删除所有数据，此操作不可恢复 (y/N): ")
            if answer2.lower() not in ['y', 'yes']:
                print("❌ 删除操作已取消")
                return

        print("💥 开始删除数据库...")
        drop_db()
        print("✅ 数据库删除成功")

    except Exception as e:
        print(f"❌ 删除失败: {e}")
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="小遥搜索数据库管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s backup                    # 创建备份
  %(prog)s backup -d /path/to/backup  # 指定备份目录
  %(prog)s restore /path/to/backup   # 恢复备份
  %(prog)s list                      # 列出备份
  %(prog)s cleanup --keep 3          # 清理旧备份，保留3个
  %(prog)s health                    # 检查健康状态
  %(prog)s info                      # 显示数据库信息
        """
    )

    parser.add_argument(
        '--backup-dir', '-d',
        help=f"备份目录路径 (默认: {os.path.join(settings.DATA_DIR, 'backups')})"
    )

    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help="跳过确认提示"
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 备份命令
    backup_parser = subparsers.add_parser('backup', help='创建数据库备份')
    backup_parser.set_defaults(func=cmd_backup)

    # 恢复命令
    restore_parser = subparsers.add_parser('restore', help='从备份恢复数据库')
    restore_parser.add_argument('backup_path', help='备份文件路径')
    restore_parser.set_defaults(func=cmd_restore)

    # 列出备份命令
    list_parser = subparsers.add_parser('list', help='列出所有备份文件')
    list_parser.set_defaults(func=cmd_list)

    # 清理备份命令
    cleanup_parser = subparsers.add_parser('cleanup', help='清理旧备份文件')
    cleanup_parser.add_argument(
        '--keep', '-k',
        type=int,
        default=5,
        help='保留的备份数量 (默认: 5)'
    )
    cleanup_parser.set_defaults(func=cmd_cleanup)

    # 健康检查命令
    health_parser = subparsers.add_parser('health', help='检查数据库健康状态')
    health_parser.set_defaults(func=cmd_health)

    # 数据库信息命令
    info_parser = subparsers.add_parser('info', help='显示数据库信息')
    info_parser.set_defaults(func=cmd_info)

    # 初始化命令
    init_parser = subparsers.add_parser('init', help='初始化数据库')
    init_parser.set_defaults(func=cmd_init)

    # 删除命令
    drop_parser = subparsers.add_parser('drop', help='删除数据库 (危险操作)')
    drop_parser.set_defaults(func=cmd_drop)

    # 解析参数
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 执行命令
    args.func(args)


if __name__ == "__main__":
    main()