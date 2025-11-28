"""
分块配置参数

管理前端透明分块方案的所有配置参数。
支持动态配置和环境变量覆盖。
"""

import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import json
from pathlib import Path

from app.core.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class ChunkingConfig:
    """分块配置数据类"""
    # 基础分块参数
    enabled: bool = True                    # 是否启用分块功能
    default_chunk_size: int = 500          # 默认分块大小（字符数）
    default_overlap: int = 50              # 默认重叠大小（字符数）
    chunk_strategy: str = "500+50"         # 分块策略字符串

    # 分块边界参数
    min_chunk_size: int = 200              # 最小分块大小
    max_chunk_size: int = 2000             # 最大分块大小
    min_overlap: int = 0                   # 最小重叠大小
    max_overlap: int = 200                 # 最大重叠大小

    # 分块决策参数
    chunking_threshold: int = 600          # 触发分块的内容长度阈值
    auto_chunk_types: List[str] = None     # 自动分块的文件类型列表

    # 性能优化参数
    embedding_batch_size: int = 32         # 向量嵌入批处理大小
    index_update_batch_size: int = 100     # 索引更新批处理大小
    max_concurrent_chunks: int = 10        # 最大并发分块处理数

    # 搜索优化参数
    chunk_search_multiplier: float = 3.0   # 分块搜索结果倍数
    min_chunk_relevance: float = 0.3       # 最小分块相关性阈值

    # 质量控制参数
    quality_check_enabled: bool = True     # 是否启用分块质量检查
    max_chunks_per_document: int = 100     # 每个文档最大分块数
    paragraph_boundary_priority: bool = True  # 优先使用段落边界

    def __post_init__(self):
        """初始化后处理"""
        if self.auto_chunk_types is None:
            self.auto_chunk_types = ['document', 'text', 'pdf', 'markdown']

        # 验证参数范围
        self._validate_parameters()

    def _validate_parameters(self):
        """验证参数范围"""
        self.default_chunk_size = max(self.min_chunk_size, min(self.default_chunk_size, self.max_chunk_size))
        self.default_overlap = max(self.min_overlap, min(self.default_overlap, self.max_overlap))
        self.embedding_batch_size = max(1, min(self.embedding_batch_size, 128))
        self.chunk_search_multiplier = max(1.0, min(self.chunk_search_multiplier, 10.0))

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChunkingConfig':
        """从字典创建配置"""
        return cls(**data)


class ChunkConfigManager:
    """分块配置管理器

    功能：
    - 配置参数的加载和保存
    - 环境变量覆盖
    - 配置验证
    - 动态配置更新
    """

    def __init__(self, config_file: Optional[str] = None):
        """初始化配置管理器

        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file or self._get_default_config_path()
        self.config = ChunkingConfig()
        self._load_config()

    def _get_default_config_path(self) -> str:
        """获取默认配置文件路径"""
        data_root = os.getenv('DATA_ROOT', '../data')
        config_dir = os.path.join(data_root, 'configs')
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, 'chunk_config.json')

    def _load_config(self):
        """加载配置"""
        try:
            # 1. 首先加载默认配置
            self.config = ChunkingConfig()

            # 2. 从配置文件加载
            if os.path.exists(self.config_file):
                self._load_from_file()
                logger.info(f"从配置文件加载分块配置: {self.config_file}")
            else:
                logger.info("配置文件不存在，使用默认配置")
                self._save_config()  # 保存默认配置

            # 3. 从环境变量覆盖
            self._load_from_env()
            logger.info("应用环境变量配置覆盖")

            # 4. 最终验证
            self._validate_all_config()
            logger.info("分块配置加载完成")

        except Exception as e:
            logger.error(f"加载分块配置失败: {e}")
            # 使用默认配置
            self.config = ChunkingConfig()

    def _load_from_file(self):
        """从文件加载配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 验证配置数据
            if isinstance(data, dict):
                self.config = ChunkingConfig.from_dict(data)
            else:
                logger.warning("配置文件格式错误，使用默认配置")

        except json.JSONDecodeError as e:
            logger.error(f"配置文件JSON格式错误: {e}")
        except Exception as e:
            logger.error(f"从文件加载配置失败: {e}")

    def _load_from_env(self):
        """从环境变量加载配置"""
        env_mappings = {
            'CHUNK_ENABLED': ('enabled', bool),
            'CHUNK_DEFAULT_SIZE': ('default_chunk_size', int),
            'CHUNK_DEFAULT_OVERLAP': ('default_overlap', int),
            'CHUNK_STRATEGY': ('chunk_strategy', str),
            'CHUNK_MIN_SIZE': ('min_chunk_size', int),
            'CHUNK_MAX_SIZE': ('max_chunk_size', int),
            'CHUNK_THRESHOLD': ('chunking_threshold', int),
            'CHUNK_EMBEDDING_BATCH': ('embedding_batch_size', int),
            'CHUNK_QUALITY_CHECK': ('quality_check_enabled', bool),
            'CHUNK_AUTO_TYPES': ('auto_chunk_types', list),
        }

        for env_var, (config_key, value_type) in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                try:
                    if value_type == bool:
                        parsed_value = env_value.lower() in ('true', '1', 'yes', 'on')
                    elif value_type == int:
                        parsed_value = int(env_value)
                    elif value_type == float:
                        parsed_value = float(env_value)
                    elif value_type == list:
                        # 逗号分隔的字符串列表
                        parsed_value = [item.strip() for item in env_value.split(',') if item.strip()]
                    else:
                        parsed_value = env_value

                    setattr(self.config, config_key, parsed_value)
                    logger.debug(f"环境变量覆盖: {config_key} = {parsed_value}")

                except (ValueError, TypeError) as e:
                    logger.warning(f"环境变量 {env_var} 解析失败: {e}")

    def _validate_all_config(self):
        """验证所有配置"""
        try:
            # 验证基础参数
            if self.config.default_chunk_size <= 0:
                raise ValueError("默认分块大小必须大于0")

            if self.config.default_overlap < 0:
                raise ValueError("默认重叠大小不能小于0")

            if self.config.default_overlap >= self.config.default_chunk_size:
                raise ValueError("重叠大小不能大于等于分块大小")

            # 验证范围参数
            if self.config.min_chunk_size >= self.config.max_chunk_size:
                raise ValueError("最小分块大小必须小于最大分块大小")

            if self.config.min_overlap > self.config.max_overlap:
                raise ValueError("最小重叠大小不能大于最大重叠大小")

            # 验证性能参数
            if self.config.embedding_batch_size <= 0:
                raise ValueError("嵌入批处理大小必须大于0")

            if self.config.max_concurrent_chunks <= 0:
                raise ValueError("最大并发分块数必须大于0")

            logger.debug("配置验证通过")

        except ValueError as e:
            logger.error(f"配置验证失败: {e}")
            raise

    def _save_config(self):
        """保存配置到文件"""
        try:
            # 确保配置目录存在
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config.to_dict(), f, indent=2, ensure_ascii=False)

            logger.info(f"配置保存到文件: {self.config_file}")

        except Exception as e:
            logger.error(f"保存配置失败: {e}")

    def get_config(self) -> ChunkingConfig:
        """获取当前配置"""
        return self.config

    def update_config(self, **kwargs):
        """更新配置参数

        Args:
            **kwargs: 要更新的配置参数
        """
        try:
            # 更新配置
            for key, value in kwargs.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
                    logger.info(f"更新配置: {key} = {value}")
                else:
                    logger.warning(f"未知配置参数: {key}")

            # 重新验证
            self._validate_all_config()

            # 保存到文件
            self._save_config()

            logger.info("配置更新完成")

        except Exception as e:
            logger.error(f"更新配置失败: {e}")
            raise

    def reset_to_defaults(self):
        """重置为默认配置"""
        logger.info("重置配置为默认值")
        self.config = ChunkingConfig()
        self._save_config()

    def get_effective_chunk_size(self, content_length: int) -> int:
        """根据内容长度计算有效分块大小

        Args:
            content_length: 内容长度

        Returns:
            int: 有效分块大小
        """
        if content_length <= self.config.chunking_threshold:
            return content_length  # 不分块

        # 根据内容长度动态调整分块大小
        if content_length <= 1000:
            return self.config.default_chunk_size
        elif content_length <= 5000:
            return min(self.config.default_chunk_size * 2, self.config.max_chunk_size)
        else:
            return self.config.max_chunk_size

    def get_effective_overlap(self, chunk_size: int) -> int:
        """根据分块大小计算有效重叠大小

        Args:
            chunk_size: 分块大小

        Returns:
            int: 有效重叠大小
        """
        # 重叠大小为分块大小的10%，但不超过配置的限制
        overlap = int(chunk_size * 0.1)
        return max(self.config.min_overlap, min(overlap, self.config.max_overlap))

    def should_chunk_content(self, content: str, file_type: str) -> bool:
        """判断内容是否应该分块

        Args:
            content: 内容
            file_type: 文件类型

        Returns:
            bool: 是否应该分块
        """
        if not self.config.enabled:
            return False

        if not content or len(content) <= self.config.chunking_threshold:
            return False

        if file_type not in self.config.auto_chunk_types:
            return False

        return True

    def get_chunking_strategy_string(self, content_length: int) -> str:
        """获取分块策略字符串

        Args:
            content_length: 内容长度

        Returns:
            str: 分块策略字符串
        """
        if content_length <= self.config.chunking_threshold:
            return "no_chunk"

        chunk_size = self.get_effective_chunk_size(content_length)
        overlap = self.get_effective_overlap(chunk_size)
        return f"{chunk_size}+{overlap}"

    def export_config(self) -> Dict[str, Any]:
        """导出配置为字典（包含元数据）"""
        return {
            'config': self.config.to_dict(),
            'metadata': {
                'config_file': self.config_file,
                'last_updated': self._get_file_mtime(),
                'version': '1.0.0'
            }
        }

    def import_config(self, config_data: Dict[str, Any]):
        """导入配置

        Args:
            config_data: 配置数据
        """
        try:
            if 'config' in config_data:
                self.config = ChunkingConfig.from_dict(config_data['config'])
            else:
                self.config = ChunkingConfig.from_dict(config_data)

            self._validate_all_config()
            self._save_config()
            logger.info("配置导入成功")

        except Exception as e:
            logger.error(f"导入配置失败: {e}")
            raise

    def _get_file_mtime(self) -> Optional[str]:
        """获取配置文件修改时间"""
        try:
            if os.path.exists(self.config_file):
                mtime = os.path.getmtime(self.config_file)
                from datetime import datetime
                return datetime.fromtimestamp(mtime).isoformat()
        except Exception:
            pass
        return None

    def get_config_summary(self) -> Dict[str, Any]:
        """获取配置摘要"""
        return {
            'enabled': self.config.enabled,
            'chunk_strategy': self.config.chunk_strategy,
            'default_chunk_size': self.config.default_chunk_size,
            'default_overlap': self.config.default_overlap,
            'chunking_threshold': self.config.chunking_threshold,
            'auto_chunk_types': self.config.auto_chunk_types,
            'quality_check_enabled': self.config.quality_check_enabled,
            'config_file': self.config_file
        }


# 创建全局配置管理器实例
_config_manager: Optional[ChunkConfigManager] = None


def get_chunk_config_manager(config_file: Optional[str] = None) -> ChunkConfigManager:
    """获取分块配置管理器实例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ChunkConfigManager(config_file)
    return _config_manager


def get_chunk_config() -> ChunkingConfig:
    """获取当前分块配置"""
    return get_chunk_config_manager().get_config()


def update_chunk_config(**kwargs):
    """更新分块配置"""
    get_chunk_config_manager().update_config(**kwargs)


def reload_chunk_config(config_file: Optional[str] = None):
    """重新加载分块配置"""
    global _config_manager
    _config_manager = ChunkConfigManager(config_file)