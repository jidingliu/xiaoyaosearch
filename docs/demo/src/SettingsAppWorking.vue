<template>
  <div class="settings-working">
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
          <a-row :gutter="24">
            <!-- 左侧菜单 -->
            <a-col :span="6">
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
                  <template #icon><ShieldCheckOutlined /></template>
                  隐私设置
                </a-menu-item>
              </a-menu>
            </a-col>

            <!-- 右侧内容 -->
            <a-col :span="18">
              <div class="settings-content">
                <!-- 默认显示 -->
                <div v-if="!activeKey" class="welcome-panel">
                  <a-card>
                    <h2>欢迎使用设置中心</h2>
                    <p>请从左侧菜单选择要配置的设置项</p>
                  </a-card>
                </div>

                <!-- LLM模型设置 -->
                <div v-else-if="activeKey === 'model'">
                  <a-card title="LLM模型设置" class="settings-card">
                    <div class="setting-section">
                      <h4>模型类型</h4>
                      <a-radio-group v-model:value="llmConfig.type" @change="onLlmTypeChange">
                        <a-radio value="cloud">云端API</a-radio>
                        <a-radio value="local">本地Ollama</a-radio>
                      </a-radio-group>
                    </div>

                    <div class="setting-section">
                      <h4>API配置</h4>
                      <a-form layout="vertical">
                        <a-form-item label="API地址">
                          <a-input v-model:value="llmConfig.apiUrl" placeholder="https://api.openai.com" />
                        </a-form-item>
                        <a-form-item label="访问令牌">
                          <a-input-password v-model:value="llmConfig.apiKey" placeholder="sk-*********************" />
                        </a-form-item>
                        <a-form-item label="模型名称">
                          <a-select v-model:value="llmConfig.model" placeholder="选择模型">
                            <a-select-option value="gpt-4">GPT-4</a-select-option>
                            <a-select-option value="gpt-3.5-turbo">GPT-3.5 Turbo</a-select-option>
                          </a-select>
                        </a-form-item>
                      </a-form>
                    </div>

                    <div class="setting-actions">
                      <a-button @click="testConnection" :loading="isTesting">测试连接</a-button>
                      <a-button type="primary" @click="saveSettings">保存设置</a-button>
                    </div>
                  </a-card>
                </div>

                <!-- 语音识别设置 -->
                <div v-else-if="activeKey === 'voice'">
                  <a-card title="语音识别设置" class="settings-card">
                    <div class="setting-section">
                      <h4>识别引擎</h4>
                      <a-radio-group v-model:value="voiceConfig.type">
                        <a-radio value="cloud">云端API</a-radio>
                        <a-radio value="local">本地FastWhisper</a-radio>
                      </a-radio-group>
                    </div>

                    <div class="setting-section">
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
                      </a-form>
                    </div>

                    <div class="setting-actions">
                      <a-button @click="testRecording">测试录音</a-button>
                      <a-button type="primary" @click="saveSettings">保存设置</a-button>
                    </div>
                  </a-card>
                </div>

                <!-- 其他设置项的简化版本 -->
                <div v-else>
                  <a-card :title="getSettingTitle(activeKey)" class="settings-card">
                    <p>{{ getSettingDescription(activeKey) }}</p>
                    <div class="setting-actions">
                      <a-button type="primary" @click="saveSettings">保存设置</a-button>
                    </div>
                  </a-card>
                </div>
              </div>
            </a-col>
          </a-row>
        </div>
      </a-layout-content>
    </a-layout>
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
  ShieldCheckOutlined
} from '@ant-design/icons-vue'

// 状态管理
const selectedKeys = ref<string[]>(['model'])
const activeKey = ref<string>('model')
const isTesting = ref(false)

// LLM配置
const llmConfig = reactive({
  type: 'cloud',
  apiUrl: 'https://api.openai.com',
  apiKey: '',
  model: 'gpt-4'
})

// 语音配置
const voiceConfig = reactive({
  type: 'cloud',
  maxDuration: 30
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
const testConnection = () => {
  isTesting.value = true
  setTimeout(() => {
    isTesting.value = false
    message.success('连接测试成功')
  }, 2000)
}

// 测试录音
const testRecording = () => {
  message.info('开始测试录音功能...')
}

// 保存设置
const saveSettings = () => {
  console.log('保存设置:', {
    llm: llmConfig,
    voice: voiceConfig
  })
  message.success('设置已保存')
}

// 获取设置标题
const getSettingTitle = (key: string): string => {
  const titles = {
    vision: '视觉模型设置',
    general: '通用设置',
    privacy: '隐私设置'
  }
  return titles[key] || '设置'
}

// 获取设置描述
const getSettingDescription = (key: string): string => {
  const descriptions = {
    vision: '配置图片理解和搜索模型',
    general: '配置应用程序的常规选项',
    privacy: '配置数据隐私和安全选项'
  }
  return descriptions[key] || '设置配置'
}

// 返回
const goBack = () => {
  message.info('返回上一页')
}

// 组件挂载
onMounted(() => {
  console.log('设置页面组件已挂载 - 工作版本')
})
</script>

<style scoped>
.settings-working {
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
}

.settings-container {
  max-width: 1200px;
  margin: 0 auto;
}

.settings-menu {
  background: #fff;
  border-radius: 8px;
  padding: 16px 0;
  height: fit-content;
}

.settings-content {
  min-height: 600px;
}

.settings-card {
  margin-bottom: 24px;
}

.welcome-panel {
  text-align: center;
  padding: 60px 0;
}

.setting-section {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.setting-section:last-child {
  border-bottom: none;
}

.setting-section h4 {
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

:deep(.ant-form-item) {
  margin-bottom: 16px;
}

:deep(.ant-form-item-label > label) {
  font-weight: 500;
  color: #333;
}
</style>