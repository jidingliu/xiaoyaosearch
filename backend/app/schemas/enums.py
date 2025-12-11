"""
API枚举类型定义
定义请求和响应中使用的枚举类型
"""
from enum import Enum


class InputType(str, Enum):
    """输入类型枚举"""
    TEXT = "text"
    VOICE = "voice"
    IMAGE = "image"


class SearchType(str, Enum):
    """搜索类型枚举"""
    SEMANTIC = "semantic"  # 语义搜索
    FULLTEXT = "fulltext"  # 全文搜索
    HYBRID = "hybrid"      # 混合搜索


class FileType(str, Enum):
    """文件类型枚举"""
    VIDEO = "video"      # 对应文件扩展名（mp4、avi）
    AUDIO = "audio"      # 对应文件扩展名（mp3、wav）
    DOCUMENT = "document"  # 对应文件扩展名（txt、md、doc/docx、xls/xlsx、ppt/pptx、pdf）
    IMAGE = "image"      # 对应文件扩展名（png、jpg、jpeg）


class JobType(str, Enum):
    """索引任务类型枚举"""
    CREATE = "create"
    UPDATE = "update"
    REBUILD = "rebuild"
    DELETE = "delete"


class JobStatus(str, Enum):
    """索引任务状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ModelType(str, Enum):
    """AI模型类型枚举"""
    EMBEDDING = "embedding"
    SPEECH = "speech"
    VISION = "vision"
    LLM = "llm"


class ProviderType(str, Enum):
    """AI模型提供商类型枚举"""
    LOCAL = "local"
    CLOUD = "cloud"