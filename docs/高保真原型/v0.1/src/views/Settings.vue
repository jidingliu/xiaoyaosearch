<template>
  <div class="settings-container">
    <div class="settings-header">
      <h2>设置</h2>
      <p>配置小遥搜索的各项参数和AI模型</p>
    </div>

    <a-tabs v-model:activeKey="activeTab" type="card" class="settings-tabs">
      <!-- 模型设置 -->
      <a-tab-pane key="models" tab="AI模型设置">
        <div class="settings-section">
          <h3>LLM模型配置</h3>
          <a-form layout="vertical" class="model-form">
            <a-form-item label="模型类型">
              <a-radio-group v-model:value="llmSettings.provider">
                <a-radio value="cloud">云端API</a-radio>
                <a-radio value="local">本地Ollama</a-radio>
              </a-radio-group>
            </a-form-item>

            <!-- 云端API配置 -->
            <div v-if="llmSettings.provider === 'cloud'" class="api-config">
              <h4>云端API配置</h4>
              <a-form-item label="API地址">
                <a-input v-model:value="llmSettings.apiEndpoint" placeholder="https://api.openai.com" />
              </a-form-item>
              <a-form-item label="访问密钥">
                <a-password v-model:value="llmSettings.apiKey" placeholder="sk-*********************" />
              </a-form-item>
              <a-form-item label="模型名称">
                <a-select v-model:value="llmSettings.modelName" style="width: 100%">
                  <a-select value="gpt-4">GPT-4</a-select>
                  <a-select value="gpt-3.5-turbo">GPT-3.5 Turbo</a-select>
                  <a-select value="claude-3">Claude 3</a-select>
                </a-select>
              </a-form-item>
              <a-form-item label="最大Token">
                <a-input-number v-model:value="llmSettings.maxTokens" :min="512" :max="8192" style="width: 100%" />
              </a-form-item>
            </div>

            <!-- 本地Ollama配置 -->
            <div v-else class="ollama-config">
              <h4>本地Ollama配置</h4>
              <a-form-item label="API地址">
                <a-input v-model:value="llmSettings.ollamaEndpoint" placeholder="http://localhost:11434" />
              </a-form-item>
              <a-form-item label="模型名称">
                <a-select v-model:value="llmSettings.ollamaModel" style="width: 100%">
                  <a-select value="qwen2.5:7b">Qwen2.5 7B</a-select>
                  <a-select value="llama3:8b">Llama3 8B</a-select>
                  <a-select value="mixtral:8x7b">Mixtral 8x7B</a-select>
                </a-select>
              </a-form-item>
              <a-form-item>
                <a-button type="link">下载更多模型</a-button>
              </a-form-item>
            </div>

            <a-form-item>
              <a-space>
                <a-button type="primary" @click="testConnection" :loading="testingConnection">
                  <ApiOutlined />
                  测试连接
                </a-button>
                <a-button @click="saveLLMSettings">保存设置</a-button>
              </a-space>
            </a-form-item>
          </a-form>
        </div>

        <!-- 语音设置 -->
        <div class="settings-section">
          <h3>语音识别设置</h3>
          <a-form layout="vertical">
            <a-form-item label="识别引擎">
              <a-radio-group v-model:value="speechSettings.provider">
                <a-radio value="cloud">云端API</a-radio>
                <a-radio value="local">本地FastWhisper</a-radio>
              </a-radio-group>
            </a-form-item>

            <div v-if="speechSettings.provider === 'cloud'" class="api-config">
              <a-form-item label="API地址">
                <a-input v-model:value="speechSettings.apiEndpoint" placeholder="https://api.speech.com" />
              </a-form-item>
              <a-form-item label="访问密钥">
                <a-password v-model:value="speechSettings.apiKey" placeholder="sk-*********************" />
              </a-form-item>
            </div>

            <div v-else class="local-config">
              <a-form-item label="模型大小">
                <a-select v-model:value="speechSettings.modelSize" style="width: 100%">
                  <a-select value="base">Base (快速)</a-select>
                  <a-select value="small">Small (平衡)</a-select>
                  <a-select value="medium">Medium (精确)</a-select>
                </a-select>
              </a-form-item>
              <a-form-item label="设备">
                <a-select v-model:value="speechSettings.device" style="width: 100%">
                  <a-select value="cpu">CPU</a-select>
                  <a-select value="cuda">CUDA (GPU)</a-select>
                  <a-select value="metal">Metal (Apple Silicon)</a-select>
                </a-select>
              </a-form-item>
              <a-form-item>
                <a-space>
                  <a-button type="primary" ghost>一键安装</a-button>
                  <a-button>检测可用性</a-button>
                </a-space>
              </a-form-item>
            </div>

            <a-form-item label="录音设置">
              <a-row :gutter="16">
                <a-col :span="12">
                  <a-form-item label="最长录音">
                    <a-input-number
                      v-model:value="speechSettings.maxDuration"
                      :min="5"
                      :max="120"
                      addon-after="秒"
                      style="width: 100%"
                    />
                  </a-form-item>
                </a-col>
                <a-col :span="12">
                  <a-form-item label="音质">
                    <a-select v-model:value="speechSettings.quality" style="width: 100%">
                      <a-select value="high">高质量</a-select>
                      <a-select value="standard">标准</a-select>
                    </a-select>
                  </a-form-item>
                </a-col>
              </a-row>
            </a-form-item>

            <a-form-item>
              <a-space>
                <a-button type="primary" @click="testRecording">
                  <AudioOutlined />
                  测试录音
                </a-button>
                <a-button @click="saveSpeechSettings">保存设置</a-button>
              </a-space>
            </a-form-item>
          </a-form>
        </div>
      </a-tab-pane>

      <!-- 通用设置 -->
      <a-tab-pane key="general" tab="通用设置">
        <div class="settings-section">
          <h3>搜索设置</h3>
          <a-form layout="vertical">
            <a-form-item label="默认返回结果数">
              <a-slider
                v-model:value="generalSettings.defaultResults"
                :min="10"
                :max="100"
                :step="10"
                :marks="{ 10: '10', 50: '50', 100: '100' }"
              />
            </a-form-item>
            <a-form-item label="相似度阈值">
              <a-slider
                v-model:value="generalSettings.threshold"
                :min="0"
                :max="1"
                :step="0.1"
                :tooltip-formatter="(value) => `${(value * 100).toFixed(0)}%`"
              />
            </a-form-item>
            <a-form-item label="最大文件大小">
              <a-input-number
                v-model:value="generalSettings.maxFileSize"
                :min="10"
                :max="100"
                addon-after="MB"
                style="width: 200px"
              />
            </a-form-item>
          </a-form>
        </div>

        <div class="settings-section">
          <h3>界面设置</h3>
          <a-form layout="vertical">
            <a-form-item label="主题">
              <a-radio-group v-model:value="generalSettings.theme">
                <a-radio value="light">浅色主题</a-radio>
                <a-radio value="dark">深色主题</a-radio>
                <a-radio value="auto">跟随系统</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item label="语言">
              <a-select v-model:value="generalSettings.language" style="width: 200px">
                <a-select value="zh-CN">简体中文</a-select>
                <a-select value="en-US">English</a-select>
              </a-select>
            </a-form-item>
            <a-form-item label="动画效果">
              <a-switch v-model:checked="generalSettings.enableAnimations" />
              <span class="form-help">启用界面动画和过渡效果</span>
            </a-form-item>
          </a-form>
        </div>

        <div class="settings-section">
          <h3>数据设置</h3>
          <a-form layout="vertical">
            <a-form-item label="搜索历史">
              <a-switch v-model:checked="generalSettings.saveHistory" />
              <span class="form-help">保存搜索历史记录</span>
            </a-form-item>
            <a-form-item label="自动清理">
              <a-switch v-model:checked="generalSettings.autoCleanup" />
              <span class="form-help">自动清理过期的搜索历史</span>
            </a-form-item>
            <a-form-item label="数据目录">
              <a-input
                v-model:value="generalSettings.dataPath"
                placeholder="选择数据存储目录"
                readonly
              />
              <a-button type="link" @click="selectDataPath">选择目录</a-button>
            </a-form-item>
          </a-form>

          <a-space>
            <a-button type="primary" @click="saveGeneralSettings">保存设置</a-button>
            <a-button @click="resetSettings">重置默认</a-button>
            <a-button danger @click="clearAllData">清空数据</a-button>
          </a-space>
        </div>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { message, Modal } from 'ant-design-vue'
import {
  ApiOutlined,
  AudioOutlined
} from '@ant-design/icons-vue'

// 响应式数据
const activeTab = ref('models')
const testingConnection = ref(false)

// LLM设置
const llmSettings = reactive({
  provider: 'local',
  apiEndpoint: 'https://api.openai.com',
  apiKey: '',
  modelName: 'gpt-4',
  maxTokens: 4096,
  ollamaEndpoint: 'http://localhost:11434',
  ollamaModel: 'qwen2.5:7b'
})

// 语音设置
const speechSettings = reactive({
  provider: 'local',
  apiEndpoint: 'https://api.speech.com',
  apiKey: '',
  modelSize: 'base',
  device: 'cpu',
  maxDuration: 30,
  quality: 'standard'
})

// 通用设置
const generalSettings = reactive({
  defaultResults: 20,
  threshold: 0.7,
  maxFileSize: 50,
  theme: 'light',
  language: 'zh-CN',
  enableAnimations: true,
  saveHistory: true,
  autoCleanup: true,
  dataPath: 'D:\\XiaoyaoSearch\\Data'
})

// 方法
const testConnection = async () => {
  testingConnection.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 2000))
    message.success('连接测试成功！')
  } catch (error) {
    message.error('连接测试失败，请检查配置')
  } finally {
    testingConnection.value = false
  }
}

const testRecording = () => {
  message.info('录音测试功能开发中...')
}

const saveLLMSettings = () => {
  message.success('LLM模型设置已保存')
}

const saveSpeechSettings = () => {
  message.success('语音设置已保存')
}

const saveGeneralSettings = () => {
  message.success('通用设置已保存')
}

const resetSettings = () => {
  Modal.confirm({
    title: '确认重置',
    content: '确定要重置所有设置为默认值吗？',
    onOk() {
      message.success('设置已重置')
    }
  })
}

const clearAllData = () => {
  Modal.confirm({
    title: '确认清空数据',
    content: '确定要清空所有数据吗？此操作不可恢复！',
    okType: 'danger',
    onOk() {
      message.success('数据已清空')
    }
  })
}

const selectDataPath = () => {
  message.info('目录选择功能开发中...')
}
</script>

<style scoped>
.settings-container {
  max-width: 800px;
  margin: 0 auto;
  padding: var(--space-6);
}

.settings-header {
  margin-bottom: var(--space-8);
}

.settings-header h2 {
  margin: 0 0 var(--space-2);
  color: var(--text-primary);
}

.settings-header p {
  margin: 0;
  color: var(--text-secondary);
}

.settings-tabs {
  background: var(--surface-01);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-base);
  overflow: hidden;
}

.settings-section {
  padding: var(--space-6);
  border-bottom: 1px solid var(--border-light);
}

.settings-section:last-child {
  border-bottom: none;
}

.settings-section h3 {
  margin: 0 0 var(--space-4);
  color: var(--text-primary);
  font-size: 1.125rem;
  font-weight: 600;
}

.settings-section h4 {
  margin: var(--space-4) 0 var(--space-3);
  color: var(--text-secondary);
  font-size: 1rem;
  font-weight: 500;
}

.api-config,
.ollama-config,
.local-config {
  background: var(--surface-02);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  margin: var(--space-3) 0;
}

.form-help {
  margin-left: var(--space-2);
  color: var(--text-tertiary);
  font-size: 0.875rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .settings-container {
    padding: var(--space-4);
  }

  .settings-section {
    padding: var(--space-4);
  }
}
</style>