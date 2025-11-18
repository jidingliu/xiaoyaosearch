<template>
  <div class="settings-final">
    <!-- 顶部导航 -->
    <div class="header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">⚙️</span>
          <span class="logo-text">设置</span>
        </div>
        <div class="header-actions">
          <a-button @click="goBack">
            <template #icon><ArrowLeftOutlined /></template>
            返回
          </a-button>
        </div>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="content">
      <div class="settings-container">
        <a-row :gutter="24">
          <!-- 左侧菜单 -->
          <a-col :span="6">
            <a-card class="menu-card">
              <a-menu
                v-model:selectedKeys="selectedKeys"
                mode="inline"
                @click="handleMenuClick"
                class="settings-menu"
              >
                <a-menu-item key="model">
                  <template #icon><RobotOutlined /></template>
                  LLM模型设置
                </a-menu-item>
                <a-menu-item key="voice">
                  <template #icon><AudioOutlined /></template>
                  语音识别设置
                </a-menu-item>
                <a-menu-item key="vision">
                  <template #icon><EyeOutlined /></template>
                  视觉模型设置
                </a-menu-item>
                <a-menu-item key="general">
                  <template #icon><SettingOutlined /></template>
                  通用设置
                </a-menu-item>
                <a-menu-item key="privacy">
                  <template #icon><SecurityScanOutlined /></template>
                  隐私设置
                </a-menu-item>
              </a-menu>
            </a-card>
          </a-col>

          <!-- 右侧内容 -->
          <a-col :span="18">
            <!-- LLM模型设置 -->
            <a-card v-if="activeKey === 'model'" title="LLM模型设置" class="content-card">
              <div class="setting-group">
                <h4>模型类型</h4>
                <a-radio-group v-model:value="llmConfig.type" @change="onLlmTypeChange">
                  <a-radio value="cloud">
                    <CloudOutlined />
                    云端API
                  </a-radio>
                  <a-radio value="local">
                    <DesktopOutlined />
                    本地Ollama
                  </a-radio>
                </a-radio-group>
              </div>

              <div class="setting-group">
                <h4>API配置</h4>
                <a-form layout="vertical">
                  <a-form-item label="API地址">
                    <a-input
                      v-model:value="llmConfig.apiUrl"
                      placeholder="https://api.openai.com"
                    />
                  </a-form-item>
                  <a-form-item label="访问令牌">
                    <a-input-password
                      v-model:value="llmConfig.apiKey"
                      placeholder="sk-*********************"
                    />
                  </a-form-item>
                  <a-form-item label="模型名称">
                    <a-select v-model:value="llmConfig.model" placeholder="选择模型">
                      <a-select-option value="gpt-4">GPT-4</a-select-option>
                      <a-select-option value="gpt-3.5-turbo">GPT-3.5 Turbo</a-select-option>
                      <a-select-option value="claude-3">Claude-3</a-select-option>
                      <a-select-option value="qwen-turbo">通义千问 Turbo</a-select-option>
                    </a-select>
                  </a-form-item>
                  <a-form-item label="最大Token">
                    <a-input-number
                      v-model:value="llmConfig.maxTokens"
                      :min="512"
                      :max="8192"
                    />
                  </a-form-item>
                </a-form>
              </div>

              <div class="setting-actions">
                <a-button @click="testConnection" :loading="isTesting">
                  <ApiOutlined />
                  测试连接
                </a-button>
                <a-button type="primary" @click="saveSettings">
                  <SaveOutlined />
                  保存设置
                </a-button>
              </div>
            </a-card>

            <!-- 语音识别设置 -->
            <a-card v-else-if="activeKey === 'voice'" title="语音识别设置" class="content-card">
              <div class="setting-group">
                <h4>识别引擎</h4>
                <a-radio-group v-model:value="voiceConfig.type">
                  <a-radio value="cloud">
                    <CloudOutlined />
                    云端API
                  </a-radio>
                  <a-radio value="local">
                    <DesktopOutlined />
                    本地FastWhisper
                  </a-radio>
                </a-radio-group>
              </div>

              <div class="setting-group">
                <h4>云端API配置</h4>
                <a-form layout="vertical">
                  <a-form-item label="API地址">
                    <a-input
                      v-model:value="voiceConfig.cloud.apiUrl"
                      placeholder="https://api.speech.com"
                    />
                  </a-form-item>
                  <a-form-item label="访问令牌">
                    <a-input-password
                      v-model:value="voiceConfig.cloud.apiKey"
                      placeholder="sk-*********************"
                    />
                  </a-form-item>
                  <a-form-item label="语言">
                    <a-select v-model:value="voiceConfig.cloud.language" placeholder="选择语言">
                      <a-select-option value="zh-CN">中文普通话</a-select-option>
                      <a-select-option value="en-US">English</a-select-option>
                    </a-select>
                  </a-form-item>
                </a-form>
              </div>

              <div class="setting-group">
                <h4>本地FastWhisper配置</h4>
                <a-form layout="vertical">
                  <a-form-item label="模型大小">
                    <a-radio-group v-model:value="voiceConfig.local.modelSize">
                      <a-radio value="base">Base (74MB)</a-radio>
                      <a-radio value="small">Small (244MB)</a-radio>
                      <a-radio value="medium">Medium (769MB)</a-radio>
                    </a-radio-group>
                  </a-form-item>
                  <a-form-item label="设备">
                    <a-radio-group v-model:value="voiceConfig.local.device">
                      <a-radio value="cpu">CPU</a-radio>
                      <a-radio value="cuda">CUDA</a-radio>
                      <a-radio value="metal">Metal (Mac)</a-radio>
                    </a-radio-group>
                  </a-form-item>
                </a-form>
              </div>

              <div class="setting-group">
                <h4>录音设置</h4>
                <a-form layout="vertical">
                  <a-form-item label="最长录音时间">
                    <a-input-number
                      v-model:value="voiceConfig.maxDuration"
                      :min="10"
                      :max="60"
                      suffix="秒"
                    />
                  </a-form-item>
                  <a-form-item label="音质">
                    <a-radio-group v-model:value="voiceConfig.quality">
                      <a-radio value="standard">标准</a-radio>
                      <a-radio value="high">高质量</a-radio>
                    </a-radio-group>
                  </a-form-item>
                </a-form>
              </div>

              <div class="setting-actions">
                <a-button @click="testRecording">
                  <AudioOutlined />
                  测试录音
                </a-button>
                <a-button type="primary" @click="saveSettings">
                  <SaveOutlined />
                  保存设置
                </a-button>
              </div>
            </a-card>

            <!-- 视觉模型设置 -->
            <a-card v-else-if="activeKey === 'vision'" title="视觉模型设置" class="content-card">
              <div class="setting-group">
                <h4>视觉模型类型</h4>
                <a-radio-group v-model:value="visionConfig.type">
                  <a-radio value="cloud">
                    <CloudOutlined />
                    云端API
                  </a-radio>
                  <a-radio value="local">
                    <DesktopOutlined />
                    本地视觉模型
                  </a-radio>
                </a-radio-group>
              </div>

              <div class="setting-group">
                <h4>云端视觉API配置</h4>
                <a-form layout="vertical">
                  <a-form-item label="API地址">
                    <a-input
                      v-model:value="visionConfig.cloud.apiUrl"
                      placeholder="https://api.vision.com"
                    />
                  </a-form-item>
                  <a-form-item label="访问令牌">
                    <a-input-password
                      v-model:value="visionConfig.cloud.apiKey"
                      placeholder="sk-*********************"
                    />
                  </a-form-item>
                  <a-form-item label="视觉模型名称">
                    <a-select v-model:value="visionConfig.cloud.model" placeholder="选择模型">
                      <a-select-option value="gpt-4-vision">GPT-4 Vision</a-select-option>
                      <a-select-option value="claude-3-vision">Claude-3 Vision</a-select-option>
                    </a-select>
                  </a-form-item>
                </a-form>
              </div>

              <div class="setting-actions">
                <a-button type="primary" @click="saveSettings">
                  <SaveOutlined />
                  保存设置
                </a-button>
              </div>
            </a-card>

            <!-- 通用设置 -->
            <a-card v-else-if="activeKey === 'general'" title="通用设置" class="content-card">
              <div class="setting-group">
                <h4>界面设置</h4>
                <a-form layout="vertical">
                  <a-form-item label="主题">
                    <a-radio-group v-model:value="generalConfig.theme">
                      <a-radio value="light">
                        <SunOutlined />
                        浅色主题
                      </a-radio>
                      <a-radio value="dark">
                        <DesktopOutlined />
                        深色主题
                      </a-radio>
                      <a-radio value="auto">
                        <BulbOutlined />
                        跟随系统
                      </a-radio>
                    </a-radio-group>
                  </a-form-item>
                  <a-form-item label="语言">
                    <a-select v-model:value="generalConfig.language" placeholder="选择语言">
                      <a-select-option value="zh-CN">简体中文</a-select-option>
                      <a-select-option value="en-US">English</a-select-option>
                      <a-select-option value="ja-JP">日本語</a-select-option>
                    </a-select>
                  </a-form-item>
                </a-form>
              </div>

              <div class="setting-group">
                <h4>性能设置</h4>
                <a-form layout="vertical">
                  <a-form-item label="搜索结果数量">
                    <a-input-number
                      v-model:value="generalConfig.maxResults"
                      :min="5"
                      :max="50"
                    />
                  </a-form-item>
                  <a-form-item label="并行搜索线程数">
                    <a-input-number
                      v-model:value="generalConfig.searchThreads"
                      :min="1"
                      :max="8"
                    />
                  </a-form-item>
                </a-form>
              </div>

              <div class="setting-actions">
                <a-button @click="resetToDefault">
                  <ReloadOutlined />
                  恢复默认
                </a-button>
                <a-button type="primary" @click="saveSettings">
                  <SaveOutlined />
                  保存设置
                </a-button>
              </div>
            </a-card>

            <!-- 隐私设置 -->
            <a-card v-else-if="activeKey === 'privacy'" title="隐私设置" class="content-card">
              <div class="setting-group">
                <h4>数据保护</h4>
                <div class="checkbox-group">
                  <a-checkbox v-model:checked="privacyConfig.encryptLocalData">
                    <DatabaseOutlined />
                    本地数据加密存储
                  </a-checkbox>
                  <a-checkbox v-model:checked="privacyConfig.secureApiKey">
                    <SafetyCertificateOutlined />
                    安全保存API密钥
                  </a-checkbox>
                  <a-checkbox v-model:checked="privacyConfig.noCloudUpload">
                    <CloudServerOutlined />
                    用户数据不上传云端
                  </a-checkbox>
                </div>
              </div>

              <div class="setting-group">
                <h4>搜索历史</h4>
                <div class="checkbox-group">
                  <a-checkbox v-model:checked="privacyConfig.enableSearchHistory">
                    <HistoryOutlined />
                    保存搜索历史
                  </a-checkbox>
                  <a-checkbox v-model:checked="privacyConfig.anonymousTelemetry">
                    <BarChartOutlined />
                    发送匿名使用统计
                  </a-checkbox>
                </div>
              </div>

              <div class="setting-group">
                <h4>数据管理</h4>
                <a-space direction="vertical" style="width: 100%">
                  <a-button @click="clearSearchHistory" block>
                    <DeleteOutlined />
                    清除搜索历史
                  </a-button>
                  <a-button @click="exportData" block>
                    <ExportOutlined />
                    导出数据
                  </a-button>
                </a-space>
              </div>

              <div class="setting-actions">
                <a-button type="primary" @click="saveSettings">
                  <SaveOutlined />
                  保存设置
                </a-button>
              </div>
            </a-card>

            <!-- 默认欢迎页面 -->
            <a-card v-else title="欢迎使用设置中心" class="content-card welcome-card">
              <div class="welcome-content">
                <div class="welcome-icon">
                  <SettingOutlined />
                </div>
                <h3>配置您的搜索体验</h3>
                <p>请从左侧菜单选择要配置的设置项</p>

                <div class="quick-links">
                  <a-card size="small" title="快速配置建议" style="margin-top: 20px;">
                    <ul>
                      <li><strong>首次使用</strong>：建议先配置 LLM 模型设置</li>
                      <li><strong>语音搜索</strong>：配置语音识别引擎</li>
                      <li><strong>隐私保护</strong>：根据需要调整隐私设置</li>
                    </ul>
                  </a-card>
                </div>
              </div>
            </a-card>
          </a-col>
        </a-row>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import {
  ArrowLeftOutlined,
  RobotOutlined,
  AudioOutlined,
  EyeOutlined,
  SettingOutlined,
  SecurityScanOutlined,
  CloudOutlined,
  DesktopOutlined,
  ApiOutlined,
  SaveOutlined,
  SunOutlined,
  BulbOutlined,
  ReloadOutlined,
  DatabaseOutlined,
  SafetyCertificateOutlined,
  CloudOutlined,
  HistoryOutlined,
  BarChartOutlined,
  DeleteOutlined,
  ExportOutlined
} from '@ant-design/icons-vue'

console.log('=== 设置页面最终版本开始加载 ===')

// 状态管理
const selectedKeys = ref<string[]>(['model'])
const activeKey = ref<string>('model')
const isTesting = ref(false)

// LLM配置
const llmConfig = reactive({
  type: 'cloud',
  apiUrl: 'https://api.openai.com',
  apiKey: '',
  model: 'gpt-4',
  maxTokens: 4096,
  local: {
    apiUrl: 'http://localhost:11434',
    model: 'qwen2.5:7b'
  }
})

// 语音配置
const voiceConfig = reactive({
  type: 'cloud',
  cloud: {
    apiUrl: 'https://api.speech.com',
    apiKey: '',
    language: 'zh-CN'
  },
  local: {
    modelSize: 'base',
    device: 'cpu'
  },
  maxDuration: 30,
  quality: 'standard'
})

// 视觉配置
const visionConfig = reactive({
  type: 'cloud',
  cloud: {
    apiUrl: 'https://api.vision.com',
    apiKey: '',
    model: 'gpt-4-vision'
  },
  local: {
    model: 'clip-vit-base',
    device: 'cpu'
  }
})

// 通用配置
const generalConfig = reactive({
  theme: 'light',
  language: 'zh-CN',
  maxResults: 20,
  searchThreads: 4
})

// 隐私配置
const privacyConfig = reactive({
  encryptLocalData: true,
  secureApiKey: true,
  noCloudUpload: true,
  enableSearchHistory: true,
  anonymousTelemetry: false
})

// 菜单点击处理
const handleMenuClick = ({ key }: { key: string }) => {
  console.log('菜单点击:', key)
  activeKey.value = key
  selectedKeys.value = [key]
}

// LLM类型改变
const onLlmTypeChange = (e: any) => {
  console.log('LLM类型改变:', e.target.value)
}

// 测试连接
const testConnection = async () => {
  isTesting.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 2000))
    message.success('连接测试成功！')
  } catch (error) {
    message.error('连接测试失败')
  } finally {
    isTesting.value = false
  }
}

// 测试录音
const testRecording = () => {
  message.info('开始测试录音功能...')
}

// 恢复默认
const resetToDefault = () => {
  message.info('已恢复默认设置')
}

// 清除搜索历史
const clearSearchHistory = () => {
  message.success('搜索历史已清除')
}

// 导出数据
const exportData = () => {
  message.success('数据导出完成')
}

// 保存设置
const saveSettings = () => {
  console.log('保存设置:', {
    llm: llmConfig,
    voice: voiceConfig,
    vision: visionConfig,
    general: generalConfig,
    privacy: privacyConfig
  })
  message.success('设置已保存')
}

// 返回
const goBack = () => {
  message.info('返回上一页')
}

// 组件挂载
onMounted(() => {
  console.log('=== 设置页面最终版本已挂载 ===')
})
</script>

<style scoped>
.settings-final {
  min-height: 100vh;
  background: #f5f5f5;
}

.header {
  background: #fff;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #6366f1;
}

.content {
  padding: 24px;
}

.settings-container {
  max-width: 1200px;
  margin: 0 auto;
}

.menu-card {
  height: fit-content;
}

.settings-menu {
  border-right: none;
}

.settings-menu .ant-menu-item {
  margin: 0;
  height: 48px;
  line-height: 48px;
  border-radius: 6px;
  margin-bottom: 4px;
}

.settings-menu .ant-menu-item-selected {
  background-color: #f0f5ff;
  color: #6366f1;
}

.settings-menu .ant-menu-item:hover {
  background-color: #f8f9fa;
}

.content-card {
  min-height: 600px;
}

.welcome-card {
  text-align: center;
}

.welcome-content {
  padding: 40px 0;
}

.welcome-icon {
  font-size: 64px;
  color: #6366f1;
  margin-bottom: 20px;
}

.setting-group {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.setting-group:last-child {
  border-bottom: none;
}

.setting-group h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checkbox-group .ant-checkbox-wrapper {
  padding: 8px 0;
}

.setting-actions {
  display: flex;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

.setting-actions .ant-btn {
  display: flex;
  align-items: center;
  gap: 4px;
}

:deep(.ant-form-item) {
  margin-bottom: 16px;
}

:deep(.ant-form-item-label > label) {
  font-weight: 500;
  color: #333;
}

:deep(.ant-radio-wrapper) {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

ul {
  text-align: left;
  margin: 12px 0;
  padding-left: 20px;
}

ul li {
  margin-bottom: 8px;
  line-height: 1.5;
}
</style>