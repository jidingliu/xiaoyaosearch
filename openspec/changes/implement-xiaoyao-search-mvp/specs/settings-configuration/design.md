# 设置与配置模块设计

## 架构概述
设置与配置模块提供全面的系统配置管理，包括搜索、索引、AI、性能、界面、隐私等各个方面的设置选项，确保用户可以根据需求定制系统行为。

## 核心组件设计

### 1. 设置管理器 (SettingsManager)
**职责**: 统一管理所有系统设置

```python
@dataclass
class Settings:
    # 搜索设置
    search_mode: str = "hybrid"             # semantic, keyword, hybrid
    results_per_page: int = 20
    auto_suggestions: bool = True
    search_history_enabled: bool = True

    # 索引设置
    indexed_file_types: List[str] = field(default_factory=lambda: [
        ".pdf", ".docx", ".xlsx", ".pptx", ".txt", ".md"
    ])
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    index_update_frequency: str = "realtime" # realtime, hourly, daily, manual
    excluded_directories: List[str] = field(default_factory=list)

    # AI设置
    ai_mode: str = "local"                  # local, cloud, hybrid
    local_models: Dict[str, str] = field(default_factory=dict)  # model_type -> model_name
    cloud_api_config: Dict[str, str] = field(default_factory=dict)
    gpu_acceleration: bool = True

    # 性能设置
    max_memory_usage: int = 2048            # MB
    max_concurrent_tasks: int = 4
    cache_size: int = 512                   # MB

    # 界面设置
    theme: str = "light"                    # light, dark, auto
    language: str = "zh-CN"                 # zh-CN, en-US
    font_size: int = 14                     # 12, 14, 16, 18

    # 隐私设置
    search_retention_days: int = 90
    auto_cleanup_enabled: bool = True
    telemetry_enabled: bool = False

class SettingsManager:
    def __init__(self, storage: Storage, validator: SettingsValidator):
        self.storage = storage
        self.validator = validator
        self.settings: Settings = Settings()
        self.observers: List[SettingsObserver] = []

    async def load_settings(self) -> Settings:
        settings_data = await self.storage.get_settings()
        if settings_data:
            # 合并默认设置和存储设置
            self.settings = Settings(**{**self.settings.__dict__, **settings_data})
        else:
            await self.save_settings(self.settings)
        return self.settings

    async def save_settings(self, settings: Settings) -> bool:
        # 验证设置
        if not self.validator.validate(settings):
            return False

        # 保存到存储
        success = await self.storage.save_settings(settings.__dict__)
        if success:
            self.settings = settings
            await self.notify_observers(settings)
        return success

    async def update_setting(self, key: str, value: Any) -> bool:
        if not hasattr(self.settings, key):
            return False

        # 验证单个设置项
        if not self.validator.validate_setting(key, value):
            return False

        setattr(self.settings, key, value)
        return await self.save_settings(self.settings)

    def get_setting(self, key: str, default: Any = None) -> Any:
        return getattr(self.settings, key, default)

    def add_observer(self, observer: SettingsObserver):
        self.observers.append(observer)

    async def notify_observers(self, settings: Settings):
        for observer in self.observers:
            await observer.on_settings_changed(settings)
```

### 2. 设置验证器 (SettingsValidator)
**职责**: 验证设置值的有效性

```python
class SettingsValidator:
    def __init__(self):
        self.validation_rules = self._build_validation_rules()

    def _build_validation_rules(self) -> Dict[str, Dict]:
        return {
            "search_mode": {
                "type": str,
                "choices": ["semantic", "keyword", "hybrid"],
                "required": True
            },
            "results_per_page": {
                "type": int,
                "min": 5,
                "max": 100,
                "required": True
            },
            "max_file_size": {
                "type": int,
                "min": 1024,  # 1KB
                "max": 1024 * 1024 * 1024,  # 1GB
                "required": True
            },
            "ai_mode": {
                "type": str,
                "choices": ["local", "cloud", "hybrid"],
                "required": True
            },
            "max_memory_usage": {
                "type": int,
                "min": 512,  # 512MB
                "max": 8192,  # 8GB
                "required": True
            },
            "theme": {
                "type": str,
                "choices": ["light", "dark", "auto"],
                "required": True
            },
            "language": {
                "type": str,
                "choices": ["zh-CN", "en-US"],
                "required": True
            }
        }

    def validate(self, settings: Settings) -> ValidationResult:
        errors = []

        for key, rule in self.validation_rules.items():
            value = getattr(settings, key, None)
            result = self.validate_setting(key, value)
            if not result.is_valid:
                errors.extend(result.errors)

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

    def validate_setting(self, key: str, value: Any) -> ValidationResult:
        if key not in self.validation_rules:
            return ValidationResult(is_valid=False, errors=[f"未知的设置项: {key}"])

        rule = self.validation_rules[key]
        errors = []

        # 类型检查
        if "type" in rule and not isinstance(value, rule["type"]):
            errors.append(f"{key} 必须是 {rule['type'].__name__} 类型")

        # 选择检查
        if "choices" in rule and value not in rule["choices"]:
            errors.append(f"{key} 必须是以下值之一: {', '.join(rule['choices'])}")

        # 数值范围检查
        if isinstance(value, (int, float)):
            if "min" in rule and value < rule["min"]:
                errors.append(f"{key} 不能小于 {rule['min']}")
            if "max" in rule and value > rule["max"]:
                errors.append(f"{key} 不能大于 {rule['max']}")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
```

### 3. AI模型配置管理器 (AIModelConfigManager)
**职责**: 管理AI模型的配置和切换

```python
class AIModelConfigManager:
    def __init__(self, settings_manager: SettingsManager, model_registry: ModelRegistry):
        self.settings_manager = settings_manager
        self.model_registry = model_registry

    async def get_available_models(self, model_type: str) -> List[ModelInfo]:
        return await self.model_registry.get_models_by_type(model_type)

    async def download_model(self, model_name: str, progress_callback: Callable = None):
        model_info = await self.model_registry.get_model_info(model_name)
        if not model_info:
            raise ValueError(f"未找到模型: {model_name}")

        # 检查磁盘空间
        if not await self.check_disk_space(model_info.size):
            raise InsufficientSpaceError("磁盘空间不足")

        # 下载模型
        downloader = ModelDownloader(model_info, progress_callback)
        await downloader.download()

    async def set_active_model(self, model_type: str, model_name: str) -> bool:
        # 验证模型是否已下载
        if not await self.model_registry.is_model_downloaded(model_name):
            return False

        # 更新设置
        local_models = self.settings_manager.get_setting("local_models", {})
        local_models[model_type] = model_name
        return await self.settings_manager.update_setting("local_models", local_models)

    async def configure_cloud_api(self, provider: str, config: Dict[str, str]) -> bool:
        # 验证API配置
        if not await self.validate_cloud_config(provider, config):
            return False

        # 更新云端配置
        cloud_config = self.settings_manager.get_setting("cloud_api_config", {})
        cloud_config[provider] = config
        return await self.settings_manager.update_setting("cloud_api_config", cloud_config)

    async def validate_cloud_config(self, provider: str, config: Dict[str, str]) -> bool:
        if provider == "openai":
            return await self.validate_openai_config(config)
        elif provider == "azure":
            return await self.validate_azure_config(config)
        return False

    async def validate_openai_config(self, config: Dict[str, str]) -> bool:
        # 测试API密钥有效性
        client = OpenAI(api_key=config.get("api_key"))
        try:
            await client.models.list()
            return True
        except Exception:
            return False
```

### 4. 界面配置管理器 (UIConfigManager)
**职责**: 管理界面相关的设置

```python
class UIConfigManager:
    def __init__(self, settings_manager: SettingsManager):
        self.settings_manager = settings_manager
        self.theme_manager = ThemeManager()
        self.language_manager = LanguageManager()

    async def apply_theme(self, theme_name: str):
        # 验证主题
        if theme_name not in ["light", "dark", "auto"]:
            raise ValueError("无效的主题名称")

        # 应用主题
        await self.theme_manager.apply_theme(theme_name)

        # 更新设置
        await self.settings_manager.update_setting("theme", theme_name)

    async def apply_language(self, language_code: str):
        # 验证语言
        if language_code not in ["zh-CN", "en-US"]:
            raise ValueError("不支持的语言代码")

        # 应用语言
        await self.language_manager.set_language(language_code)

        # 更新设置
        await self.settings_manager.update_setting("language", language_code)

    async def apply_font_size(self, font_size: int):
        # 验证字体大小
        valid_sizes = [12, 14, 16, 18]
        if font_size not in valid_sizes:
            raise ValueError(f"字体大小必须是以下值之一: {valid_sizes}")

        # 应用字体大小
        await self.theme_manager.set_font_size(font_size)

        # 更新设置
        await self.settings_manager.update_setting("font_size", font_size)

    async def get_ui_config(self) -> UIConfig:
        settings = self.settings_manager.settings
        return UIConfig(
            theme=settings.theme,
            language=settings.language,
            font_size=settings.font_size,
            animations_enabled=True,  # 可以添加更多UI设置
            compact_mode=False
        )
```

### 5. 性能配置管理器 (PerformanceConfigManager)
**职责**: 管理性能相关的设置

```python
class PerformanceConfigManager:
    def __init__(self, settings_manager: SettingsManager, system_monitor: SystemMonitor):
        self.settings_manager = settings_manager
        self.system_monitor = system_monitor

    async def apply_memory_limit(self, memory_limit_mb: int):
        # 验证内存限制
        available_memory = await self.system_monitor.get_available_memory()
        if memory_limit_mb > available_memory:
            raise ValueError("内存限制超过可用内存")

        # 应用内存限制
        await self.system_monitor.set_memory_limit(memory_limit_mb)

        # 更新设置
        await self.settings_manager.update_setting("max_memory_usage", memory_limit_mb)

    async def apply_gpu_acceleration(self, enabled: bool):
        if enabled:
            # 检查GPU可用性
            if not await self.system_monitor.has_gpu():
                raise ValueError("系统没有可用的GPU")
        else:
            # 切换到CPU模式
            await self.system_monitor.disable_gpu()

        # 更新设置
        await self.settings_manager.update_setting("gpu_acceleration", enabled)

    async def apply_concurrency_limit(self, limit: int):
        # 验证并发限制
        cpu_cores = await self.system_monitor.get_cpu_cores()
        if limit > cpu_cores * 2:
            raise ValueError(f"并发限制不应超过CPU核心数的2倍 ({cpu_cores * 2})")

        # 应用并发限制
        await self.system_monitor.set_concurrency_limit(limit)

        # 更新设置
        await self.settings_manager.update_setting("max_concurrent_tasks", limit)

    async def get_performance_recommendations(self) -> List[str]:
        """提供性能优化建议"""
        recommendations = []
        system_info = await self.system_monitor.get_system_info()

        # 内存建议
        if system_info.total_memory < 4096:  # 4GB
            recommendations.append("建议增加内存以获得更好的性能")

        # GPU建议
        if system_info.has_gpu and not self.settings_manager.get_setting("gpu_acceleration"):
            recommendations.append("启用GPU加速可以显著提升AI处理速度")

        # 并发建议
        cpu_usage = await self.system_monitor.get_cpu_usage()
        if cpu_usage > 80:
            recommendations.append("系统负载较高，建议降低并发任务数量")

        return recommendations
```

### 6. 设置导入导出管理器 (SettingsImportExportManager)
**职责**: 处理设置的导入导出功能

```python
class SettingsImportExportManager:
    def __init__(self, settings_manager: SettingsManager):
        self.settings_manager = settings_manager

    async def export_settings(self, file_path: Path, include_sensitive: bool = False) -> bool:
        try:
            settings = self.settings_manager.settings

            # 创建导出数据
            export_data = {
                "version": "1.0",
                "export_time": datetime.now().isoformat(),
                "settings": {}
            }

            # 根据敏感性选择导出内容
            for key, value in settings.__dict__.items():
                if self.is_sensitive_setting(key) and not include_sensitive:
                    export_data["settings"][key] = "[REDACTED]"
                else:
                    export_data["settings"][key] = value

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            logger.error(f"导出设置失败: {e}")
            return False

    async def import_settings(self, file_path: Path, merge: bool = True) -> bool:
        try:
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)

            # 验证版本兼容性
            if not self.is_version_compatible(import_data.get("version", "1.0")):
                raise ValueError("设置文件版本不兼容")

            imported_settings = import_data.get("settings", {})

            if merge:
                # 合并设置
                current_settings = self.settings_manager.settings.__dict__
                merged_settings = {**current_settings, **imported_settings}
                new_settings = Settings(**merged_settings)
            else:
                # 完全替换设置
                new_settings = Settings(**imported_settings)

            # 验证并保存设置
            validator = SettingsValidator()
            if validator.validate(new_settings).is_valid:
                return await self.settings_manager.save_settings(new_settings)
            else:
                raise ValueError("导入的设置包含无效值")

        except Exception as e:
            logger.error(f"导入设置失败: {e}")
            return False

    def is_sensitive_setting(self, key: str) -> bool:
        """判断是否为敏感设置"""
        sensitive_keys = ["cloud_api_config", "api_keys", "tokens"]
        return any(sensitive in key.lower() for sensitive in sensitive_keys)

    def is_version_compatible(self, version: str) -> bool:
        """检查版本兼容性"""
        # 简单的版本兼容性检查
        supported_versions = ["1.0"]
        return version in supported_versions
```

## 数据存储设计

### 设置表
```sql
CREATE TABLE settings (
    category TEXT NOT NULL,     -- 设置类别: search, index, ai, performance, ui, privacy
    key TEXT NOT NULL,          -- 设置键
    value TEXT,                 -- 设置值（JSON格式）
    value_type TEXT,            -- 值类型: string, integer, boolean, array, object
    default_value TEXT,         -- 默认值
    description TEXT,           -- 设置描述
    is_sensitive BOOLEAN DEFAULT 0,  -- 是否为敏感信息
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (category, key)
);
```

### 设置历史表
```sql
CREATE TABLE settings_history (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    key TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    change_reason TEXT,         -- 修改原因: user_import, system_update, manual_change
    INDEX(category, key, changed_at)
);
```

## API接口设计

### 通用设置API
```
GET /api/v1/settings
- 获取所有设置

GET /api/v1/settings/{category}
- 获取指定类别的设置

PUT /api/v1/settings/{category}/{key}
- 更新单个设置项

PATCH /api/v1/settings
- 批量更新设置

POST /api/v1/settings/reset
- 重置设置到默认值
```

### AI模型配置API
```
GET /api/v1/settings/ai/models/available
- 获取可用模型列表

POST /api/v1/settings/ai/models/{model_name}/download
- 下载模型

PUT /api/v1/settings/ai/models/active
- 设置活跃模型

POST /api/v1/settings/ai/cloud/configure
- 配置云端API

GET /api/v1/settings/ai/cloud/status
- 获取云端服务状态
```

### 性能配置API
```
GET /api/v1/settings/performance/recommendations
- 获取性能优化建议

GET /api/v1/settings/performance/status
- 获取当前性能状态

PUT /api/v1/settings/performance/memory-limit
- 设置内存限制

PUT /api/v1/settings/performance/gpu-acceleration
- 设置GPU加速
```

### 导入导出API
```
POST /api/v1/settings/export
- 导出设置
{
  "include_sensitive": false,
  "format": "json"
}

POST /api/v1/settings/import
- 导入设置
{
  "file_path": "settings.json",
  "merge": true
}
```

## 用户体验设计

### 1. 设置分组
- **搜索设置**: 搜索模式、结果数量、建议功能
- **索引设置**: 文件类型、大小限制、更新频率
- **AI设置**: 模型配置、云端服务、GPU加速
- **性能设置**: 内存限制、并发控制、缓存配置
- **界面设置**: 主题、语言、字体大小
- **隐私设置**: 历史记录、数据清理、敏感目录

### 2. 设置搜索
- 支持设置项搜索
- 快速定位相关设置
- 智能设置建议

### 3. 设置预览
- 实时预览设置效果
- 设置变更对比
- 一键恢复默认值

### 4. 设置验证
- 实时输入验证
- 友好的错误提示
- 设置冲突检测

## 性能考虑

### 1. 设置缓存
- 常用设置内存缓存
- 异步持久化
- 批量更新优化

### 2. 懒加载
- 按需加载设置类别
- 复杂设置后台处理
- 大型配置分页显示

### 3. 设置同步
- 设置变更实时同步
- 跨组件状态一致
- 原子性更新操作