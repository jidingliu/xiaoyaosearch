#!/usr/bin/env python3
"""
分块功能测试脚本

测试前端透明分块方案的各个组件。
验证分块服务、搜索服务、索引服务是否正常工作。
"""

import os
import sys
import asyncio
import logging
from typing import List, Dict, Any

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_chunk_service():
    """测试分块服务"""
    logger.info("=== 测试分块服务 ===")
    try:
        from app.services.chunk_service import get_chunk_service

        chunk_service = get_chunk_service()

        # 测试短内容（不分块）
        short_content = "这是一个短内容，不需要分块处理。"
        short_chunks = chunk_service.intelligent_chunking(short_content)
        logger.info(f"短内容分块结果: {len(short_chunks)} 个分块")
        assert len(short_chunks) == 1, "短内容应该返回1个分块"

        # 测试长内容（需要分块）
        long_content = """
        第一段内容。这是第一段的内容，包含一些文字描述。这段内容比较长，足够用来测试分块算法的有效性。我们需要确保分块能够在合适的边界处进行分割，比如段落边界或者句子边界。通过智能分块，我们可以将长文档分割成多个大小适中的片段，每个片段都包含完整的语义内容，这样可以提高搜索的准确性和相关性。分块算法应该能够识别段落之间的分隔符，并在这些地方进行分割。

        第二段内容。这是第二段的内容，继续测试分块功能。分块算法应该能够识别段落之间的分隔符，并在这些地方进行分割。这样可以保证每个分块的内容是完整的语义单元，提高搜索的准确性。我们需要确保分块策略能够正确处理不同类型的内容，包括技术文档、文章、报告等。通过合适的分块大小和重叠设置，我们可以平衡搜索精度和性能。

        第三段内容。这是第三段的内容，用来测试分块的数量和大小控制。通过合适的分块策略，我们可以将长文档分割成多个大小适中的分块，每个分块都包含完整的内容和相关的上下文信息。这样可以提高搜索的精度和相关性。分块服务应该支持多种分块策略，包括固定大小分块、语义边界分块、段落分块等。同时，分块的重叠设置也很重要，可以确保在搜索时不会因为边界而丢失相关信息。

        第四段内容。这是第四段的内容，进一步测试分块功能的完整性。分块算法应该能够处理各种复杂的内容结构，包括表格、列表、代码块等。在分块时，我们需要考虑内容的逻辑结构，确保每个分块都是一个有意义的语义单元。这样可以提高搜索结果的质量，让用户更容易找到相关的信息。分块功能是前端透明分块方案的核心组件，它的性能和质量直接影响整个系统的搜索效果。
        """

        long_chunks = chunk_service.intelligent_chunking(long_content, "500+50")
        logger.info(f"长内容分块结果: {len(long_chunks)} 个分块")
        assert len(long_chunks) > 1, "长内容应该返回多个分块"

        # 验证分块质量
        validation_result = chunk_service.validate_chunks(long_chunks)
        logger.info(f"分块质量验证: {validation_result['valid']}, 质量评分: {validation_result.get('quality_score', 0):.2f}")

        # 测试内容重装
        reassembled_content = chunk_service.reassemble_content(long_chunks)
        logger.info(f"重装内容长度: {len(reassembled_content)}, 原始长度: {len(long_content)}")

        logger.info("✅ 分块服务测试通过")
        return True

    except Exception as e:
        logger.error(f"❌ 分块服务测试失败: {e}")
        return False


async def test_chunk_config():
    """测试分块配置"""
    logger.info("=== 测试分块配置 ===")
    try:
        from app.config.chunk_config import get_chunk_config_manager, get_chunk_config

        config_manager = get_chunk_config_manager()
        config = get_chunk_config()

        logger.info(f"默认配置: {config_manager.get_config_summary()}")

        # 测试配置更新
        config_manager.update_config(
            default_chunk_size=600,
            default_overlap=60,
            chunking_threshold=700
        )
        logger.info("配置更新成功")

        # 测试智能分块决策
        should_chunk = config_manager.should_chunk_content("测试内容", "document")
        logger.info(f"分块决策测试: {should_chunk}")

        # 测试策略生成
        strategy = config_manager.get_chunking_strategy_string(1500)
        logger.info(f"策略生成测试: {strategy}")

        logger.info("✅ 分块配置测试通过")
        return True

    except Exception as e:
        logger.error(f"❌ 分块配置测试失败: {e}")
        return False


async def test_transparent_adapter():
    """测试透明适配器"""
    logger.info("=== 测试透明适配器 ===")
    try:
        from app.services.transparent_adapter import get_transparent_search_adapter, get_transparent_index_adapter

        # 测试搜索适配器
        search_adapter = get_transparent_search_adapter(
            enable_chunk_search=True
        )

        logger.info("搜索适配器初始化成功")
        search_stats = search_adapter.get_search_stats()
        logger.info(f"搜索适配器状态: {search_stats['adapter_config']}")

        # 测试索引适配器
        data_root = os.getenv('DATA_ROOT', '../data')
        index_adapter = get_transparent_index_adapter(
            data_root=data_root,
            enable_chunk_indexing=True,
            chunk_strategy="500+50"
        )

        logger.info("索引适配器初始化成功")
        index_status = index_adapter.get_index_status()
        logger.info(f"索引适配器配置: {index_status['adapter_config']}")

        logger.info("✅ 透明适配器测试通过")
        return True

    except Exception as e:
        logger.error(f"❌ 透明适配器测试失败: {e}")
        return False


async def test_database_models():
    """测试数据库模型"""
    logger.info("=== 测试数据库模型 ===")
    try:
        from app.core.database import engine
        from sqlalchemy import text

        # 测试数据库连接
        with engine.connect() as conn:
            # 验证files表的新字段
            result = conn.execute(text("""
                SELECT COUNT(*) as count FROM pragma_table_info('files')
                WHERE name IN ('is_chunked', 'total_chunks', 'chunk_strategy', 'avg_chunk_size')
            """))
            row = result.fetchone()
            fields_count = row[0] if row else 0
            logger.info(f"Files表分块字段数量: {fields_count}")
            assert fields_count == 4, f"应该有4个分块字段，实际有{fields_count}个"

            # 验证file_chunks表
            result = conn.execute(text("""
                SELECT COUNT(*) as count FROM sqlite_master
                WHERE type='table' AND name='file_chunks'
            """))
            row = result.fetchone()
            chunks_table_exists = row[0] > 0 if row else False
            logger.info(f"File_chunks表存在: {chunks_table_exists}")
            assert chunks_table_exists, "file_chunks表应该存在"

        logger.info("✅ 数据库模型测试通过")
        return True

    except Exception as e:
        logger.error(f"❌ 数据库模型测试失败: {e}")
        return False


async def test_ai_models():
    """测试AI模型服务"""
    logger.info("=== 测试AI模型服务 ===")
    try:
        from app.services.ai_model_manager import ai_model_service

        # 测试文本嵌入
        test_text = "这是一个测试文本，用于验证AI模型的功能。"
        embedding = await ai_model_service.text_embedding(test_text, normalize_embeddings=True)

        logger.info(f"文本嵌入测试成功，向量维度: {len(embedding) if embedding else 0}")
        assert embedding is not None, "文本嵌入不能为None"
        assert len(embedding) > 0, "文本嵌入不能为空"

        # 测试批量嵌入
        batch_texts = [
            "第一个测试文本",
            "第二个测试文本",
            "第三个测试文本"
        ]
        batch_embeddings = await ai_model_service.batch_text_embedding(batch_texts, normalize_embeddings=True)

        logger.info(f"批量嵌入测试成功，数量: {len(batch_embeddings)}")
        assert len(batch_embeddings) == len(batch_texts), "批量嵌入数量应该匹配"

        logger.info("✅ AI模型服务测试通过")
        return True

    except Exception as e:
        logger.error(f"❌ AI模型服务测试失败: {e}")
        return False


async def run_all_tests():
    """运行所有测试"""
    logger.info("🚀 开始分块功能全面测试")

    tests = [
        ("分块服务", test_chunk_service),
        ("分块配置", test_chunk_config),
        ("透明适配器", test_transparent_adapter),
        ("数据库模型", test_database_models),
        ("AI模型服务", test_ai_models)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            logger.info(f"\n开始测试: {test_name}")
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"测试 {test_name} 时发生异常: {e}")
            results.append((test_name, False))

    # 总结测试结果
    logger.info("\n" + "="*60)
    logger.info("📊 测试结果总结")
    logger.info("="*60)

    passed_count = 0
    total_count = len(results)

    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        logger.info(f"{test_name:20} {status}")
        if result:
            passed_count += 1

    logger.info(f"\n总体结果: {passed_count}/{total_count} 测试通过")

    if passed_count == total_count:
        logger.info("🎉 所有测试通过！分块功能实施成功！")
    else:
        logger.warning(f"⚠️  有 {total_count - passed_count} 个测试失败，需要检查相关功能")

    return passed_count == total_count


def main():
    """主函数"""
    try:
        # 创建事件循环运行异步测试
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        logger.info("测试被用户中断")
        sys.exit(1)
    except Exception as e:
        logger.error(f"测试过程中发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()