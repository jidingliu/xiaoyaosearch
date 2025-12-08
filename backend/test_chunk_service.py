#!/usr/bin/env python3
"""
简单测试分块索引服务的修改
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 不加载AI模型管理器，只测试基础功能
def test_chunk_service():
    print("测试分块索引服务...")

    # 测试实例化
    try:
        from app.services.chunk_index_service import ChunkIndexService

        service = ChunkIndexService(
            chunk_faiss_index_path="test_chunks.faiss",
            chunk_whoosh_index_path="test_whoosh",
            use_ai_models=False  # 关闭AI模型避免依赖问题
        )

        print("✅ 分块索引服务实例化成功")
        print(f"   - 分块Faiss路径: {service.chunk_faiss_index_path}")
        print(f"   - 分块Whoosh路径: {service.chunk_whoosh_index_path}")
        print(f"   - 分块策略: {service.chunk_strategy}")
        print(f"   - 索引统计: {service.index_stats}")

        return True

    except Exception as e:
        print(f"❌ 分块索引服务实例化失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_should_chunk():
    print("\n测试分块判断逻辑...")

    try:
        from app.services.chunk_index_service import ChunkIndexService

        service = ChunkIndexService(
            chunk_faiss_index_path="test_chunks.faiss",
            chunk_whoosh_index_path="test_whoosh",
            use_ai_models=False
        )

        # 测试分块判断
        short_content = "这是一个短内容，不需要分块"
        long_content = "这是一个非常长的内容，" * 100  # 重复100次，足够长

        should_chunk_short = service._should_chunk_document(short_content, "txt")
        should_chunk_long = service._should_chunk_document(long_content, "txt")

        print(f"✅ 短内容分块判断: {should_chunk_short} (应该是False)")
        print(f"✅ 长内容分块判断: {should_chunk_long} (应该是True)")

        # 测试逻辑应该是正确的
        assert should_chunk_short == False, "短内容不应该分块"
        assert should_chunk_long == True, "长内容应该分块"

        return True

    except Exception as e:
        print(f"❌ 分块判断测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_index_stats():
    print("\n测试索引统计功能...")

    try:
        from app.services.chunk_index_service import ChunkIndexService

        service = ChunkIndexService(
            chunk_faiss_index_path="test_chunks.faiss",
            chunk_whoosh_index_path="test_whoosh",
            use_ai_models=False
        )

        # 测试统计更新
        initial_stats = service.index_stats.copy()
        service._update_index_stats(5)  # 处理了5个文档

        updated_stats = service.index_stats

        print(f"✅ 初始统计: {initial_stats}")
        print(f"✅ 更新后统计: {updated_stats}")

        # 验证更新逻辑
        assert updated_stats['total_documents_processed'] == 5
        assert updated_stats['chunked_documents'] == 5
        assert updated_stats['total_chunks_created'] == 15  # 5 * 3
        assert updated_stats['avg_chunks_per_document'] == 3.0

        return True

    except Exception as e:
        print(f"❌ 索引统计测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("分块索引服务修改验证")
    print("=" * 60)

    success_count = 0
    total_tests = 3

    # 运行测试
    if test_chunk_service():
        success_count += 1

    if test_should_chunk():
        success_count += 1

    if test_index_stats():
        success_count += 1

    # 输出结果
    print("\n" + "=" * 60)
    print(f"测试完成: {success_count}/{total_tests} 通过")

    if success_count == total_tests:
        print("✅ 所有测试通过！分块索引服务修改成功。")
        sys.exit(0)
    else:
        print("❌ 部分测试失败，需要检查修改。")
        sys.exit(1)