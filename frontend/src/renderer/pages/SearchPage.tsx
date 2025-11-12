import React, { useState } from 'react'
import {
  Card,
  Typography,
  message
} from 'antd'

import SearchInput from '@/renderer/components/Common/SearchInput'
import SearchResultsList, { SearchResultItem } from '@/renderer/components/Common/SearchResultsList'

const { Title } = Typography

const SearchPage: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<SearchResultItem[]>([])

  const handleSearch = async (value: string, options?: any) => {
    if (!value.trim()) return

    setLoading(true)
    setSearchQuery(value)

    try {
      // 模拟搜索API调用
      await new Promise(resolve => setTimeout(resolve, 1000))

      // 模拟搜索结果
      const mockResults: SearchResultItem[] = [
        {
          id: '1',
          title: '产品设计方案.docx',
          path: '/Users/用户/Documents/产品设计方案.docx',
          size: 2048576,
          modified_time: '2024-11-08',
          file_type: 'docx',
          score: 0.95,
          summary: '这是一个关于产品设计方案的文档，包含了产品的功能设计、界面设计和用户体验设计...',
          highlights: ['产品设计', '用户体验'],
          preview_available: true,
          tags: ['设计', '产品', 'UI/UX']
        },
        {
          id: '2',
          title: '技术规格说明书.pdf',
          path: '/Users/用户/Documents/技术规格说明书.pdf',
          size: 3145728,
          modified_time: '2024-11-05',
          file_type: 'pdf',
          score: 0.87,
          summary: '详细的技术规格说明文档，包括系统架构、技术选型和实现细节...',
          highlights: ['技术规格', '系统架构'],
          preview_available: true,
          tags: ['技术', '架构', '文档']
        },
        {
          id: '3',
          'title': '市场分析报告.xlsx',
          'path': '/Users/用户/Downloads/市场分析报告.xlsx',
          'size': 1572864,
          'modified_time': '2024-11-10',
          'file_type': 'xlsx',
          'score': 0.82,
          'summary': '包含市场调研数据、竞品分析和未来市场趋势预测的详细报告...',
          'highlights': ['市场分析', '竞品分析'],
          'preview_available': false,
          'tags': ['市场', '分析', '数据']
        }
      ]

      setSearchResults(mockResults)
    } catch (error) {
      console.error('搜索失败:', error)
      message.error('搜索失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  const handlePreview = (item: SearchResultItem) => {
    message.info(`预览文件: ${item.title}`)
  }

  const handleOpen = (item: SearchResultItem) => {
    message.info(`打开文件: ${item.title}`)
  }

  const handleDownload = (item: SearchResultItem) => {
    message.info(`下载文件: ${item.title}`)
  }

  const handleShare = (item: SearchResultItem) => {
    message.info(`分享文件: ${item.title}`)
  }

  const handleFavoriteToggle = (item: SearchResultItem) => {
    const updatedResults = searchResults.map(result =>
      result.id === item.id
        ? { ...result, is_favorite: !result.is_favorite }
        : result
    )
    setSearchResults(updatedResults)
    message.success(item.is_favorite ? '已取消收藏' : '已添加到收藏')
  }

  return (
    <div className="search-page" style={{ maxWidth: '1200px', margin: '0 auto' }}>
      {/* 搜索区域 */}
      <Card style={{ marginBottom: 24 }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <Title level={2}>
            智能文件搜索
          </Title>
        </div>

        <SearchInput
          placeholder="输入搜索关键词，支持语义搜索..."
          loading={loading}
          onSearch={handleSearch}
          suggestions={[]}
          showVoiceInput={true}
          showAdvancedOptions={true}
          size="large"
        />
      </Card>

      {/* 搜索结果区域 */}
      <SearchResultsList
        results={searchResults}
        loading={loading}
        query={searchQuery}
        onPreview={handlePreview}
        onOpen={handleOpen}
        onDownload={handleDownload}
        onShare={handleShare}
        onFavoriteToggle={handleFavoriteToggle}
        showPagination={true}
        showSelection={true}
        showActions={true}
      />
    </div>
  )
}

export default SearchPage