"""
简化的文件索引系统测试脚本

测试基本功能，不依赖复杂的索引库
"""

import os
import sys
import tempfile
from pathlib import Path
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 尝试导入，如果失败则跳过相关测试
try:
    from app.core.config import get_settings
    CONFIG_AVAILABLE = True
except ImportError as e:
    logger.warning(f"无法导入配置模块: {e}")
    CONFIG_AVAILABLE = False

from app.services.file_scanner import FileScanner
from app.services.metadata_extractor import MetadataExtractor
from app.services.content_parser import ContentParser

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


def main():
    """主测试函数"""
    logger.info("开始简化文件索引系统测试")

    # 创建临时测试目录
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir)
        logger.info(f"创建临时测试目录: {test_dir}")

        try:
            # 创建测试文件
            test_files = create_test_files(test_dir)

            # 初始化服务
            logger.info("初始化服务...")
            scanner = FileScanner(max_workers=2)
            extractor = MetadataExtractor()
            parser = ContentParser(max_content_length=100*1024)

            # 运行各项测试
            test_results = []

            # 1. 测试文件扫描
            test_results.append(("文件扫描", test_file_scanner(scanner, test_dir)))

            # 2. 测试元数据提取
            test_results.append(("元数据提取", test_metadata_extractor(extractor, test_files)))

            # 3. 测试内容解析
            test_results.append(("内容解析", test_content_parser(parser, test_files)))

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
                logger.info("🎉 所有基础测试通过！文件索引系统核心功能正常。")
                logger.info("📝 注意：由于依赖问题，完整的索引功能（Faiss/Whoosh）需要在生产环境中测试。")
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