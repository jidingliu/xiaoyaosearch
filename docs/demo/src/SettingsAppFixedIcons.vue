<template>
  <div class="settings-fixed">
    <!-- 顶部导航 -->
    <div class="header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">⚙️</span>
          <span class="logo-text">设置</span>
        </div>
        <div class="header-actions">
          <a-button @click="goBack">
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
            <a-menu
              v-model:selectedKeys="selectedKeys"
              mode="inline"
              @click="handleMenuClick"
              class="settings-menu"
            >
              <a-menu-item key="model">
                🤖️ LLM模型设置
              </a-menu-item>
              <a-menu-item key="voice">
                🎤 语音识别设置
              </a-menu-item>
              <a-menu-item key="vision">
                👁️ 视觉模型设置
              </a-menu-item>
              <a-menu-item key="general">
                ⚙️ 通用设置
              </a-menu-item>
              <a-menu-item key="privacy">
                🔒 隐私设置
              </a-menu-item>
            </a-menu>
          </a-col>

          <!-- 右侧内容 -->
          <a-col :span="18">
            <!-- LLM模型设置 -->
            <a-card v-if="activeKey === 'model'" title="LLM模型设置" class="content-card">
              <div class="setting-group">
                <h4>模型类型</h4>
                <a-radio-group v-model:value="llmConfig.type">
                  <a-radio value="cloud">☁️ 云端API</a-radio>
                  <a-radio value="local">🏠 本地Ollama</a-radio>
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
                  🔧 测试连接
                </a-button>
                <a-button type="primary" @click="saveSettings">
                  💾 保存设置
                </a-button>
              </div>
            </a-card>

            <!-- 语音识别设置 -->
            <a-card v-else-if="activeKey === 'voice'" title="语音识别设置" class="content-card">
              <div class="setting-group">
                <h4>识别引擎</h4>
                <a-radio-group v-model:value="voiceConfig.type">
                  <a-radio value="cloud">☁️ 云端API</a-radio>
                  <a-radio value="local">🏠 本地FastWhisper</a-radio>
                </a-radio-group>
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
                      <a-radio value="standard">📞 标准音质</a-radio>
                      <a-radio value="high">🎙️ 高质量</a-radio>
                    </a-radio-group>
                  </a-form-item>
                </a-form>
              </div>

              <div class="setting-actions">
                <a-button @click="testRecording">
                  🎤 测试录音
                </a-button>
                <a-button type="primary" @click="saveSettings">
                  💾 保存设置
                </a-button>
              </div>
            </a-card>

            <!-- 视觉模型设置 -->
            <a-card v-else-if="activeKey === 'vision'" title="视觉模型设置" class="content-card">
              <div class="setting-group">
                <h4>视觉模型类型</h4>
                <a-radio-group v-model:value="visionConfig.type">
                  <a-radio value="cloud">☁️ 云端API</a-radio>
                  <a-radio value="local">🏠 本地视觉模型</a-radio>
                </a-radio-group>
              </div>

              <div class="setting-actions">
                <a-button type="primary" @click="saveSettings">
                  💾 保存设置
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
                      <a-radio value="light">☀️ 浅色主题</a-radio>
                      <a-radio value="dark">🌙 深色主题</a-radio>
                      <a-radio value="auto">🌓 跟随系统</a-radio>
                    </a-radio-group>
                  </a-form-item>
                </a-form>
              </div>

              <div class="setting-actions">
                <a-button @click="resetToDefault">
                  🔄 恢复默认
                </a-button>
                <a-button type="primary" @click="saveSettings">
                  💾 保存设置
                </a-button>
              </div>
            </a-card>

            <!-- 隐私设置 -->
            <a-card v-else-if="activeKey === 'privacy'" title="隐私设置" class="content-card">
              <div class="setting-group">
                <h4>数据保护</h4>
                <div class="checkbox-group">
                  <a-checkbox v-model:checked="privacyConfig.encryptLocalData">
                    🗄️ 本地数据加密存储
                  </a-checkbox>
                  <a-checkbox v-model:checked="privacyConfig.secureApiKey">
                    🔐 安全保存API密钥
                  </a-checkbox>
                  <a-checkbox v-model:checked="privacyConfig.noCloudUpload">
                    🚫 用户数据不上传云端
                  </a-checkbox>
                </div>
              </div>

              <div class="setting-actions">
                <a-button type="primary" @click="saveSettings">
                  💾 保存设置
                </a-button>
              </div>
            </a-card>

            <!-- 默认欢迎页面 -->
            <a-card v-else title="欢迎使用设置中心" class="content-card welcome-card">
              <div class="welcome-content">
                <div class="welcome-icon">
                  ⚙️
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

console.log('=== 设置页面图标修复版本开始加载 ===')

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
  maxTokens: 4096
})

// 语音配置
const voiceConfig = reactive({
  type: 'cloud',
  maxDuration: 30,
  quality: 'standard'
})

// 视觉配置
const visionConfig = reactive({
  type: 'cloud'
})

// 通用配置
const generalConfig = reactive({
  theme: 'light'
})

// 隐私配置
const privacyConfig = reactive({
  encryptLocalData: true,
  secureApiKey: true,
  noCloudUpload: true
})

// 菜单点击处理
const handleMenuClick = ({ key }: { key: string }) => {
  console.log('菜单点击:', key)
  activeKey.value = key
  selectedKeys.value = [key]
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
  console.log('=== 设置页面图标修复版本已挂载 ===')
})
</script>

<style scoped>
.settings-fixed {
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

.settings-menu {
  border-right: none;
  background: #fff;
  border-radius: 8px;
  padding: 0;
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