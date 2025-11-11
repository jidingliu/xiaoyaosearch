"""
索引管理器 - 整合Faiss和Whoosh
"""

import os
import pickle
import hashlib
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import faiss
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, NUMERIC, KEYWORD
from whoosh.qparser import QueryParser, MultifieldParser
from jieba.analyse import ChineseAnalyzer
import logging

logger = logging.getLogger(__name__)


class IndexManager:
    """索引管理器 - 整合向量索引和全文索引"""

    def __init__(self, index_dir: str):
        self.index_dir = index_dir
        self.vector_index = None
        self.text_index = None
        self.text_schema = None
        self.document_mapping = {}  # ID到文档内容的映射
        self._initialize_indices()

    def _initialize_indices(self):
        """初始化索引"""
        try:
            # 创建索引目录
            os.makedirs(self.index_dir, exist_ok=True)

            # 初始化Faiss向量索引
            self._init_vector_index()

            # 初始化Whoosh全文索引
            self._init_text_index()

            logger.info(f"索引管理器初始化完成: {self.index_dir}")

        except Exception as e:
            logger.error(f"索引初始化失败: {str(e)}")
            raise

    def _init_vector_index(self):
        """初始化Faiss向量索引"""
        try:
            vector_index_path = os.path.join(self.index_dir, "vector.index")
            mapping_path = os.path.join(self.index_dir, "vector_mapping.pkl")

            if os.path.exists(vector_index_path):
                # 加载现有索引
                self.vector_index = faiss.read_index(vector_index_path)
                if os.path.exists(mapping_path):
                    with open(mapping_path, 'rb') as f:
                        self.document_mapping = pickle.load(f)
                logger.info(f"加载现有向量索引: {self.vector_index.ntotal} 个向量")
            else:
                # 创建新索引
                dimension = 768  # BGE模型的向量维度
                self.vector_index = faiss.IndexFlatIP(dimension)  # 内积搜索
                logger.info("创建新的向量索引")

        except Exception as e:
            logger.error(f"向量索引初始化失败: {str(e)}")
            raise

    def _init_text_index(self):
        """初始化Whoosh全文索引"""
        try:
            text_index_path = os.path.join(self.index_dir, "text_index")

            if exists_in(text_index_path):
                # 打开现有索引
                self.text_index = open_dir(text_index_path)
                logger.info("打开现有全文索引")
            else:
                # 创建新索引
                os.makedirs(text_index_path, exist_ok=True)
                self.text_index = create_in(text_index_path, self._create_schema())
                logger.info("创建新的全文索引")

        except Exception as e:
            logger.error(f"全文索引初始化失败: {str(e)}")
            raise

    def _create_schema(self):
        """创建Whoosh索引模式"""
        self.text_schema = Schema(
            id=ID(stored=True, unique=True),
            title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
            content=TEXT(stored=True, analyzer=ChineseAnalyzer()),
            file_path=KEYWORD(stored=True),
            file_type=KEYWORD(stored=True),
            modified_time=NUMERIC(stored=True, sortable=True),
            size=NUMERIC(stored=True, sortable=True)
        )
        return self.text_schema

    def add_document(self, doc_id: str, content: str, vector: np.ndarray, metadata: Dict[str, Any]):
        """添加文档到索引"""
        try:
            # 添加到向量索引
            if len(vector.shape) == 1:
                vector = vector.reshape(1, -1)

            # 归一化向量（如果使用余弦相似度）
            vector = vector / np.linalg.norm(vector, axis=1, keepdims=True)

            # 获取当前索引大小作为ID
            current_size = self.vector_index.ntotal
            self.vector_index.add(vector)

            # 记录映射关系
            self.document_mapping[current_size] = {
                'doc_id': doc_id,
                'metadata': metadata
            }

            # 添加到全文索引
            writer = self.text_index.writer()
            writer.add_document(
                id=doc_id,
                title=metadata.get('title', ''),
                content=content,
                file_path=metadata.get('file_path', ''),
                file_type=metadata.get('file_type', ''),
                modified_time=metadata.get('modified_time', 0),
                size=metadata.get('size', 0)
            )
            writer.commit()

            logger.debug(f"文档已添加到索引: {doc_id}")

        except Exception as e:
            logger.error(f"添加文档到索引失败: {str(e)}")
            raise

    def search_vector(self, query_vector: np.ndarray, top_k: int = 20) -> List[Dict[str, Any]]:
        """向量搜索"""
        try:
            if len(query_vector.shape) == 1:
                query_vector = query_vector.reshape(1, -1)

            # 归一化查询向量
            query_vector = query_vector / np.linalg.norm(query_vector, axis=1, keepdims=True)

            # 执行搜索
            scores, indices = self.vector_index.search(query_vector, min(top_k, self.vector_index.ntotal))

            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx >= 0:  # 有效索引
                    doc_info = self.document_mapping.get(idx, {})
                    results.append({
                        'doc_id': doc_info.get('doc_id', ''),
                        'score': float(score),
                        'vector_rank': i + 1,
                        'metadata': doc_info.get('metadata', {})
                    })

            return results

        except Exception as e:
            logger.error(f"向量搜索失败: {str(e)}")
            return []

    def search_text(self, query: str, top_k: int = 20) -> List[Dict[str, Any]]:
        """全文搜索"""
        try:
            with self.text_index.searcher() as searcher:
                # 使用多字段搜索
                parser = MultifieldParser(
                    ["title", "content"],
                    schema=self.text_schema,
                    fieldboosts={"title": 2.0, "content": 1.0}
                )
                query_obj = parser.parse(query)

                results = searcher.search(query_obj, limit=top_k)

            formatted_results = []
            for i, hit in enumerate(results):
                formatted_results.append({
                    'doc_id': hit['id'],
                    'score': hit.score,
                    'text_rank': i + 1,
                    'metadata': {
                        'title': hit.get('title', ''),
                        'content_preview': hit.get('content', '')[:200] + '...',
                        'file_path': hit.get('file_path', ''),
                        'file_type': hit.get('file_type', ''),
                        'modified_time': hit.get('modified_time', 0),
                        'size': hit.get('size', 0)
                    }
                })

            return formatted_results

        except Exception as e:
            logger.error(f"全文搜索失败: {str(e)}")
            return []

    def search_hybrid(self, query: str, query_vector: np.ndarray, top_k: int = 20,
                     vector_weight: float = 0.6) -> List[Dict[str, Any]]:
        """混合搜索 - 结合向量搜索和全文搜索"""
        try:
            # 获取搜索结果
            vector_results = self.search_vector(query_vector, top_k * 2)
            text_results = self.search_text(query, top_k * 2)

            # 使用RRF算法融合结果
            k = 60  # RRF参数
            doc_scores = {}

            # 向量搜索结果
            for result in vector_results:
                doc_id = result['doc_id']
                vector_rank = result['vector_rank']
                score = result['score']
                rrf_score = vector_weight * (k / (k + vector_rank))
                doc_scores[doc_id] = {
                    'rrf_score': rrf_score,
                    'vector_score': score,
                    'text_score': 0.0,
                    'metadata': result['metadata']
                }

            # 全文搜索结果
            for result in text_results:
                doc_id = result['doc_id']
                text_rank = result['text_rank']
                score = result['score']
                rrf_score = (1 - vector_weight) * (k / (k + text_rank))

                if doc_id in doc_scores:
                    doc_scores[doc_id]['rrf_score'] += rrf_score
                    doc_scores[doc_id]['text_score'] = score
                else:
                    doc_scores[doc_id] = {
                        'rrf_score': rrf_score,
                        'vector_score': 0.0,
                        'text_score': score,
                        'metadata': result['metadata']
                    }

            # 排序并返回结果
            sorted_results = sorted(
                doc_scores.items(),
                key=lambda x: x[1]['rrf_score'],
                reverse=True
            )

            final_results = []
            for doc_id, scores in sorted_results[:top_k]:
                final_results.append({
                    'doc_id': doc_id,
                    'score': scores['rrf_score'],
                    'vector_score': scores['vector_score'],
                    'text_score': scores['text_score'],
                    'metadata': scores['metadata']
                })

            return final_results

        except Exception as e:
            logger.error(f"混合搜索失败: {str(e)}")
            return []

    def save_indices(self):
        """保存索引到磁盘"""
        try:
            # 保存向量索引
            vector_index_path = os.path.join(self.index_dir, "vector.index")
            faiss.write_index(self.vector_index, vector_index_path)

            # 保存文档映射
            mapping_path = os.path.join(self.index_dir, "vector_mapping.pkl")
            with open(mapping_path, 'wb') as f:
                pickle.dump(self.document_mapping, f)

            logger.info("索引已保存到磁盘")

        except Exception as e:
            logger.error(f"保存索引失败: {str(e)}")
            raise

    def get_stats(self) -> Dict[str, Any]:
        """获取索引统计信息"""
        return {
            'vector_index_size': self.vector_index.ntotal,
            'text_index_size': len(self.document_mapping),
            'index_directory': self.index_dir
        }

    def delete_document(self, doc_id: str):
        """从索引中删除文档（暂时不支持，需要重建索引）"""
        logger.warning("文档删除功能暂时不支持，需要重建索引")
        # TODO: 实现文档删除功能
        pass

    def rebuild_index(self):
        """重建索引"""
        try:
            # 保存当前索引状态
            backup_dir = self.index_dir + "_backup"
            if os.path.exists(self.index_dir):
                import shutil
                shutil.move(self.index_dir, backup_dir)

            # 重新初始化
            self._initialize_indices()

            logger.info("索引重建完成")

        except Exception as e:
            logger.error(f"索引重建失败: {str(e)}")
            raise