/**
 * API服务 - 与后端通信
 */

import axios, { AxiosInstance, AxiosResponse } from 'axios'

// API响应接口
interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

// API客户端类
class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: 'http://localhost:8000/api/v1',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // 请求拦截器
    this.client.interceptors.request.use(
      (config) => {
        // 可以在这里添加认证token等
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // 响应拦截器
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        return response
      },
      (error) => {
        console.error('API Error:', error)
        return Promise.reject(error)
      }
    )
  }

  // 通用请求方法
  private async request<T>(method: string, url: string, data?: any): Promise<T> {
    try {
      const response = await this.client.request({
        method,
        url,
        data,
      })
      return response.data
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // GET请求
  async get<T>(url: string): Promise<T> {
    return this.request<T>('GET', url)
  }

  // POST请求
  async post<T>(url: string, data?: any): Promise<T> {
    return this.request<T>('POST', url, data)
  }

  // PUT请求
  async put<T>(url: string, data?: any): Promise<T> {
    return this.request<T>('PUT', url, data)
  }

  // DELETE请求
  async delete<T>(url: string): Promise<T> {
    return this.request<T>('DELETE', url)
  }
}

// 创建API客户端实例
const apiClient = new ApiClient()

// 搜索API
export const searchApi = {
  // 搜索文件
  search: (params: {
    q: string
    type?: string
    start_date?: string
    end_date?: string
    size?: number
    page?: number
  }) => apiClient.get('/search', { params }),

  // 理解查询
  understandQuery: (query: string) => apiClient.post('/search/understand', { query }),

  // 获取搜索建议
  getSuggestions: (q: string, limit?: number) =>
    apiClient.get('/search/suggestions', { params: { q, limit } }),
}

// 文件API
export const fileApi = {
  // 获取文件列表
  list: (params?: {
    directory_id?: string
    type?: string
    indexed_only?: boolean
    page?: number
    size?: number
  }) => apiClient.get('/files', { params }),

  // 获取文件信息
  get: (fileId: string) => apiClient.get(`/files/${fileId}`),

  // 预览文件
  preview: (fileId: string, highlights?: string) =>
    apiClient.get(`/files/${fileId}/preview`, { params: { highlights } }),

  // 打开文件
  open: (fileId: string) => apiClient.post(`/files/${fileId}/open`),

  // 删除文件
  delete: (fileId: string) => apiClient.delete(`/files/${fileId}`),

  // 上传文件
  upload: (file: File, directoryId?: string) => {
    const formData = new FormData()
    formData.append('file', file)
    if (directoryId) {
      formData.append('directory_id', directoryId)
    }
    return apiClient.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
}

// 目录API
export const directoryApi = {
  // 获取目录列表
  list: () => apiClient.get('/directories'),

  // 添加目录
  add: (data: { path: string; name?: string }) => apiClient.post('/directories', data),

  // 获取目录信息
  get: (directoryId: string) => apiClient.get(`/directories/${directoryId}`),

  // 扫描目录
  scan: (directoryId: string, fullScan?: boolean) =>
    apiClient.post(`/directories/${directoryId}/scan`, null, {
      params: { full_scan: fullScan },
    }),

  // 移除目录
  remove: (directoryId: string, removeFiles?: boolean) =>
    apiClient.delete(`/directories/${directoryId}`, {
      params: { remove_files: removeFiles },
    }),

  // 获取扫描状态
  getScanStatus: (directoryId: string) => apiClient.get(`/directories/${directoryId}/status`),
}

// 用户API
export const userApi = {
  // 获取当前用户
  getCurrent: () => apiClient.get('/users/current'),

  // 创建用户
  create: () => apiClient.post('/users'),
}

// 设置API
export const settingsApi = {
  // 获取设置
  get: () => apiClient.get('/settings'),

  // 更新设置
  update: (settings: Record<string, any>) => apiClient.put('/settings', settings),

  // 重置设置
  reset: () => apiClient.post('/settings/reset'),

  // 导出设置
  export: () => apiClient.post('/settings/export'),

  // 导入设置
  import: (settings: Record<string, any>) => apiClient.post('/settings/import', settings),
}

export default apiClient