import React, { useState } from 'react'
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
  Form,
  Tabs,
  InputNumber,
  Input,
  Upload,
  Progress,
  Tag,
  List,
  Modal,
  message
} from 'antd'
import {
  SaveOutlined,
  ReloadOutlined,
  SearchOutlined,
  DatabaseOutlined,
  SettingOutlined,
  UserOutlined,
  SecurityScanOutlined,
  UploadOutlined,
  DownloadOutlined,
  DeleteOutlined,
  InfoCircleOutlined,
  CloudOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons'

const { Title, Text } = Typography
const { Option } = Select
const { TabPane } = Tabs

const SettingsPage: React.FC = () => {
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [indexStats, setIndexStats] = useState({
    totalFiles: 1250,
    indexedFiles: 1180,
    indexSize: '245MB',
    lastUpdate: '2024-11-12 14:30'
  })

  const handleSaveSettings = async () => {
    try {
      setLoading(true)
      const values = await form.validateFields()
      console.log('保存设置:', values)

      // 这里调用保存设置的API
      // await settingsApi.update(values)

      message.success('设置保存成功')
    } catch (error) {
      console.error('保存设置失败:', error)
      message.error('保存设置失败')
    } finally {
      setLoading(false)
    }
  }

  const handleResetSettings = () => {
    Modal.confirm({
      title: '重置设置',
      content: '确定要重置所有设置为默认值吗？此操作不可撤销。',
      icon: <ExclamationCircleOutlined />,
      onOk: () => {
        form.resetFields()
        message.success('设置已重置为默认值')
      }
    })
  }

  const handleExportSettings = () => {
    // 导出设置功能
    const settings = form.getFieldsValue()
    const dataStr = JSON.stringify(settings, null, 2)
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)

    const exportFileDefaultName = 'xiaoyao-search-settings.json'

    const linkElement = document.createElement('a')
    linkElement.setAttribute('href', dataUri)
    linkElement.setAttribute('download', exportFileDefaultName)
    linkElement.click()

    message.success('设置导出成功')
  }

  const handleImportSettings = (file: any) => {
    // 导入设置功能
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const settings = JSON.parse(e.target?.result as string)
        form.setFieldsValue(settings)
        message.success('设置导入成功')
      } catch (error) {
        message.error('设置文件格式错误')
      }
    }
    reader.readAsText(file)
    return false // 阻止自动上传
  }

  const handleRebuildIndex = () => {
    Modal.confirm({
      title: '重建索引',
      content: '重建索引需要较长时间，期间搜索功能可能不可用。确定要继续吗？',
      icon: <DatabaseOutlined />,
      onOk: () => {
        message.info('索引重建已开始，请稍候...')
        // 这里调用重建索引的API
      }
    })
  }

  const handleClearCache = () => {
    Modal.confirm({
      title: '清理缓存',
      content: '确定要清理所有缓存数据吗？这将释放存储空间但可能影响搜索性能。',
      icon: <DeleteOutlined />,
      onOk: () => {
        message.success('缓存清理完成')
      }
    })
  }

  return (
    <div className="settings-page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <Title level={2} style={{ margin: 0 }}>
          应用设置
        </Title>
        <Space>
          <Button icon={<UploadOutlined />} onClick={handleExportSettings}>
            导出设置
          </Button>
          <Upload
            accept=".json"
            showUploadList={false}
            beforeUpload={handleImportSettings}
          >
            <Button icon={<DownloadOutlined />}>
              导入设置
            </Button>
          </Upload>
        </Space>
      </div>

      <Form
        form={form}
        layout="vertical"
        initialValues={{
          search_mode: 'hybrid',
          results_per_page: 20,
          auto_suggestions: true,
          index_update_frequency: 'realtime',
          max_file_size: 100,
          ai_mode: 'local',
          gpu_acceleration: true,
          theme: 'light',
          language: 'zh-CN'
        }}
      >
        <Tabs defaultActiveKey="search" type="card">
          {/* 搜索设置 */}
          <TabPane tab={<span><SearchOutlined />搜索设置</span>} key="search">
            <div className="settings-tab-content">
              <Card title="基础搜索设置" style={{ marginBottom: 24 }}>
                <Form.Item
                  name="search_mode"
                  label="搜索模式"
                  help="选择默认的搜索算法和策略"
                >
                  <Select>
                    <Option value="semantic">语义搜索 - 理解查询意图</Option>
                    <Option value="keyword">关键词搜索 - 精确匹配</Option>
                    <Option value="hybrid">混合搜索 - 平衡精度和召回</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="results_per_page"
                  label="每页显示结果数"
                  help="控制搜索结果列表每页显示的文件数量"
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
                  help="在输入时显示相关的搜索建议"
                >
                  <Switch />
                </Form.Item>

                <Form.Item
                  name="search_history"
                  label="保存搜索历史"
                  valuePropName="checked"
                  help="记录搜索历史以便快速重复搜索"
                >
                  <Switch defaultChecked />
                </Form.Item>
              </Card>

              <Card title="高级搜索选项">
                <Form.Item
                  name="enable_fuzzy_search"
                  label="启用模糊搜索"
                  valuePropName="checked"
                  help="允许包含拼写错误的搜索查询"
                >
                  <Switch />
                </Form.Item>

                <Form.Item
                  name="min_query_length"
                  label="最小查询长度"
                  help="执行搜索所需的最少字符数"
                >
                  <InputNumber min={1} max={10} defaultValue={2} />
                </Form.Item>

                <Form.Item
                  name="search_timeout"
                  label="搜索超时时间 (秒)"
                  help="单次搜索的最大执行时间"
                >
                  <InputNumber min={5} max={60} defaultValue={30} />
                </Form.Item>
              </Card>
            </div>
          </TabPane>

          {/* 索引设置 */}
          <TabPane tab={<span><DatabaseOutlined />索引管理</span>} key="index">
            <div className="settings-tab-content">
              <Card title="索引统计信息" style={{ marginBottom: 24 }}>
                <List
                  dataSource={[
                    { title: '总文件数', value: indexStats.totalFiles, icon: <InfoCircleOutlined /> },
                    { title: '已索引文件', value: indexStats.indexedFiles, icon: <DatabaseOutlined /> },
                    { title: '索引大小', value: indexStats.indexSize, icon: <CloudOutlined /> },
                    { title: '最后更新', value: indexStats.lastUpdate, icon: <SecurityScanOutlined /> }
                  ]}
                  renderItem={(item) => (
                    <List.Item>
                      <List.Item.Meta
                        avatar={item.icon}
                        title={item.title}
                        description={<Text strong>{item.value}</Text>}
                      />
                    </List.Item>
                  )}
                />

                <Progress
                  percent={Math.round((indexStats.indexedFiles / indexStats.totalFiles) * 100)}
                  status="active"
                  style={{ marginTop: 16 }}
                />
              </Card>

              <Card title="索引设置" style={{ marginBottom: 24 }}>
                <Form.Item
                  name="index_update_frequency"
                  label="索引更新频率"
                  help="自动检测和索引文件变更的频率"
                >
                  <Select>
                    <Option value="realtime">实时更新 - 立即响应文件变化</Option>
                    <Option value="hourly">每小时 - 平衡性能和及时性</Option>
                    <Option value="daily">每天 - 低资源消耗</Option>
                    <Option value="manual">手动更新 - 完全控制</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="max_file_size"
                  label="最大文件大小 (MB)"
                  help="跳过超过此大小的文件以提高性能"
                >
                  <Slider
                    min={10}
                    max={1000}
                    step={10}
                    marks={{ 10: '10MB', 100: '100MB', 500: '500MB', 1000: '1GB' }}
                  />
                </Form.Item>

                <Form.Item
                  name="file_types"
                  label="支持的文件类型"
                  help="选择需要索引的文件类型"
                >
                  <Select
                    mode="multiple"
                    placeholder="选择文件类型"
                    defaultValue={['pdf', 'docx', 'xlsx', 'txt', 'md']}
                  >
                    <Option value="pdf">PDF文档</Option>
                    <Option value="docx">Word文档</Option>
                    <Option value="xlsx">Excel表格</Option>
                    <Option value="pptx">PowerPoint</Option>
                    <Option value="txt">文本文件</Option>
                    <Option value="md">Markdown</Option>
                    <Option value="jpg">JPEG图片</Option>
                    <Option value="png">PNG图片</Option>
                  </Select>
                </Form.Item>
              </Card>

              <Card title="索引维护">
                <Space direction="vertical" style={{ width: '100%' }}>
                  <Button
                    type="primary"
                    icon={<DatabaseOutlined />}
                    onClick={handleRebuildIndex}
                    block
                  >
                    重建索引
                  </Button>

                  <Button
                    icon={<DeleteOutlined />}
                    onClick={handleClearCache}
                    block
                  >
                    清理缓存
                  </Button>
                </Space>
              </Card>
            </div>
          </TabPane>

          {/* AI设置 */}
          <TabPane tab={<span><CloudOutlined />AI设置</span>} key="ai">
            <div className="settings-tab-content">
              <Card title="AI模型配置" style={{ marginBottom: 24 }}>
                <Form.Item
                  name="ai_mode"
                  label="AI运行模式"
                  help="选择AI服务的运行方式"
                >
                  <Select>
                    <Option value="local">本地模式 - 完全离线运行</Option>
                    <Option value="cloud">云端模式 - 使用在线服务</Option>
                    <Option value="hybrid">混合模式 - 智能切换</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="gpu_acceleration"
                  label="GPU加速"
                  valuePropName="checked"
                  help="启用GPU加速提升AI处理性能"
                >
                  <Switch />
                </Form.Item>

                <Form.Item
                  name="ai_cache_enabled"
                  label="启用AI结果缓存"
                  valuePropName="checked"
                  help="缓存AI处理结果以提升响应速度"
                >
                  <Switch defaultChecked />
                </Form.Item>
              </Card>

              <Alert
                message="AI设置说明"
                description={
                  <div>
                    <p><strong>本地模式：</strong>完全在本地运行，数据隐私性最好，但需要较多硬件资源。</p>
                    <p><strong>云端模式：</strong>使用云端AI服务，功能更强大，但需要网络连接。</p>
                    <p><strong>混合模式：</strong>根据情况智能选择本地或云端服务，平衡性能和隐私。</p>
                  </div>
                }
                type="info"
                showIcon
                style={{ marginBottom: 24 }}
              />
            </div>
          </TabPane>

          {/* 界面设置 */}
          <TabPane tab={<span><SettingOutlined />界面设置</span>} key="ui">
            <div className="settings-tab-content">
              <Card title="外观设置" style={{ marginBottom: 24 }}>
                <Form.Item
                  name="theme"
                  label="主题"
                  help="选择应用的外观主题"
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
                  help="选择界面显示语言"
                >
                  <Select>
                    <Option value="zh-CN">简体中文</Option>
                    <Option value="en-US">English</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="font_size"
                  label="字体大小"
                  help="调整界面字体大小"
                >
                  <Select defaultValue="medium">
                    <Option value="small">小</Option>
                    <Option value="medium">中</Option>
                    <Option value="large">大</Option>
                  </Select>
                </Form.Item>
              </Card>

              <Card title="行为设置">
                <Form.Item
                  name="minimize_to_tray"
                  label="最小化到托盘"
                  valuePropName="checked"
                  help="关闭窗口时最小化到系统托盘"
                >
                  <Switch />
                </Form.Item>

                <Form.Item
                  name="auto_start"
                  label="开机自启"
                  valuePropName="checked"
                  help="系统启动时自动运行小遥搜索"
                >
                  <Switch />
                </Form.Item>

                <Form.Item
                  name="show_notifications"
                  label="显示通知"
                  valuePropName="checked"
                  help="显示系统通知提醒"
                >
                  <Switch defaultChecked />
                </Form.Item>
              </Card>
            </div>
          </TabPane>
        </Tabs>
      </Form>

      {/* 操作按钮 */}
      <Card style={{ marginTop: 24 }}>
        <Space>
          <Button
            type="primary"
            icon={<SaveOutlined />}
            loading={loading}
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
  )
}

export default SettingsPage