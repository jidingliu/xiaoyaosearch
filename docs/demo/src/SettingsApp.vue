<template>
  <a-config-provider :theme="{ token: { colorPrimary: '#6366F1' } }">
    <div class="settings-app">
      <a-layout class="layout">
        <!-- 头部导航 -->
        <a-layout-header class="header">
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
        </a-layout-header>

        <!-- 主要内容区 -->
        <a-layout-content class="content">
          <div class="settings-container">
            <a-layout style="background: #fff; min-height: 600px;">
              <!-- 左侧菜单 -->
              <a-layout-sider
                v-model:selectedKeys="selectedKeys"
                :open-keys="openKeys"
                theme="light"
                width="240"
                class="settings-sider"
              >
                <a-menu
                  v-model:selectedKeys="selectedKeys"
                  mode="inline"
                  :open-keys="openKeys"
                  @openChange="onOpenChange"
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
                    <template #icon><ShieldCheckOutlined /></template>
                    隐私设置
                  </a-menu-item>
                </a-menu>
              </a-layout-sider>

              <!-- 右侧内容区 -->
              <a-layout-content class="settings-content">
                <!-- LLM模型设置 -->
                <div v-show="selectedKeys[0] === 'model'" class="setting-panel">
                  <div class="panel-header">
                    <h2>LLM模型设置</h2>
                    <p>配置用于语义理解的AI模型</p>
                  </div>

                  <div class="setting-section">
                    <h3>模型类型</h3>
                    <a-radio-group v-model:value="llmConfig.type" @change="handleLlmTypeChange">
                      <a-radio value="cloud">
                        <template #icon><CloudOutlined /></template>
                        云端API
                      </a-radio>
                      <a-radio value="local">
                        <template #icon><DesktopOutlined /></template>
                        本地Ollama
                      </a-radio>
                    </a-radio-group>
                  </div>

                  <!-- 云端API配置 -->
                  <div v-if="llmConfig.type === 'cloud'" class="setting-section">
                    <h3>云端API配置</h3>
                    <a-form layout="vertical">
                      <a-form-item label="API地址">
                        <a-input
                          v-model:value="llmConfig.cloud.apiUrl"
                          placeholder="https://api.openai.com"
                        />
                      </a-form-item>
                      <a-form-item label="访问令牌">
                        <a-input-password
                          v-model:value="llmConfig.cloud.apiKey"
                          placeholder="sk-*********************"
                        />
                      </a-form-item>
                      <a-form-item label="模型名称">
                        <a-select
                          v-model:value="llmConfig.cloud.model"
                          placeholder="选择模型"
                        >
                          <a-select-option value="gpt-4">GPT-4</a-select-option>
                          <a-select-option value="gpt-3.5-turbo">GPT-3.5 Turbo</a-select-option>
                          <a-select-option value="claude-3">Claude-3</a-select-option>
                          <a-select-option value="qwen-turbo">通义千问 Turbo</a-select-option>
                        </a-select>
                      </a-form-item>
                      <a-form-item label="最大Token">
                        <a-input-number
                          v-model:value="llmConfig.cloud.maxTokens"
                          :min="512"
                          :max="8192"
                          style="width: 200px"
                        />
                      </a-form-item>
                    </a-form>
                  </div>

                  <!-- 本地Ollama配置 -->
                  <div v-if="llmConfig.type === 'local'" class="setting-section">
                    <h3>本地Ollama配置</h3>
                    <a-form layout="vertical">
                      <a-form-item label="API地址">
                        <a-input
                          v-model:value="llmConfig.local.apiUrl"
                          placeholder="http://localhost:11434"
                        />
                      </a-form-item>
                      <a-form-item label="模型名称">
                        <div class="model-select-row">
                          <a-select
                            v-model:value="llmConfig.local.model"
                            placeholder="选择模型"
                            style="flex: 1"
                          >
                            <a-select-option value="qwen2.5:7b">Qwen2.5:7b</a-select-option>
                            <a-select-option value="llama3:8b">Llama3:8b</a-select-option>
                            <a-select-option value="chatglm3:6b">ChatGLM3:6b</a-select-option>
                            <a-select-option value="mistral:7b">Mistral:7b</a-select-option>
                          </a-select>
                          <a-button @click="refreshModels" :loading="isLoadingModels">
                            <template #icon><ReloadOutlined /></template>
                            刷新模型列表
                          </a-button>
                        </div>
                      </a-form-item>
                    </a-form>
                  </div>

                  <div class="setting-actions">
                    <a-button @click="testConnection" :loading="isTesting">
                      <template #icon><ApiOutlined /></template>
                      测试连接
                    </a-button>
                    <a-button type="primary" @click="saveSettings">
                      <template #icon><SaveOutlined /></template>
                      保存
                    </a-button>
                  </div>
                </div>

                <!-- 语音识别设置 -->
                <div v-show="selectedKeys[0] === 'voice'" class="setting-panel">
                  <div class="panel-header">
                    <h2>语音识别设置</h2>
                    <p>配置语音转文字引擎</p>
                  </div>

                  <div class="setting-section">
                    <h3>识别引擎</h3>
                    <a-radio-group v-model:value="voiceConfig.type" @change="handleVoiceTypeChange">
                      <a-radio value="cloud">
                        <template #icon><CloudOutlined /></template>
                        云端API
                      </a-radio>
                      <a-radio value="local">
                        <template #icon><DesktopOutlined /></template>
                        本地FastWhisper
                      </a-radio>
                    </a-radio-group>
                  </div>

                  <!-- 云端语音API配置 -->
                  <div v-if="voiceConfig.type === 'cloud'" class="setting-section">
                    <h3>云端API配置</h3>
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
                        <a-select
                          v-model:value="voiceConfig.cloud.language"
                          placeholder="选择语言"
                        >
                          <a-select-option value="zh-CN">中文普通话</a-select-option>
                          <a-select-option value="en-US">English</a-select-option>
                          <a-select-option value="ja-JP">日本語</a-select-option>
                          <a-select-option value="ko-KR">한국어</a-select-option>
                        </a-select>
                      </a-form-item>
                    </a-form>
                  </div>

                  <!-- 本地FastWhisper配置 -->
                  <div v-if="voiceConfig.type === 'local'" class="setting-section">
                    <h3>本地FastWhisper</h3>
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

                    <div class="local-model-actions">
                      <a-button
                        v-if="!voiceConfig.local.enabled"
                        type="primary"
                        @click="enableLocalWhisper"
                        :loading="isEnablingWhisper"
                      >
                        <template #icon><ThunderboltOutlined /></template>
                        一键启用
                      </a-button>
                      <a-button
                        v-else
                        type="default"
                        @click="downloadWhisperModel"
                        :loading="isDownloadingModel"
                      >
                        <template #icon><DownloadOutlined /></template>
                        下载模型
                      </a-button>
                    </div>
                  </div>

                  <!-- 录音设置 -->
                  <div class="setting-section">
                    <h3>录音设置</h3>
                    <a-form layout="vertical">
                      <a-form-item label="最长录音时间">
                        <a-input-number
                          v-model:value="voiceConfig.maxDuration"
                          :min="10"
                          :max="60"
                          suffix="秒"
                          style="width: 200px"
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
                      <template #icon><AudioOutlined /></template>
                      测试录音
                    </a-button>
                    <a-button type="primary" @click="saveSettings">
                      <template #icon><SaveOutlined /></template>
                      保存
                    </a-button>
                  </div>
                </div>

                <!-- 视觉模型设置 -->
                <div v-show="selectedKeys[0] === 'vision'" class="setting-panel">
                  <div class="panel-header">
                    <h2>视觉模型设置</h2>
                    <p>配置图片理解和搜索模型</p>
                  </div>

                  <div class="setting-section">
                    <h3>视觉模型类型</h3>
                    <a-radio-group v-model:value="visionConfig.type">
                      <a-radio value="cloud">
                        <template #icon><CloudOutlined /></template>
                        云端API
                      </a-radio>
                      <a-radio value="local">
                        <template #icon><DesktopOutlined /></template>
                        本地视觉模型
                      </a-radio>
                    </a-radio-group>
                  </div>

                  <!-- 云端视觉API配置 -->
                  <div v-if="visionConfig.type === 'cloud'" class="setting-section">
                    <h3>云端API配置</h3>
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
                        <a-select
                          v-model:value="visionConfig.cloud.model"
                          placeholder="选择模型"
                        >
                          <a-select-option value="gpt-4-vision">GPT-4 Vision</a-select-option>
                          <a-select-option value="claude-3-vision">Claude-3 Vision</a-select-option>
                          <a-select-option value="qwen-vl">通义千问 VL</a-select-option>
                        </a-select>
                      </a-form-item>
                    </a-form>
                  </div>

                  <!-- 本地视觉模型配置 -->
                  <div v-if="visionConfig.type === 'local'" class="setting-section">
                    <h3>本地视觉模型</h3>
                    <a-form layout="vertical">
                      <a-form-item label="模型类型">
                        <a-select
                          v-model:value="visionConfig.local.model"
                          placeholder="选择模型"
                        >
                          <a-select-option value="clip-vit-base">CLIP ViT-Base</a-select-option>
                          <a-select-option value="clip-vit-large">CLIP ViT-Large</a-select-option>
                          <a-select-option value="openclip">OpenCLIP</a-select-option>
                        </a-select>
                      </a-form-item>
                      <a-form-item label="设备">
                        <a-radio-group v-model:value="visionConfig.local.device">
                          <a-radio value="cpu">CPU</a-radio>
                          <a-radio value="cuda">CUDA</a-radio>
                          <a-radio value="mps">MPS (Apple Silicon)</a-radio>
                        </a-radio-group>
                      </a-form-item>
                    </a-form>

                    <div class="local-model-actions">
                      <a-button
                        type="primary"
                        @click="enableLocalVision"
                        :loading="isEnablingVision"
                      >
                        <template #icon><ThunderboltOutlined /></template>
                        一键启用
                      </a-button>
                    </div>
                  </div>

                  <div class="setting-actions">
                    <a-button type="primary" @click="saveSettings">
                      <template #icon><SaveOutlined /></template>
                      保存
                    </a-button>
                  </div>
                </div>

                <!-- 通用设置 -->
                <div v-show="selectedKeys[0] === 'general'" class="setting-panel">
                  <div class="panel-header">
                    <h2>通用设置</h2>
                    <p>应用程序常规配置</p>
                  </div>

                  <div class="setting-section">
                    <h3>界面设置</h3>
                    <a-form layout="vertical">
                      <a-form-item label="主题">
                        <a-radio-group v-model:value="generalConfig.theme">
                          <a-radio value="light">
                            <template #icon><SunOutlined /></template>
                            浅色主题
                          </a-radio>
                          <a-radio value="dark">
                            <template #icon><MoonOutlined /></template>
                            深色主题
                          </a-radio>
                          <a-radio value="auto">
                            <template #icon><BulbOutlined /></template>
                            跟随系统
                          </a-radio>
                        </a-radio-group>
                      </a-form-item>
                      <a-form-item label="语言">
                        <a-select
                          v-model:value="generalConfig.language"
                          placeholder="选择语言"
                        >
                          <a-select-option value="zh-CN">简体中文</a-select-option>
                          <a-select-option value="en-US">English</a-select-option>
                          <a-select-option value="ja-JP">日本語</a-select-option>
                        </a-select>
                      </a-form-item>
                    </a-form>
                  </div>

                  <div class="setting-section">
                    <h3>性能设置</h3>
                    <a-form layout="vertical">
                      <a-form-item label="搜索结果数量">
                        <a-input-number
                          v-model:value="generalConfig.maxResults"
                          :min="5"
                          :max="50"
                          style="width: 200px"
                        />
                      </a-form-item>
                      <a-form-item label="并行搜索线程数">
                        <a-input-number
                          v-model:value="generalConfig.searchThreads"
                          :min="1"
                          :max="8"
                          style="width: 200px"
                        />
                      </a-form-item>
                    </a-form>
                  </div>

                  <div class="setting-actions">
                    <a-button @click="resetToDefault">
                      <template #icon><ReloadOutlined /></template>
                      恢复默认
                    </a-button>
                    <a-button type="primary" @click="saveSettings">
                      <template #icon><SaveOutlined /></template>
                      保存
                    </a-button>
                  </div>
                </div>

                <!-- 隐私设置 -->
                <div v-show="selectedKeys[0] === 'privacy'" class="setting-panel">
                  <div class="panel-header">
                    <h2>隐私设置</h2>
                    <p>保护您的数据和隐私</p>
                  </div>

                  <div class="setting-section">
                    <h3>数据保护</h3>
                    <a-form layout="vertical">
                      <a-form-item>
                        <a-checkbox v-model:checked="privacyConfig.encryptLocalData">
                          本地数据加密存储
                        </a-checkbox>
                      </a-form-item>
                      <a-form-item>
                        <a-checkbox v-model:checked="privacyConfig.secureApiKey">
                          安全保存API密钥
                        </a-checkbox>
                      </a-form-item>
                      <a-form-item>
                        <a-checkbox v-model:checked="privacyConfig.noCloudUpload">
                          用户数据不上传云端
                        </a-checkbox>
                      </a-form-item>
                    </a-form>
                  </div>

                  <div class="setting-section">
                    <h3>搜索历史</h3>
                    <a-form layout="vertical">
                      <a-form-item>
                        <a-checkbox v-model:checked="privacyConfig.enableSearchHistory">
                          保存搜索历史
                        </a-checkbox>
                      </a-form-item>
                      <a-form-item>
                        <a-checkbox v-model:checked="privacyConfig.anonymousTelemetry">
                          发送匿名使用统计
                        </a-checkbox>
                      </a-form-item>
                    </a-form>

                    <div class="privacy-actions">
                      <a-button @click="clearSearchHistory" danger>
                        <template #icon><DeleteOutlined /></template>
                        清除搜索历史
                      </a-button>
                      <a-button @click="exportData">
                        <template #icon><ExportOutlined /></template>
                        导出数据
                      </a-button>
                    </div>
                  </div>

                  <div class="setting-actions">
                    <a-button type="primary" @click="saveSettings">
                      <template #icon><SaveOutlined /></template>
                      保存
                    </a-button>
                  </div>
                </div>
              </a-layout-content>
            </a-layout>
          </div>
        </a-layout-content>
      </a-layout>
    </div>
  </a-config-provider>
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
  ShieldCheckOutlined,
  CloudOutlined,
  DesktopOutlined,
  ApiOutlined,
  SaveOutlined,
  ReloadOutlined,
  ThunderboltOutlined,
  DownloadOutlined,
  SunOutlined,
  MoonOutlined,
  BulbOutlined,
  DeleteOutlined,
  ExportOutlined
} from '@ant-design/icons-vue'

// 状态管理
const selectedKeys = ref(['model'])
const openKeys = ref([])
const isTesting = ref(false)
const isLoadingModels = ref(false)
const isEnablingWhisper = ref(false)
const isDownloadingModel = ref(false)
const isEnablingVision = ref(false)

// LLM配置
const llmConfig = reactive({
  type: 'cloud',
  cloud: {
    apiUrl: 'https://api.openai.com',
    apiKey: '',
    model: 'gpt-4',
    maxTokens: 4096
  },
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
    device: 'cpu',
    enabled: false
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

// 菜单切换
const onOpenChange = (keys: string[]) => {
  openKeys.value = keys
}

// LLM类型切换
const handleLlmTypeChange = (e: any) => {
  llmConfig.type = e.target.value
}

// 语音类型切换
const handleVoiceTypeChange = (e: any) => {
  voiceConfig.type = e.target.value
}

// 测试连接
const testConnection = async () => {
  isTesting.value = true
  try {
    // 模拟测试连接
    await new Promise(resolve => setTimeout(resolve, 2000))
    message.success('连接测试成功')
  } catch (error) {
    message.error('连接测试失败')
  } finally {
    isTesting.value = false
  }
}

// 刷新模型列表
const refreshModels = async () => {
  isLoadingModels.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1500))
    message.success('模型列表已刷新')
  } catch (error) {
    message.error('刷新模型列表失败')
  } finally {
    isLoadingModels.value = false
  }
}

// 启用本地Whisper
const enableLocalWhisper = async () => {
  isEnablingWhisper.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 3000))
    voiceConfig.local.enabled = true
    message.success('本地FastWhisper已启用')
  } catch (error) {
    message.error('启用本地FastWhisper失败')
  } finally {
    isEnablingWhisper.value = false
  }
}

// 下载Whisper模型
const downloadWhisperModel = async () => {
  isDownloadingModel.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 5000))
    message.success('模型下载完成')
  } catch (error) {
    message.error('模型下载失败')
  } finally {
    isDownloadingModel.value = false
  }
}

// 测试录音
const testRecording = () => {
  message.info('开始测试录音功能...')
}

// 启用本地视觉模型
const enableLocalVision = async () => {
  isEnablingVision.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 3000))
    message.success('本地视觉模型已启用')
  } catch (error) {
    message.error('启用本地视觉模型失败')
  } finally {
    isEnablingVision.value = false
  }
}

// 清除搜索历史
const clearSearchHistory = () => {
  message.success('搜索历史已清除')
}

// 导出数据
const exportData = () => {
  message.success('数据导出完成')
}

// 恢复默认设置
const resetToDefault = () => {
  message.info('已恢复默认设置')
}

// 保存设置
const saveSettings = () => {
  message.success('设置已保存')
}

// 返回
const goBack = () => {
  message.info('返回上一页')
}

// 组件挂载
onMounted(() => {
  // 初始化设置
})
</script>

<style scoped>
.settings-app {
  min-height: 100vh;
  background: #f5f5f5;
}

.layout {
  min-height: 100vh;
}

.header {
  background: #fff;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
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
  background: #f5f5f5;
}

.settings-container {
  max-width: 1200px;
  margin: 0 auto;
}

.settings-sider {
  border-right: 1px solid #f0f0f0;
}

.settings-content {
  padding: 32px;
  overflow-y: auto;
  max-height: calc(100vh - 112px);
}

.setting-panel {
  max-width: 600px;
}

.panel-header {
  margin-bottom: 32px;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 16px;
}

.panel-header h2 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 24px;
  font-weight: 600;
}

.panel-header p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.setting-section {
  margin-bottom: 32px;
}

.setting-section h3 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.model-select-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.local-model-actions {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.privacy-actions {
  margin-top: 16px;
  display: flex;
  gap: 12px;
}

.setting-actions {
  display: flex;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

.setting-actions .ant-btn {
  min-width: 100px;
}

:deep(.ant-menu-item) {
  margin: 0;
  height: 48px;
  line-height: 48px;
}

:deep(.ant-menu-item-selected) {
  background-color: #f0f5ff;
  border-right: 3px solid #6366f1;
}

:deep(.ant-radio-wrapper) {
  display: flex;
  align-items: center;
  height: 32px;
  margin-right: 16px;
  margin-bottom: 8px;
}

:deep(.ant-form-item) {
  margin-bottom: 16px;
}

:deep(.ant-form-item-label > label) {
  font-weight: 500;
  color: #333;
}
</style>