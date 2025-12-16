// 搜索API服务

import type {
  SearchRequest,
  SearchResponse,
  MultimodalResponse,
  SearchHistory,
  SearchResult
} from '@/types/api'
import { InputType, FileType, SearchType } from '@/types/api'
import { httpClient } from '@/utils/http'

// 搜索服务
export class SearchService {
  // 文本搜索
  static async search(params: SearchRequest): Promise<SearchResponse> {
    return await httpClient.post<SearchResponse>('/api/search', params)
  }

  // 多模态搜索
  static async multimodalSearch(
    inputType: InputType.VOICE | InputType.IMAGE,
    file: File,
    searchType: SearchType = SearchType.HYBRID,
    limit: number = 100,
    threshold: number = 0.5,
    fileTypes?: FileType[]
  ): Promise<MultimodalResponse> {
    const formData = new FormData()
    formData.append('file', file)  // 后端期望的文件字段名是 'file'
    formData.append('input_type', inputType)
    formData.append('search_type', searchType)
    formData.append('limit', limit.toString())
    formData.append('threshold', threshold.toString())

    if (fileTypes && fileTypes.length > 0) {
      fileTypes.forEach(fileType => {
        formData.append('file_types', fileType)
      })
    }

    return await httpClient.postFormData<MultimodalResponse>('/api/search/multimodal', formData)
  }

  // 获取搜索历史
  static async getHistory(limit = 100, offset = 0): Promise<{ success: boolean; data: { history: SearchHistory[]; total: number } }> {
    return await httpClient.get<{ success: boolean; data: { history: SearchHistory[]; total: number } }>(`/api/search/history?limit=${limit}&offset=${offset}`)
  }

  // 删除搜索历史
  static async deleteHistory(id: number): Promise<{ success: boolean; message: string }> {
    return await httpClient.delete<{ success: boolean; message: string }>(`/api/search/history/${id}`)
  }

  // 清空搜索历史
  static async clearHistory(): Promise<{ success: boolean; message: string }> {
    return await httpClient.delete<{ success: boolean; message: string }>('/api/search/history')
  }

  // 搜索建议
  static async getSuggestions(query: string, limit = 5): Promise<{ success: boolean; data: { suggestions: string[]; query: string; total: number } }> {
    return await httpClient.get<{ success: boolean; data: { suggestions: string[]; query: string; total: number } }>(`/api/search/suggestions?query=${encodeURIComponent(query)}&limit=${limit}`)
  }
}