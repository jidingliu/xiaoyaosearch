import React, { useState } from 'react'
import {
  Input,
  Card,
  List,
  Typography,
  Tag,
  Space,
  Divider,
  Empty,
  Spin
} from 'antd'
import {
  SearchOutlined,
  FileTextOutlined,
  ClockCircleOutlined,
  EyeOutlined
} from '@ant-design/icons'

const { Search } = Input
const { Title, Text, Paragraph } = Typography

const SearchPage: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<any[]>([])

  const handleSearch = async (value: string) => {
    if (!value.trim()) return

    setLoading(true)
    setSearchQuery(value)

    try {
      // 模拟搜索API调用
      await new Promise(resolve => setTimeout(resolve, 1000))

      // 模拟搜索结果
      const mockResults = [
        {
          id: '1',
          title: '产品设计方案.docx',
          path: '/Users/用户/Documents/产品设计方案.docx',
          size: 2048576,
          modified_time: '2024-11-08',
          file_type: 'docx',
          score: 0.95,
          summary: '这是一个关于产品设计方案的文档，包含了产品的功能设计、界面设计和用户体验设计...',
          highlights: ['产品设计', '用户体验']
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
          highlights: ['技术规格', '系统架构']
        }
      ]

      setSearchResults(mockResults)
    } catch (error) {
      console.error('搜索失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileIcon = (fileType: string) => {
    const iconMap: Record<string, React.ReactNode> = {
      'pdf': <FileTextOutlined style={{ color: '#ff4d4f' }} />,
      'docx': <FileTextOutlined style={{ color: '#1890ff' }} />,
      'xlsx': <FileTextOutlined style={{ color: '#52c41a' }} />,
      'pptx': <FileTextOutlined style={{ color: '#fa8c16' }} />,
      'txt': <FileTextOutlined style={{ color: '#722ed1' }} />,
      'md': <FileTextOutlined style={{ color: '#13c2c2' }} />
    }
    return iconMap[fileType] || <FileTextOutlined />
  }

  return (
    <div className="search-page">
      {/* 搜索区域 */}
      <Card className="search-card" style={{ marginBottom: 24 }}>
        <div className="search-container">
          <Title level={2} style={{ textAlign: 'center', marginBottom: 32 }}>
            智能文件搜索
          </Title>

          <Search
            placeholder="输入搜索关键词，支持语义搜索..."
            allowClear
            enterButton={
              <Button type="primary" icon={<SearchOutlined />}>
                搜索
              </Button>
            }
            size="large"
            onSearch={handleSearch}
            loading={loading}
            style={{ marginBottom: 16 }}
          />

          <div className="search-tips">
            <Text type="secondary">
              💡 提示：您可以使用自然语言搜索，如"上周的产品设计PPT"、"关于AI的技术文档"等
            </Text>
          </div>
        </div>
      </Card>

      {/* 搜索结果区域 */}
      <Card
        className="results-card"
        title={
          searchQuery ? (
            <Space>
              <span>搜索结果</span>
              <Text type="secondary">({searchResults.length}个文件)</Text>
            </Space>
          ) : (
            '搜索结果'
          )
        }
      >
        {loading ? (
          <div className="loading-container">
            <Spin size="large" />
            <Text style={{ marginLeft: 16 }}>正在搜索中...</Text>
          </div>
        ) : searchResults.length > 0 ? (
          <List
            dataSource={searchResults}
            renderItem={(item) => (
              <List.Item
                key={item.id}
                className="search-result-item"
                style={{ padding: '16px 0' }}
              >
                <Card
                  size="small"
                  className="search-result-card"
                  hoverable
                  style={{ width: '100%' }}
                  actions={[
                    <EyeOutlined key="preview" title="预览" />,
                    <span key="more">...</span>
                  ]}
                >
                  <div className="result-header">
                    <Space>
                      {getFileIcon(item.file_type)}
                      <Title level={5} style={{ margin: 0 }}>
                        {item.title}
                      </Title>
                      <Tag color="blue">{item.file_type.toUpperCase()}</Tag>
                    </Space>

                    <Space>
                      <Text type="secondary">
                        {formatFileSize(item.size)}
                      </Text>
                      <Text type="secondary">
                        <ClockCircleOutlined /> {item.modified_time}
                      </Text>
                    </Space>
                  </div>

                  <Divider style={{ margin: '12px 0' }} />

                  <div className="result-content">
                    <Paragraph
                      ellipsis={{ rows: 2, expandable: true }}
                      style={{ marginBottom: 8 }}
                    >
                      {item.summary}
                    </Paragraph>

                    {item.highlights.length > 0 && (
                      <div className="result-highlights">
                        <Text strong>关键词：</Text>
                        {item.highlights.map((highlight: string, index: number) => (
                          <Tag key={index} color="orange" style={{ margin: '2px 4px 2px 0' }}>
                            {highlight}
                          </Tag>
                        ))}
                      </div>
                    )}

                    <div className="result-path">
                      <Text type="secondary" code>
                        {item.path}
                      </Text>
                    </div>
                  </div>
                </Card>
              </List.Item>
            )}
          />
        ) : searchQuery ? (
          <Empty
            description="未找到相关文件"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        ) : (
          <Empty
            description="请输入搜索关键词"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        )}
      </Card>

      <style jsx>{`
        .search-page {
          max-width: 1200px;
          margin: 0 auto;
        }

        .search-card {
          text-align: center;
        }

        .search-container {
          max-width: 800px;
          margin: 0 auto;
        }

        .search-tips {
          margin-top: 16px;
          text-align: left;
        }

        .loading-container {
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 60px 0;
        }

        .search-result-item {
          padding: 0 !important;
        }

        .search-result-card {
          transition: all 0.2s ease;
        }

        .search-result-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }

        .result-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
        }

        .result-highlights {
          margin-top: 8px;
        }

        .result-path {
          margin-top: 8px;
        }
      `}</style>
    </div>
  )
}

export default SearchPage