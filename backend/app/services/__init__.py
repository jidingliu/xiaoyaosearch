"""
服务层模块

提供各种业务服务，包括文件扫描、元数据提取、内容解析、索引构建、分块功能等核心功能。
"""

from .file_scanner import FileScanner
from .metadata_extractor import MetadataExtractor
from .content_parser import ContentParser
from .index_builder import IndexBuilder
from .file_index_service import FileIndexService

# 分块功能服务
from .chunk_service import ChunkService, get_chunk_service
from .chunk_search_service import ChunkSearchService, get_chunk_search_service
from .chunk_index_service import ChunkIndexService, get_chunk_index_service

__all__ = [
    # 传统服务
    "FileScanner",
    "MetadataExtractor",
    "ContentParser",
    "IndexBuilder",
    "FileIndexService",

    # 分块功能服务
    "ChunkService",
    "get_chunk_service",
    "ChunkSearchService",
    "get_chunk_search_service",
    "ChunkIndexService",
    "get_chunk_index_service"
]