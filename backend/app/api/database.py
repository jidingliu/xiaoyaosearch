"""
数据库状态API端点
提供数据库表结构和状态信息
"""
from fastapi import APIRouter, HTTPException
from sqlalchemy import inspect, text
from app.core.database import get_db, engine
from typing import Dict, Any, List

router = APIRouter(prefix="/api/database", tags=["数据库状态"])

@router.get("/status", summary="获取数据库状态")
async def get_database_status():
    """
    获取数据库详细状态信息

    Returns:
        dict: 数据库状态信息
    """
    try:
        # 检查数据库连接
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        # 获取外键约束状态
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA foreign_keys"))
            fk_status = result.fetchone()[0]

        # 获取表的详细信息
        table_info = {}
        for table_name in sorted(tables):
            if table_name.startswith('sqlite_'):
                continue

            columns = inspector.get_columns(table_name)
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = result.fetchone()[0]

            table_info[table_name] = {
                "column_count": len(columns),
                "record_count": count,
                "columns": [{"name": col["name"], "type": str(col["type"])} for col in columns[:5]]
            }

        # 检查软外键关系
        foreign_key_info = {}
        if 'files' in tables:
            with engine.connect() as conn:
                # 获取files表的样例ID
                result = conn.execute(text("SELECT id FROM files LIMIT 5"))
                file_ids = [row[0] for row in result.fetchall()]

                foreign_key_info["files_sample_ids"] = file_ids

                # 检查file_content表的关联
                if 'file_content' in tables:
                    result = conn.execute(text("SELECT DISTINCT file_id FROM file_content LIMIT 5"))
                    content_file_ids = [row[0] for row in result.fetchall()]
                    foreign_key_info["file_content_file_ids"] = content_file_ids

                # 检查file_chunks表的关联
                if 'file_chunks' in tables:
                    result = conn.execute(text("SELECT DISTINCT file_id, COUNT(*) as chunk_count FROM file_chunks GROUP BY file_id LIMIT 5"))
                    chunks_info = [(row[0], row[1]) for row in result.fetchall()]
                    foreign_key_info["file_chunks_info"] = chunks_info

        return {
            "success": True,
            "data": {
                "database_status": "connected",
                "foreign_keys_enabled": bool(fk_status),
                "total_tables": len([t for t in tables if not t.startswith('sqlite_')]),
                "tables": table_info,
                "foreign_key_relationships": foreign_key_info,
                "soft_foreign_key_mode": not bool(fk_status)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取数据库状态失败: {str(e)}")