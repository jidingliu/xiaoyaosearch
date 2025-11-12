# 小遥搜索 API 文档

## 概述

小遥搜索 API 提供完整的文件搜索、索引管理、用户管理和设置配置功能。API 基于 FastAPI 构建，遵循 RESTful 设计原则，支持跨域请求和自动文档生成。

**基础URL**: `http://localhost:8000/api/v1`

**交互式文档**: `http://localhost:8000/api/v1/docs`

## 认证

当前版本使用本地用户认证，通过用户ID识别用户身份。后续版本将支持更完善的认证机制。

## API 端点

### 搜索模块

#### 搜索文件
```http
GET /search?q={query}&type={file_type}&start_date={date}&end_date={date}&size={count}&page={page}
```

**描述**: 执行智能文件搜索，支持语义搜索和关键词搜索

**查询参数**:
- `q` (string, 必需): 搜索查询内容
- `type` (string, 可选): 文件类型过滤 (pdf, docx, txt等)
- `start_date` (string, 可选): 开始日期 (YYYY-MM-DD)
- `end_date` (string, 可选): 结束日期 (YYYY-MM-DD)
- `size` (integer, 可选): 返回结果数量，默认20，最大100
- `page` (integer, 可选): 页码，默认1

**响应示例**:
```json
{
  "query": "机器学习",
  "total": 15,
  "results": [
    {
      "id": "file_123",
      "title": "机器学习基础.pdf",
      "path": "/Users/用户/Documents/机器学习基础.pdf",
      "size": 2048576,
      "modified_time": "2024-11-08",
      "file_type": "pdf",
      "score": 0.95,
      "summary": "这是一个关于机器学习基础的文档...",
      "highlights": ["机器学习", "基础"]
    }
  ],
  "search_time": 0.234,
  "suggestions": ["深度学习", "神经网络", "AI算法"]
}
```

#### 查询理解
```http
POST /search/understand
```

**描述**: 使用AI理解用户查询意图

**请求体**:
```json
{
  "query": "上周的产品设计PPT"
}
```

**响应示例**:
```json
{
  "keywords": ["产品设计", "PPT"],
  "semantic_query": "产品设计相关的演示文稿",
  "time_range": {
    "start_date": "2024-11-03",
    "end_date": "2024-11-09"
  },
  "file_types": ["ppt", "pptx"],
  "intent": "search_with_time_filter"
}
```

#### 搜索建议
```http
GET /search/suggestions?q={prefix}&limit={count}
```

**查询参数**:
- `q` (string, 必需): 查询前缀
- `limit` (integer, 可选): 建议数量，默认5，最大20

**响应示例**:
```json
{
  "suggestions": [
    "机器学习算法",
    "机器学习基础",
    "机器学习应用"
  ]
}
```

### 文件管理模块

#### 获取文件列表
```http
GET /files?directory_id={id}&type={type}&indexed_only={boolean}&page={page}&size={size}
```

**查询参数**:
- `directory_id` (string, 可选): 目录ID
- `type` (string, 可选): 文件类型过滤
- `indexed_only` (boolean, 可选): 仅显示已索引文件，默认true
- `page` (integer, 可选): 页码，默认1
- `size` (integer, 可选): 每页数量，默认50，最大100

**响应示例**:
```json
[
  {
    "id": "file_456",
    "file_name": "技术规格说明书.pdf",
    "file_path": "/Users/用户/Documents/技术规格说明书.pdf",
    "size": 3145728,
    "file_type": "pdf",
    "mime_type": "application/pdf",
    "modified_time": "2024-11-05",
    "created_at": "2024-11-01",
    "indexed_at": "2024-11-08",
    "status": "indexed",
    "is_deleted": false
  }
]
```

#### 获取文件信息
```http
GET /files/{file_id}
```

**响应示例**:
```json
{
  "id": "file_456",
  "file_name": "技术规格说明书.pdf",
  "file_path": "/Users/用户/Documents/技术规格说明书.pdf",
  "size": 3145728,
  "file_type": "pdf",
  "mime_type": "application/pdf",
  "modified_time": "2024-11-05",
  "created_at": "2024-11-01",
  "indexed_at": "2024-11-08",
  "status": "indexed",
  "is_deleted": false
}
```

#### 预览文件
```http
GET /files/{file_id}/preview?highlights={keywords}
```

**查询参数**:
- `highlights` (string, 可选): 高亮关键词，用逗号分隔

**响应示例**:
```json
{
  "file_id": "file_456",
  "file_name": "技术规格说明书.pdf",
  "file_type": "pdf",
  "preview_type": "text",
  "content": "文档预览内容...",
  "metadata": {
    "pages": 25,
    "author": "作者"
  },
  "highlights": ["技术", "规格"],
  "preview_url": "/api/v1/files/file_456/preview/image.jpg"
}
```

#### 打开文件
```http
POST /files/{file_id}/open
```

**响应示例**:
```json
{
  "message": "文件已打开"
}
```

#### 删除文件索引
```http
DELETE /files/{file_id}
```

**响应示例**:
```json
{
  "message": "文件已删除"
}
```

#### 上传文件
```http
POST /files/upload?directory_id={id}
```

**请求**: `multipart/form-data`
- `file` (file, 必需): 要上传的文件
- `directory_id` (string, 可选): 目标目录ID

**响应示例**:
```json
{
  "id": "file_789",
  "file_name": "新文档.pdf",
  "file_path": "/Users/用户/新文档.pdf",
  "size": 1024000,
  "file_type": "pdf",
  "mime_type": "application/pdf",
  "modified_time": "2024-11-10",
  "created_at": "2024-11-10",
  "indexed_at": "2024-11-10",
  "status": "pending",
  "is_deleted": false
}
```

### 目录管理模块

#### 获取目录列表
```http
GET /directories
```

**响应示例**:
```json
[
  {
    "id": "dir_123",
    "path": "/Users/用户/Documents",
    "name": "Documents",
    "status": "active",
    "file_count": 1250,
    "indexed_count": 1180,
    "last_scan_time": "2024-11-08 10:30:00",
    "created_at": "2024-11-01",
    "updated_at": "2024-11-08",
    "error_message": null
  }
]
```

#### 添加索引目录
```http
POST /directories
```

**请求体**:
```json
{
  "path": "/Users/用户/Projects",
  "name": "Projects"
}
```

**响应示例**:
```json
{
  "id": "dir_456",
  "path": "/Users/用户/Projects",
  "name": "Projects",
  "status": "active",
  "file_count": 0,
  "indexed_count": 0,
  "last_scan_time": null,
  "created_at": "2024-11-10",
  "updated_at": "2024-11-10"
}
```

#### 获取目录信息
```http
GET /directories/{directory_id}
```

**响应示例**:
```json
{
  "id": "dir_123",
  "path": "/Users/用户/Documents",
  "name": "Documents",
  "status": "active",
  "file_count": 1250,
  "indexed_count": 1180,
  "last_scan_time": "2024-11-08 10:30:00",
  "created_at": "2024-11-01",
  "updated_at": "2024-11-08",
  "error_message": null
}
```

#### 扫描目录
```http
POST /directories/{directory_id}/scan?full_scan={boolean}
```

**查询参数**:
- `full_scan` (boolean, 可选): 是否全量扫描，默认false

**响应示例**:
```json
{
  "message": "目录扫描已启动",
  "task_id": "scan_task_dir_123",
  "directory_id": "dir_123",
  "full_scan": false
}
```

#### 获取扫描状态
```http
GET /directories/{directory_id}/status
```

**响应示例**:
```json
{
  "directory_id": "dir_123",
  "is_scanning": true,
  "progress": 0.75,
  "current_file": "/Users/用户/Documents/当前文档.pdf",
  "total_files": 1250,
  "scanned_files": 937,
  "error_count": 3,
  "start_time": "2024-11-10 09:00:00",
  "estimated_completion": "2024-11-10 09:15:00"
}
```

#### 移除索引目录
```http
DELETE /directories/{directory_id}?remove_files={boolean}
```

**查询参数**:
- `remove_files` (boolean, 可选): 是否同时删除相关文件索引，默认false

**响应示例**:
```json
{
  "message": "目录已移除"
}
```

### 用户管理模块

#### 获取当前用户
```http
GET /users/current
```

**响应示例**:
```json
{
  "id": "user_123",
  "username": "用户",
  "created_at": "2024-11-01",
  "last_login": "2024-11-10",
  "is_active": true
}
```

#### 创建用户
```http
POST /users
```

**响应示例**:
```json
{
  "id": "user_456",
  "username": "用户abc123",
  "created_at": "2024-11-10",
  "last_login": "2024-11-10",
  "is_active": true
}
```

### 设置管理模块

#### 获取用户设置
```http
GET /settings
```

**响应示例**:
```json
{
  "search_mode": "hybrid",
  "results_per_page": 20,
  "auto_suggestions": true,
  "search_history_enabled": true,
  "indexed_file_types": [".pdf", ".docx", ".txt"],
  "max_file_size": 104857600,
  "index_update_frequency": "realtime",
  "ai_mode": "local",
  "local_models": {},
  "cloud_api_config": {},
  "gpu_acceleration": true,
  "theme": "light",
  "language": "zh-CN",
  "font_size": 14,
  "max_memory_usage": 2048,
  "max_concurrent_tasks": 4,
  "cache_size": 512
}
```

#### 更新用户设置
```http
PUT /settings
```

**请求体**:
```json
{
  "search_mode": "semantic",
  "results_per_page": 30,
  "ai_mode": "hybrid"
}
```

**响应示例**:
```json
{
  "search_mode": "semantic",
  "results_per_page": 30,
  "auto_suggestions": true,
  "search_history_enabled": true,
  "ai_mode": "hybrid"
}
```

#### 重置设置
```http
POST /settings/reset
```

**响应示例**:
```json
{
  "message": "设置已重置",
  "settings": {
    "search_mode": "hybrid",
    "results_per_page": 20,
    ...
  }
}
```

#### 导出设置
```http
POST /settings/export
```

**响应示例**:
```json
{
  "version": "0.1.0",
  "export_time": "2024-11-10T10:30:00Z",
  "settings": {
    "search_mode": "hybrid",
    "results_per_page": 20,
    ...
  }
}
```

#### 导入设置
```http
POST /settings/import
```

**请求体**:
```json
{
  "version": "0.1.0",
  "settings": {
    "search_mode": "semantic",
    "results_per_page": 25
  }
}
```

**响应示例**:
```json
{
  "message": "设置导入成功",
  "settings": {
    "search_mode": "semantic",
    "results_per_page": 25
  }
}
```

### 数据库管理模块

#### 数据库健康检查
```http
GET /database/health
```

**描述**: 检查数据库连接健康状态

**响应示例**:
```json
{
  "status": "healthy",
  "message": "数据库连接正常",
  "timestamp": "2024-11-10T10:30:00Z"
}
```

#### 获取数据库信息
```http
GET /database/info
```

**描述**: 获取数据库详细信息和统计

**响应示例**:
```json
{
  "database_type": "SQLite",
  "database_path": "/path/to/xiaoyao_search.db",
  "file_size_bytes": 1048576,
  "file_size_mb": 1.0,
  "tables_count": 7,
  "connection_pool": {
    "pool_size": "StaticPool",
    "checked_out": "N/A"
  }
}
```

#### 创建数据库备份
```http
POST /database/backup?backup_dir={path}
```

**查询参数**:
- `backup_dir` (string, 可选): 备份目录路径

**响应示例**:
```json
{
  "success": true,
  "message": "数据库备份创建成功",
  "backup_path": "/path/to/data/backups/xiaoyao_search.db.backup_20241110_103000"
}
```

#### 列出备份文件
```http
GET /database/backups?backup_dir={path}
```

**查询参数**:
- `backup_dir` (string, 可选): 备份目录路径

**响应示例**:
```json
{
  "success": true,
  "backups": [
    {
      "filename": "xiaoyao_search.db.backup_20241110_103000",
      "path": "/path/to/data/backups/xiaoyao_search.db.backup_20241110_103000",
      "size_bytes": 1048576,
      "size_mb": 1.0,
      "created_at": "2024-11-10T10:30:00Z",
      "modified_at": "2024-11-10T10:30:00Z"
    }
  ],
  "count": 1
}
```

#### 恢复数据库
```http
POST /database/restore
```

**请求体**:
```json
{
  "backup_path": "/path/to/data/backups/xiaoyao_search.db.backup_20241110_103000"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "数据库已从 /path/to/data/backups/xiaoyao_search.db.backup_20241110_103000 恢复成功"
}
```

#### 清理旧备份
```http
DELETE /database/backups/cleanup?keep_count={count}&backup_dir={path}
```

**查询参数**:
- `keep_count` (integer, 必需): 保留的备份数量，默认5
- `backup_dir` (string, 可选): 备份目录路径

**响应示例**:
```json
{
  "success": true,
  "message": "旧备份清理完成，保留了最新的 5 个备份",
  "deleted_count": 2
}
```

#### 清理数据库碎片
```http
POST /database/vacuum
```

**描述**: 执行VACUUM命令清理数据库碎片，优化数据库文件大小

**响应示例**:
```json
{
  "success": true,
  "message": "数据库清理完成",
  "operation": "VACUUM"
}
```

#### 分析数据库统计
```http
POST /database/analyze
```

**描述**: 执行ANALYZE命令更新数据库统计信息，优化查询性能

**响应示例**:
```json
{
  "success": true,
  "message": "数据库分析完成，查询优化信息已更新",
  "operation": "ANALYZE"
}
```

#### 获取数据库统计信息
```http
GET /database/stats
```

**描述**: 获取详细的数据库统计信息

**响应示例**:
```json
{
  "success": true,
  "stats": {
    "tables": {
      "users": 1,
      "files": 150,
      "directories": 5,
      "search_history": 45,
      "favorites": 12,
      "settings": 20,
      "index_status": 1
    },
    "total_records": 234,
    "table_count": 7,
    "database_size_bytes": 2097152,
    "database_size_mb": 2.0,
    "users_count": 1,
    "files_count": 150,
    "directories_count": 5,
    "search_history_count": 45,
    "file_types": {
      "pdf": 80,
      "docx": 30,
      "txt": 20,
      "md": 15,
      "pptx": 5
    }
  },
  "timestamp": "2024-11-10T10:30:00Z"
}
```

## 健康检查

#### 根路径
```http
GET /
```

**响应示例**:
```json
{
  "message": "小遥搜索API服务运行中",
  "version": "0.1.0",
  "status": "healthy"
}
```

#### 健康检查
```http
GET /health
```

**响应示例**:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

## 错误处理

API 使用标准的 HTTP 状态码：

- `200 OK`: 请求成功
- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未授权
- `403 Forbidden`: 禁止访问
- `404 Not Found`: 资源不存在
- `422 Unprocessable Entity`: 请求体格式错误
- `500 Internal Server Error`: 服务器内部错误

错误响应格式：
```json
{
  "detail": "错误描述信息",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-11-10T10:30:00Z"
}
```

## 限制

- 搜索查询最大长度: 1000 字符
- 单页结果最大数量: 100
- 文件上传最大大小: 100MB
- API 请求频率限制: 100 请求/分钟

## 开发工具

### 自动生成文档
- **Swagger UI**: `http://localhost:8000/api/v1/docs`
- **ReDoc**: `http://localhost:8000/api/v1/redoc`

### API 测试
项目包含完整的测试套件，使用 pytest 框架：

```bash
cd backend
pytest tests/
```

### 数据库管理
```bash
python manage.py init    # 初始化数据库
python manage.py check    # 检查数据库状态
python manage.py reset    # 重置数据库
```