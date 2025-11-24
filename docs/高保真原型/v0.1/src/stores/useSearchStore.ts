import { defineStore } from 'pinia'
import { ref, computed, reactive, watch } from 'vue'
import { searchApi } from '@/api/search'
import type { SearchRequest, SearchResult, MultimodalRequest } from '@/types/api'

// 接口定义
interface SearchStats {
  total: number
  searchTime: number
  queryUsed: string
  inputProcessed: boolean
}

interface IndexStats {
  indexedFiles: number
  totalSize: number
  todaySearches: number
  lastIndexTime: Date | null
}

interface SearchSuggestion {
  text: string
  type: 'history' | 'suggestion' | 'file'
  metadata?: any
}

export const useSearchStore = defineStore('search', () => {
  // 状态定义
  const results = ref<SearchResult[]>([])
  const suggestions = ref<string[]>([])
  const isSearching = ref(false)
  const hasSearched = ref(false)
  const currentQuery = ref('')
  const currentAIEngine = ref('Ollama')
  const searchSpace = ref('所有文件夹')

  // 搜索统计
  const searchStats = reactive<SearchStats>({
    total: 0,
    searchTime: 0,
    queryUsed: '',
    inputProcessed: false
  })

  // 索引统计
  const indexStats = reactive<IndexStats>({
    indexedFiles: 0,
    totalSize: 0,
    todaySearches: 0,
    lastIndexTime: null
  })

  // 搜索配置
  const searchConfig = reactive({
    searchType: 'hybrid' as 'semantic' | 'fulltext' | 'hybrid',
    threshold: 0.7,
    limit: 20,
    fileTypes: [] as string[]
  })

  // 计算属性
  const hasResults = computed(() => results.value.length > 0)
  const resultCount = computed(() => results.value.length)
  const canLoadMore = computed(() => results.value.length < searchStats.total)

  // 搜索方法
  const search = async (request: SearchRequest) => {
    try {
      isSearching.value = true
      currentQuery.value = request.query

      // 应用搜索配置
      const searchRequest = {
        ...request,
        search_type: request.search_type || searchConfig.searchType,
        threshold: request.threshold || searchConfig.threshold,
        limit: request.limit || searchConfig.limit,
        file_types: request.file_types || searchConfig.fileTypes
      }

      console.log('发送搜索请求:', searchRequest)

      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 800))

      // 模拟搜索结果
      const mockResponse = await mockSearchResponse(searchRequest)

      if (mockResponse.success) {
        results.value = mockResponse.data.results
        Object.assign(searchStats, {
          total: mockResponse.data.total,
          searchTime: mockResponse.data.search_time,
          queryUsed: mockResponse.data.query_used,
          inputProcessed: mockResponse.data.input_processed
        })

        hasSearched.value = true
        return mockResponse
      } else {
        throw new Error(mockResponse.error?.message || '搜索失败')
      }
    } catch (error) {
      console.error('搜索错误:', error)
      throw error
    } finally {
      isSearching.value = false
    }
  }

  // 多模态搜索
  const multimodalSearch = async (inputType: 'voice' | 'image', file: File) => {
    try {
      isSearching.value = true

      console.log('多模态搜索:', inputType, file.name)

      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 1200))

      // 模拟多模态搜索结果
      const mockResponse = await mockMultimodalResponse(inputType, file)

      if (mockResponse.success) {
        results.value = mockResponse.data.search_results
        Object.assign(searchStats, {
          total: mockResponse.data.search_results.length,
          searchTime: 1.2,
          queryUsed: mockResponse.data.converted_text,
          inputProcessed: true
        })

        hasSearched.value = true
        return mockResponse
      } else {
        throw new Error(mockResponse.error?.message || '多模态搜索失败')
      }
    } catch (error) {
      console.error('多模态搜索错误:', error)
      throw error
    } finally {
      isSearching.value = false
    }
  }

  // 加载更多结果
  const loadMore = async (query: string, offset: number) => {
    try {
      const searchRequest: SearchRequest = {
        query,
        limit: 20,
        offset,
        search_type: searchConfig.searchType,
        threshold: searchConfig.threshold
      }

      const response = await search(searchRequest)
      if (response.success) {
        // 追加新结果
        results.value.push(...response.data.results)
        return response
      }
    } catch (error) {
      console.error('加载更多错误:', error)
      throw error
    }
  }

  // 获取搜索建议
  const getSuggestions = async (query: string) => {
    try {
      if (!query.trim()) {
        suggestions.value = []
        return
      }

      // 模拟搜索建议
      const mockSuggestions = await mockSearchSuggestions(query)
      suggestions.value = mockSuggestions
    } catch (error) {
      console.error('获取搜索建议错误:', error)
      suggestions.value = []
    }
  }

  // 清除搜索结果
  const clearResults = () => {
    results.value = []
    hasSearched.value = false
    currentQuery.value = ''
    Object.assign(searchStats, {
      total: 0,
      searchTime: 0,
      queryUsed: '',
      inputProcessed: false
    })
  }

  // 更新搜索配置
  const updateSearchConfig = (config: Partial<typeof searchConfig>) => {
    Object.assign(searchConfig, config)
  }

  // 初始化搜索
  const initializeSearch = async () => {
    try {
      // 加载索引统计
      await loadIndexStats()

      // 加载搜索配置
      await loadSearchConfig()

      console.log('搜索初始化完成')
    } catch (error) {
      console.error('搜索初始化失败:', error)
    }
  }

  // 加载索引统计
  const loadIndexStats = async () => {
    try {
      // 模拟索引统计
      const mockStats = await mockIndexStats()
      Object.assign(indexStats, mockStats)
    } catch (error) {
      console.error('加载索引统计失败:', error)
    }
  }

  // 加载搜索配置
  const loadSearchConfig = async () => {
    try {
      // 从本地存储加载配置
      const savedConfig = localStorage.getItem('xiaoyao-search-config')
      if (savedConfig) {
        const config = JSON.parse(savedConfig)
        updateSearchConfig(config)
      }
    } catch (error) {
      console.error('加载搜索配置失败:', error)
    }
  }

  // 保存搜索配置
  const saveSearchConfig = () => {
    try {
      localStorage.setItem('xiaoyao-search-config', JSON.stringify(searchConfig))
    } catch (error) {
      console.error('保存搜索配置失败:', error)
    }
  }

  // 模拟数据生成方法
  const mockSearchResponse = async (request: SearchRequest) => {
    // 根据查询词生成不同的模拟结果
    const mockResults: SearchResult[] = []
    const resultCount = Math.floor(Math.random() * 15) + 5

    for (let i = 0; i < Math.min(resultCount, request.limit || 20); i++) {
      mockResults.push({
        file_id: Date.now() + i,
        file_name: generateMockFileName(request.query, i),
        file_path: generateMockFilePath(request.query, i),
        file_type: generateMockFileType(i),
        relevance_score: Math.random() * 0.3 + 0.7, // 0.7-1.0
        preview_text: generateMockPreviewText(request.query),
        highlight: generateMockHighlight(request.query),
        created_at: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString(),
        modified_at: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString(),
        file_size: Math.floor(Math.random() * 10 * 1024 * 1024), // 最大10MB
        match_type: request.search_type || 'hybrid'
      })
    }

    return {
      success: true,
      data: {
        results: mockResults,
        total: resultCount,
        search_time: Math.random() * 0.5 + 0.3, // 0.3-0.8秒
        query_used: request.query,
        input_processed: false
      }
    }
  }

  const mockMultimodalResponse = async (inputType: 'voice' | 'image', file: File) => {
    const convertedText = inputType === 'voice' ? '人工智能发展趋势' : '包含AI相关内容的图片'
    const mockResults: SearchResult[] = []

    const resultCount = Math.floor(Math.random() * 10) + 3
    for (let i = 0; i < resultCount; i++) {
      mockResults.push({
        file_id: Date.now() + i,
        file_name: generateMockFileName(convertedText, i),
        file_path: generateMockFilePath(convertedText, i),
        file_type: generateMockFileType(i),
        relevance_score: Math.random() * 0.3 + 0.7,
        preview_text: generateMockPreviewText(convertedText),
        highlight: generateMockHighlight(convertedText),
        created_at: new Date().toISOString(),
        modified_at: new Date().toISOString(),
        file_size: Math.floor(Math.random() * 5 * 1024 * 1024),
        match_type: 'semantic'
      })
    }

    return {
      success: true,
      data: {
        converted_text: convertedText,
        confidence: Math.random() * 0.2 + 0.8, // 0.8-1.0
        search_results: mockResults,
        file_info: {
          filename: file.name,
          size: file.size,
          content_type: file.type
        }
      }
    }
  }

  const mockSearchSuggestions = async (query: string): Promise<string[]> => {
    const baseSuggestions = [
      '人工智能',
      '机器学习',
      '深度学习',
      '数据分析',
      '算法优化'
    ]

    return baseSuggestions.filter(s => s.includes(query))
  }

  const mockIndexStats = async () => ({
    indexedFiles: Math.floor(Math.random() * 10000) + 1000,
    totalSize: Math.floor(Math.random() * 50) + 10, // GB
    todaySearches: Math.floor(Math.random() * 100) + 10,
    lastIndexTime: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000)
  })

  // 辅助方法
  const generateMockFileName = (query: string, index: number): string => {
    const templates = [
      `${query}_研究报告_${index + 1}.pdf`,
      `${query}技术文档_v${index + 1}.docx`,
      `AI_${query}_分析_${index + 1}.xlsx`,
      `${query}项目总结_${index + 1}.md`,
      `${query}会议记录_${index + 1}.txt`
    ]
    return templates[index % templates.length]
  }

  const generateMockFilePath = (query: string, index: number): string => {
    const paths = [
      `D:\\Work\\Documents\\${query}`,
      `C:\\Users\\Documents\\AI项目\\${query}`,
      `D:\\Projects\\Research\\${query}`,
      `C:\\Downloads\\${query}`,
      `D:\\Study\\Materials\\${query}`
    ]
    return `${paths[index % paths.length]}\\${generateMockFileName(query, index)}`
  }

  const generateMockFileType = (index: number): string => {
    const types = ['document', 'document', 'document', 'spreadsheet', 'text']
    return types[index % types.length]
  }

  const generateMockPreviewText = (query: string): string => {
    const templates = [
      `这份文档详细分析了${query}的最新发展趋势，包含了大量的技术细节和实践案例...`,
      `本文档探讨了${query}在实际应用中的各种挑战和解决方案，为相关从业者提供了宝贵的参考...`,
      `${query}是当前技术领域的热点话题，本文从多个角度深入剖析了其核心技术和发展前景...`,
      `针对${query}的研究已经取得了重要进展，本文总结了最新的研究成果和未来发展方向...`,
      `${query}的应用场景越来越广泛，本文通过具体案例展示了其在不同领域的实际应用效果...`
    ]
    return templates[Math.floor(Math.random() * templates.length)]
  }

  const generateMockHighlight = (query: string): string => {
    return `关于<em>${query}</em>的详细分析显示，这一技术在未来的发展潜力巨大，值得深入研究。`
  }

  // 监听配置变化并保存
  const unwatchConfig = watch(searchConfig, saveSearchConfig, { deep: true })

  return {
    // 状态
    results,
    suggestions,
    isSearching,
    hasSearched,
    currentQuery,
    currentAIEngine,
    searchSpace,
    searchStats,
    indexStats,
    searchConfig,

    // 计算属性
    hasResults,
    resultCount,
    canLoadMore,

    // 方法
    search,
    multimodalSearch,
    loadMore,
    getSuggestions,
    clearResults,
    updateSearchConfig,
    initializeSearch,
    loadIndexStats,
    loadSearchConfig,
    saveSearchConfig
  }
})