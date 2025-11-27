// WebSocket Mock服务 - 模拟实时通信

export interface MockWebSocketMessage {
  type: string
  data: any
  timestamp?: string
}

export interface MockWebSocketCallbacks {
  onOpen?: () => void
  onMessage?: (message: MockWebSocketMessage) => void
  onClose?: () => void
  onError?: (error: Error) => void
}

export class WebSocketMock {
  private url: string
  private callbacks: MockWebSocketCallbacks = {}
  private isConnected: boolean = false
  private messageQueue: MockWebSocketMessage[] = []
  private intervals: NodeJS.Timeout[] = []
  private reconnectAttempts: number = 0
  private maxReconnectAttempts: number = 5

  constructor(url: string) {
    this.url = url
  }

  connect(callbacks?: MockWebSocketCallbacks) {
    if (callbacks) {
      this.callbacks = callbacks
    }

    // 模拟连接延迟
    setTimeout(() => {
      this.isConnected = true
      this.callbacks.onOpen?.()

      // 处理消息队列
      this.processMessageQueue()

      // 根据URL类型启动相应的Mock功能
      if (this.url.includes('/index/')) {
        this.startIndexProgressMock()
      } else if (this.url.includes('/search-suggest')) {
        this.startSearchSuggestMock()
      }
    }, 100 + Math.random() * 200)
  }

  disconnect() {
    this.isConnected = false
    this.clearIntervals()
    this.callbacks.onClose?.()
  }

  send(data: any) {
    if (!this.isConnected) {
      return false
    }

    try {
      const message = typeof data === 'string' ? JSON.parse(data) : data

      // 处理搜索建议请求
      if (this.url.includes('/search-suggest') && message.type === 'search_suggest') {
        this.handleSearchSuggestRequest(message.data)
      }

      return true
    } catch (error) {
      console.error('WebSocket send error:', error)
      return false
    }
  }

  onMessage(callback: (message: MockWebSocketMessage) => void) {
    this.callbacks.onMessage = callback
  }

  private processMessageQueue() {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift()
      this.callbacks.onMessage?.(message!)
    }
  }

  private queueMessage(message: MockWebSocketMessage) {
    if (this.isConnected && this.callbacks.onMessage) {
      this.callbacks.onMessage(message)
    } else {
      this.messageQueue.push(message)
    }
  }

  private clearIntervals() {
    this.intervals.forEach(interval => clearInterval(interval))
    this.intervals = []
  }

  // 索引进度Mock功能
  private startIndexProgressMock() {
    // 模拟定期发送进度更新
    const progressInterval = setInterval(() => {
      if (!this.isConnected) return

      // 从URL中提取索引ID
      const indexId = this.extractIndexIdFromUrl()
      if (!indexId) return

      // 模拟进度数据
      const progress = Math.floor(Math.random() * 20) + 60 // 60-80%的进度
      const processedFiles = Math.floor((progress / 100) * 200)
      const totalFiles = 200

      this.queueMessage({
        type: 'progress_update',
        data: {
          index_id: indexId,
          status: 'processing',
          progress: progress,
          processed_files: processedFiles,
          total_files: totalFiles,
          current_file: `document_${processedFiles}.pdf`,
          speed: Math.floor(Math.random() * 10) + 5 // 5-15 files/sec
        },
        timestamp: new Date().toISOString()
      })

      // 随机模拟完成
      if (Math.random() < 0.05) { // 5%概率完成
        this.queueMessage({
          type: 'completed',
          data: {
            index_id: indexId,
            status: 'completed',
            progress: 100,
            processed_files: totalFiles - Math.floor(Math.random() * 5),
            total_files: totalFiles,
            error_count: Math.floor(Math.random() * 3),
            completed_at: new Date().toISOString()
          },
          timestamp: new Date().toISOString()
        })

        // 索引完成后停止发送进度更新
        clearInterval(progressInterval)
      }
    }, 2000) // 每2秒发送一次进度更新

    this.intervals.push(progressInterval)

    // 模拟错误情况
    if (Math.random() < 0.1) { // 10%概率出现错误
      setTimeout(() => {
        if (!this.isConnected) return

        this.queueMessage({
          type: 'error',
          data: {
            index_id: indexId,
            status: 'failed',
            error_type: 'file_access_error',
            error_message: '无法访问部分文件，权限不足',
            failed_file: 'restricted_document.pdf',
            progress: Math.floor(Math.random() * 40) + 10
          },
          timestamp: new Date().toISOString()
        })
      }, 5000 + Math.random() * 5000)
    }
  }

  // 搜索建议Mock功能
  private startSearchSuggestMock() {
    // 搜索建议不需要定期推送，只响应客户端请求
    // 但可以模拟一些系统状态更新
    const statusInterval = setInterval(() => {
      if (!this.isConnected) return

      // 偶尔发送系统状态
      if (Math.random() < 0.2) { // 20%概率发送状态
        this.queueMessage({
          type: 'status',
          data: {
            service_status: 'healthy',
            active_connections: Math.floor(Math.random() * 10) + 1,
            requests_per_second: Math.floor(Math.random() * 50) + 10,
            cache_hit_rate: Math.floor(Math.random() * 30) + 70 // 70-100%
          },
          timestamp: new Date().toISOString()
        })
      }
    }, 10000) // 每10秒检查一次

    this.intervals.push(statusInterval)
  }

  private handleSearchSuggestRequest(requestData: { query: string; limit: number }) {
    // 模拟搜索建议生成
    setTimeout(() => {
      if (!this.isConnected) return

      const { query, limit = 5 } = requestData
      let suggestions: string[] = []

      if (query.trim()) {
        // 基于查询词生成相关建议
        const baseSuggestions = [
          `${query} 教程`,
          `${query} 最佳实践`,
          `${query} 应用案例`,
          `${query} 开发指南`,
          `${query} 解决方案`
        ]

        suggestions = baseSuggestions.slice(0, limit)
      } else {
        // 热门搜索建议
        suggestions = [
          '人工智能',
          '机器学习',
          '深度学习',
          'Python编程',
          '数据分析'
        ].slice(0, limit)
      }

      this.queueMessage({
        type: 'suggestions',
        data: {
          suggestions: suggestions,
          query: query,
          total: suggestions.length,
          processing_time: (Math.random() * 100 + 50).toFixed(0) // 50-150ms
        },
        timestamp: new Date().toISOString()
      })
    }, 50 + Math.random() * 150) // 50-200ms延迟
  }

  private extractIndexIdFromUrl(): number | null {
    const match = this.url.match(/\/index\/(\d+)/)
    return match ? parseInt(match[1]) : null
  }

  // 模拟重连机制
  reconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      this.callbacks.onError?.(new Error('Max reconnect attempts exceeded'))
      return
    }

    this.reconnectAttempts++
    const delay = Math.pow(2, this.reconnectAttempts) * 1000 // 指数退避

    setTimeout(() => {
      console.log(`WebSocket attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      this.connect()
    }, delay)
  }

  // 模拟网络抖动
  simulateNetworkIssue() {
    if (!this.isConnected) return

    setTimeout(() => {
      this.isConnected = false
      this.callbacks.onError?.(new Error('Network connection lost'))

      // 尝试重连
      setTimeout(() => {
        this.reconnect()
      }, 1000)
    }, Math.random() * 10000 + 5000) // 5-15秒后出现网络问题
  }
}

// WebSocket连接管理器
export class WebSocketManager {
  private static connections: Map<string, WebSocketMock> = new Map()

  static createConnection(url: string, callbacks?: MockWebSocketCallbacks): WebSocketMock {
    const existingConnection = this.connections.get(url)

    if (existingConnection) {
      existingConnection.disconnect()
    }

    const ws = new WebSocketMock(url)
    this.connections.set(url, ws)

    ws.connect(callbacks)

    return ws
  }

  static getConnection(url: string): WebSocketMock | undefined {
    return this.connections.get(url)
  }

  static closeConnection(url: string): boolean {
    const ws = this.connections.get(url)
    if (ws) {
      ws.disconnect()
      this.connections.delete(url)
      return true
    }
    return false
  }

  static closeAllConnections(): void {
    this.connections.forEach((ws, url) => {
      ws.disconnect()
    })
    this.connections.clear()
  }
}

// 便捷函数
export function createIndexWebSocket(indexId: number, callbacks?: MockWebSocketCallbacks): WebSocketMock {
  const url = `ws://127.0.0.1:8000/ws/index/${indexId}`
  return WebSocketManager.createConnection(url, callbacks)
}

export function createSearchSuggestWebSocket(callbacks?: MockWebSocketCallbacks): WebSocketMock {
  const url = 'ws://127.0.0.1:8000/ws/search-suggest'
  return WebSocketManager.createConnection(url, callbacks)
}