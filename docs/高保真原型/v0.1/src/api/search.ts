import api from './config'
import type {
  SearchRequest,
  SearchResponse,
  MultimodalResponse,
  SearchHistory,
  SearchResult
} from '@/types/api'

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

  // 获取搜索历史
  static async getHistory(limit = 20, offset = 0): Promise<{ success: boolean; data: { history: SearchHistory[]; total: number } }> {
    return await api.get(`/api/search/history?limit=${limit}&offset=${offset}`)
  }

  // 删除搜索历史
  static async deleteHistory(id: number): Promise<{ success: boolean; message: string }> {
    return await api.delete(`/api/search/history/${id}`)
  }

  // 清空搜索历史
  static async clearHistory(): Promise<{ success: boolean; message: string }> {
    return await api.delete('/api/search/history')
  }
}

// Mock 数据服务
export class SearchServiceMock {
  private static mockResults: SearchResult[] = [
    {
      file_id: 1,
      file_name: 'AI发展报告.pdf',
      file_path: 'D:\\Work\\Documents\\AI发展报告.pdf',
      file_type: 'document' as any,
      relevance_score: 0.92,
      preview_text: '人工智能技术在过去几年中取得了突破性进展，特别是在自然语言处理、计算机视觉和机器学习等领域...',
      highlight: '人工智能技术在过去几年中取得了<em>突破性进展</em>，特别是在自然语言处理、计算机视觉和机器学习等领域...',
      created_at: '2024-01-15T10:30:00Z',
      modified_at: '2024-01-15T10:30:00Z',
      file_size: 2048576,
      match_type: 'hybrid'
    },
    {
      file_id: 2,
      file_name: '技术会议录音.mp3',
      file_path: 'D:\\Work\\Audio\\技术会议录音.mp3',
      file_type: 'audio' as any,
      relevance_score: 0.87,
      preview_text: '今天的会议主要讨论了AI技术发展趋势，包括大语言模型、多模态AI等前沿技术...',
      highlight: '今天的会议主要讨论了<em>AI技术发展趋势</em>，包括大语言模型、多模态AI等前沿技术...',
      created_at: '2024-01-10T14:20:00Z',
      modified_at: '2024-01-10T14:20:00Z',
      file_size: 5242880,
      match_type: 'semantic'
    },
    {
      file_id: 3,
      file_name: '产品设计方案.docx',
      file_path: 'D:\\Work\\Documents\\产品设计方案.docx',
      file_type: 'document' as any,
      relevance_score: 0.78,
      preview_text: '本方案基于用户需求调研，结合AI技术创新，提出智能搜索产品的设计思路...',
      highlight: '本方案基于用户需求调研，结合<em>AI技术创新</em>，提出智能搜索产品的设计思路...',
      created_at: '2024-01-08T09:15:00Z',
      modified_at: '2024-01-08T09:15:00Z',
      file_size: 1024576,
      match_type: 'fulltext'
    }
  ]

  static async search(params: SearchRequest): Promise<SearchResponse> {
    // 模拟网络延迟
    await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 400))

    // 简单的模拟搜索逻辑
    let filteredResults = this.mockResults.filter(result =>
      result.file_name.toLowerCase().includes(params.query.toLowerCase()) ||
      result.preview_text.toLowerCase().includes(params.query.toLowerCase())
    )

    // 根据相关性排序
    filteredResults.sort((a, b) => b.relevance_score - a.relevance_score)

    // 限制结果数量
    const limitedResults = filteredResults.slice(0, params.limit || 20)

    return {
      success: true,
      data: {
        results: limitedResults,
        total: filteredResults.length,
        search_time: 0.8 + Math.random() * 0.4,
        query_used: params.query,
        input_processed: false
      }
    }
  }

  static async multimodalSearch(inputType: 'voice' | 'image', file: File): Promise<MultimodalResponse> {
    // 模拟网络延迟
    await new Promise(resolve => setTimeout(resolve, 1500 + Math.random() * 500))

    const convertedText = inputType === 'voice'
      ? '请帮我找一些关于人工智能的资料'
      : '搜索图片中的内容相关信息'

    return {
      success: true,
      data: {
        converted_text: convertedText,
        confidence: 0.85 + Math.random() * 0.1,
        search_results: this.mockResults.slice(0, 2),
        file_info: {
          filename: file.name,
          size: file.size,
          content_type: file.type
        }
      }
    }
  }

  static async getHistory(limit = 20, offset = 0): Promise<{ success: boolean; data: { history: SearchHistory[]; total: number } }> {
    await new Promise(resolve => setTimeout(resolve, 200))

    const mockHistory: SearchHistory[] = [
      {
        id: 1,
        search_query: '人工智能发展趋势',
        input_type: 'text' as any,
        search_type: 'hybrid' as any,
        ai_model_used: 'bge-m3',
        result_count: 5,
        response_time: 0.15,
        created_at: '2024-01-20T14:30:00Z'
      },
      {
        id: 2,
        search_query: '技术会议录音',
        input_type: 'voice' as any,
        search_type: 'semantic' as any,
        ai_model_used: 'faster-whisper',
        result_count: 3,
        response_time: 1.2,
        created_at: '2024-01-19T16:45:00Z'
      }
    ]

    return {
      success: true,
      data: {
        history: mockHistory.slice(offset, offset + limit),
        total: mockHistory.length
      }
    }
  }
}