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

    # 图片类 - P0要求
    '.png', '.jpg', '.jpeg',

    # 文档类 - P0要求
    # Office文档 (支持现代格式和经典格式)
    '.pdf', '.docx', '.xlsx', '.pptx',  # 现代Office格式
    '.doc', '.xls', '.ppt',  # 经典Office格式
    # 文本文档
    '.txt', '.md',
}

# 文件类型分类
MVP_FILE_TYPES: Dict[str, str] = {
    '.mp4': 'video',
    '.avi': 'video',
    '.mp3': 'audio',
    '.wav': 'audio',
    '.png': 'image',
    '.jpg': 'image',
    '.jpeg': 'image',
    '.pdf': 'document',
    '.docx': 'document',
    '.xlsx': 'document',
    '.pptx': 'document',
    '.doc': 'document',
    '.xls': 'document',
    '.ppt': 'document',
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
        'extract_content': True,  # 音频类启用语音转文字功能
        'extract_metadata': True,  # 同时提取元数据
        'priority': 2,
        'max_duration': 15 * 60,  # 15分钟时长限制（秒），超过时长将截取前15分钟内容
        'whisper_model': 'base',  # 使用的Whisper模型
        'language': 'zh',  # 语音识别语言
        'metadata_fields': ['duration', 'bitrate', 'sample_rate', 'title', 'artist', 'album'],
    },
    'video': {
        'extract_content': True,  # 视频类启用音频轨道提取+语音转文字
        'extract_metadata': True,  # 同时提取元数据
        'priority': 2,
        'max_duration': 15 * 60,  # 15分钟时长限制（秒），超过时长将截取前15分钟内容
        'whisper_model': 'base',  # 使用的Whisper模型
        'language': 'zh',  # 语音识别语言
        'ffmpeg_audio_codec': 'pcm_s16le',  # 音频编码格式
        'ffmpeg_sample_rate': 16000,  # 采样率
        'ffmpeg_channels': 1,  # 单声道
        'metadata_fields': ['duration', 'resolution', 'fps', 'codec', 'title'],
    },
    'image': {
        'extract_content': True,  # 图片类启用CLIP图像理解功能
        'extract_metadata': True,  # 同时提取元数据
        'priority': 2,
        'clip_model': 'chinese-clip-vit-base-patch16',  # 使用的CLIP模型
        'max_image_size': 512,  # 最大图像尺寸
        'metadata_fields': ['width', 'height', 'format', 'mode'],
    },
}

# 内容解析器方法映射
MVP_CONTENT_PARSER_METHODS: Dict[str, str] = {
    # Office文档解析 (现代格式 + 经典格式)
    '.pdf': '_parse_pdf',
    '.docx': '_parse_docx',
    '.xlsx': '_parse_excel',
    '.pptx': '_parse_pptx',
    '.doc': '_parse_doc',  # 经典Word格式
    '.xls': '_parse_excel',  # 经典Excel格式
    '.ppt': '_parse_ppt',   # 经典PowerPoint格式

    # 文本文档解析
    '.txt': '_parse_text',
    '.md': '_parse_markdown',

    # 音视频元数据解析
    '.mp3': '_parse_audio_metadata',
    '.wav': '_parse_audio_metadata',
    '.mp4': '_parse_video_metadata',
    '.avi': '_parse_video_metadata',
    '.png': '_parse_image_content',
    '.jpg': '_parse_image_content',
    '.jpeg': '_parse_image_content',
}

# MVP功能开关
MVP_FEATURES = {
    'ENABLE_AUDIO_TRANSCRIPTION': True,   # 音频转文字功能已启用
    'ENABLE_VIDEO_TRANSCRIPTION': True,   # 视频转文字功能已启用
    'ENABLE_IMAGE_UNDERSTANDING': True,   # 图片理解功能已启用
    'ENABLE_CODE_INDEXING': False,        # 代码索引暂不实现
    'ENABLE_ARCHIVE_INDEXING': False,     # 压缩包索引暂不实现
}

# 格式友好显示名称
MVP_FORMAT_DISPLAY_NAMES: Dict[str, str] = {
    '.mp4': 'MP4视频',
    '.avi': 'AVI视频',
    '.mp3': 'MP3音频',
    '.wav': 'WAV音频',
    '.png': 'PNG图片',
    '.jpg': 'JPEG图片',
    '.jpeg': 'JPEG图片',
    '.pdf': 'PDF文档',
    '.docx': 'Word文档',
    '.xlsx': 'Excel表格',
    '.pptx': 'PowerPoint演示文稿',
    '.doc': 'Word文档(经典)',
    '.xls': 'Excel表格(经典)',
    '.ppt': 'PowerPoint演示文稿(经典)',
    '.txt': '文本文件',
    '.md': 'Markdown文档',
}

# 统计信息
MVP_FORMAT_STATS = {
    'total_formats': len(MVP_SUPPORTED_EXTENSIONS),
    'video_formats': 2,
    'audio_formats': 2,
    'image_formats': 3,  # PNG, JPG, JPEG
    'document_formats': 9,  # 现代Office格式(6) + 经典Office格式(3)
    'content_extraction_formats': 16,  # 所有格式都支持内容提取（包括音视频转录+图片理解）
    'transcription_enabled_formats': 4,  # 支持语音转录的格式（音频+视频）
    'understanding_enabled_formats': 10,  # 支持内容理解的格式（文档+图片）
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