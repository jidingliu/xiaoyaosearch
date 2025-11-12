import React, { useState } from 'react'
import {
  List,
  Card,
  Space,
  Tag,
  Typography,
  Divider,
  Button,
  Tooltip,
  Dropdown,
  Empty,
  Spin,
  Pagination,
  Checkbox,
  message
} from 'antd'
import {
  EyeOutlined,
  FolderOpenOutlined,
  DownloadOutlined,
  ShareAltOutlined,
  StarOutlined,
  StarFilled,
  MoreOutlined,
  CalendarOutlined,
  FileOutlined,
  FireOutlined,
  ClockCircleOutlined
} from '@ant-design/icons'

import FileIcon, { getFileTypeColor, getFileTypeLabel } from './FileIcon'
import ActionBar, { FileActions, StarActions } from './ActionBar'

const { Text, Title, Paragraph } = Typography

export interface SearchResultItem {
  id: string
  title: string
  path: string
  size: number
  modified_time: string
  file_type: string
  score: number
  summary: string
  highlights: string[]
  is_favorite?: boolean
  preview_available?: boolean
  tags?: string[]
}

export interface SearchResultsListProps {
  results: SearchResultItem[]
  loading?: boolean
  query?: string
  total?: number
  currentPage?: number
  pageSize?: number
  onPageChange?: (page: number, pageSize: number) => void
  onPreview?: (item: SearchResultItem) => void
  onOpen?: (item: SearchResultItem) => void
  onDownload?: (item: SearchResultItem) => void
  onShare?: (item: SearchResultItem) => void
  onFavoriteToggle?: (item: SearchResultItem) => void
  onSelectChange?: (selectedItems: SearchResultItem[]) => void
  showPagination?: boolean
  showSelection?: boolean
  showActions?: boolean
  className?: string
  style?: React.CSSProperties
}

const SearchResultsList: React.FC<SearchResultsListProps> = ({
  results = [],
  loading = false,
  query,
  total,
  currentPage = 1,
  pageSize = 20,
  onPageChange,
  onPreview,
  onOpen,
  onDownload,
  onShare,
  onFavoriteToggle,
  onSelectChange,
  showPagination = true,
  showSelection = false,
  showActions = true,
  className = '',
  style = {}
}) => {
  const [selectedItems, setSelectedItems] = useState<SearchResultItem[]>([])

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString)
    const now = new Date()
    const diffTime = Math.abs(now.getTime() - date.getTime())
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

    if (diffDays === 0) {
      return '今天'
    } else if (diffDays === 1) {
      return '昨天'
    } else if (diffDays < 7) {
      return `${diffDays}天前`
    } else if (diffDays < 30) {
      const weeks = Math.floor(diffDays / 7)
      return `${weeks}周前`
    } else if (diffDays < 365) {
      const months = Math.floor(diffDays / 30)
      return `${months}个月前`
    } else {
      return date.toLocaleDateString('zh-CN')
    }
  }

  const getScoreIcon = (score: number) => {
    if (score >= 0.9) {
      return <FireOutlined style={{ color: '#ff4d4f' }} title="高度匹配" />
    } else if (score >= 0.7) {
      return <StarOutlined style={{ color: '#fa8c16' }} title="高度相关" />
    } else if (score >= 0.5) {
      return <StarOutlined style={{ color: '#1890ff' }} title="相关" />
    }
    return null
  }

  const getScoreTag = (score: number) => {
    let color = 'default'
    let text = '一般'

    if (score >= 0.9) {
      color = 'red'
      text = '精确'
    } else if (score >= 0.7) {
      color = 'orange'
      text = '高度相关'
    } else if (score >= 0.5) {
      color = 'blue'
      text = '相关'
    }

    return (
      <Tag color={color} style={{ fontSize: '12px' }}>
        {text}
      </Tag>
    )
  }

  const handleItemSelect = (item: SearchResultItem, checked: boolean) => {
    let newSelectedItems: SearchResultItem[]

    if (checked) {
      newSelectedItems = [...selectedItems, item]
    } else {
      newSelectedItems = selectedItems.filter(selected => selected.id !== item.id)
    }

    setSelectedItems(newSelectedItems)

    if (onSelectChange) {
      onSelectChange(newSelectedItems)
    }
  }

  const handleSelectAll = (checked: boolean) => {
    const newSelectedItems = checked ? [...results] : []
    setSelectedItems(newSelectedItems)

    if (onSelectChange) {
      onSelectChange(newSelectedItems)
    }
  }

  const handleFavoriteToggle = (item: SearchResultItem, e: React.MouseEvent) => {
    e.stopPropagation()

    if (onFavoriteToggle) {
      onFavoriteToggle(item)
    } else {
      message.success(item.is_favorite ? '已取消收藏' : '已添加到收藏')
    }
  }

  const getActionButtons = (item: SearchResultItem) => {
    const actions = [
      FileActions.Preview(() => onPreview?.(item), !item.preview_available),
      FileActions.Open(() => onOpen?.(item)),
      FileActions.Download(() => onDownload?.(item)),
      FileActions.Share(() => onShare?.(item))
    ]

    return actions
  }

  const renderListItem = (item: SearchResultItem) => {
    const actionButtons = getActionButtons(item)

    return (
      <List.Item
        key={item.id}
        className="search-result-item"
        style={{ padding: 0, marginBottom: 16 }}
        actions={showActions ? [
          <ActionBar
            key="actions"
            actions={actionButtons}
            size="small"
          />
        ] : []}
      >
        <Card
          size="small"
          className="search-result-card"
          hoverable
          style={{ width: '100%', transition: 'all 0.2s ease' }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-2px)'
            e.currentTarget.style.boxShadow = '0 4px 16px rgba(0,0,0,0.1)'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)'
            e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
            {/* 选择框 */}
            {showSelection && (
              <div style={{ marginTop: 4 }}>
                <Checkbox
                  checked={selectedItems.some(selected => selected.id === item.id)}
                  onChange={(e) => handleItemSelect(item, e.target.checked)}
                />
              </div>
            )}

            {/* 文件图标和基本信息 */}
            <div style={{ flex: 1, minWidth: 0 }}>
              {/* 标题行 */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, flex: 1, minWidth: 0 }}>
                  <FileIcon
                    fileType={item.file_type}
                    size={20}
                  />

                  <Title
                    level={5}
                    style={{ margin: 0, flex: 1, minWidth: 0 }}
                    ellipsis={{ rows: 1, tooltip: item.title }}
                  >
                    <span
                      style={{ cursor: 'pointer' }}
                      onClick={() => onOpen?.(item)}
                    >
                      {item.title}
                    </span>
                  </Title>

                  <Tag color={getFileTypeColor(item.file_type)} style={{ fontSize: '12px', flexShrink: 0 }}>
                    {getFileTypeLabel(item.file_type)}
                  </Tag>

                  {getScoreIcon(item.score)}

                  {/* 收藏按钮 */}
                  <Button
                    type="text"
                    size="small"
                    icon={item.is_favorite ? <StarFilled style={{ color: '#faad14' }} /> : <StarOutlined />}
                    onClick={(e) => handleFavoriteToggle(item, e)}
                    style={{ flexShrink: 0 }}
                  />
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    {formatFileSize(item.size)}
                  </Text>
                  <Tooltip title={`修改时间: ${item.modified_time}`}>
                    <Text type="secondary" style={{ fontSize: '12px', display: 'flex', alignItems: 'center', gap: 4 }}>
                      <ClockCircleOutlined />
                      {formatDate(item.modified_time)}
                    </Text>
                  </Tooltip>
                  {getScoreTag(item.score)}
                </div>
              </div>

              {/* 文件摘要 */}
              <Paragraph
                ellipsis={{ rows: 2, expandable: true, symbol: '更多' }}
                style={{ marginBottom: 8, fontSize: '14px', color: '#666' }}
              >
                {item.summary}
              </Paragraph>

              {/* 关键词高亮 */}
              {item.highlights && item.highlights.length > 0 && (
                <div style={{ marginBottom: 8 }}>
                  <Text strong style={{ fontSize: '12px', color: '#666' }}>关键词：</Text>
                  {item.highlights.map((highlight, index) => (
                    <Tag
                      key={index}
                      color="orange"
                      style={{
                        margin: '2px 4px 2px 0',
                        fontSize: '12px',
                        cursor: 'pointer'
                      }}
                      onClick={() => {
                        // 点击关键词重新搜索
                        console.log('搜索关键词:', highlight)
                      }}
                    >
                      {highlight}
                    </Tag>
                  ))}
                </div>
              )}

              {/* 文件路径 */}
              <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                <FileOutlined style={{ color: '#8c8c8c', fontSize: '12px' }} />
                <Text
                  code
                  type="secondary"
                  style={{ fontSize: '12px', flex: 1 }}
                  ellipsis={{ tooltip: item.path }}
                >
                  {item.path}
                </Text>
              </div>

              {/* 标签 */}
              {item.tags && item.tags.length > 0 && (
                <div style={{ marginTop: 8 }}>
                  {item.tags.map((tag, index) => (
                    <Tag
                      key={index}
                      color="geekblue"
                      style={{
                        fontSize: '12px',
                        margin: '2px 4px 2px 0'
                      }}
                    >
                      {tag}
                    </Tag>
                  ))}
                </div>
              )}
            </div>
          </div>
        </Card>
      </List.Item>
    )
  }

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 0' }}>
        <Spin size="large" />
        <div style={{ marginTop: 16 }}>
          <Text type="secondary">正在搜索中...</Text>
        </div>
      </div>
    )
  }

  if (!query) {
    return (
      <Empty
        description="请输入搜索关键词"
        image={Empty.PRESENTED_IMAGE_SIMPLE}
        style={{ padding: '60px 0' }}
      />
    )
  }

  if (results.length === 0) {
    return (
      <Empty
        description="未找到相关文件"
        image={Empty.PRESENTED_IMAGE_SIMPLE}
        style={{ padding: '60px 0' }}
      >
        <Button type="primary" onClick={() => console.log('清空搜索')}>
          清空搜索
        </Button>
      </Empty>
    )
  }

  return (
    <div className={`search-results-list ${className}`} style={style}>
      {/* 结果统计和批量操作 */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <Text strong>
            找到 {total || results.length} 个相关文件
          </Text>

          {showSelection && (
            <Checkbox
              checked={selectedItems.length === results.length && results.length > 0}
              indeterminate={selectedItems.length > 0 && selectedItems.length < results.length}
              onChange={(e) => handleSelectAll(e.target.checked)}
            >
              全选 ({selectedItems.length})
            </Checkbox>
          )}
        </div>

        {selectedItems.length > 0 && showActions && (
          <Space>
            <Button size="small" icon={<DownloadOutlined />}>
              批量下载
            </Button>
            <Button size="small" icon={<StarOutlined />}>
              批量收藏
            </Button>
          </Space>
        )}
      </div>

      {/* 搜索结果列表 */}
      <List
        dataSource={results}
        renderItem={renderListItem}
        style={{ marginBottom: showPagination ? 24 : 0 }}
      />

      {/* 分页 */}
      {showPagination && total && total > pageSize && (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '16px 0' }}>
          <Pagination
            current={currentPage}
            total={total}
            pageSize={pageSize}
            onChange={onPageChange}
            showSizeChanger
            showQuickJumper
            showTotal={(total, range) =>
              `第 ${range[0]}-${range[1]} 项，共 ${total} 项`
            }
          />
        </div>
      )}
    </div>
  )
}

export default SearchResultsList