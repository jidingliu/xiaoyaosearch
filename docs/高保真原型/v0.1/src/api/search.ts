import axios from 'axios'
import type {
  SearchRequest,
  SearchResponse,
  MultimodalResponse,
  SearchHistory,
  ApiResponse
} from '@/types/api'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// 搜索服务类
export class SearchService {
  // 文本搜索
  static async search(params: SearchRequest): Promise<SearchResponse> {
    return await api.post('/api/search', params)
  }

  // 多模态搜索
  static async multimodalSearch(inputType: 'voice' | 'image', file: File): Promise<MultimodalResponse> {
    const formData = new FormData()
    formData.append('input_type', inputType)
    formData.append('file', file)

    return await api.post('/api/search/multimodal', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }

  // 搜索历史
  static async getHistory(limit = 20, offset = 0): Promise<ApiResponse<{
    history: SearchHistory[]
    total: number
  }>> {
    return await api.get(`/api/search/history?limit=${limit}&offset=${offset}`)
  }

  // 清除搜索历史
  static async clearHistory(): Promise<ApiResponse> {
    return await api.delete('/api/search/history')
  }

  // 搜索建议
  static async getSuggestions(query: string, limit = 5): Promise<ApiResponse<{
    suggestions: string[]
  }>> {
    return await api.get(`/api/search/suggestions?q=${encodeURIComponent(query)}&limit=${limit}`)
  }
}

// 导出默认实例
export const searchApi = SearchService

// WebSocket连接管理
export class WebSocketManager {
  private static instance: WebSocketManager
  private connections: Map<string, WebSocket> = new Map()

  static getInstance(): WebSocketManager {
    if (!WebSocketManager.instance) {
      WebSocketManager.instance = new WebSocketManager()
    }
    return WebSocketManager.instance
  }

  // 连接WebSocket
  connect(url: string, onMessage?: (data: any) => void): WebSocket {
    if (this.connections.has(url)) {
      const existingWs = this.connections.get(url)!
      if (existingWs.readyState === WebSocket.OPEN) {
        return existingWs
      } else {
        this.connections.delete(url)
      }
    }

    const ws = new WebSocket(url)

    ws.onopen = () => {
      console.log('WebSocket连接已建立:', url)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        onMessage?.(data)
      } catch (error) {
        console.error('解析WebSocket消息失败:', error)
      }
    }

    ws.onclose = () => {
      console.log('WebSocket连接已关闭:', url)
      this.connections.delete(url)
    }

    ws.onerror = (error) => {
      console.error('WebSocket错误:', error)
    }

    this.connections.set(url, ws)
    return ws
  }

  // 断开连接
  disconnect(url: string): void {
    const ws = this.connections.get(url)
    if (ws) {
      ws.close()
      this.connections.delete(url)
    }
  }

  // 发送消息
  send(url: string, data: any): void {
    const ws = this.connections.get(url)
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(data))
    } else {
      console.warn('WebSocket未连接:', url)
    }
  }

  // 断开所有连接
  disconnectAll(): void {
    this.connections.forEach((ws, url) => {
      this.disconnect(url)
    })
  }
}

// 导出WebSocket管理器实例
export const wsManager = WebSocketManager.getInstance()