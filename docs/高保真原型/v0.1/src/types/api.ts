// API接口类型定义

// 输入类型枚举
export type InputType = 'text' | 'voice' | 'image'

// 搜索类型枚举
export type SearchType = 'semantic' | 'fulltext' | 'hybrid'

// 文件类型枚举
export type FileType = 'video' | 'audio' | 'document' | 'image' | 'spreadsheet' | 'text' | 'other'

// 索引状态枚举
export type IndexStatus = 'pending' | 'processing' | 'completed' | 'failed' | 'paused'

// 模型提供商枚举
export type ModelProvider = 'local' | 'cloud'

// 模型类型枚举
export type ModelType = 'embedding' | 'speech' | 'vision' | 'llm'

// 搜索请求接口
export interface SearchRequest {
  query: string                    // 搜索查询词 (1-500字符)
  input_type?: InputType           // 输入类型，默认TEXT
  search_type?: SearchType         // 搜索类型，默认HYBRID
  limit?: number                   // 返回结果数量 (1-100)，默认20
  threshold?: number               // 相似度阈值 (0.0-1.0)，默认0.7
  file_types?: FileType[]          // 文件类型过滤
  offset?: number                  // 偏移量，用于分页
}

// 多模态请求接口
export interface MultimodalRequest {
  input_type: InputType            // 输入类型voice或image
  file: File                       // 上传的文件
  duration?: number                // 音频最长时长秒数 (1-120)，默认30
}

// 索引创建请求接口
export interface IndexCreateRequest {
  folder_path: string              // 索引文件夹路径
  file_types?: string[]            // 支持文件类型
  recursive?: boolean              // 是否递归搜索子文件夹
  exclude_patterns?: string[]      // 排除模式
}

// AI模型配置请求接口
export interface AIModelConfigRequest {
  model_type: ModelType            // 模型类型 embedding/speech/vision/llm
  provider: ModelProvider          // 提供商类型 local/cloud
  model_name: string               // 模型名称 (1-100字符)
  config: Record<string, any>      // 模型配置参数
  is_active?: boolean              // 是否激活
}

// 应用设置请求接口
export interface AppSettingsRequest {
  search?: {
    default_limit?: number         // 默认搜索结果数量
    default_threshold?: number     // 默认相似度阈值
    max_file_size?: number         // 最大文件大小
  }
  indexing?: {
    max_concurrent_jobs?: number   // 最大并发索引任务
    supported_formats?: string[]   // 支持的文件格式
    auto_rebuild?: boolean         // 自动重建索引
  }
  ui?: {
    theme?: 'light' | 'dark'       // 主题
    language?: string              // 语言
    animation_enabled?: boolean    // 是否启用动画
    compact_mode?: boolean         // 紧凑模式
  }
}

// 搜索结果接口
export interface SearchResult {
  file_id: number                  // 文件ID
  file_name: string                // 文件名
  file_path: string                // 文件路径
  file_type: FileType              // 文件类型
  relevance_score: number          // 相关性分数 (0.0-1.0)
  preview_text: string             // 预览文本 (最多200字符)
  highlight: string                // 高亮片段
  created_at: string               // 文件创建时间
  modified_at: string              // 文件修改时间
  file_size: number                // 文件大小(字节)
  match_type: string               // 匹配类型 semantic/fulltext/hybrid
  is_favorite?: boolean            // 是否收藏
  tags?: string[]                  // 标签
}

// 索引任务接口
export interface IndexJob {
  id: number                       // 任务ID
  folder_path: string              // 文件夹路径
  status: IndexStatus              // 任务状态
  progress: number                 // 进度百分比 (0-100)
  total_files: number              // 总文件数
  processed_files: number          // 已处理文件数
  error_count: number              // 错误文件数
  started_at: string               // 开始时间
  completed_at?: string            // 完成时间
  error_message?: string           // 错误信息
  current_file?: string            // 当前处理文件
}

// AI模型配置接口
export interface AIModelConfig {
  id: number                       // 配置ID
  model_type: ModelType            // 模型类型
  provider: ModelProvider          // 提供商
  model_name: string               // 模型名称
  config_json: string              // 配置JSON字符串
  is_active: boolean               // 是否激活
  created_at: string               // 创建时间
  updated_at: string               // 更新时间
}

// 搜索历史接口
export interface SearchHistory {
  id: number                       // 历史记录ID
  search_query: string             // 搜索查询
  input_type: InputType            // 输入类型
  search_type: SearchType          // 搜索类型
  ai_model_used: string            // 使用的AI模型
  result_count: number             // 结果数量
  response_time: number            // 响应时间(毫秒)
  created_at: string               // 创建时间
}

// 应用设置接口
export interface AppSettings {
  app_name: string                 // 应用名称
  version: string                  // 版本号
  search: {
    default_limit: number          // 默认搜索结果数量
    default_threshold: number      // 默认相似度阈值
    max_file_size: number          // 最大文件大小
  }
  indexing: {
    max_concurrent_jobs: number    // 最大并发索引任务
    supported_formats: string[]    // 支持的文件格式
    auto_rebuild: boolean          // 自动重建索引
  }
  ui: {
    theme: 'light' | 'dark'        // 主题
    language: string               // 语言
    animation_enabled: boolean     // 是否启用动画
    compact_mode: boolean          // 紧凑模式
  }
}

// 系统健康检查接口
export interface SystemHealth {
  status: 'healthy' | 'unhealthy' | 'degraded'    // 系统状态
  database: {
    status: 'connected' | 'disconnected'           // 数据库状态
    response_time: number                           // 响应时间
  }
  ai_models: Record<string, {
    status: 'loaded' | 'not_loaded' | 'error'      // 模型状态
    memory_usage?: string                           // 内存使用
    error?: string                                  // 错误信息
  }>
  indexes: Record<string, {
    status: 'ready' | 'building' | 'error'         // 索引状态
    document_count: number                          // 文档数量
  }>
  timestamp: string                 // 检查时间
}

// WebSocket消息类型
export interface WebSocketMessage {
  type: string                      // 消息类型
  data: any                        // 消息数据
  timestamp?: string               // 时间戳
}

// 索引进度更新消息
export interface IndexProgressMessage extends WebSocketMessage {
  type: 'progress_update'
  data: {
    index_id: number               // 索引ID
    status: IndexStatus            // 状态
    progress: number               // 进度
    processed_files: number        // 已处理文件数
    total_files: number            // 总文件数
    current_file?: string          // 当前文件
  }
}

// 索引完成消息
export interface IndexCompletedMessage extends WebSocketMessage {
  type: 'completed'
  data: {
    index_id: number               // 索引ID
    status: IndexStatus            // 最终状态
    progress: number               // 最终进度
    processed_files: number        // 已处理文件数
    total_files: number            // 总文件数
    error_count: number            // 错误数量
    completed_at: string           // 完成时间
  }
}

// 搜索建议消息
export interface SearchSuggestionsMessage extends WebSocketMessage {
  type: 'suggestions'
  data: {
    suggestions: string[]          // 建议列表
  }
}

// 统一响应格式
export interface ApiResponse<T = any> {
  success: boolean                 // 是否成功
  data?: T                        // 响应数据
  message?: string                 // 响应消息
  error?: {
    code: string                   // 错误码
    message: string                // 错误信息
    details?: string               // 详细信息
  }
}

// 搜索响应格式
export interface SearchResponse extends ApiResponse<{
  results: SearchResult[]           // 搜索结果
  total: number                    // 总结果数
  search_time: number              // 搜索耗时(秒)
  query_used: string               // 实际使用的查询词
  input_processed: boolean         // 是否进行了输入预处理
}> {}

// 多模态搜索响应格式
export interface MultimodalResponse extends ApiResponse<{
  converted_text: string           // 转换后的文本
  confidence: number               // 转换置信度
  search_results: SearchResult[]   // 搜索结果
  file_info: {
    filename: string               // 文件名
    size: number                   // 文件大小
    content_type: string           // 内容类型
  }
}> {}

// 分页响应格式
export interface PaginatedResponse<T = any> extends ApiResponse<{
  items: T[]                       // 数据项
  total: number                    // 总数量
  page: number                     // 当前页码
  page_size: number                // 每页大小
  total_pages: number              // 总页数
}> {}