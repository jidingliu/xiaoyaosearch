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
                theme="light"
                width="240"
                class="settings-sider"
              >
                <a-menu
                  v-model:selectedKeys="selectedKeys"
                  mode="inline"
                  @click="handleMenuClick"
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
                <div v-if="activeKey === 'model'" class="setting-panel">
                  <div class="panel-header">
                    <h2>LLM模型设置</h2>
                    <p>配置用于语义理解的AI模型</p>
                  </div>

                  <div class="setting-section">
                    <h3>模型类型</h3>
                    <a-radio-group v-model:value="llmConfig.type">
                      <a-radio value="cloud">云端API</a-radio>
                      <a-radio value="local">本地Ollama</a-radio>
                    </a-radio-group>
                  </div>

                  <div class="setting-section">
                    <h3>配置信息</h3>
                    <a-form layout="vertical">
                      <a-form-item label="API地址">
                        <a-input v-model:value="llmConfig.apiUrl" placeholder="请输入API地址" />
                      </a-form-item>
                      <a-form-item label="访问令牌">
                        <a-input-password v-model:value="llmConfig.apiKey" placeholder="请输入访问令牌" />
                      </a-form-item>
                    </a-form>
                  </div>

                  <div class="setting-actions">
                    <a-button @click="testConnection" :loading="isTesting">测试连接</a-button>
                    <a-button type="primary" @click="saveSettings">保存</a-button>
                  </div>
                </div>

                <!-- 语音识别设置 -->
                <div v-else-if="activeKey === 'voice'" class="setting-panel">
                  <div class="panel-header">
                    <h2>语音识别设置</h2>
                    <p>配置语音转文字引擎</p>
                  </div>

                  <div class="setting-section">
                    <h3>识别引擎</h3>
                    <a-radio-group v-model:value="voiceConfig.type">
                      <a-radio value="cloud">云端API</a-radio>
                      <a-radio value="local">本地FastWhisper</a-radio>
                    </a-radio-group>
                  </div>

                  <div class="setting-section">
                    <h3>录音设置</h3>
                    <a-form layout="vertical">
                      <a-form-item label="最长录音时间">
                        <a-input-number
                          v-model:value="voiceConfig.maxDuration"
                          :min="10"
                          :max="60"
                          suffix="秒"
                        />
                      </a-form-item>
                    </a-form>
                  </div>

                  <div class="setting-actions">
                    <a-button @click="testRecording">测试录音</a-button>
                    <a-button type="primary" @click="saveSettings">保存</a-button>
                  </div>
                </div>

                <!-- 视觉模型设置 -->
                <div v-else-if="activeKey === 'vision'" class="setting-panel">
                  <div class="panel-header">
                    <h2>视觉模型设置</h2>
                    <p>配置图片理解和搜索模型</p>
                  </div>

                  <div class="setting-section">
                    <h3>视觉模型类型</h3>
                    <a-radio-group v-model:value="visionConfig.type">
                      <a-radio value="cloud">云端API</a-radio>
                      <a-radio value="local">本地视觉模型</a-radio>
                    </a-radio-group>
                  </div>

                  <div class="setting-actions">
                    <a-button type="primary" @click="saveSettings">保存</a-button>
                  </div>
                </div>

                <!-- 通用设置 -->
                <div v-else-if="activeKey === 'general'" class="setting-panel">
                  <div class="panel-header">
                    <h2>通用设置</h2>
                    <p>应用程序常规配置</p>
                  </div>

                  <div class="setting-section">
                    <h3>界面设置</h3>
                    <a-form layout="vertical">
                      <a-form-item label="主题">
                        <a-radio-group v-model:value="generalConfig.theme">
                          <a-radio value="light">浅色主题</a-radio>
                          <a-radio value="dark">深色主题</a-radio>
                          <a-radio value="auto">跟随系统</a-radio>
                        </a-radio-group>
                      </a-form-item>
                    </a-form>
                  </div>

                  <div class="setting-actions">
                    <a-button @click="resetToDefault">恢复默认</a-button>
                    <a-button type="primary" @click="saveSettings">保存</a-button>
                  </div>
                </div>

                <!-- 隐私设置 -->
                <div v-else-if="activeKey === 'privacy'" class="setting-panel">
                  <div class="panel-header">
                    <h2>隐私设置</h2>
                    <p>保护您的数据和隐私</p>
                  </div>

                  <div class="setting-section">
                    <h3>数据保护</h3>
                    <a-checkbox-group v-model:value="privacyConfig.options">
                      <a-checkbox value="encrypt">本地数据加密存储</a-checkbox>
                      <a-checkbox value="secure">安全保存API密钥</a-checkbox>
                      <a-checkbox value="noCloud">用户数据不上传云端</a-checkbox>
                    </a-checkbox-group>
                  </div>

                  <div class="setting-actions">
                    <a-button type="primary" @click="saveSettings">保存</a-button>
                  </div>
                </div>

                <!-- 默认显示 -->
                <div v-else class="setting-panel">
                  <div class="panel-header">
                    <h2>设置</h2>
                    <p>请从左侧菜单选择要配置的设置项</p>
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
  ShieldCheckOutlined
} from '@ant-design/icons-vue'

// 状态管理
const selectedKeys = ref(['model'])
const activeKey = ref('model')
const isTesting = ref(false)

// 配置数据
const llmConfig = reactive({
  type: 'cloud',
  apiUrl: 'https://api.openai.com',
  apiKey: ''
})

const voiceConfig = reactive({
  type: 'cloud',
  maxDuration: 30
})

const visionConfig = reactive({
  type: 'cloud'
})

const generalConfig = reactive({
  theme: 'light'
})

const privacyConfig = reactive({
  options: ['encrypt', 'secure', 'noCloud']
})

// 菜单点击处理
const handleMenuClick = ({ key }: { key: string }) => {
  activeKey.value = key
  console.log('菜单点击:', key)
}

// 测试连接
const testConnection = async () => {
  isTesting.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 2000))
    message.success('连接测试成功')
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

// 保存设置
const saveSettings = () => {
  message.success('设置已保存')
}

// 恢复默认
const resetToDefault = () => {
  message.info('已恢复默认设置')
}

// 返回
const goBack = () => {
  message.info('返回上一页')
}

// 组件挂载
onMounted(() => {
  console.log('设置页面组件已挂载')
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

.setting-actions {
  display: flex;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
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
</style>