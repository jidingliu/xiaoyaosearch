"""
分块索引服务

扩展现有索引构建功能，支持分块级索引构建。
提供透明的分块索引能力，保持与现有API完全兼容。
"""

import os
import pickle
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging
from pathlib import Path

from app.core.logging_config import get_logger
from app.services.chunk_service import get_chunk_service, ChunkInfo

try:
    import faiss
    import numpy as np
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logging.warning("faiss未安装，向量索引功能不可用")

try:
    from whoosh import index, fields, schema
    from whoosh.filedb.filestore import FileStorage
    WHOOSH_AVAILABLE = True
except ImportError:
    WHOOSH_AVAILABLE = False
    logging.warning("whoosh未安装，全文索引功能不可用")

try:
    from app.services.ai_model_manager import ai_model_service
    AI_MODEL_SERVICE_AVAILABLE = True
except ImportError as e:
    AI_MODEL_SERVICE_AVAILABLE = False
    ai_model_service = None
    logger.warning(f"AI模型服务不可用: {e}")

logger = get_logger(__name__)


class ChunkIndexService:
    """分块索引服务

    功能：
    - 自动分块检测和处理
    - 分块级Faiss向量索引构建
    - 分块级Whoosh全文索引构建
    - 批量向量化优化
    - 完全向后兼容现有索引流程
    """

    def __init__(
        self,
        faiss_index_path: str,
        whoosh_index_path: str,
        chunk_faiss_index_path: Optional[str] = None,
        chunk_whoosh_index_path: Optional[str] = None,
        use_ai_models: bool = True,
        chunk_strategy: str = "500+50"
    ):
        """初始化分块索引服务

        Args:
            faiss_index_path: 传统Faiss索引文件路径
            whoosh_index_path: 传统Whoosh索引目录路径
            chunk_faiss_index_path: 分块Faiss索引文件路径
            chunk_whoosh_index_path: 分块Whoosh索引目录路径
            use_ai_models: 是否使用AI模型
            chunk_strategy: 分块策略
        """
        self.faiss_index_path = faiss_index_path
        self.whoosh_index_path = whoosh_index_path
        self.use_ai_models = use_ai_models
        self.chunk_strategy = chunk_strategy

        # 设置分块索引路径
        if not chunk_faiss_index_path:
            chunk_faiss_index_path = faiss_index_path.replace('.faiss', '_chunks.faiss')
        if not chunk_whoosh_index_path:
            chunk_whoosh_index_path = whoosh_index_path + '_chunks'

        self.chunk_faiss_index_path = chunk_faiss_index_path
        self.chunk_whoosh_index_path = chunk_whoosh_index_path

        # 初始化分块服务
        self.chunk_service = get_chunk_service()

        # 索引统计
        self.index_stats = {
            'total_documents_processed': 0,
            'total_chunks_created': 0,
            'chunked_documents': 0,
            'traditional_documents': 0,
            'avg_chunks_per_document': 0.0,
            'embedding_batch_size': 32,
            'last_index_time': None
        }

        # 确保索引目录存在
        os.makedirs(os.path.dirname(self.chunk_faiss_index_path), exist_ok=True)
        os.makedirs(self.chunk_whoosh_index_path, exist_ok=True)

    async def build_chunk_indexes(self, documents: List[Dict[str, Any]]) -> bool:
        """构建分块索引

        Args:
            documents: 文档列表

        Returns:
            bool: 构建是否成功
        """
        try:
            logger.info(f"开始构建分块索引，文档数量: {len(documents)}")
            start_time = datetime.now()

            # 1. 分离需要分块的文档和传统文档
            chunked_docs, traditional_docs = self._separate_documents(documents)

            logger.info(f"需要分块的文档: {len(chunked_docs)}, 传统文档: {len(traditional_docs)}")

            # 2. 处理需要分块的文档
            if chunked_docs:
                success = await self._process_chunked_documents(chunked_docs)
                if not success:
                    logger.error("分块文档处理失败")
                    return False

            # 3. 处理传统文档（如果分块索引不存在，传统文档也添加到分块索引中）
            if traditional_docs and not self._chunk_indexes_exist():
                success = await self._process_traditional_documents(traditional_docs)
                if not success:
                    logger.error("传统文档处理失败")
                    return False

            # 4. 更新统计信息
            self._update_index_stats(len(chunked_docs), len(traditional_docs))
            self.index_stats['last_index_time'] = datetime.now()

            duration = datetime.now() - start_time
            logger.info(f"分块索引构建完成，耗时: {duration.total_seconds():.2f} 秒")

            return True

        except Exception as e:
            logger.error(f"构建分块索引失败: {e}")
            return False

    def _separate_documents(self, documents: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """分离需要分块的文档和传统文档

        Args:
            documents: 文档列表

        Returns:
            Tuple[List[Dict], List[Dict]]: (需要分块的文档, 传统文档)
        """
        chunked_docs = []
        traditional_docs = []

        for doc in documents:
            content = doc.get('content', '')
            file_type = doc.get('file_type', '')

            # 判断是否需要分块
            if self._should_chunk_document(content, file_type):
                chunked_docs.append(doc)
            else:
                traditional_docs.append(doc)

        return chunked_docs, traditional_docs

    def _should_chunk_document(self, content: str, file_type: str) -> bool:
        """判断文档是否需要分块

        Args:
            content: 文档内容
            file_type: 文件类型

        Returns:
            bool: 是否需要分块
        """
        # 1. 内容长度检查
        if not content or len(content) <= 600:  # 略大于分块大小
            return False

        # 2. 文件类型检查
        chunkable_types = ['document', 'text', 'pdf']
        if file_type not in chunkable_types:
            return False

        # 3. 内容结构检查（有段落分隔符的内容更适合分块）
        paragraph_indicators = ['\n\n', '。', '！', '？', '. ', '! ', '? ']
        has_paragraphs = any(indicator in content for indicator in paragraph_indicators)

        return has_paragraphs

    async def _process_chunked_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """处理需要分块的文档

        Args:
            documents: 需要分块的文档列表

        Returns:
            bool: 处理是否成功
        """
        try:
            logger.info(f"开始处理 {len(documents)} 个需要分块的文档")

            # 1. 对每个文档进行分块
            all_chunks = []
            for doc in documents:
                chunks = await self._chunk_document(doc)
                all_chunks.extend(chunks)

            logger.info(f"分块完成，共生成 {len(all_chunks)} 个分块")

            # 2. 构建分块Faiss向量索引
            if FAISS_AVAILABLE and self.use_ai_models and AI_MODEL_SERVICE_AVAILABLE:
                faiss_success = await self._build_chunk_faiss_index(all_chunks)
                if not faiss_success:
                    logger.warning("分块Faiss索引构建失败，但继续构建其他索引")
            else:
                logger.info("跳过分块Faiss索引构建（条件不满足）")
                faiss_success = True

            # 3. 构建分块Whoosh全文索引
            if WHOOSH_AVAILABLE:
                whoosh_success = await self._build_chunk_whoosh_index(all_chunks)
                if not whoosh_success:
                    logger.warning("分块Whoosh索引构建失败，但继续构建其他索引")
            else:
                logger.info("跳过分块Whoosh索引构建（条件不满足）")
                whoosh_success = True

            # 4. 保存分块数据到数据库
            db_success = await self._save_chunks_to_database(all_chunks)
            if not db_success:
                logger.warning("分块数据保存失败，但索引构建已完成")

            return faiss_success and whoosh_success

        except Exception as e:
            logger.error(f"处理分块文档失败: {e}")
            return False

    async def _chunk_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """对单个文档进行分块

        Args:
            document: 文档数据

        Returns:
            List[Dict[str, Any]]: 分块列表
        """
        try:
            content = document.get('content', '')
            file_id = document.get('id', '')

            # 使用分块服务进行智能分块
            chunk_infos = self.chunk_service.intelligent_chunking(content, self.chunk_strategy)

            # 转换为分块数据格式
            chunks = []
            for chunk_info in chunk_infos:
                chunk_data = {
                    'file_id': file_id,
                    'chunk_index': chunk_info.chunk_index,
                    'content': chunk_info.content,
                    'content_length': chunk_info.content_length,
                    'start_position': chunk_info.start_position,
                    'end_position': chunk_info.end_position,
                    'file_name': document.get('file_name', ''),
                    'file_path': document.get('file_path', ''),
                    'file_type': document.get('file_type', ''),
                    'file_size': document.get('file_size', 0),
                    'modified_time': document.get('modified_time', ''),
                    'created_at': datetime.now()
                }
                chunks.append(chunk_data)

            return chunks

        except Exception as e:
            logger.error(f"文档分块失败 {document.get('file_name', 'unknown')}: {e}")
            return []

    async def _build_chunk_faiss_index(self, chunks: List[Dict[str, Any]]) -> bool:
        """构建分块Faiss向量索引

        Args:
            chunks: 分块列表

        Returns:
            bool: 构建是否成功
        """
        try:
            logger.info(f"开始构建分块Faiss索引，分块数量: {len(chunks)}")

            # 1. 批量生成向量嵌入
            embeddings = await self._generate_chunk_embeddings(chunks)
            if not embeddings:
                logger.error("向量嵌入生成失败")
                return False

            # 2. 创建Faiss索引
            dimension = len(embeddings[0])
            index = faiss.IndexFlatIP(dimension)  # 使用内积相似度

            # 3. 添加向量到索引
            embeddings_array = np.array(embeddings, dtype=np.float32)
            index.add(embeddings_array)

            # 4. 保存索引
            faiss.write_index(index, self.chunk_faiss_index_path)

            # 5. 保存元数据
            metadata = {
                'chunk_ids': [str(chunk.get('chunk_index', f'chunk_{i}')) + '_' + str(chunk.get('file_id', '')) for i, chunk in enumerate(chunks)],
                'file_ids': [chunk.get('file_id', '') for chunk in chunks],
                'dimension': dimension,
                'total_chunks': len(chunks),
                'created_at': datetime.now().isoformat(),
                'chunk_strategy': self.chunk_strategy
            }

            metadata_path = self.chunk_faiss_index_path.replace('.faiss', '_metadata.pkl')
            with open(metadata_path, 'wb') as f:
                pickle.dump(metadata, f)

            logger.info(f"分块Faiss索引构建成功，维度: {dimension}, 分块数: {index.ntotal}")
            return True

        except Exception as e:
            logger.error(f"构建分块Faiss索引失败: {e}")
            return False

    async def _generate_chunk_embeddings(self, chunks: List[Dict[str, Any]]) -> List[List[float]]:
        """批量生成分块向量嵌入

        Args:
            chunks: 分块列表

        Returns:
            List[List[float]]: 向量嵌入列表
        """
        try:
            embeddings = []
            batch_size = self.index_stats['embedding_batch_size']

            logger.info(f"开始批量生成 {len(chunks)} 个分块的向量嵌入，批次大小: {batch_size}")

            for i in range(0, len(chunks), batch_size):
                batch_chunks = chunks[i:i + batch_size]
                batch_texts = [chunk['content'] for chunk in batch_chunks if chunk['content'].strip()]

                if not batch_texts:
                    continue

                # 批量生成嵌入
                batch_embeddings = await ai_model_service.batch_text_embedding(
                    batch_texts,
                    normalize_embeddings=True
                )

                embeddings.extend(batch_embeddings)

                # 进度日志
                processed = min(i + batch_size, len(chunks))
                logger.debug(f"向量嵌入进度: {processed}/{len(chunks)}")

            logger.info(f"向量嵌入生成完成，共 {len(embeddings)} 个")
            return embeddings

        except Exception as e:
            logger.error(f"生成分块向量嵌入失败: {e}")
            return []

    async def _build_chunk_whoosh_index(self, chunks: List[Dict[str, Any]]) -> bool:
        """构建分块Whoosh全文索引

        Args:
            chunks: 分块列表

        Returns:
            bool: 构建是否成功
        """
        try:
            logger.info(f"开始构建分块Whoosh索引，分块数量: {len(chunks)}")

            # 1. 定义分块索引schema
            chunk_schema = schema.Schema(
                id=fields.ID(stored=True),
                chunk_id=fields.ID(stored=True),
                file_id=fields.ID(stored=True),
                file_name=fields.TEXT(stored=True),
                file_path=fields.ID(stored=True),
                file_type=fields.ID(stored=True),
                content=fields.TEXT(stored=True),
                chunk_index=fields.NUMERIC(stored=True, sortable=True),
                start_position=fields.NUMERIC(stored=True),
                end_position=fields.NUMERIC(stored=True),
                content_length=fields.NUMERIC(stored=True),
                modified_time=fields.ID(stored=True),
                created_at=fields.ID(stored=True)
            )

            # 2. 创建或打开索引
            if os.path.exists(self.chunk_whoosh_index_path) and os.listdir(self.chunk_whoosh_index_path):
                # 索引已存在，打开并添加
                storage = FileStorage(self.chunk_whoosh_index_path)
                ix = storage.open_index(schema=chunk_schema)
                writer = ix.writer()
            else:
                # 创建新索引
                storage = FileStorage(self.chunk_whoosh_index_path)
                ix = storage.create_index(chunk_schema)
                writer = ix.writer()

            try:
                # 3. 添加分块到索引
                for i, chunk in enumerate(chunks):
                    # 生成唯一的分块ID
                    chunk_id = f"{chunk['file_id']}_chunk_{chunk['chunk_index']}"

                    writer.add_document(
                        id=str(i),
                        chunk_id=chunk_id,
                        file_id=str(chunk['file_id']),
                        file_name=chunk['file_name'],
                        file_path=chunk['file_path'],
                        file_type=chunk['file_type'],
                        content=chunk['content'],
                        chunk_index=chunk['chunk_index'],
                        start_position=chunk['start_position'],
                        end_position=chunk['end_position'],
                        content_length=chunk['content_length'],
                        modified_time=chunk['modified_time'],
                        created_at=chunk['created_at'].isoformat() if isinstance(chunk['created_at'], datetime) else str(chunk['created_at'])
                    )

                    # 定期提交以避免内存占用过大
                    if (i + 1) % 100 == 0:
                        writer.commit()
                        writer = ix.writer()  # 重新获取writer
                        logger.debug(f"已索引 {i + 1}/{len(chunks)} 个分块")

                # 最终提交
                writer.commit()

                logger.info(f"分块Whoosh索引构建成功")
                return True

            except Exception as e:
                writer.cancel()
                raise e

        except Exception as e:
            logger.error(f"构建分块Whoosh索引失败: {e}")
            return False

    async def _process_traditional_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """处理传统文档（将它们作为单个分块添加到分块索引中）

        Args:
            documents: 传统文档列表

        Returns:
            bool: 处理是否成功
        """
        try:
            logger.info(f"处理 {len(documents)} 个传统文档作为单分块")

            # 将传统文档转换为单分块格式
            single_chunks = []
            for doc in documents:
                chunk_data = {
                    'file_id': doc.get('id', ''),
                    'chunk_index': 0,
                    'content': doc.get('content', ''),
                    'content_length': len(doc.get('content', '')),
                    'start_position': 0,
                    'end_position': len(doc.get('content', '')),
                    'file_name': doc.get('file_name', ''),
                    'file_path': doc.get('file_path', ''),
                    'file_type': doc.get('file_type', ''),
                    'file_size': doc.get('file_size', 0),
                    'modified_time': doc.get('modified_time', ''),
                    'created_at': datetime.now()
                }
                single_chunks.append(chunk_data)

            # 构建索引（使用相同的流程）
            return await self._process_chunked_documents(single_chunks)

        except Exception as e:
            logger.error(f"处理传统文档失败: {e}")
            return False

    async def _save_chunks_to_database(self, chunks: List[Dict[str, Any]]) -> bool:
        """保存分块数据到数据库

        Args:
            chunks: 分块列表

        Returns:
            bool: 保存是否成功
        """
        try:
            from app.core.database import SessionLocal
            from app.models.file_chunk import FileChunkModel

            db = SessionLocal()
            try:
                logger.info(f"开始保存 {len(chunks)} 个分块到数据库")

                for i, chunk_data in enumerate(chunks):
                    # 检查是否已存在
                    existing_chunk = db.query(FileChunkModel).filter(
                        FileChunkModel.file_id == int(chunk_data['file_id']),
                        FileChunkModel.chunk_index == chunk_data['chunk_index']
                    ).first()

                    if existing_chunk:
                        # 更新现有分块
                        for key, value in chunk_data.items():
                            if hasattr(existing_chunk, key) and key != 'id':
                                setattr(existing_chunk, key, value)
                        existing_chunk.indexed_at = datetime.now()
                    else:
                        # 创建新分块记录
                        chunk_record = FileChunkModel(
                            file_id=int(chunk_data['file_id']),
                            chunk_index=chunk_data['chunk_index'],
                            content=chunk_data['content'],
                            content_length=chunk_data['content_length'],
                            start_position=chunk_data['start_position'],
                            end_position=chunk_data['end_position'],
                            is_indexed=True,
                            index_status='completed',
                            indexed_at=datetime.now()
                        )
                        db.add(chunk_record)

                    # 定期提交
                    if (i + 1) % 50 == 0:
                        db.commit()
                        logger.debug(f"已保存 {i + 1}/{len(chunks)} 个分块")

                # 最终提交
                db.commit()
                logger.info(f"成功保存 {len(chunks)} 个分块到数据库")
                return True

            finally:
                db.close()

        except Exception as e:
            logger.error(f"保存分块到数据库失败: {e}")
            return False

    def _chunk_indexes_exist(self) -> bool:
        """检查分块索引是否存在"""
        faiss_exists = os.path.exists(self.chunk_faiss_index_path)
        whoosh_exists = os.path.exists(self.chunk_whoosh_index_path) and os.listdir(self.chunk_whoosh_index_path)
        return faiss_exists or whoosh_exists

    def _update_index_stats(self, chunked_count: int, traditional_count: int):
        """更新索引统计信息"""
        self.index_stats['total_documents_processed'] += chunked_count + traditional_count
        self.index_stats['chunked_documents'] += chunked_count
        self.index_stats['traditional_documents'] += traditional_count

        # 估算总分块数（假设平均每个文档3个分块）
        self.index_stats['total_chunks_created'] += chunked_count * 3 + traditional_count

        # 计算平均分块数
        total_docs = self.index_stats['total_documents_processed']
        if total_docs > 0:
            self.index_stats['avg_chunks_per_document'] = self.index_stats['total_chunks_created'] / total_docs

    async def update_chunk_indexes(self, new_chunks: List[Dict[str, Any]]) -> bool:
        """增量更新分块索引

        Args:
            new_chunks: 新分块列表

        Returns:
            bool: 更新是否成功
        """
        try:
            logger.info(f"开始增量更新分块索引，新分块数: {len(new_chunks)}")

            # 1. 更新Faiss索引（如果存在）
            if FAISS_AVAILABLE and os.path.exists(self.chunk_faiss_index_path):
                faiss_success = await self._update_faiss_index(new_chunks)
            else:
                faiss_success = True  # 如果没有索引，认为更新成功

            # 2. 更新Whoosh索引（如果存在）
            if WHOOSH_AVAILABLE and os.path.exists(self.chunk_whoosh_index_path):
                whoosh_success = await self._update_whoosh_index(new_chunks)
            else:
                whoosh_success = True

            # 3. 保存到数据库
            db_success = await self._save_chunks_to_database(new_chunks)

            return faiss_success and whoosh_success and db_success

        except Exception as e:
            logger.error(f"增量更新分块索引失败: {e}")
            return False

    async def _update_faiss_index(self, new_chunks: List[Dict[str, Any]]) -> bool:
        """增量更新Faiss索引"""
        try:
            # 读取现有索引
            index = faiss.read_index(self.chunk_faiss_index_path)

            # 生成新向量的嵌入
            embeddings = await self._generate_chunk_embeddings(new_chunks)
            if not embeddings:
                return False

            # 添加新向量
            embeddings_array = np.array(embeddings, dtype=np.float32)
            index.add(embeddings_array)

            # 保存更新后的索引
            faiss.write_index(index, self.chunk_faiss_index_path)

            # 更新元数据
            metadata_path = self.chunk_faiss_index_path.replace('.faiss', '_metadata.pkl')
            with open(metadata_path, 'rb') as f:
                metadata = pickle.load(f)

            metadata['chunk_ids'].extend([
                str(chunk.get('chunk_index', f'chunk_{i}')) + '_' + str(chunk.get('file_id', ''))
                for i, chunk in enumerate(new_chunks)
            ])
            metadata['file_ids'].extend([chunk.get('file_id', '') for chunk in new_chunks])
            metadata['total_chunks'] = index.ntotal
            metadata['last_updated'] = datetime.now().isoformat()

            with open(metadata_path, 'wb') as f:
                pickle.dump(metadata, f)

            logger.info(f"Faiss索引增量更新成功，新增 {len(embeddings)} 个向量")
            return True

        except Exception as e:
            logger.error(f"Faiss索引增量更新失败: {e}")
            return False

    async def _update_whoosh_index(self, new_chunks: List[Dict[str, Any]]) -> bool:
        """增量更新Whoosh索引"""
        try:
            from whoosh import index as whoosh_index

            ix = whoosh_index.open_dir(self.chunk_whoosh_index_path)
            writer = ix.writer()

            try:
                for i, chunk in enumerate(new_chunks):
                    chunk_id = f"{chunk['file_id']}_chunk_{chunk['chunk_index']}"

                    writer.add_document(
                        id=str(int(time.time() * 1000000) + i),  # 生成唯一ID
                        chunk_id=chunk_id,
                        file_id=str(chunk['file_id']),
                        file_name=chunk['file_name'],
                        file_path=chunk['file_path'],
                        file_type=chunk['file_type'],
                        content=chunk['content'],
                        chunk_index=chunk['chunk_index'],
                        start_position=chunk['start_position'],
                        end_position=chunk['end_position'],
                        content_length=chunk['content_length'],
                        modified_time=chunk['modified_time'],
                        created_at=chunk['created_at'].isoformat() if isinstance(chunk['created_at'], datetime) else str(chunk['created_at'])
                    )

                writer.commit()
                logger.info(f"Whoosh索引增量更新成功，新增 {len(new_chunks)} 个分块")
                return True

            except Exception as e:
                writer.cancel()
                raise e

        except Exception as e:
            logger.error(f"Whoosh索引增量更新失败: {e}")
            return False

    def get_index_stats(self) -> Dict[str, Any]:
        """获取索引统计信息"""
        stats = self.index_stats.copy()

        # 添加索引文件信息
        stats.update({
            'chunk_faiss_index_path': self.chunk_faiss_index_path,
            'chunk_whoosh_index_path': self.chunk_whoosh_index_path,
            'chunk_faiss_index_exists': os.path.exists(self.chunk_faiss_index_path),
            'chunk_whoosh_index_exists': os.path.exists(self.chunk_whoosh_index_path) and os.listdir(self.chunk_whoosh_index_path),
            'chunk_strategy': self.chunk_strategy
        })

        # 如果索引存在，添加索引大小信息
        if os.path.exists(self.chunk_faiss_index_path):
            stats['chunk_faiss_index_size'] = os.path.getsize(self.chunk_faiss_index_path)

        return stats

    def cleanup_indexes(self):
        """清理索引文件"""
        try:
            # 删除分块索引文件
            if os.path.exists(self.chunk_faiss_index_path):
                os.remove(self.chunk_faiss_index_path)
                metadata_path = self.chunk_faiss_index_path.replace('.faiss', '_metadata.pkl')
                if os.path.exists(metadata_path):
                    os.remove(metadata_path)

            # 删除Whoosh索引目录
            if os.path.exists(self.chunk_whoosh_index_path):
                import shutil
                shutil.rmtree(self.chunk_whoosh_index_path)

            logger.info("分块索引文件清理完成")

        except Exception as e:
            logger.error(f"清理分块索引失败: {e}")


# 创建全局分块索引服务实例
_chunk_index_service: Optional[ChunkIndexService] = None


def get_chunk_index_service() -> ChunkIndexService:
    """获取分块索引服务实例"""
    global _chunk_index_service
    if _chunk_index_service is None:
        # 使用默认路径创建服务实例
        data_root = os.getenv('DATA_ROOT', '../data')
        faiss_path = os.path.join(data_root, 'indexes/faiss/document_index.faiss')
        whoosh_path = os.path.join(data_root, 'indexes/whoosh')

        _chunk_index_service = ChunkIndexService(
            faiss_index_path=faiss_path,
            whoosh_index_path=whoosh_path,
            use_ai_models=True
        )

    return _chunk_index_service


def reload_chunk_index_service():
    """重新加载分块索引服务"""
    global _chunk_index_service
    _chunk_index_service = None