import React from 'react'
import {
  Card,
  Typography,
  Divider,
  Switch,
  Select,
  Slider,
  Button,
  Space,
  Alert,
  Form
} from 'antd'
import { SaveOutlined, ReloadOutlined } from '@ant-design/icons'

const { Title, Text } = Typography
const { Option } = Select

const SettingsPage: React.FC = () => {
  const [form] = Form.useForm()

  const handleSaveSettings = () => {
    form.validateFields().then(values => {
      console.log('保存设置:', values)
      // 这里调用保存设置的API
    })
  }

  const handleResetSettings = () => {
    form.resetFields()
  }

  return (
    <div className="settings-page">
      <Title level={2} style={{ marginBottom: 24 }}>
        应用设置
      </Title>

      <div className="settings-content">
        {/* 搜索设置 */}
        <Card title="搜索设置" style={{ marginBottom: 24 }}>
          <Form form={form} layout="vertical">
            <Form.Item
              name="search_mode"
              label="搜索模式"
              initialValue="hybrid"
            >
              <Select>
                <Option value="semantic">语义搜索</Option>
                <Option value="keyword">关键词搜索</Option>
                <Option value="hybrid">混合搜索</Option>
              </Select>
            </Form.Item>

            <Form.Item
              name="results_per_page"
              label="每页显示结果数"
              initialValue={20}
            >
              <Slider
                min={10}
                max={100}
                step={10}
                marks={{ 10: '10', 50: '50', 100: '100' }}
              />
            </Form.Item>

            <Form.Item
              name="auto_suggestions"
              label="自动搜索建议"
              valuePropName="checked"
              initialValue={true}
            >
              <Switch />
            </Form.Item>
          </Form>
        </Card>

        {/* 索引设置 */}
        <Card title="索引设置" style={{ marginBottom: 24 }}>
          <Form form={form} layout="vertical">
            <Form.Item
              name="index_update_frequency"
              label="索引更新频率"
              initialValue="realtime"
            >
              <Select>
                <Option value="realtime">实时更新</Option>
                <Option value="hourly">每小时</Option>
                <Option value="daily">每天</Option>
                <Option value="manual">手动更新</Option>
              </Select>
            </Form.Item>

            <Form.Item
              name="max_file_size"
              label="最大文件大小 (MB)"
              initialValue={100}
            >
              <Slider
                min={10}
                max={1000}
                step={10}
                marks={{ 10: '10MB', 100: '100MB', 500: '500MB', 1000: '1GB' }}
              />
            </Form.Item>
          </Form>
        </Card>

        {/* AI设置 */}
        <Card title="AI设置" style={{ marginBottom: 24 }}>
          <Form form={form} layout="vertical">
            <Form.Item
              name="ai_mode"
              label="AI运行模式"
              initialValue="local"
            >
              <Select>
                <Option value="local">本地模式</Option>
                <Option value="cloud">云端模式</Option>
                <Option value="hybrid">混合模式</Option>
              </Select>
            </Form.Item>

            <Form.Item
              name="gpu_acceleration"
              label="GPU加速"
              valuePropName="checked"
              initialValue={true}
            >
              <Switch />
            </Form.Item>
          </Form>

          <Alert
            message="AI设置说明"
            description="本地模式：完全在本地运行，数据隐私性最好。云端模式：使用云端AI服务，功能更强大。混合模式：结合本地和云端优势。"
            type="info"
            showIcon
            style={{ marginTop: 16 }}
          />
        </Card>

        {/* 界面设置 */}
        <Card title="界面设置" style={{ marginBottom: 24 }}>
          <Form form={form} layout="vertical">
            <Form.Item
              name="theme"
              label="主题"
              initialValue="light"
            >
              <Select>
                <Option value="light">浅色主题</Option>
                <Option value="dark">深色主题</Option>
                <Option value="auto">跟随系统</Option>
              </Select>
            </Form.Item>

            <Form.Item
              name="language"
              label="语言"
              initialValue="zh-CN"
            >
              <Select>
                <Option value="zh-CN">简体中文</Option>
                <Option value="en-US">English</Option>
              </Select>
            </Form.Item>
          </Form>
        </Card>

        {/* 操作按钮 */}
        <Card>
          <Space>
            <Button
              type="primary"
              icon={<SaveOutlined />}
              onClick={handleSaveSettings}
            >
              保存设置
            </Button>
            <Button
              icon={<ReloadOutlined />}
              onClick={handleResetSettings}
            >
              重置设置
            </Button>
          </Space>
        </Card>
      </div>
    </div>
  )
}

export default SettingsPage