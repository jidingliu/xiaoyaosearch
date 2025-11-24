"""
MVP配置文件
根据PRD P0要求配置小遥搜索MVP阶段支持的文件格式
"""

import os
from typing import Set, Dict, Any

# MVP环境变量控制
MVP_MODE = os.getenv('MVP_MODE', 'true').lower() == 'true'

# MVP阶段支持的文件扩展名（PRD P0要求）
MVP_SUPPORTED_EXTENSIONS: Set[str] = {
    # 视频类 - P0要求
    '.mp4', '.avi',

    # 音频类 - P0要求
    '.mp3', '.wav',

    # 文档类 - P0要求
    # Office文档 (MVP支持现代格式)
    '.pdf', '.docx', '.xlsx', '.pptx',  # 现代Office格式
    # 注意：.doc, .xls, .ppt为老格式，MVP阶段暂不支持，可后续扩展
    # 文本文档
    '.txt', '.md',
}

# 文件类型分类
MVP_FILE_TYPES: Dict[str, str] = {
    '.mp4': 'video',
    '.avi': 'video',
    '.mp3': 'audio',
    '.wav': 'audio',
    '.pdf': 'document',
    '.docx': 'document',
    '.xlsx': 'document',
    '.pptx': 'document',
    '.txt': 'document',
    '.md': 'document',
}

# 内容提取策略配置
MVP_CONTENT_EXTRACTION_CONFIG: Dict[str, Dict[str, Any]] = {
    'document': {
        'extract_content': True,  # 文档类提取完整文本内容
        'priority': 1,
        'max_content_length': 1024 * 1024,  # 1MB
    },
    'audio': {
        'extract_content': False,  # 音频类暂不提取内容（未来功能）
        'extract_metadata': True,  # 只提取元数据
        'priority': 2,
        'metadata_fields': ['duration', 'bitrate', 'sample_rate', 'title', 'artist', 'album'],
    },
    'video': {
        'extract_content': False,  # 视频类暂不提取内容（未来功能）
        'extract_metadata': True,  # 只提取元数据
        'priority': 2,
        'metadata_fields': ['duration', 'resolution', 'fps', 'codec', 'title'],
    },
}

# 内容解析器方法映射
MVP_CONTENT_PARSER_METHODS: Dict[str, str] = {
    # Office文档解析 (现代格式)
    '.pdf': '_parse_pdf',
    '.docx': '_parse_docx',
    '.xlsx': '_parse_excel',
    '.pptx': '_parse_pptx',

    # 文本文档解析
    '.txt': '_parse_text',
    '.md': '_parse_markdown',

    # 音视频元数据解析
    '.mp3': '_parse_audio_metadata',
    '.wav': '_parse_audio_metadata',
    '.mp4': '_parse_video_metadata',
    '.avi': '_parse_video_metadata',
}

# MVP功能开关
MVP_FEATURES = {
    'ENABLE_AUDIO_TRANSCRIPTION': False,  # 音频转文字暂不实现
    'ENABLE_VIDEO_TRANSCRIPTION': False,  # 视频转文字暂不实现
    'ENABLE_IMAGE_OCR': False,            # 图片OCR暂不实现
    'ENABLE_CODE_INDEXING': False,        # 代码索引暂不实现
    'ENABLE_ARCHIVE_INDEXING': False,     # 压缩包索引暂不实现
}

# 格式友好显示名称
MVP_FORMAT_DISPLAY_NAMES: Dict[str, str] = {
    '.mp4': 'MP4视频',
    '.avi': 'AVI视频',
    '.mp3': 'MP3音频',
    '.wav': 'WAV音频',
    '.pdf': 'PDF文档',
    '.docx': 'Word文档',
    '.xlsx': 'Excel表格',
    '.pptx': 'PowerPoint演示文稿',
    '.txt': '文本文件',
    '.md': 'Markdown文档',
}

# 统计信息
MVP_FORMAT_STATS = {
    'total_formats': len(MVP_SUPPORTED_EXTENSIONS),
    'video_formats': 2,
    'audio_formats': 2,
    'document_formats': 6,  # 现代Office格式
    'content_extraction_formats': 6,  # 只统计提取文本内容的格式
}

def get_mvp_supported_extensions() -> Set[str]:
    """获取MVP支持的文件扩展名"""
    return MVP_SUPPORTED_EXTENSIONS if MVP_MODE else set()

def get_file_type(extension: str) -> str:
    """根据扩展名获取文件类型"""
    return MVP_FILE_TYPES.get(extension.lower(), 'unknown')

def get_content_config(file_type: str) -> Dict[str, Any]:
    """根据文件类型获取内容提取配置"""
    return MVP_CONTENT_EXTRACTION_CONFIG.get(file_type, {})

def get_parser_method(extension: str) -> str:
    """根据扩展名获取解析器方法名"""
    return MVP_CONTENT_PARSER_METHODS.get(extension.lower(), '')

def is_mvp_mode() -> bool:
    """检查是否处于MVP模式"""
    return MVP_MODE

def get_format_display_name(extension: str) -> str:
    """获取格式友好显示名称"""
    return MVP_FORMAT_DISPLAY_NAMES.get(extension.lower(), extension.upper())