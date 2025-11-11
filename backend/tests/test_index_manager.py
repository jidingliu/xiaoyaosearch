"""
索引管理器测试
"""

import pytest
import numpy as np
import tempfile
import shutil
from pathlib import Path

from app.core.index_manager import IndexManager


class TestIndexManager:
    """索引管理器测试类"""

    @pytest.fixture
    def temp_index_dir(self):
        """临时索引目录"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def index_manager(self, temp_index_dir):
        """索引管理器实例"""
        return IndexManager(temp_index_dir)

    def test_initialization(self, index_manager):
        """测试索引初始化"""
        assert index_manager.vector_index is not None
        assert index_manager.text_index is not None
        assert index_manager.document_mapping is not None

    def test_add_document(self, index_manager):
        """测试添加文档"""
        doc_id = "test_doc_1"
        content = "这是一个测试文档的内容"
        vector = np.random.random(768).astype(np.float32)
        metadata = {
            "title": "测试文档",
            "file_path": "/test/path/file.txt",
            "file_type": "txt"
        }

        # 添加文档
        index_manager.add_document(doc_id, content, vector, metadata)

        # 验证索引大小
        assert index_manager.vector_index.ntotal == 1
        assert len(index_manager.document_mapping) == 1

    def test_vector_search(self, index_manager):
        """测试向量搜索"""
        # 添加测试文档
        content = "机器学习是人工智能的一个重要分支"
        vector = np.random.random(768).astype(np.float32)
        metadata = {
            "title": "AI文档",
            "file_path": "/test/ai_doc.txt",
            "file_type": "txt"
        }
        index_manager.add_document("ai_doc", content, vector, metadata)

        # 执行搜索
        query_vector = np.random.random(768).astype(np.float32)
        results = index_manager.search_vector(query_vector, top_k=5)

        assert isinstance(results, list)
        if results:
            assert 'doc_id' in results[0]
            assert 'score' in results[0]
            assert 'vector_rank' in results[0]

    def test_text_search(self, index_manager):
        """测试全文搜索"""
        # 添加测试文档
        content = "这是一个关于深度学习的文档"
        vector = np.random.random(768).astype(np.float32)
        metadata = {
            "title": "深度学习文档",
            "file_path": "/test/deep_learning.txt",
            "file_type": "txt"
        }
        index_manager.add_document("dl_doc", content, vector, metadata)

        # 执行搜索
        results = index_manager.search_text("学习", top_k=5)

        assert isinstance(results, list)
        if results:
            assert 'doc_id' in results[0]
            assert 'score' in results[0]
            assert 'text_rank' in results[0]

    def test_hybrid_search(self, index_manager):
        """测试混合搜索"""
        # 添加测试文档
        docs = [
            ("人工智能的发展", "AI文档", "/test/ai.txt"),
            ("机器学习算法", "ML文档", "/test/ml.txt"),
            ("深度学习网络", "DL文档", "/test/dl.txt")
        ]

        for i, (content, title, path) in enumerate(docs):
            vector = np.random.random(768).astype(np.float32)
            metadata = {
                "title": title,
                "file_path": path,
                "file_type": "txt"
            }
            index_manager.add_document(f"doc_{i}", content, vector, metadata)

        # 执行混合搜索
        query_vector = np.random.random(768).astype(np.float32)
        results = index_manager.search_hybrid("学习", query_vector, top_k=5)

        assert isinstance(results, list)
        if results:
            assert 'doc_id' in results[0]
            assert 'score' in results[0]
            assert 'vector_score' in results[0]
            assert 'text_score' in results[0]

    def test_save_and_load_indices(self, index_manager, temp_index_dir):
        """测试索引保存和加载"""
        # 添加测试数据
        vector = np.random.random(768).astype(np.float32)
        index_manager.add_document("save_test", "测试保存", vector, {"title": "保存测试"})

        # 保存索引
        index_manager.save_indices()

        # 创建新的索引管理器并加载
        new_index_manager = IndexManager(temp_index_dir)

        # 验证数据已加载
        assert new_index_manager.vector_index.ntotal == 1
        assert len(new_index_manager.document_mapping) == 1

    def test_get_stats(self, index_manager):
        """测试获取统计信息"""
        stats = index_manager.get_stats()

        assert isinstance(stats, dict)
        assert 'vector_index_size' in stats
        assert 'text_index_size' in stats
        assert 'index_directory' in stats


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])