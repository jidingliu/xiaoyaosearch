"""
WebSocket接口路由
提供实时通信功能，包括索引进度推送和搜索建议
"""
import json
import asyncio
from typing import Dict, Set, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.core.logging_config import get_logger
from app.utils.enum_helpers import get_enum_value
from app.schemas.enums import JobStatus

router = APIRouter()
logger = get_logger(__name__)

# 存储活跃的WebSocket连接
class ConnectionManager:
    """WebSocket连接管理器"""

    def __init__(self):
        # 存储所有活跃连接
        self.active_connections: Dict[str, WebSocket] = {}
        # 存储索引任务订阅
        self.index_subscriptions: Dict[int, Set[str]] = {}
        # 存储搜索建议连接
        self.search_connections: Set[str] = set()

    async def connect(self, websocket: WebSocket, connection_id: str):
        """接受WebSocket连接"""
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        logger.info(f"WebSocket连接已建立: {connection_id}, 总连接数: {len(self.active_connections)}")

    def disconnect(self, connection_id: str):
        """断开WebSocket连接"""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]

        # 清理索引订阅
        for index_id in list(self.index_subscriptions.keys()):
            if connection_id in self.index_subscriptions[index_id]:
                self.index_subscriptions[index_id].remove(connection_id)
                if not self.index_subscriptions[index_id]:
                    del self.index_subscriptions[index_id]

        # 清理搜索建议连接
        self.search_connections.discard(connection_id)

        logger.info(f"WebSocket连接已断开: {connection_id}, 总连接数: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, connection_id: str):
        """发送个人消息"""
        if connection_id in self.active_connections:
            try:
                await self.active_connections[connection_id].send_text(json.dumps(message, ensure_ascii=False))
            except Exception as e:
                logger.error(f"发送消息失败 {connection_id}: {str(e)}")
                self.disconnect(connection_id)

    async def broadcast_to_index_subscribers(self, message: dict, index_id: int):
        """向索引任务订阅者广播消息"""
        if index_id in self.index_subscriptions:
            disconnected_connections = []

            for connection_id in self.index_subscriptions[index_id].copy():
                if connection_id in self.active_connections:
                    try:
                        await self.active_connections[connection_id].send_text(
                            json.dumps(message, ensure_ascii=False)
                        )
                    except Exception as e:
                        logger.error(f"广播索引消息失败 {connection_id}: {str(e)}")
                        disconnected_connections.append(connection_id)
                else:
                    disconnected_connections.append(connection_id)

            # 清理断开的连接
            for conn_id in disconnected_connections:
                self.disconnect(conn_id)

    async def broadcast_to_search_connections(self, message: dict):
        """向搜索建议连接广播消息"""
        disconnected_connections = []

        for connection_id in self.search_connections.copy():
            if connection_id in self.active_connections:
                try:
                    await self.active_connections[connection_id].send_text(
                        json.dumps(message, ensure_ascii=False)
                    )
                except Exception as e:
                    logger.error(f"广播搜索建议失败 {connection_id}: {str(e)}")
                    disconnected_connections.append(connection_id)
            else:
                disconnected_connections.append(connection_id)

        # 清理断开的连接
        for conn_id in disconnected_connections:
            self.disconnect(conn_id)

    def subscribe_to_index(self, connection_id: str, index_id: int):
        """订阅索引任务进度"""
        if index_id not in self.index_subscriptions:
            self.index_subscriptions[index_id] = set()
        self.index_subscriptions[index_id].add(connection_id)
        logger.info(f"连接 {connection_id} 订阅索引任务 {index_id}")

    def subscribe_to_search_suggestions(self, connection_id: str):
        """订阅搜索建议"""
        self.search_connections.add(connection_id)
        logger.info(f"连接 {connection_id} 订阅搜索建议")

# 全局连接管理器实例
manager = ConnectionManager()


def generate_connection_id() -> str:
    """生成唯一连接ID"""
    import uuid
    return str(uuid.uuid4())


@router.websocket("/ws/index/{index_id}")
async def websocket_index_progress(websocket: WebSocket, index_id: int):
    """
    索引进度实时推送WebSocket接口

    - **index_id**: 索引任务ID
    """
    connection_id = generate_connection_id()
    logger.info(f"新索引进度WebSocket连接请求: index_id={index_id}, connection_id={connection_id}")

    try:
        # 建立连接
        await manager.connect(websocket, connection_id)
        manager.subscribe_to_index(connection_id, index_id)

        # 获取数据库连接
        from app.core.database import SessionLocal
        db = SessionLocal()

        try:
            # 验证索引任务是否存在
            from app.models.index_job import IndexJobModel
            index_job = db.query(IndexJobModel).filter(IndexJobModel.id == index_id).first()

            if not index_job:
                await manager.send_personal_message({
                    "type": "error",
                    "data": {
                        "error": f"索引任务 {index_id} 不存在",
                        "index_id": index_id,
                        "timestamp": datetime.now().isoformat()
                    }
                }, connection_id)
                return

            # 发送当前状态
            await manager.send_personal_message({
                "type": "status_update",
                "data": {
                    "index_id": index_id,
                    "status": index_job.status,
                    "progress": index_job.processed_files,
                    "total_files": index_job.total_files,
                    "processed_files": index_job.processed_files,
                    "error_count": index_job.error_count,
                    "folder_path": index_job.folder_path,
                    "started_at": index_job.started_at.isoformat() if index_job.started_at else None,
                    "completed_at": index_job.completed_at.isoformat() if index_job.completed_at else None,
                    "error_message": index_job.error_message,
                    "timestamp": datetime.now().isoformat()
                }
            }, connection_id)

            # 启动进度监控任务
            progress_task = asyncio.create_task(
                monitor_index_progress(connection_id, index_id, db)
            )

            # 保持连接活跃，监听客户端消息
            while True:
                try:
                    # 等待客户端消息（可能为心跳包）
                    data = await websocket.receive_text()
                    message = json.loads(data) if data else {}

                    # 处理心跳包
                    if message.get("type") == "ping":
                        await manager.send_personal_message({
                            "type": "pong",
                            "timestamp": datetime.now().isoformat()
                        }, connection_id)

                except WebSocketDisconnect:
                    break
                except json.JSONDecodeError:
                    logger.warning(f"收到无效JSON消息: {connection_id}")
                except Exception as e:
                    logger.error(f"处理WebSocket消息错误 {connection_id}: {str(e)}")
                    break

        finally:
            db.close()
            if 'progress_task' in locals():
                progress_task.cancel()
                try:
                    await progress_task
                except asyncio.CancelledError:
                    pass

    except WebSocketDisconnect:
        logger.info(f"索引进度WebSocket客户端主动断开: {connection_id}")
    except Exception as e:
        logger.error(f"索引进度WebSocket错误 {connection_id}: {str(e)}")
        await manager.send_personal_message({
            "type": "error",
            "data": {
                "error": f"服务器内部错误: {str(e)}",
                "index_id": index_id,
                "timestamp": datetime.now().isoformat()
            }
        }, connection_id)
    finally:
        manager.disconnect(connection_id)


@router.websocket("/ws/search-suggest")
async def websocket_search_suggestions(websocket: WebSocket):
    """
    搜索建议推送WebSocket接口
    """
    connection_id = generate_connection_id()
    logger.info(f"新搜索建议WebSocket连接请求: connection_id={connection_id}")

    try:
        # 建立连接
        await manager.connect(websocket, connection_id)
        manager.subscribe_to_search_suggestions(connection_id)

        # 发送连接确认
        await manager.send_personal_message({
            "type": "connected",
            "data": {
                "connection_id": connection_id,
                "service": "search_suggestions",
                "timestamp": datetime.now().isoformat()
            }
        }, connection_id)

        # 保持连接活跃，监听搜索建议请求
        while True:
            try:
                # 接收客户端消息
                data = await websocket.receive_text()
                message = json.loads(data) if data else {}

                # 处理搜索建议请求
                if message.get("type") == "search_suggestions":
                    query = message.get("query", "")
                    limit = message.get("limit", 5)

                    # 生成搜索建议
                    suggestions = await generate_search_suggestions(query, limit)

                    await manager.send_personal_message({
                        "type": "suggestions",
                        "data": {
                            "query": query,
                            "suggestions": suggestions,
                            "total": len(suggestions),
                            "timestamp": datetime.now().isoformat()
                        }
                    }, connection_id)

                # 处理心跳包
                elif message.get("type") == "ping":
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    }, connection_id)

                else:
                    logger.warning(f"未知消息类型: {message.get('type')} from {connection_id}")

            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                logger.warning(f"收到无效JSON消息: {connection_id}")
            except Exception as e:
                logger.error(f"处理搜索建议WebSocket消息错误 {connection_id}: {str(e)}")
                break

    except WebSocketDisconnect:
        logger.info(f"搜索建议WebSocket客户端主动断开: {connection_id}")
    except Exception as e:
        logger.error(f"搜索建议WebSocket错误 {connection_id}: {str(e)}")
        await manager.send_personal_message({
            "type": "error",
            "data": {
                "error": f"服务器内部错误: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        }, connection_id)
    finally:
        manager.disconnect(connection_id)


async def monitor_index_progress(connection_id: str, index_id: int, db: Session):
    """
    监控索引任务进度
    """
    from app.models.index_job import IndexJobModel

    last_status = None
    last_progress = -1

    try:
        while True:
            # 检查连接是否还存在
            if connection_id not in manager.active_connections:
                break

            # 刷新数据库会话
            db.refresh(db.query(IndexJobModel).filter(IndexJobModel.id == index_id).first())

            # 获取当前任务状态
            index_job = db.query(IndexJobModel).filter(IndexJobModel.id == index_id).first()

            if not index_job:
                # 任务不存在，发送错误消息
                await manager.send_personal_message({
                    "type": "error",
                    "data": {
                        "error": f"索引任务 {index_id} 不存在或已被删除",
                        "index_id": index_id,
                        "timestamp": datetime.now().isoformat()
                    }
                }, connection_id)
                break

            # 检查状态或进度是否有变化
            status_changed = index_job.status != last_status
            progress_changed = index_job.processed_files != last_progress

            if status_changed or progress_changed:
                # 发送进度更新
                message_type = "completed" if index_job.status in [
                    get_enum_value(JobStatus.COMPLETED),
                    get_enum_value(JobStatus.FAILED)
                ] else "progress_update"

                await manager.broadcast_to_index_subscribers({
                    "type": message_type,
                    "data": {
                        "index_id": index_id,
                        "status": index_job.status,
                        "progress": int((index_job.processed_files / index_job.total_files * 100)
                                       if index_job.total_files > 0 else 0),
                        "processed_files": index_job.processed_files,
                        "total_files": index_job.total_files,
                        "error_count": index_job.error_count,
                        "started_at": index_job.started_at.isoformat() if index_job.started_at else None,
                        "completed_at": index_job.completed_at.isoformat() if index_job.completed_at else None,
                        "error_message": index_job.error_message,
                        "timestamp": datetime.now().isoformat()
                    }
                }, index_id)

                last_status = index_job.status
                last_progress = index_job.processed_files

                # 如果任务已完成或失败，停止监控
                if index_job.status in [
                    get_enum_value(JobStatus.COMPLETED),
                    get_enum_value(JobStatus.FAILED)
                ]:
                    logger.info(f"索引任务 {index_id} 已完成，停止进度监控")
                    break

            # 等待2秒再检查下一次
            await asyncio.sleep(2)

    except asyncio.CancelledError:
        logger.info(f"索引任务 {index_id} 进度监控任务已取消")
    except Exception as e:
        logger.error(f"监控索引任务 {index_id} 进度时出错: {str(e)}")
        await manager.send_personal_message({
            "type": "error",
            "data": {
                "error": f"监控进度时出错: {str(e)}",
                "index_id": index_id,
                "timestamp": datetime.now().isoformat()
            }
        }, connection_id)


async def generate_search_suggestions(query: str, limit: int) -> list:
    """
    生成搜索建议

    基于搜索历史和常见模式生成建议
    """
    if not query or len(query) < 1:
        return []

    try:
        from app.core.database import SessionLocal
        from app.models.search_history import SearchHistoryModel

        db = SessionLocal()
        try:
            # 从搜索历史中查找匹配的建议
            history_suggestions = db.query(SearchHistoryModel.search_query)\
                .filter(SearchHistoryModel.search_query.like(f"{query}%"))\
                .distinct()\
                .limit(limit * 2)\
                .all()

            suggestions = [row[0] for row in history_suggestions if row[0] != query]

            # 如果历史建议不够，添加一些常见的搜索模式
            if len(suggestions) < limit:
                common_patterns = [
                    f"{query}技术",
                    f"{query}发展",
                    f"{query}应用",
                    f"{query}方法",
                    f"{query}工具",
                    f"{query}教程",
                    f"{query}介绍",
                    f"{query}原理",
                    f"{query}实践",
                    f"{query}案例"
                ]

                for pattern in common_patterns:
                    if pattern not in suggestions and len(suggestions) < limit:
                        suggestions.append(pattern)

            return suggestions[:limit]

        finally:
            db.close()

    except Exception as e:
        logger.error(f"生成搜索建议失败: {str(e)}")
        # 返回一些默认建议
        return [
            f"{query}技术",
            f"{query}发展",
            f"{query}应用"
        ][:limit]


# 导出连接管理器，供其他模块使用
__all__ = ["manager", "ConnectionManager"]