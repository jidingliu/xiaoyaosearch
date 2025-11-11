import React, { useState } from 'react'
import {
  Card,
  Button,
  Table,
  Progress,
  Space,
  Tag,
  Typography,
  Empty,
  message,
  Modal
} from 'antd'
import {
  PlusOutlined,
  FolderOpenOutlined,
  DeleteOutlined,
  PlayCircleOutlined,
  PauseCircleOutlined,
  ReloadOutlined
} from '@ant-design/icons'

const { Title, Text } = Typography

const IndexPage: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [directories, setDirectories] = useState([
    {
      id: '1',
      path: '/Users/用户/Documents',
      status: 'active',
      file_count: 1250,
      indexed_count: 1180,
      last_scan_time: '2024-11-08 10:30:00'
    },
    {
      id: '2',
      path: '/Users/用户/Desktop',
      status: 'active',
      file_count: 85,
      indexed_count: 85,
      last_scan_time: '2024-11-08 09:15:00'
    }
  ])

  const [isIndexing, setIsIndexing] = useState(false)
  const [indexProgress, setIndexProgress] = useState(0)

  // 表格列定义
  const columns = [
    {
      title: '目录路径',
      dataIndex: 'path',
      key: 'path',
      render: (path: string) => (
        <Space>
          <FolderOpenOutlined />
          <Text code>{path}</Text>
        </Space>
      )
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const statusConfig = {
          active: { color: 'green', text: '活跃' },
          inactive: { color: 'orange', text: '未活跃' },
          error: { color: 'red', text: '错误' }
        }
        const config = statusConfig[status as keyof typeof statusConfig]
        return <Tag color={config.color}>{config.text}</Tag>
      }
    },
    {
      title: '文件数量',
      dataIndex: 'file_count',
      key: 'file_count',
      render: (count: number) => <Text>{count.toLocaleString()}</Text>
    },
    {
      title: '已索引',
      dataIndex: 'indexed_count',
      key: 'indexed_count',
      render: (indexed: number, record: any) => {
        const percentage = (indexed / record.file_count) * 100
        return (
          <Space direction="vertical" size="small" style={{ width: 120 }}>
            <Text>{indexed.toLocaleString()}</Text>
            <Progress
              percent={Math.round(percentage)}
              size="small"
              status={percentage === 100 ? 'success' : 'active'}
            />
          </Space>
        )
      }
    },
    {
      title: '最后扫描',
      dataIndex: 'last_scan_time',
      key: 'last_scan_time',
      render: (time: string) => <Text>{time}</Text>
    },
    {
      title: '操作',
      key: 'actions',
      render: (_, record: any) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<ReloadOutlined />}
            onClick={() => handleScanDirectory(record.id)}
          >
            重新扫描
          </Button>
          <Button
            type="link"
            size="small"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleRemoveDirectory(record.id)}
          >
            移除
          </Button>
        </Space>
      )
    }
  ]

  const handleAddDirectory = async () => {
    try {
      const result = await window.electronAPI.dialog.showOpenDialog({
        properties: ['openDirectory'],
        title: '选择要索引的目录'
      })

      if (!result.canceled && result.filePaths.length > 0) {
        const newDirectory = result.filePaths[0]

        // 检查是否已存在
        if (directories.some(dir => dir.path === newDirectory)) {
          message.warning('该目录已存在于索引列表中')
          return
        }

        // 添加新目录
        const newDir = {
          id: Date.now().toString(),
          path: newDirectory,
          status: 'active',
          file_count: 0,
          indexed_count: 0,
          last_scan_time: new Date().toISOString()
        }

        setDirectories([...directories, newDir])
        message.success('目录添加成功')

        // 自动开始扫描
        handleScanDirectory(newDir.id)
      }
    } catch (error) {
      message.error('添加目录失败')
    }
  }

  const handleRemoveDirectory = (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要移除这个目录吗？这将从索引中删除该目录的所有文件。',
      onOk: () => {
        setDirectories(directories.filter(dir => dir.id !== id))
        message.success('目录已移除')
      }
    })
  }

  const handleScanDirectory = async (id: string) => {
    setLoading(true)
    setIsIndexing(true)
    setIndexProgress(0)

    try {
      // 模拟扫描过程
      for (let i = 0; i <= 100; i += 5) {
        await new Promise(resolve => setTimeout(resolve, 100))
        setIndexProgress(i)
      }

      message.success('目录扫描完成')

      // 更新目录状态
      setDirectories(directories.map(dir => {
        if (dir.id === id) {
          return {
            ...dir,
            indexed_count: dir.file_count,
            last_scan_time: new Date().toISOString()
          }
        }
        return dir
      }))
    } catch (error) {
      message.error('目录扫描失败')
    } finally {
      setLoading(false)
      setIsIndexing(false)
      setIndexProgress(0)
    }
  }

  const handleGlobalIndex = async () => {
    if (directories.length === 0) {
      message.warning('请先添加要索引的目录')
      return
    }

    setLoading(true)
    setIsIndexing(true)

    try {
      // 模拟全局索引
      for (let i = 0; i <= 100; i += 2) {
        await new Promise(resolve => setTimeout(resolve, 200))
        setIndexProgress(i)
      }

      message.success('全局索引构建完成')
    } catch (error) {
      message.error('索引构建失败')
    } finally {
      setLoading(false)
      setIsIndexing(false)
      setIndexProgress(0)
    }
  }

  const totalFiles = directories.reduce((sum, dir) => sum + dir.file_count, 0)
  const totalIndexed = directories.reduce((sum, dir) => sum + dir.indexed_count, 0)
  const overallProgress = totalFiles > 0 ? (totalIndexed / totalFiles) * 100 : 0

  return (
    <div className="index-page">
      {/* 总体状态 */}
      <Card className="overview-card" style={{ marginBottom: 24 }}>
        <div className="overview-content">
          <div className="overview-stats">
            <Space size="large">
              <div>
                <Title level={4} style={{ margin: 0 }}>
                  {directories.length}
                </Title>
                <Text type="secondary">索引目录</Text>
              </div>
              <div>
                <Title level={4} style={{ margin: 0 }}>
                  {totalFiles.toLocaleString()}
                </Title>
                <Text type="secondary">总文件数</Text>
              </div>
              <div>
                <Title level={4} style={{ margin: 0 }}>
                  {totalIndexed.toLocaleString()}
                </Title>
                <Text type="secondary">已索引文件</Text>
              </div>
            </Space>
          </div>

          <div className="overview-progress">
            <Text strong>整体索引进度</Text>
            <Progress
              percent={Math.round(overallProgress)}
              status={overallProgress === 100 ? 'success' : 'active'}
              style={{ marginTop: 8 }}
            />
          </div>

          <div className="overview-actions">
            <Space>
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={handleAddDirectory}
              >
                添加目录
              </Button>
              <Button
                icon={isIndexing ? <PauseCircleOutlined /> : <PlayCircleOutlined />}
                onClick={handleGlobalIndex}
                loading={loading}
                disabled={directories.length === 0}
              >
                {isIndexing ? '暂停索引' : '开始索引'}
              </Button>
            </Space>
          </div>
        </div>

        {isIndexing && (
          <div className="indexing-progress" style={{ marginTop: 16 }}>
            <Text>正在构建索引...</Text>
            <Progress percent={indexProgress} status="active" />
          </div>
        )}
      </Card>

      {/* 目录列表 */}
      <Card
        title="索引目录"
        extra={
          <Button
            type="link"
            icon={<PlusOutlined />}
            onClick={handleAddDirectory}
          >
            添加目录
          </Button>
        }
      >
        {directories.length > 0 ? (
          <Table
            dataSource={directories}
            columns={columns}
            rowKey="id"
            loading={loading}
            pagination={false}
          />
        ) : (
          <Empty
            description="还没有添加任何索引目录"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          >
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={handleAddDirectory}
            >
              添加第一个目录
            </Button>
          </Empty>
        )}
      </Card>

      <style jsx>{`
        .index-page {
          max-width: 1200px;
          margin: 0 auto;
        }

        .overview-card {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .overview-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 24px;
        }

        .overview-stats .ant-typography {
          color: white !important;
        }

        .overview-progress {
          flex: 1;
          min-width: 200px;
        }

        .overview-progress .ant-typography {
          color: white !important;
        }

        .overview-actions {
          display: flex;
          gap: 12px;
        }

        .indexing-progress {
          padding-top: 16px;
          border-top: 1px solid rgba(255, 255, 255, 0.2);
        }

        .indexing-progress .ant-typography {
          color: white !important;
        }
      `}</style>
    </div>
  )
}

export default IndexPage