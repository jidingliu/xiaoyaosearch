# 用户系统模块设计

## 架构概述
用户系统模块提供本地用户管理、数据隔离、隐私保护等功能，确保每个用户都有独立的、安全的使用环境。

## 核心组件设计

### 1. 用户管理器 (UserManager)
**职责**: 管理本地用户的创建、识别和切换

```python
@dataclass
class User:
    id: str                    # UUID
    username: str             # 显示名称
    created_at: datetime
    last_login: datetime
    is_active: bool = True
    preferences: Dict[str, Any] = field(default_factory=dict)

class UserManager:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.current_user: Optional[User] = None

    async def initialize(self) -> User:
        # 检查是否有现有用户
        users = await self.get_all_users()

        if not users:
            # 创建新用户
            user = await self.create_user()
        else:
            # 获取最后活跃用户
            user = max(users, key=lambda u: u.last_login)

        self.current_user = user
        await self.update_last_login(user.id)
        return user

    async def create_user(self, username: str = None) -> User:
        user_id = str(uuid.uuid4())
        if not username:
            username = f"用户{user_id[:8]}"

        user = User(
            id=user_id,
            username=username,
            created_at=datetime.now(),
            last_login=datetime.now()
        )

        await self.storage.save_user(user)
        await self.create_user_data_directory(user.id)
        return user

    async def switch_user(self, user_id: str) -> User:
        user = await self.storage.get_user(user_id)
        if user:
            self.current_user = user
            await self.update_last_login(user_id)
        return user
```

### 2. 用户数据隔离器 (UserDataIsolator)
**职责**: 确保不同用户数据的完全隔离

```python
class UserDataIsolator:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.current_user_id: Optional[str] = None

    def get_user_data_path(self, user_id: str) -> Path:
        return self.base_path / "users" / user_id

    def get_current_user_path(self) -> Path:
        if not self.current_user_id:
            raise ValueError("No current user set")
        return self.get_user_data_path(self.current_user_id)

    def get_user_db_path(self, user_id: str) -> Path:
        return self.get_user_data_path(user_id) / "data.db"

    def get_user_index_path(self, user_id: str) -> Path:
        return self.get_user_data_path(user_id) / "indexes"

    def get_user_cache_path(self, user_id: str) -> Path:
        return self.get_user_data_path(user_id) / "cache"

    async def create_user_environment(self, user_id: str):
        user_path = self.get_user_data_path(user_id)

        # 创建用户目录结构
        directories = [
            user_path,
            user_path / "indexes",
            user_path / "cache",
            user_path / "logs",
            user_path / "backups"
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        # 初始化用户数据库
        await self.initialize_user_database(user_id)
```

### 3. 用户偏好管理器 (UserPreferenceManager)
**职责**: 管理用户的个性化设置和偏好

```python
@dataclass
class UserPreferences:
    # 界面设置
    theme: str = "light"                    # light, dark
    language: str = "zh-CN"                # zh-CN, en-US
    font_size: int = 14                    # 12, 14, 16, 18

    # 搜索设置
    default_search_mode: str = "semantic"   # semantic, keyword, hybrid
    results_per_page: int = 20
    auto_suggestions: bool = True

    # 索引设置
    auto_index: bool = True
    index_file_types: List[str] = field(default_factory=lambda: [
        ".pdf", ".docx", ".xlsx", ".pptx", ".txt", ".md"
    ])
    max_file_size: int = 100 * 1024 * 1024  # 100MB

    # AI设置
    ai_mode: str = "local"                 # local, cloud, hybrid
    local_models: Dict[str, bool] = field(default_factory=dict)
    cloud_api_key: Optional[str] = None

    # 隐私设置
    save_search_history: bool = True
    auto_cleanup_history: bool = True
    history_retention_days: int = 90

class UserPreferenceManager:
    def __init__(self, user_id: str, storage: Storage):
        self.user_id = user_id
        self.storage = storage
        self.preferences: UserPreferences = UserPreferences()

    async def load_preferences(self) -> UserPreferences:
        prefs_data = await self.storage.get_user_preferences(self.user_id)
        if prefs_data:
            # 合并默认设置和用户设置
            default_prefs = UserPreferences()
            user_prefs = UserPreferences(**{**default_prefs.__dict__, **prefs_data})
            self.preferences = user_prefs
        return self.preferences

    async def save_preferences(self, preferences: UserPreferences):
        await self.storage.save_user_preferences(self.user_id, preferences.__dict__)
        self.preferences = preferences

    async def update_preference(self, key: str, value: Any):
        setattr(self.preferences, key, value)
        await self.save_preferences(self.preferences)

    def get_preference(self, key: str, default: Any = None):
        return getattr(self.preferences, key, default)
```

### 4. 用户数据统计器 (UserStatisticsCollector)
**职责**: 收集和分析用户使用数据

```python
@dataclass
class UserStatistics:
    total_files_indexed: int = 0
    total_searches: int = 0
    total_file_size: int = 0
    favorite_count: int = 0
    last_active_date: datetime = field(default_factory=datetime.now)
    avg_search_time: float = 0.0
    top_search_terms: List[str] = field(default_factory=list)
    file_type_distribution: Dict[str, int] = field(default_factory=dict)

class UserStatisticsCollector:
    def __init__(self, user_id: str, storage: Storage):
        self.user_id = user_id
        self.storage = storage

    async def record_file_indexed(self, file_path: Path, file_size: int):
        await self.storage.increment_user_stat(self.user_id, "total_files_indexed")
        await self.storage.add_to_user_stat(self.user_id, "total_file_size", file_size)

        # 更新文件类型分布
        file_ext = file_path.suffix.lower()
        await self.storage.update_file_type_distribution(self.user_id, file_ext)

    async def record_search(self, query: str, search_time: float):
        await self.storage.increment_user_stat(self.user_id, "total_searches")
        await self.storage.update_search_time_stats(self.user_id, search_time)
        await self.storage.update_search_terms(self.user_id, query)

    async def get_statistics(self) -> UserStatistics:
        stats_data = await self.storage.get_user_statistics(self.user_id)
        return UserStatistics(**stats_data)

    async def get_usage_insights(self) -> Dict[str, Any]:
        stats = await self.get_statistics()

        return {
            "most_active_day": await self.get_most_active_day(),
            "preferred_file_types": self.get_top_file_types(stats.file_type_distribution),
            "search_efficiency": self.calculate_search_efficiency(stats),
            "storage_usage": self.format_storage_usage(stats.total_file_size),
            "activity_trend": await self.get_activity_trend()
        }
```

### 5. 用户隐私保护器 (UserPrivacyProtector)
**职责**: 保护用户数据隐私和安全

```python
class UserPrivacyProtector:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.encryption_key = self.get_or_create_encryption_key()

    def get_or_create_encryption_key(self) -> bytes:
        key_file = self.get_user_data_path() / ".encryption_key"

        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # 生成新的加密密钥
            key = os.urandom(32)  # 256-bit key
            with open(key_file, 'wb') as f:
                f.write(key)
            # 设置文件权限（仅用户可读写）
            os.chmod(key_file, 0o600)
            return key

    def encrypt_sensitive_data(self, data: str) -> str:
        """加密敏感数据"""
        cipher = AES.new(self.encryption_key, AES.MODE_GCM)
        ciphertext, auth_tag = cipher.encrypt_and_digest(data.encode())

        # 组合 nonce + auth_tag + ciphertext
        encrypted_data = cipher.nonce + auth_tag + ciphertext
        return base64.b64encode(encrypted_data).decode()

    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """解密敏感数据"""
        encrypted_bytes = base64.b64decode(encrypted_data)

        # 分离 nonce + auth_tag + ciphertext
        nonce = encrypted_bytes[:12]
        auth_tag = encrypted_bytes[12:28]
        ciphertext = encrypted_bytes[28:]

        cipher = AES.new(self.encryption_key, AES.MODE_GCM, nonce=nonce)
        decrypted_data = cipher.decrypt_and_verify(ciphertext, auth_tag)
        return decrypted_data.decode()

    async def cleanup_sensitive_data(self, days_to_keep: int = 90):
        """清理过期的敏感数据"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        # 清理搜索历史
        await self.cleanup_search_history(cutoff_date)

        # 清理临时文件
        await self.cleanup_temporary_files()

        # 清理缓存
        await self.cleanup_cache(cutoff_date)
```

### 6. 用户会话管理器 (UserSessionManager)
**职责**: 管理用户会话状态

```python
class UserSessionManager:
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
        self.session_timeout = 24 * 60 * 60  # 24小时

    async def create_session(self, user_id: str) -> str:
        session_id = str(uuid.uuid4())
        session_data = {
            "user_id": user_id,
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        }

        await self.save_session(session_id, session_data)
        return session_id

    async def validate_session(self, session_id: str) -> bool:
        session_data = await self.get_session(session_id)
        if not session_data:
            return False

        # 检查会话是否超时
        last_activity = session_data["last_activity"]
        if (datetime.now() - last_activity).seconds > self.session_timeout:
            await self.delete_session(session_id)
            return False

        # 更新最后活动时间
        session_data["last_activity"] = datetime.now()
        await self.save_session(session_id, session_data)
        return True

    async def cleanup_expired_sessions(self):
        """清理过期会话"""
        cutoff_time = datetime.now() - timedelta(seconds=self.session_timeout)
        await self.delete_sessions_before(cutoff_time)
```

## 数据存储设计

### 用户表
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    preferences TEXT, -- JSON格式的偏好设置
    storage_used INTEGER DEFAULT 0,
    INDEX(last_login)
);
```

### 用户统计表
```sql
CREATE TABLE user_statistics (
    user_id TEXT PRIMARY KEY,
    total_files_indexed INTEGER DEFAULT 0,
    total_searches INTEGER DEFAULT 0,
    total_file_size INTEGER DEFAULT 0,
    favorite_count INTEGER DEFAULT 0,
    avg_search_time REAL DEFAULT 0.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 搜索历史表
```sql
CREATE TABLE search_history (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    query TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result_count INTEGER,
    search_time REAL,
    encrypted_data TEXT, -- 加密的敏感信息
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX(user_id, timestamp)
);
```

### 文件类型统计表
```sql
CREATE TABLE file_type_stats (
    user_id TEXT NOT NULL,
    file_extension TEXT NOT NULL,
    count INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, file_extension),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## API接口设计

### 用户管理API
```
GET /api/v1/user/current
- 获取当前用户信息

POST /api/v1/users
- 创建新用户

PUT /api/v1/users/{user_id}
- 更新用户信息

GET /api/v1/users
- 获取所有用户列表
```

### 偏好设置API
```
GET /api/v1/user/preferences
- 获取用户偏好设置

PUT /api/v1/user/preferences
- 更新偏好设置

PATCH /api/v1/user/preferences/{key}
- 更新单个偏好设置
```

### 统计数据API
```
GET /api/v1/user/statistics
- 获取用户使用统计

GET /api/v1/user/insights
- 获取使用洞察和建议

POST /api/v1/user/statistics/reset
- 重置统计数据
```

### 数据管理API
```
POST /api/v1/user/data/export
- 导出用户数据

POST /api/v1/user/data/import
- 导入用户数据

DELETE /api/v1/user/data/cleanup
- 清理用户数据
```

## 安全考虑

### 1. 数据加密
- 敏感数据AES-256加密
- 加密密钥本地存储
- 安全密钥管理

### 2. 访问控制
- 用户数据严格隔离
- 路径访问控制
- 权限验证

### 3. 隐私保护
- 数据本地存储
- 最小数据收集
- 用户数据控制

### 4. 会话安全
- 会话超时机制
- 安全会话管理
- 异常登录检测

## 性能优化

### 1. 数据缓存
- 用户偏好缓存
- 统计数据缓存
- 会话数据缓存

### 2. 懒加载
- 统计数据按需计算
- 历史数据分页加载
- 大文件异步处理

### 3. 数据清理
- 自动清理过期数据
- 压缩历史数据
- 优化存储空间