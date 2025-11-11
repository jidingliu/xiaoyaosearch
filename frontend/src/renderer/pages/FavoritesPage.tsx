import React, { useState } from 'react'
import {
  Card,
  Typography,
  Empty,
  Tag,
  Space,
  Button,
  Tooltip
} from 'antd'
import {
  StarOutlined,
  StarFilled,
  FileTextOutlined,
  ClockCircleOutlined,
  DeleteOutlined
} from '@ant-design/icons'

const { Title, Text, Paragraph } = Typography

interface FavoriteItem {
  id: string
  file_path: string
  title: string
  description?: string
  category?: string
  tags: string[]
  created_at: string
  accessed_at: string
}

const FavoritesPage: React.FC = () => {
  const [favorites, setFavorites] = useState<FavoriteItem[]>([
    {
      id: '1',
      file_path: '/Users/用户/Documents/重要文档.pdf',
      title: '重要文档.pdf',
      description: '包含项目相关的重要信息和规格说明',
      category: '工作文档',
      tags: ['重要', '项目', '规格'],
      created_at: '2024-11-01',
      accessed_at: '2024-11-08'
    },
    {
      id: '2',
      file_path: '/Users/用户/Desktop/学习笔记.md',
      title: '学习笔记.md',
      description: '机器学习和深度学习的学习笔记',
      category: '学习资料',
      tags: ['机器学习', '深度学习', '笔记'],
      created_at: '2024-10-15',
      accessed_at: '2024-11-07'
    }
  ])

  const getFileIcon = (filePath: string) => {
    const ext = filePath.split('.').pop()?.toLowerCase()
    const iconMap: Record<string, React.ReactNode> = {
      'pdf': <FileTextOutlined style={{ color: '#ff4d4f' }} />,
      'docx': <FileTextOutlined style={{ color: '#1890ff' }} />,
      'xlsx': <FileTextOutlined style={{ color: '#52c41a' }} />,
      'md': <FileTextOutlined style={{ color: '#722ed1' }} />
    }
    return iconMap[ext || ''] || <FileTextOutlined />
  }

  const handleRemoveFavorite = (id: string) => {
    setFavorites(favorites.filter(fav => fav.id !== id))
  }

  const handleToggleFavorite = (item: FavoriteItem) => {
    // 这里切换收藏状态
    console.log('Toggle favorite:', item)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-CN')
  }

  return (
    <div className="favorites-page">
      <div className="page-header">
        <Title level={2}>我的收藏</Title>
        <Text type="secondary">
          共 {favorites.length} 个收藏文件
        </Text>
      </div>

      {favorites.length > 0 ? (
        <div className="favorites-list">
          {favorites.map((item) => (
            <Card
              key={item.id}
              className="favorite-item"
              hoverable
              actions={[
                <Tooltip title="取消收藏" key="unfavorite">
                  <Button
                    type="text"
                    icon={<StarFilled style={{ color: '#faad14' }} />}
                    onClick={() => handleToggleFavorite(item)}
                  />
                </Tooltip>,
                <Tooltip title="删除" key="delete">
                  <Button
                    type="text"
                    danger
                    icon={<DeleteOutlined />}
                    onClick={() => handleRemoveFavorite(item.id)}
                  />
                </Tooltip>
              ]}
            >
              <div className="favorite-content">
                <div className="favorite-header">
                  <Space>
                    {getFileIcon(item.file_path)}
                    <Title level={5} style={{ margin: 0 }}>
                      {item.title}
                    </Title>
                  </Space>

                  {item.category && (
                    <Tag color="blue">{item.category}</Tag>
                  )}
                </div>

                {item.description && (
                  <Paragraph
                    type="secondary"
                    ellipsis={{ rows: 2 }}
                    style={{ margin: '12px 0' }}
                  >
                    {item.description}
                  </Paragraph>
                )}

                <div className="favorite-meta">
                  <Space direction="vertical" size="small" style={{ width: '100%' }}>
                    <div className="file-path">
                      <Text code style={{ fontSize: 12 }}>
                        {item.file_path}
                      </Text>
                    </div>

                    {item.tags.length > 0 && (
                      <div className="tags">
                        <Text strong>标签：</Text>
                        <Space wrap size="small">
                          {item.tags.map((tag, index) => (
                            <Tag key={index} size="small">
                              {tag}
                            </Tag>
                          ))}
                        </Space>
                      </div>
                    )}

                    <div className="timestamps">
                      <Space split={<span>|</span>}>
                        <Text type="secondary" style={{ fontSize: 12 }}>
                          <StarOutlined /> 收藏于 {formatDate(item.created_at)}
                        </Text>
                        <Text type="secondary" style={{ fontSize: 12 }}>
                          <ClockCircleOutlined /> 最后访问 {formatDate(item.accessed_at)}
                        </Text>
                      </Space>
                    </div>
                  </Space>
                </div>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <Empty
            description="还没有收藏任何文件"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          >
            <Text type="secondary">
              在搜索结果中点击星标图标来收藏重要文件
            </Text>
          </Empty>
        </Card>
      )}

      <style jsx>{`
        .favorites-page {
          max-width: 1000px;
          margin: 0 auto;
        }

        .page-header {
          margin-bottom: 24px;
        }

        .favorites-list {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
          gap: 16px;
        }

        .favorite-item {
          height: 100%;
          transition: all 0.2s ease;
        }

        .favorite-item:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }

        .favorite-content {
          height: 100%;
          display: flex;
          flex-direction: column;
        }

        .favorite-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 8px;
        }

        .favorite-meta {
          margin-top: auto;
          padding-top: 12px;
        }

        .file-path {
          word-break: break-all;
        }

        .tags {
          margin-top: 8px;
        }

        .timestamps {
          margin-top: 8px;
        }

        @media (max-width: 768px) {
          .favorites-list {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  )
}

export default FavoritesPage