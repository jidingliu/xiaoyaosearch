# 小遥搜索 API 接口文档

## 概述

小遥搜索API基于FastAPI构建，提供RESTful接口和WebSocket实时通信，支持前端Electron应用调用本地后端服务。所有接口遵循HTTP/HTTPS协议，使用JSON格式进行数据交换。

## 基础信息

- **Base URL**: `http://localhost:8000`
- **API版本**: `v1`
- **认证方式**: 本地应用无需认证
- **数据格式**: JSON
- **字符编码**: UTF-8
- **时区**: UTC

## 数据类型定义

### 基础数据类型

#### FileInfo (文件信息)
```json
{
  "file_id": "string",              // 文件唯一标识
  "file_path": "string",            // 文件绝对路径
  "file_name": "string",            // 文件名
  "file_extension": "string",       // 文件扩展名 (如: pdf, docx, jpg)
  "file_size": "integer",           // 文件大小 (字节)
  "mime_type": "string",            // MIME类型
  "content_type": "string",         // 内容类型: document/image/audio/video/code
  "content_text": "string",         // 提取的文本内容
  "content_preview": "string",      // 内容预览 (前200字符)
  "content_summary": "string",      // AI生成摘要
  "ocr_text": "string",             // OCR提取的文本
  "transcription_text": "string",   // 音频转录文本
  "tags": ["string"],               // 标签列表
  "metadata": {                     // 文件元数据
    "author": "string",
    "title": "string",
    "subject": "string",
    "keywords": "string",
    "created_date": "string",        // 原始创建日期
    "page_count": "integer",         // 页数 (文档)
    "duration": "number",           // 时长 (音视频，秒)
    "width": "integer",             // 宽度 (图片/视频)
    "height": "integer",            // 高度 (图片/视频)
    "frame_rate": "number",         // 帧率 (视频)
    "bitrate": "integer",           // 比特率 (音视频)
    "custom": "object"              // 自定义元数据
  },
  "index_status": "string",         // 索引状态: pending/processing/completed/failed
  "search_count": "integer",        // 搜索次数
  "last_accessed_at": "string",     // 最后访问时间 (ISO 8601)
  "file_created_at": "string",     // 文件创建时间 (ISO 8601)
  "file_modified_at": "string",     // 文件修改时间 (ISO 8601)
  "indexed_at": "string",          // 索引时间 (ISO 8601)
  "created_at": "string",          // 记录创建时间 (ISO 8601)
  "updated_at": "string"           // 记录更新时间 (ISO 8601)
}
```

#### SearchResult (搜索结果项)
```json
{
  "file": "FileInfo",               // 文件信息对象
  "relevance_score": "number",      // 相关性分数 (0-1)
  "matches": [                      // 匹配片段
    {
      "field": "string",            // 匹配字段: content/title/path/metadata
      "snippet": "string",          // 匹配片段 (包含HTML高亮标记)
      "position": "integer",        // 匹配位置
      "score": "number"             // 片段相关性分数
    }
  ],
  "highlighted_content": "string",  // 高亮显示的内容
  "vector_score": "number",         // 向量搜索分数
  "text_score": "number",          // 全文搜索分数
  "ai_insights": {                  // AI分析结果
    "keywords": ["string"],         // 关键词
    "entities": [                   // 实体识别
      {
        "type": "string",          // 实体类型: person/organization/location/date
        "text": "string",          // 实体文本
        "confidence": "number"     // 置信度
      }
    ],
    "sentiment": "string",          // 情感分析: positive/neutral/negative
    "category": "string",           // 内容分类
    "language": "string"            // 语言识别
  }
}
```

#### SearchQuery (搜索查询)
```json
{
  "text": "string",                 // 文本查询
  "voice_base64": "string",         // 语音查询 (base64编码)
  "image_base64": "string",         // 图片查询 (base64编码)
  "audio_format": "string",         // 音频格式: wav/mp3/flac/m4a
  "image_format": "string",         // 图片格式: jpeg/png/webp
  "search_mode": "string",          // 搜索模式: hybrid/vector/fulltext
  "filters": {                      // 过滤条件
    "content_types": ["string"],    // 内容类型过滤
    "file_extensions": ["string"],  // 文件扩展名过滤
    "directories": ["string"],      // 目录范围
    "tags": ["string"],             // 标签过滤
    "date_range": {
      "start": "string",           // 开始日期 (YYYY-MM-DD)
      "end": "string"              // 结束日期 (YYYY-MM-DD)
    },
    "size_range": {
      "min": "integer",            // 最小文件大小 (字节)
      "max": "integer"             // 最大文件大小 (字节)
    }
  },
  "sort": {                         // 排序条件
    "field": "string",             // 排序字段: relevance/date/name/size/type
    "order": "string"              // 排序方向: asc/desc
  },
  "pagination": {
    "page": "integer",             // 页码 (从1开始)
    "size": "integer"              // 每页大小
  },
  "highlight": "boolean",           // 是否高亮关键词
  "include_content": "boolean",    // 是否包含内容预览
  "max_results": "integer",        // 最大结果数量
  "timeout": "integer"             // 超时时间 (秒)
}
```

#### Directory (索引目录)
```json
{
  "id": "integer",                  // 目录ID
  "directory_path": "string",       // 目录绝对路径
  "directory_name": "string",       // 目录名
  "parent_path": "string",          // 父目录路径
  "is_watched": "boolean",         // 是否正在监控
  "is_indexed": "boolean",         // 是否已索引
  "watch_recursive": "boolean",     // 是否递归监控
  "file_types": ["string"],         // 指定索引的文件类型 (空表示全部)
  "exclude_patterns": ["string"],   // 排除模式列表
  "file_count": "integer",          // 文件总数
  "indexed_count": "integer",       // 已索引文件数
  "failed_count": "integer",        // 索引失败文件数
  "total_size": "integer",          // 总大小 (字节)
  "indexed_size": "integer",        // 已索引大小 (字节)
  "last_scanned_at": "string",      // 最后扫描时间 (ISO 8601)
  "status": "string",               // 状态: idle/scanning/indexing/completed/error
  "progress": "number",             // 进度百分比 (0-100)
  "error_message": "string",        // 错误信息
  "created_at": "string",          // 添加时间 (ISO 8601)
  "updated_at": "string"           // 更新时间 (ISO 8601)
}
```

### 枚举类型定义

#### ContentType (内容类型)
- `document` - 文档类型 (pdf, docx, txt, md等)
- `image` - 图片类型 (jpg, png, gif, webp等)
- `audio` - 音频类型 (mp3, wav, flac, m4a等)
- `video` - 视频类型 (mp4, avi, mkv, mov等)
- `code` - 代码类型 (py, js, ts, java等)
- `archive` - 压缩包类型 (zip, rar, 7z等)

#### IndexStatus (索引状态)
- `pending` - 等待处理
- `processing` - 正在处理
- `completed` - 完成
- `failed` - 失败
- `skipped` - 跳过

#### SearchMode (搜索模式)
- `hybrid` - 混合搜索 (向量+全文)
- `vector` - 向量搜索
- `fulltext` - 全文搜索
- `semantic` - 语义搜索

#### SortField (排序字段)
- `relevance` - 相关性
- `date` - 日期
- `name` - 名称
- `size` - 大小
- `type` - 类型

#### QueryType (查询类型)
- `text` - 文本查询
- `voice` - 语音查询
- `image` - 图片查询
- `mixed` - 混合查询

## 通用响应格式

### 成功响应

```json
{
  "success": true,
  "data": {},  // 具体数据
  "message": "操作成功",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 错误响应

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "details": {}  // 详细错误信息
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 分页响应

```json
{
  "success": true,
  "data": {
    "items": [],  // 数据列表
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 100,
      "pages": 5,
      "has_next": true,
      "has_prev": false
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 搜索接口

### 1. 执行搜索

**接口**: `POST /api/v1/search`

**描述**: 执行多模态搜索，支持文本、语音、图片搜索

**请求参数**:

```json
{
  "query": {
    "text": "搜索关键词",          // 文本查询 (可选)
    "voice_base64": "base64编码的音频数据", // 语音查询 (可选)
    "image_base64": "base64编码的图片数据"  // 图片查询 (可选)
  },
  "search_mode": "hybrid",        // 搜索模式: hybrid/vector/fulltext
  "filters": {
    "content_types": ["document", "image"],  // 内容类型过滤
    "file_extensions": ["pdf", "docx"],       // 文件扩展名过滤
    "date_range": {
      "start": "2024-01-01",                 // 开始日期
      "end": "2024-12-31"                    // 结束日期
    },
    "size_range": {
      "min": 1024,                           // 最小文件大小 (字节)
      "max": 10485760                        // 最大文件大小 (字节)
    },
    "directories": ["/path/to/dir"],          // 目录范围
    "tags": ["重要", "工作"]                  // 标签过滤
  },
  "sort": {
    "field": "relevance",                    // 排序字段: relevance/date/name/size
    "order": "desc"                          // 排序方向: asc/desc
  },
  "pagination": {
    "page": 1,                               // 页码
    "size": 20                               // 每页大小
  },
  "highlight": true,              // 是否高亮关键词
  "include_content": true         // 是否包含内容预览
}
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "query_id": "uuid-query-id",
    "items": [
      {
        "file_id": 123,
        "file_path": "/path/to/document.pdf",
        "file_name": "重要文档.pdf",
        "file_extension": "pdf",
        "file_size": 1048576,
        "content_type": "document",
        "relevance_score": 0.95,
        "content_preview": "这是文档的预览内容...",
        "highlighted_content": "这是<mark>重要</mark>的文档内容...",
        "matches": [
          {
            "field": "content",
            "snippet": "这是一个<mark>重要</mark>的项目文档...",
            "position": 15
          }
        ],
        "tags": ["重要", "工作"],
        "last_modified": "2024-01-01T00:00:00Z",
        "created_at": "2024-01-01T00:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 45,
      "pages": 3,
      "has_next": true,
      "has_prev": false
    },
    "search_stats": {
      "total_time": 0.25,         // 总搜索时间 (秒)
      "vector_time": 0.12,        // 向量搜索时间
      "fulltext_time": 0.08,      // 全文搜索时间
      "fusion_time": 0.05         // 结果融合时间
    },
    "ai_analysis": {
      "keywords": ["重要", "文档", "项目"],
      "semantic_query": "与重要文档项目相关的内容",
      "intent": "document_search"
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 2. 搜索建议

**接口**: `GET /api/v1/search/suggestions`

**描述**: 获取搜索建议和自动完成

**请求参数**:

```
query: string      // 查询前缀
limit: integer     // 建议数量限制 (默认: 10)
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "suggestions": [
      {
        "text": "重要文档",
        "type": "history",         // history/popular/ai
        "count": 5,
        "description": "最近搜索过的重要文档"
      },
      {
        "text": "项目计划",
        "type": "ai",
        "suggestion": "您可能想搜索'项目规划文档'"
      }
    ]
  }
}
```

### 3. 搜索历史

**接口**: `GET /api/v1/search/history`

**描述**: 获取搜索历史记录

**请求参数**:

```
limit: integer     // 记录数量限制 (默认: 50)
type: string       // 查询类型: text/voice/image/all
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "history": [
      {
        "id": 1,
        "query_text": "重要文档",
        "query_type": "text",
        "result_count": 15,
        "created_at": "2024-01-01T00:00:00Z",
        "top_result": {
          "file_id": 123,
          "file_name": "重要文档.pdf"
        }
      }
    ]
  }
}
```

## 文件管理接口

### 1. 文件信息

**接口**: `GET /api/v1/files/{file_id}`

**描述**: 获取文件详细信息

**响应示例**:

```json
{
  "success": true,
  "data": {
    "file_id": 123,
    "file_path": "/path/to/document.pdf",
    "file_name": "重要文档.pdf",
    "file_extension": "pdf",
    "file_size": 1048576,
    "mime_type": "application/pdf",
    "content_type": "document",
    "content_text": "文档的完整文本内容...",
    "content_summary": "这是文档的AI生成摘要...",
    "ocr_text": "OCR提取的文本...",
    "transcription_text": "音频转录文本...",
    "tags": ["重要", "工作"],
    "metadata": {
      "author": "作者",
      "created_date": "2024-01-01",
      "page_count": 10
    },
    "index_status": "completed",
    "search_count": 15,
    "last_accessed_at": "2024-01-01T00:00:00Z",
    "file_created_at": "2024-01-01T00:00:00Z",
    "file_modified_at": "2024-01-01T00:00:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

### 2. 文件预览

**接口**: `GET /api/v1/files/{file_id}/preview`

**描述**: 获取文件预览内容

**请求参数**:

```
type: string       // 预览类型: text/image/audio/video
page: integer      // 文档页码 (仅对PDF等)
quality: string    // 图片质量: low/medium/high
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "preview_type": "image",
    "content": "base64编码的预览内容",
    "metadata": {
      "width": 800,
      "height": 600,
      "format": "jpeg"
    },
    "pages": {
      "current": 1,
      "total": 10
    }
  }
}
```

### 3. 文件下载

**接口**: `GET /api/v1/files/{file_id}/download`

**描述**: 下载原始文件

**响应**: 直接返回文件二进制数据

### 4. 打开文件

**接口**: `POST /api/v1/files/{file_id}/open`

**描述**: 使用系统默认应用打开文件

**响应示例**:

```json
{
  "success": true,
  "message": "文件已使用默认应用打开"
}
```

### 5. 打开所在目录

**接口**: `POST /api/v1/files/{file_id}/open-location`

**描述**: 在文件管理器中打开文件所在目录

**响应示例**:

```json
{
  "success": true,
  "message": "已打开文件所在目录"
}
```

### 6. 文件操作

**接口**: `POST /api/v1/files/{file_id}/actions`

**描述**: 执行文件操作

**请求参数**:

```json
{
  "action": "rename|move|delete|copy",
  "params": {
    "new_name": "新文件名.pdf",          // 重命名时
    "new_path": "/new/path/file.pdf",   // 移动时
    "target_path": "/copy/target.pdf"   // 复制时
  }
}
```

## 索引管理接口

### 1. 添加目录

**接口**: `POST /api/v1/index/directories`

**描述**: 添加需要索引的目录

**请求参数**:

```json
{
  "directory_path": "/path/to/directory",
  "watch_recursive": true,              // 是否递归监控
  "file_types": ["pdf", "docx"],        // 指定文件类型 (空表示全部)
  "exclude_patterns": [                 // 排除模式
    "*.tmp",
    ".git/*",
    "node_modules/*"
  ]
}
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "directory_id": 456,
    "directory_path": "/path/to/directory",
    "status": "scanning",
    "estimated_files": 1250,
    "message": "目录扫描已开始"
  }
}
```

### 2. 获取目录列表

**接口**: `GET /api/v1/index/directories`

**描述**: 获取已添加的目录列表

**响应示例**:

```json
{
  "success": true,
  "data": {
    "directories": [
      {
        "id": 456,
        "directory_path": "/path/to/directory",
        "directory_name": "Documents",
        "is_watched": true,
        "is_indexed": true,
        "file_count": 1200,
        "total_size": 1073741824,
        "indexed_count": 1150,
        "last_scanned_at": "2024-01-01T00:00:00Z",
        "status": "completed"
      }
    ]
  }
}
```

### 3. 删除目录

**接口**: `DELETE /api/v1/index/directories/{directory_id}`

**描述**: 删除索引目录

**响应示例**:

```json
{
  "success": true,
  "message": "目录已从索引中移除"
}
```

### 4. 重新索引

**接口**: `POST /api/v1/index/rebuild`

**描述**: 重建索引

**请求参数**:

```json
{
  "directory_ids": [456, 789],          // 指定目录ID (空表示全部)
  "force": false                        // 是否强制重建
}
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "task_id": "rebuild-task-uuid",
    "estimated_duration": "10-15分钟",
    "message": "索引重建已开始"
  }
}
```

### 5. 索引状态

**接口**: `GET /api/v1/index/status`

**描述**: 获取索引状态

**响应示例**:

```json
{
  "success": true,
  "data": {
    "overall_status": "running",        // idle/running/completed/error
    "progress": {
      "total_files": 5000,
      "indexed_files": 3500,
      "failed_files": 10,
      "pending_files": 1490,
      "percentage": 70
    },
    "performance": {
      "files_per_minute": 50,
      "estimated_time_remaining": "30分钟"
    },
    "current_tasks": [
      {
        "file_id": 123,
        "file_name": "document.pdf",
        "status": "processing",
        "progress": 60
      }
    ]
  }
}
```

### 6. 索引统计

**接口**: `GET /api/v1/index/stats`

**描述**: 获取索引统计信息

**响应示例**:

```json
{
  "success": true,
  "data": {
    "total_files": 10000,
    "indexed_files": 9500,
    "total_directories": 25,
    "indexed_directories": 20,
    "total_size": 10737418240,
    "index_size": 1073741824,
    "vector_count": 50000,
    "last_updated": "2024-01-01T00:00:00Z",
    "file_types": {
      "pdf": 3000,
      "docx": 2000,
      "jpg": 1500,
      "mp4": 1000
    }
  }
}
```

## AI服务接口

### 1. 查询理解

**接口**: `POST /api/v1/ai/query-analysis`

**描述**: AI查询理解和分析

**请求参数**:

```json
{
  "query": "上周的产品设计PPT",
  "context": {                        // 可选的上下文信息
    "previous_queries": ["产品设计"],
    "user_preferences": ["pdf", "ppt"]
  }
}
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "parsed_query": {
      "keywords": ["产品设计", "PPT"],
      "semantic_query": "产品设计相关的演示文稿",
      "intent": "document_search",
      "time_range": {
        "start": "2023-12-25",
        "end": "2024-01-01"
      },
      "file_types": ["ppt", "pptx"],
      "entities": [
        {
          "type": "time_expression",
          "value": "上周",
          "normalized": "2023-12-25 to 2024-01-01"
        }
      ]
    },
    "suggestions": [
      {
        "type": "filter",
        "description": "添加时间过滤: 最近一周",
        "filter": {
          "date_range": {
            "start": "2023-12-25",
            "end": "2024-01-01"
          }
        }
      }
    ]
  }
}
```

### 2. 文件摘要

**接口**: `POST /api/v1/ai/summarize`

**描述**: 生成文件摘要

**请求参数**:

```json
{
  "file_id": 123,
  "summary_type": "brief",            // brief/detailed/bullets
  "language": "zh-CN"                  // 摘要语言
}
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "summary": "这是一个关于产品设计的重要文档，包含了产品的功能规划、技术架构和开发计划。",
    "key_points": [
      "产品功能规划",
      "技术架构设计",
      "开发时间计划"
    ],
    "language": "zh-CN",
    "confidence": 0.95
  }
}
```

### 3. 语音转文字

**接口**: `POST /api/v1/ai/speech-to-text`

**描述**: 语音识别转文字

**请求参数**:

```json
{
  "audio_base64": "base64编码的音频数据",
  "audio_format": "wav",               // 音频格式: wav/mp3/flac
  "language": "zh-CN",                 // 指定语言 (可选，自动检测)
  "model": "base"                      // 模型大小: base/small/large
}
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "text": "这是语音识别的结果文本",
    "language": "zh-CN",
    "confidence": 0.92,
    "segments": [
      {
        "start": 0.0,
        "end": 2.5,
        "text": "这是语音",
        "confidence": 0.95
      },
      {
        "start": 2.5,
        "end": 5.0,
        "text": "识别的结果",
        "confidence": 0.89
      }
    ]
  }
}
```

### 4. 图片分析

**接口**: `POST /api/v1/ai/image-analysis`

**描述**: 图片内容分析和标签生成

**请求参数**:

```json
{
  "image_base64": "base64编码的图片数据",
  "image_format": "jpeg",              // 图片格式
  "analysis_type": "tags",             // tags/ocr/face/text
  "language": "zh-CN"                  // 标签语言
}
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "tags": [
      {
        "name": "风景",
        "confidence": 0.95
      },
      {
        "name": "山",
        "confidence": 0.88
      }
    ],
    "ocr_text": "图片中的文字内容",
    "objects": [
      {
        "name": "山",
        "bbox": [100, 50, 200, 150],
        "confidence": 0.92
      }
    ],
    "description": "这是一张风景优美的山景照片"
  }
}
```

## 设置接口

### 1. 获取设置

**接口**: `GET /api/v1/settings`

**描述**: 获取用户设置

**请求参数**:

```
category: string    // 设置分类: all/search/index/ui/ai/privacy
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "search": {
      "history_enabled": true,
      "auto_suggest": true,
      "default_mode": "hybrid",
      "results_per_page": 20
    },
    "indexing": {
      "auto_update": true,
      "batch_size": 10,
      "max_concurrent": 4
    },
    "ai": {
      "provider": "local",
      "models": {
        "embedding": "bge-base-zh",
        "asr": "fast-whisper-base"
      }
    }
  }
}
```

### 2. 更新设置

**接口**: `PUT /api/v1/settings`

**描述**: 更新用户设置

**请求参数**:

```json
{
  "search": {
    "default_mode": "vector",
    "results_per_page": 30
  },
  "ai": {
    "models": {
      "embedding": "bge-large-zh"
    }
  }
}
```

### 3. 重置设置

**接口**: `POST /api/v1/settings/reset`

**描述**: 重置设置为默认值

**请求参数**:

```json
{
  "categories": ["search", "ai"]       // 要重置的分类 (空表示全部)
}
```

## 标签管理接口

### 1. 获取标签

**接口**: `GET /api/v1/tags`

**描述**: 获取用户标签列表

**响应示例**:

```json
{
  "success": true,
  "data": {
    "tags": [
      {
        "id": 1,
        "name": "重要",
        "color": "#ff4d4f",
        "icon": "star",
        "usage_count": 25,
        "description": "重要文件标记"
      }
    ]
  }
}
```

### 2. 创建标签

**接口**: `POST /api/v1/tags`

**描述**: 创建新标签

**请求参数**:

```json
{
  "name": "工作",
  "color": "#1890ff",
  "icon": "briefcase",
  "description": "工作相关文件"
}
```

### 3. 文件标签关联

**接口**: `POST /api/v1/files/{file_id}/tags`

**描述**: 为文件添加标签

**请求参数**:

```json
{
  "tag_ids": [1, 2, 3],
  "auto_generated": false             // 是否AI自动生成
}
```

### 4. 收藏文件

**接口**: `POST /api/v1/bookmarks`

**描述**: 收藏文件

**请求参数**:

```json
{
  "file_id": 123,
  "folder_path": "/工作/重要文档",
  "notes": "这是很重要的项目文档",
  "rating": 5
}
```

### 5. 获取收藏

**接口**: `GET /api/v1/bookmarks`

**描述**: 获取收藏列表

**响应示例**:

```json
{
  "success": true,
  "data": {
    "bookmarks": [
      {
        "id": 1,
        "file": {
          "file_id": 123,
          "file_name": "重要文档.pdf",
          "file_path": "/path/to/document.pdf"
        },
        "folder_path": "/工作/重要文档",
        "notes": "这是很重要的项目文档",
        "rating": 5,
        "created_at": "2024-01-01T00:00:00Z"
      }
    ],
    "folders": ["/工作", "/学习", "/生活"]
  }
}
```

## 系统接口

### 1. 系统信息

**接口**: `GET /api/v1/system/info`

**描述**: 获取系统信息

**响应示例**:

```json
{
  "success": true,
  "data": {
    "app": {
      "name": "小遥搜索",
      "version": "1.0.0",
      "build": "20240101"
    },
    "system": {
      "platform": "Windows",
      "architecture": "x64",
      "python_version": "3.11.0"
    },
    "resources": {
      "cpu_usage": 15.2,
      "memory_usage": 8.1,
      "disk_usage": 45.7
    },
    "models": {
      "embedding_model": "bge-base-zh",
      "asr_model": "fast-whisper-base",
      "vision_model": "cn-clip"
    }
  }
}
```

### 2. 系统健康检查

**接口**: `GET /api/v1/system/health`

**描述**: 系统健康状态检查

**响应示例**:

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "checks": {
      "database": "ok",
      "vector_index": "ok",
      "fulltext_index": "ok",
      "ai_models": "ok",
      "disk_space": "warning"      // 可用空间不足
    },
    "uptime": 86400,
    "version": "1.0.0"
  }
}
```

### 3. 清理系统

**接口**: `POST /api/v1/system/cleanup`

**描述**: 清理系统缓存和临时文件

**请求参数**:

```json
{
  "cleanup_types": [
    "cache",         // 清理缓存
    "logs",          // 清理日志
    "temp_files",    // 清理临时文件
    "orphaned_data"  // 清理孤立数据
  ],
  "older_than": "7d" // 清理超过指定时间的文件
}
```

## WebSocket 接口

### 连接信息

**URL**: `ws://localhost:8000/ws`

**认证**: 本地应用无需认证

### 消息格式

```json
{
  "type": "message_type",
  "data": {},          // 消息数据
  "timestamp": "2024-01-01T00:00:00Z",
  "message_id": "uuid"
}
```

### 1. 索引进度推送

**类型**: `index_progress`

```json
{
  "type": "index_progress",
  "data": {
    "directory_id": 456,
    "current_file": "document.pdf",
    "progress": {
      "current": 3500,
      "total": 5000,
      "percentage": 70
    },
    "status": "processing"
  }
}
```

### 2. 搜索结果推送

**类型**: `search_results`

```json
{
  "type": "search_results",
  "data": {
    "query_id": "uuid-query-id",
    "results": [...],      // 搜索结果
    "total_found": 100,
    "complete": false      // 是否搜索完成
  }
}
```

### 3. 系统通知

**类型**: `notification`

```json
{
  "type": "notification",
  "data": {
    "level": "info",        // info/warning/error
    "title": "索引完成",
    "message": "所有文件索引已完成",
    "actions": [
      {
        "label": "查看详情",
        "action": "view_index_stats"
      }
    ]
  }
}
```

## 错误代码

| 错误代码 | HTTP状态码 | 描述 |
|---------|-----------|------|
| INVALID_REQUEST | 400 | 请求参数无效 |
| UNAUTHORIZED | 401 | 未授权访问 |
| FORBIDDEN | 403 | 禁止访问 |
| NOT_FOUND | 404 | 资源不存在 |
| METHOD_NOT_ALLOWED | 405 | 请求方法不允许 |
| CONFLICT | 409 | 资源冲突 |
| VALIDATION_ERROR | 422 | 数据验证失败 |
| RATE_LIMIT_EXCEEDED | 429 | 请求频率超限 |
| INTERNAL_ERROR | 500 | 服务器内部错误 |
| SERVICE_UNAVAILABLE | 503 | 服务不可用 |
| SEARCH_TIMEOUT | 504 | 搜索超时 |
| INDEX_NOT_READY | 503 | 索引未就绪 |
| AI_MODEL_ERROR | 503 | AI模型错误 |
| FILE_NOT_FOUND | 404 | 文件不存在 |
| FILE_ACCESS_DENIED | 403 | 文件访问被拒绝 |
| UNSUPPORTED_FILE_TYPE | 422 | 不支持的文件类型 |
| STORAGE_FULL | 507 | 存储空间不足 |

## 接口限流

为防止系统过载，部分接口实施了限流策略：

- 搜索接口: 每分钟最多60次请求
- 文件操作接口: 每分钟最多30次请求
- AI服务接口: 每分钟最多20次请求

超限返回 `429 RATE_LIMIT_EXCEEDED` 错误。

## 版本兼容性

### API版本控制

- 当前版本: v1
- 版本格式: `/api/v{major}/`
- 向后兼容: 支持最近2个主版本
- 废弃通知: 提前3个月通知API废弃

### 版本迁移

当API版本升级时：

1. 新版本发布后，旧版本继续支持3个月
2. 废弃版本会在响应头中添加警告
3. 文档会标注各版本的差异

## 示例代码

### Python 客户端示例

```python
import requests
import base64

class XiaoYaoSearchClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def search(self, query, **kwargs):
        """执行搜索"""
        url = f"{self.base_url}/api/v1/search"
        data = {"query": {"text": query}, **kwargs}
        response = requests.post(url, json=data)
        return response.json()

    def get_file_info(self, file_id):
        """获取文件信息"""
        url = f"{self.base_url}/api/v1/files/{file_id}"
        response = requests.get(url)
        return response.json()

    def add_directory(self, directory_path):
        """添加索引目录"""
        url = f"{self.base_url}/api/v1/index/directories"
        data = {"directory_path": directory_path}
        response = requests.post(url, json=data)
        return response.json()

# 使用示例
client = XiaoYaoSearchClient()

# 搜索文件
results = client.search("重要文档", search_mode="hybrid")
print(results)

# 添加索引目录
result = client.add_directory("/path/to/documents")
print(result)
```

### JavaScript 客户端示例

```javascript
class XiaoYaoSearchClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }

    async search(query, options = {}) {
        const response = await fetch(`${this.baseUrl}/api/v1/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: { text: query },
                ...options
            })
        });
        return response.json();
    }

    async getFile(fileId) {
        const response = await fetch(`${this.baseUrl}/api/v1/files/${fileId}`);
        return response.json();
    }

    async addDirectory(directoryPath) {
        const response = await fetch(`${this.baseUrl}/api/v1/index/directories`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                directory_path: directoryPath
            })
        });
        return response.json();
    }
}

// 使用示例
const client = new XiaoYaoSearchClient();

// 搜索文件
client.search('重要文档', { search_mode: 'hybrid' })
    .then(results => console.log(results));

// 添加索引目录
client.addDirectory('/path/to/documents')
    .then(result => console.log(result));
```

这个API文档为小遥搜索提供了完整的接口规范，支持前端Electron应用与本地后端服务的高效通信，实现智能搜索、文件管理和AI服务的完整功能。