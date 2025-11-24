"""
文件索引系统测试脚本

测试文件索引系统的各项功能，包括：
- 文件扫描
- 元数据提取
- 内容解析
- 索引构建
- 完整的索引流程
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import get_settings
from app.services.file_index_service import FileIndexService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_test_files(test_dir: Path) -> list[Path]:
    """创建测试文件"""
    test_files = []

    # 创建文本文档
    txt_file = test_dir / "test_document.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("这是一个测试文档。\n")
        f.write("包含中文内容用于测试文件索引系统。\n")
        f.write("This is English content for testing purposes.\n")
        f.write("文件索引系统应该能够正确解析和索引这些内容。")
    test_files.append(txt_file)

    # 创建Markdown文档
    md_file = test_dir / "test_markdown.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# 测试Markdown文档\n\n")
        f.write("这是一个**Markdown**测试文档。\n\n")
        f.write("## 功能特点\n")
        f.write("- 支持中文\n")
        f.write("- 支持英文\n")
        f.write("- 支持代码高亮\n\n")
        f.write("```python\n")
        f.write("def hello_world():\n")
        f.write("    print('Hello, World!')\n")
        f.write("```\n")
    test_files.append(md_file)

    # 创建Python代码文件
    py_file = test_dir / "test_script.py"
    with open(py_file, 'w', encoding='utf-8') as f:
        f.write("#!/usr/bin/env python3\n")
        f.write('"""\n')
        f.write("测试Python脚本\n")
        f.write("演示文件索引系统的代码解析功能\n")
        f.write('"""\n\n')
        f.write("def calculate_sum(a: int, b: int) -> int:\n")
        f.write("    \"\"\"\n")
        f.write("    计算两个数的和\n")
        f.write("    \n")
        f.write("    Args:\n")
        f.write("        a: 第一个数\n")
        f.write("        b: 第二个数\n")
        f.write("    \n")
        f.write("    Returns:\n")
        f.write("        int: 两数之和\n")
        f.write("    \"\"\"\n")
        f.write("    return a + b\n\n")
        f.write("if __name__ == \"__main__\":\n")
        f.write("    result = calculate_sum(10, 20)\n")
        f.write("    print(f\"计算结果: {result}\")\n")
    test_files.append(py_file)

    # 创建HTML文件
    html_file = test_dir / "test_webpage.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html lang=\"zh-CN\">\n")
        f.write("<head>\n")
        f.write("    <meta charset=\"UTF-8\">\n")
        f.write("    <title>测试网页</title>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write("    <h1>文件索引系统测试</h1>\n")
        f.write("    <p>这是一个用于测试文件索引系统的HTML文档。</p>\n")
        f.write("    <h2>主要功能</h2>\n")
        f.write("    <ul>\n")
        f.write("        <li>文件扫描</li>\n")
        f.write("        <li>内容解析</li>\n")
        f.write("        <li>索引构建</li>\n")
        f.write("        <li>搜索支持</li>\n")
        f.write("    </ul>\n")
        f.write("</body>\n")
        f.write("</html>\n")
    test_files.append(html_file)

    # 创建CSS文件
    css_file = test_dir / "test_styles.css"
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write("/* 测试CSS样式文件 */\n")
        f.write("body {\n")
        f.write("    font-family: 'Microsoft YaHei', Arial, sans-serif;\n")
        f.write("    line-height: 1.6;\n")
        f.write("    margin: 0;\n")
        f.write("    padding: 20px;\n")
        f.write("}\n\n")
        f.write("h1 {\n")
        f.write("    color: #333;\n")
        f.write("    border-bottom: 2px solid #007acc;\n")
        f.write("}\n\n")
        f.write("/* 响应式设计 */\n")
        f.write("@media (max-width: 768px) {\n")
        f.write("    body {\n")
        f.write("        padding: 10px;\n")
        f.write("    }\n")
        f.write("}\n")
    test_files.append(css_file)

    logger.info(f"创建了 {len(test_files)} 个测试文件")
    return test_files


def test_file_scanner(scanner, test_dir: Path) -> bool:
    """测试文件扫描功能"""
    logger.info("开始测试文件扫描功能")

    try:
        files = scanner.scan_directory(str(test_dir), recursive=True)

        if not files:
            logger.error("文件扫描失败：未找到任何文件")
            return False

        logger.info(f"文件扫描成功，找到 {len(files)} 个文件:")
        for file_info in files:
            logger.info(f"  - {file_info.name} ({file_info.extension}) - {file_info.size} 字节")

        # 检查扫描统计
        stats = scanner.get_stats()
        logger.info(f"扫描统计: {stats}")

        return True

    except Exception as e:
        logger.error(f"文件扫描测试失败: {e}")
        return False


def test_metadata_extractor(extractor, test_files: list[Path]) -> bool:
    """测试元数据提取功能"""
    logger.info("开始测试元数据提取功能")

    try:
        for test_file in test_files:
            logger.info(f"测试文件: {test_file.name}")

            metadata = extractor.extract_metadata(str(test_file))

            if 'error' in metadata:
                logger.error(f"元数据提取失败 {test_file.name}: {metadata['error']}")
                return False

            # 检查基本元数据
            required_fields = ['file_name', 'file_extension', 'file_size', 'mime_type']
            for field in required_fields:
                if field not in metadata:
                    logger.error(f"缺少必需的元数据字段: {field}")
                    return False

            logger.info(f"  文件名: {metadata.get('file_name')}")
            logger.info(f"  文件类型: {metadata.get('file_type')}")
            logger.info(f"  MIME类型: {metadata.get('mime_type')}")
            logger.info(f"  文件大小: {metadata.get('file_size')} 字节")
            logger.info(f"  内容哈希: {metadata.get('content_hash', 'N/A')}")

        logger.info("元数据提取测试通过")
        return True

    except Exception as e:
        logger.error(f"元数据提取测试失败: {e}")
        return False


def test_content_parser(parser, test_files: list[Path]) -> bool:
    """测试内容解析功能"""
    logger.info("开始测试内容解析功能")

    try:
        for test_file in test_files:
            logger.info(f"测试文件: {test_file.name}")

            parsed_content = parser.parse_content(str(test_file))

            if hasattr(parsed_content, 'error') and parsed_content.error:
                logger.error(f"内容解析失败 {test_file.name}: {parsed_content.error}")
                return False

            logger.info(f"  标题: {parsed_content.title or 'N/A'}")
            logger.info(f"  语言: {parsed_content.language or 'N/A'}")
            logger.info(f"  编码: {parsed_content.encoding or 'N/A'}")
            logger.info(f"  置信度: {parsed_content.confidence:.2f}")
            logger.info(f"  内容长度: {len(parsed_content.text)} 字符")
            logger.info(f"  内容预览: {parsed_content.text[:100]}...")

        logger.info("内容解析测试通过")
        return True

    except Exception as e:
        logger.error(f"内容解析测试失败: {e}")
        return False


def test_index_builder(builder, test_files: list[Path]) -> bool:
    """测试索引构建功能"""
    logger.info("开始测试索引构建功能")

    try:
        # 准备测试文档数据
        documents = []
        for i, test_file in enumerate(test_files):
            doc = {
                'id': f'test_doc_{i}',
                'title': test_file.stem,
                'content': test_file.read_text(encoding='utf-8'),
                'file_path': str(test_file),
                'file_name': test_file.name,
                'file_type': test_file.suffix[1:] if test_file.suffix else 'unknown',
                'file_size': test_file.stat().st_size,
                'modified_time': test_file.stat().st_mtime,
                'language': 'zh' if test_file.suffix in ['.txt', '.md'] else 'en',
                'tags': [test_file.suffix[1:]]
            }
            documents.append(doc)

        # 构建索引
        success = builder.build_indexes(documents)

        if not success:
            logger.error("索引构建失败")
            return False

        # 获取索引统计
        stats = builder.get_index_stats()
        logger.info(f"索引统计: {stats}")

        # 检查索引文件是否存在
        if not builder.index_exists():
            logger.error("索引文件不存在")
            return False

        logger.info("索引构建测试通过")
        return True

    except Exception as e:
        logger.error(f"索引构建测试失败: {e}")
        return False


def test_full_index_service(index_service, test_dir: Path) -> bool:
    """测试完整的文件索引服务"""
    logger.info("开始测试完整文件索引服务")

    try:
        # 测试完整索引构建
        logger.info("测试完整索引构建...")
        result = index_service.build_full_index(
            scan_paths=[str(test_dir)],
            progress_callback=lambda msg, progress: logger.info(f"进度: {msg} - {progress:.1f}%")
        )

        if not result['success']:
            logger.error(f"完整索引构建失败: {result.get('error', '未知错误')}")
            return False

        logger.info(f"完整索引构建成功:")
        logger.info(f"  发现文件: {result.get('total_files_found', 0)}")
        logger.info(f"  索引文档: {result.get('documents_indexed', 0)}")
        logger.info(f"  失败文件: {result.get('failed_files', 0)}")
        logger.info(f"  耗时: {result.get('duration_seconds', 0):.2f} 秒")

        # 测试索引状态
        logger.info("测试索引状态查询...")
        status = index_service.get_index_status()
        logger.info(f"索引状态: {status}")

        # 测试支持的格式
        logger.info("测试支持的格式...")
        formats = index_service.get_supported_formats()
        logger.info(f"支持的格式数量: 扫描器 {len(formats.get('scanner_formats', []))}, "
                   f"解析器 {len(formats.get('parser_formats', []))}")

        logger.info("完整文件索引服务测试通过")
        return True

    except Exception as e:
        logger.error(f"完整文件索引服务测试失败: {e}")
        return False


def main():
    """主测试函数"""
    logger.info("开始文件索引系统测试")

    # 创建临时测试目录
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir)
        logger.info(f"创建临时测试目录: {test_dir}")

        try:
            # 创建测试文件
            test_files = create_test_files(test_dir)

            # 获取设置
            settings = get_settings()

            # 创建测试数据目录
            test_data_root = test_dir / "index_data"
            test_data_root.mkdir(exist_ok=True)

            # 获取索引路径
            faiss_path = str(test_data_root / "indexes" / "faiss" / "test_index.faiss")
            whoosh_path = str(test_data_root / "indexes" / "whoosh")

            # 初始化文件索引服务
            logger.info("初始化文件索引服务...")
            index_service = FileIndexService(
                data_root=str(test_data_root),
                faiss_index_path=faiss_path,
                whoosh_index_path=whoosh_path,
                use_chinese_analyzer=True,
                scanner_config={
                    'max_workers': 2,
                    'max_file_size': 10 * 1024 * 1024,  # 10MB
                    'supported_extensions': {'.txt', '.md', '.py', '.html', '.css', '.js'}
                },
                parser_config={
                    'max_content_length': 100 * 1024  # 100KB
                }
            )

            # 获取子服务进行单独测试
            scanner = index_service.scanner
            extractor = index_service.metadata_extractor
            parser = index_service.content_parser
            builder = index_service.index_builder

            # 运行各项测试
            test_results = []

            # 1. 测试文件扫描
            test_results.append(("文件扫描", test_file_scanner(scanner, test_dir)))

            # 2. 测试元数据提取
            test_results.append(("元数据提取", test_metadata_extractor(extractor, test_files)))

            # 3. 测试内容解析
            test_results.append(("内容解析", test_content_parser(parser, test_files)))

            # 4. 测试索引构建
            test_results.append(("索引构建", test_index_builder(builder, test_files)))

            # 5. 测试完整服务
            test_results.append(("完整索引服务", test_full_index_service(index_service, test_dir)))

            # 输出测试结果
            logger.info("\n" + "="*50)
            logger.info("测试结果汇总:")
            logger.info("="*50)

            all_passed = True
            for test_name, result in test_results:
                status = "✅ 通过" if result else "❌ 失败"
                logger.info(f"{test_name:20} {status}")
                if not result:
                    all_passed = False

            logger.info("="*50)

            if all_passed:
                logger.info("🎉 所有测试通过！文件索引系统工作正常。")
                return True
            else:
                logger.error("❌ 部分测试失败，请检查相关功能。")
                return False

        except Exception as e:
            logger.error(f"测试过程中发生异常: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)