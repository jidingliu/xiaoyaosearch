// API响应类型
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

// 搜索相关类型
export interface SearchRequest {
  query: string
  type?: string
  start_date?: string
  end_date?: string
  size?: number
  page?: number
}

export interface SearchResult {
  id: string
  title: string
  path: string
  size: number
  modified_time: string
  file_type: string
  score: number
  summary: string
  highlights: string[]
}

export interface SearchResponse {
  query: string
  total: number
  results: SearchResult[]
  search_time: number
  suggestions: string[]
}

// 文件类型
export interface FileInfo {
  id: string
  name: string
  path: string
  size: number
  type: string
  modified_time: string
  indexed: boolean
}

// 用户设置类型
export interface UserSettings {
  // 搜索设置
  search_mode: 'semantic' | 'keyword' | 'hybrid'
  results_per_page: number
  auto_suggestions: boolean
  search_history_enabled: boolean

  // 索引设置
  indexed_file_types: string[]
  max_file_size: number
  index_update_frequency: 'realtime' | 'hourly' | 'daily' | 'manual'
  excluded_directories: string[]

  // AI设置
  ai_mode: 'local' | 'cloud' | 'hybrid'
  local_models: Record<string, string>
  cloud_api_config: Record<string, string>
  gpu_acceleration: boolean

  // 界面设置
  theme: 'light' | 'dark' | 'auto'
  language: 'zh-CN' | 'en-US'
  font_size: number

  // 性能设置
  max_memory_usage: number
  max_concurrent_tasks: number
  cache_size: number
}

// 目录管理类型
export interface DirectoryInfo {
  id: string
  path: string
  status: 'active' | 'inactive' | 'error'
  file_count: number
  indexed_count: number
  last_scan_time: string
  created_at: string
}

// 索引状态类型
export interface IndexStatus {
  total_files: number
  indexed_files: number
  status: 'idle' | 'indexing' | 'error'
  current_file?: string
  progress: number
  last_update: string
}

// 收藏类型
export interface FavoriteItem {
  id: string
  file_path: string
  title: string
  description?: string
  category?: string
  tags: string[]
  created_at: string
  accessed_at: string
}

// 统计类型
export interface UserStatistics {
  total_files_indexed: number
  total_searches: number
  total_file_size: number
  favorite_count: number
  last_active_date: string
  avg_search_time: number
  top_search_terms: string[]
  file_type_distribution: Record<string, number>
}

// Electron API 类型
export interface ElectronAPI {
  app: {
    getVersion: () => Promise<string>
    quit: () => Promise<void>
    minimize: () => Promise<void>
    maximize: () => Promise<void>
  }
  window: {
    close: () => Promise<void>
  }
  store: {
    get: (key: string) => Promise<any>
    set: (key: string, value: any) => Promise<void>
    delete: (key: string) => Promise<void>
  }
  dialog: {
    showOpenDialog: (options: any) => Promise<any>
    showSaveDialog: (options: any) => Promise<any>
  }
  on: (channel: string, callback: Function) => void
  off: (channel: string, callback: Function) => void
}

// 扩展Window接口
declare global {
  interface Window {
    electronAPI: ElectronAPI
  }
}

// 应用状态类型
export interface AppState {
  isLoading: boolean
  error: string | null
  user: {
    id: string
    username: string
  } | null
  settings: UserSettings
  search: {
    query: string
    results: SearchResult[]
    loading: boolean
    total: number
  }
  index: {
    status: IndexStatus
    directories: DirectoryInfo[]
  }
}

// 组件Props类型
export interface BaseComponentProps {
  className?: string
  children?: React.ReactNode
}

// 表单类型
export interface FormFieldProps {
  name: string
  label: string
  required?: boolean
  disabled?: boolean
}

// 模态框类型
export interface ModalProps {
  visible: boolean
  title: string
  onOk: () => void
  onCancel: () => void
  okText?: string
  cancelText?: string
  width?: number
}