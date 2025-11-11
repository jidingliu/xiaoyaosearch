import React, { useState, useEffect } from 'react'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import {
  Layout,
  Menu,
  Typography,
  Button,
  Space,
  Badge,
  Tooltip,
  Dropdown
} from 'antd'
import {
  SearchOutlined,
  FolderOpenOutlined,
  SettingOutlined,
  StarOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  UserOutlined,
  LogoutOutlined
} from '@ant-design/icons'

const { Header, Sider, Content } = Layout
const { Title } = Typography

interface MainLayoutProps {}

const MainLayout: React.FC<MainLayoutProps> = () => {
  const [collapsed, setCollapsed] = useState(false)
  const [indexStatus, setIndexStatus] = useState({
    isIndexing: false,
    progress: 0
  })

  const navigate = useNavigate()
  const location = useLocation()

  // 菜单项配置
  const menuItems = [
    {
      key: '/search',
      icon: <SearchOutlined />,
      label: '搜索'
    },
    {
      key: '/index',
      icon: <FolderOpenOutlined />,
      label: '索引管理'
    },
    {
      key: '/favorites',
      icon: <StarOutlined />,
      label: '收藏'
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: '设置'
    }
  ]

  // 用户下拉菜单
  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人信息'
    },
    {
      type: 'divider'
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录'
    }
  ]

  useEffect(() => {
    // 模拟获取索引状态
    const timer = setInterval(() => {
      setIndexStatus(prev => ({
        ...prev,
        progress: prev.isIndexing ? Math.min(prev.progress + 1, 100) : prev.progress
      }))
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  const handleMenuClick = ({ key }: { key: string }) => {
    navigate(key)
  }

  const handleUserMenuClick = ({ key }: { key: string }) => {
    if (key === 'logout') {
      // 处理退出登录
      console.log('退出登录')
    } else if (key === 'profile') {
      // 跳转到个人信息页面
      console.log('个人信息')
    }
  }

  return (
    <Layout className="main-layout">
      {/* 侧边栏 */}
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        width={240}
        className="main-sider"
      >
        <div className="logo-container">
          <Title
            level={3}
            style={{
              color: 'white',
              margin: collapsed ? '16px 0' : '24px 0',
              textAlign: 'center'
            }}
          >
            {collapsed ? '遥' : '小遥搜索'}
          </Title>
        </div>

        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={handleMenuClick}
          className="main-menu"
        />
      </Sider>

      <Layout>
        {/* 顶部导航栏 */}
        <Header className="main-header" style={{ padding: '0 24px' }}>
          <div className="header-left">
            <Button
              type="text"
              icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              onClick={() => setCollapsed(!collapsed)}
              style={{ fontSize: '16px', width: 64, height: 64 }}
            />
          </div>

          <div className="header-center">
            {indexStatus.isIndexing && (
              <Badge
                count={`${indexStatus.progress}%`}
                overflowCount={100}
                style={{ backgroundColor: '#52c41a' }}
              >
                <span>索引构建中...</span>
              </Badge>
            )}
          </div>

          <div className="header-right">
            <Space>
              <Tooltip title="通知">
                <Badge count={0} showZero={false}>
                  <Button type="text" icon={<span className="icon-notification" />} />
                </Badge>
              </Tooltip>

              <Dropdown
                menu={{
                  items: userMenuItems,
                  onClick: handleUserMenuClick
                }}
                placement="bottomRight"
              >
                <Button type="text" icon={<UserOutlined />} />
              </Dropdown>
            </Space>
          </div>
        </Header>

        {/* 主内容区域 */}
        <Content className="main-content">
          <div className="content-container">
            <Outlet />
          </div>
        </Content>
      </Layout>

      <style jsx>{`
        .main-layout {
          height: 100vh;
        }

        .main-sider {
          position: relative;
          z-index: 10;
        }

        .logo-container {
          padding: 0 16px;
          border-bottom: 1px solid #1f1f1f;
          overflow: hidden;
        }

        .main-menu {
          border-right: none;
        }

        .main-header {
          background: white;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
          display: flex;
          align-items: center;
          justify-content: space-between;
          z-index: 9;
        }

        .header-left,
        .header-right {
          display: flex;
          align-items: center;
        }

        .header-center {
          flex: 1;
          display: flex;
          justify-content: center;
        }

        .main-content {
          background: #f0f2f5;
          overflow: hidden;
        }

        .content-container {
          height: 100%;
          padding: 24px;
          overflow-y: auto;
        }

        .icon-notification::before {
          content: '🔔';
        }
      `}</style>
    </Layout>
  )
}

export default MainLayout