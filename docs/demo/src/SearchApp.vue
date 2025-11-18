<template>
  <a-config-provider :theme="{ token: { colorPrimary: '#6366F1' } }">
    <div class="search-app">
      <a-layout class="layout">
        <!-- 头部导航 -->
        <a-layout-header class="header">
          <div class="header-content">
            <div class="logo">
              <span class="logo-icon">🔍</span>
              <span class="logo-text">小遥搜索</span>
              <span class="version">v1.0.0</span>
            </div>
            <div class="header-actions">
              <a-button type="text" @click="showSettings">
                <template #icon><SettingOutlined /></template>
              </a-button>
              <a-button type="text" @click="showHelp">
                <template #icon><QuestionCircleOutlined /></template>
              </a-button>
            </div>
          </div>
        </a-layout-header>

        <!-- 主要内容区 -->
        <a-layout-content class="content">
          <div class="search-container">
            <!-- 搜索输入区 -->
            <div class="search-section">
              <div class="search-input-wrapper">
                <a-input-group compact>
                  <a-button
                    :type="inputMode === 'voice' ? 'primary' : 'default'"
                    @click="startVoiceInput"
                    :loading="isRecording"
                    class="input-mode-btn"
                  >
                    <template #icon><AudioOutlined /></template>
                  </a-button>
                  <a-button
                    :type="inputMode === 'image' ? 'primary' : 'default'"
                    @click="selectImage"
                    class="input-mode-btn"
                  >
                    <template #icon><PictureOutlined /></template>
                  </a-button>
                  <a-input
                    v-model:value="searchQuery"
                    placeholder="请描述您要搜索的内容..."
                    size="large"
                    class="search-input"
                    @pressEnter="handleSearch"
                    @focus="inputMode = 'text'"
                  >
                    <template #suffix>
                      <a-button
                        type="primary"
                        :loading="isSearching"
                        @click="handleSearch"
                        size="small"
                      >
                        搜索
                      </a-button>
                    </template>
                  </a-input>
                </a-input-group>
              </div>

              <!-- AI模型和搜索范围设置 -->
              <div class="search-settings">
                <a-tag color="blue">
                  <template #icon><RobotOutlined /></template>
                  AI模型: {{ currentModel }}
                </a-tag>
                <a-tag color="green">
                  <template #icon><FolderOutlined /></template>
                  搜索范围: {{ searchScope }}
                </a-tag>
              </div>
            </div>

            <!-- 搜索结果区 -->
            <div class="results-section">
              <div class="results-header" v-if="searchResults.length > 0">
                <span class="results-count">找到 {{ searchResults.length }} 个结果</span>
                <span class="search-time">用时 {{ searchTime }}s</span>
              </div>

              <div class="results-list" v-if="searchResults.length > 0">
                <div
                  v-for="(result, index) in searchResults"
                  :key="index"
                  class="result-item"
                >
                  <a-card
                    class="result-card"
                    :hoverable="true"
                    @click="selectResult(result)"
                  >
                    <template #title>
                      <div class="result-title">
                        <span class="file-icon">{{ getFileIcon(result.type) }}</span>
                        <span class="file-name">{{ result.name }}</span>
                        <a-tag color="orange" class="match-score">
                          {{ result.score }}% 匹配
                        </a-tag>
                      </div>
                    </template>

                    <div class="result-content">
                      <p class="result-description">{{ result.description }}</p>
                      <div class="result-meta">
                        <span class="file-size">{{ result.size }}</span>
                        <span class="file-date">{{ result.date }}</span>
                      </div>
                    </div>

                    <template #actions>
                      <a-button size="small" @click.stop="previewFile(result)">
                        <template #icon><EyeOutlined /></template>
                        预览
                      </a-button>
                      <a-button size="small" @click.stop="openFile(result)">
                        <template #icon><FolderOpenOutlined /></template>
                        打开位置
                      </a-button>
                      <a-button size="small" @click.stop="toggleFavorite(result)">
                        <template #icon>
                          <StarOutlined v-if="!result.isFavorite" />
                          <StarFilled v-else style="color: #fadb14;" />
                        </template>
                        {{ result.isFavorite ? '已收藏' : '收藏' }}
                      </a-button>
                    </template>
                  </a-card>
                </div>
              </div>

              <!-- 空状态 -->
              <a-empty
                v-else-if="!isSearching && searchQuery"
                description="未找到相关文件"
                class="empty-state"
              >
                <template #image>
                  <SearchOutlined style="font-size: 64px; color: #d9d9d9;" />
                </template>
              </a-empty>

              <!-- 初始状态 -->
              <a-empty
                v-else-if="!searchQuery"
                description="开始搜索您的文件"
                class="empty-state"
              >
                <template #image>
                  <RobotOutlined style="font-size: 64px; color: #6366f1;" />
                </template>
              </a-empty>
            </div>
          </div>
        </a-layout-content>

        <!-- 底部状态栏 -->
        <a-layout-footer class="footer">
          <div class="footer-content">
            <a-tag color="success">
              <template #icon><CheckCircleOutlined /></template>
              模型就绪
            </a-tag>
            <span class="status-text">已索引 {{ indexedFiles }} 个文件</span>
            <span class="status-text">搜索历史: {{ searchHistory }} 次</span>
          </div>
        </a-layout-footer>
      </a-layout>

      <!-- 语音录制弹窗 -->
      <a-modal
        v-model:open="showRecordingModal"
        title="语音录制"
        :footer="null"
        centered
        width="400px"
      >
        <div class="recording-content">
          <div class="recording-icon">
            <AudioOutlined style="font-size: 48px; color: #ff4d4f;" />
          </div>
          <div class="recording-timer">{{ recordingTime }} / 30s</div>
          <a-button
            type="primary"
            danger
            block
            size="large"
            @click="stopRecording"
          >
            停止录音
          </a-button>
        </div>
      </a-modal>

      <!-- 图片上传弹窗 -->
      <a-modal
        v-model:open="showImageModal"
        title="图片搜索"
        @ok="confirmImageSearch"
        @cancel="cancelImageSearch"
        centered
        width="500px"
      >
        <div class="image-upload-content">
          <a-upload
            v-model:file-list="imageFiles"
            list-type="picture-card"
            :before-upload="beforeImageUpload"
            :max-count="1"
            class="image-uploader"
          >
            <div v-if="imageFiles.length < 1">
              <PictureOutlined style="font-size: 24px;" />
              <div style="margin-top: 8px">上传图片</div>
            </div>
          </a-upload>
          <div class="upload-tip">
            支持 PNG、JPG 格式，最大 5MB
          </div>
        </div>
      </a-modal>

      <!-- 文件预览弹窗 -->
      <a-modal
        v-model:open="showPreviewModal"
        :title="currentPreviewFile?.name"
        @cancel="closePreview"
        :footer="null"
        centered
        width="800px"
      >
        <div class="preview-content">
          <pre class="preview-text">{{ previewContent }}</pre>
        </div>
      </a-modal>
    </div>
  </a-config-provider>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import {
  SettingOutlined,
  QuestionCircleOutlined,
  AudioOutlined,
  PictureOutlined,
  RobotOutlined,
  FolderOutlined,
  EyeOutlined,
  FolderOpenOutlined,
  StarOutlined,
  StarFilled,
  SearchOutlined,
  CheckCircleOutlined
} from '@ant-design/icons-vue'

// 状态管理
const searchQuery = ref('')
const inputMode = ref<'text' | 'voice' | 'image'>('text')
const isSearching = ref(false)
const isRecording = ref(false)
const recordingTime = ref('00:00')
const showRecordingModal = ref(false)
const showImageModal = ref(false)
const showPreviewModal = ref(false)
const imageFiles = ref([])
const previewContent = ref('')
const currentPreviewFile = ref(null)

// 配置信息
const currentModel = ref('GPT-4')
const searchScope = ref('所有文件夹')
const indexedFiles = ref(1234)
const searchHistory = ref(15)
const searchTime = ref(0.8)

// 搜索结果
const searchResults = reactive([
  {
    name: 'AI趋势讨论_2024-11-15.mp3',
    type: 'audio',
    score: 95,
    description: '昨天录制的关于AI发展趋势的团队讨论，包含大模型、商业化前景等内容...',
    size: '12.5 MB',
    date: '2024-11-15',
    path: '/Documents/AI趋势讨论_2024-11-15.mp3',
    isFavorite: false
  },
  {
    name: 'API设计文档_v2.1.md',
    type: 'document',
    score: 87,
    description: '讨论的API接口设计优化方案和实施细节，包含接口规范、数据结构定义...',
    size: '245 KB',
    date: '2024-11-10',
    path: '/Projects/API设计文档_v2.1.md',
    isFavorite: true
  },
  {
    name: '机器学习算法优化.pdf',
    type: 'document',
    score: 82,
    description: '详细介绍机器学习算法的优化方法和实践案例，涵盖梯度下降、正则化技术...',
    size: '3.2 MB',
    date: '2024-11-08',
    path: '/Documents/机器学习算法优化.pdf',
    isFavorite: false
  }
])

// 获取文件图标
const getFileIcon = (type: string) => {
  const icons = {
    audio: '🎵',
    video: '🎬',
    document: '📄',
    image: '🖼️',
    code: '💻',
    default: '📁'
  }
  return icons[type] || icons.default
}

// 开始语音输入
const startVoiceInput = () => {
  inputMode.value = 'voice'
  showRecordingModal.value = true
  isRecording.value = true
  recordingTime.value = '00:00'

  // 模拟录音计时
  let seconds = 0
  const timer = setInterval(() => {
    seconds++
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    recordingTime.value = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`

    if (seconds >= 30) {
      clearInterval(timer)
      stopRecording()
    }
  }, 1000)

  // 保存定时器ID以便清理
  ;(window as any).recordingTimer = timer
}

// 停止录音
const stopRecording = () => {
  isRecording.value = false
  showRecordingModal.value = false

  // 清理定时器
  if ((window as any).recordingTimer) {
    clearInterval((window as any).recordingTimer)
  }

  // 模拟语音转文字
  searchQuery.value = '昨天录制的关于AI趋势的讨论'
  message.success('语音识别完成')
  inputMode.value = 'text'
}

// 选择图片
const selectImage = () => {
  inputMode.value = 'image'
  showImageModal.value = true
}

// 图片上传前检查
const beforeImageUpload = (file: any) => {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
  if (!isJpgOrPng) {
    message.error('只能上传 JPG/PNG 格式的图片!')
    return false
  }
  const isLt5M = file.size / 1024 / 1024 < 5
  if (!isLt5M) {
    message.error('图片大小不能超过 5MB!')
    return false
  }
  return false // 阻止自动上传
}

// 确认图片搜索
const confirmImageSearch = () => {
  if (imageFiles.value.length === 0) {
    message.warning('请先上传图片')
    return
  }

  showImageModal.value = false
  searchQuery.value = '搜索相似图片'
  handleSearch()
  message.success('图片上传成功，开始搜索')
}

// 取消图片搜索
const cancelImageSearch = () => {
  imageFiles.value = []
  showImageModal.value = false
  inputMode.value = 'text'
}

// 执行搜索
const handleSearch = () => {
  if (!searchQuery.value.trim()) {
    message.warning('请输入搜索内容')
    return
  }

  isSearching.value = true

  // 模拟搜索过程
  setTimeout(() => {
    isSearching.value = false
    searchTime.value = (Math.random() * 1.5 + 0.3).toFixed(1)
    searchHistory.value++
    message.success(`搜索完成，找到 ${searchResults.length} 个结果`)
  }, 1000)
}

// 选择搜索结果
const selectResult = (result: any) => {
  currentPreviewFile.value = result
  showPreviewModal.value = true
  previewContent.value = `文件名: ${result.name}\n文件大小: ${result.size}\n修改时间: ${result.date}\n文件路径: ${result.path}\n\n文件描述:\n${result.description}\n\n匹配度: ${result.score}%`
}

// 预览文件
const previewFile = (result: any) => {
  selectResult(result)
}

// 打开文件
const openFile = (result: any) => {
  message.info(`打开文件位置: ${result.path}`)
}

// 切换收藏状态
const toggleFavorite = (result: any) => {
  result.isFavorite = !result.isFavorite
  message.success(result.isFavorite ? '已添加到收藏' : '已取消收藏')
}

// 关闭预览
const closePreview = () => {
  showPreviewModal.value = false
  currentPreviewFile.value = null
  previewContent.value = ''
}

// 显示设置
const showSettings = () => {
  message.info('打开设置页面')
}

// 显示帮助
const showHelp = () => {
  message.info('打开帮助页面')
}

// 组件挂载
onMounted(() => {
  // 初始化操作
})
</script>

<style scoped>
.search-app {
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

.version {
  font-size: 12px;
  color: #999;
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 4px;
}

.content {
  padding: 24px;
  background: #f5f5f5;
}

.search-container {
  max-width: 800px;
  margin: 0 auto;
}

.search-section {
  background: #fff;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 24px;
}

.search-input-wrapper {
  margin-bottom: 16px;
}

.input-mode-btn {
  width: 48px;
}

.search-input {
  flex: 1;
}

.search-settings {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.results-section {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.results-header {
  padding: 16px 24px;
  background: #fafafa;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.results-count {
  font-weight: 500;
  color: #333;
}

.search-time {
  color: #999;
  font-size: 12px;
}

.results-list {
  padding: 16px;
}

.result-item {
  margin-bottom: 16px;
}

.result-card {
  border: 1px solid #f0f0f0;
  transition: all 0.2s;
}

.result-card:hover {
  border-color: #6366f1;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
}

.result-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-icon {
  font-size: 18px;
}

.file-name {
  flex: 1;
  font-weight: 500;
}

.match-score {
  font-size: 12px;
}

.result-description {
  color: #666;
  margin-bottom: 12px;
  line-height: 1.5;
}

.result-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #999;
}

.empty-state {
  padding: 60px 0;
}

.footer {
  background: #fff;
  padding: 16px 0;
  border-top: 1px solid #f0f0f0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-text {
  color: #666;
  font-size: 12px;
}

.recording-content {
  text-align: center;
  padding: 24px 0;
}

.recording-icon {
  margin-bottom: 16px;
}

.recording-timer {
  font-size: 24px;
  font-weight: 500;
  color: #ff4d4f;
  margin-bottom: 24px;
}

.image-upload-content {
  text-align: center;
}

.image-uploader {
  margin-bottom: 16px;
}

.upload-tip {
  color: #999;
  font-size: 12px;
}

.preview-content {
  max-height: 500px;
  overflow-y: auto;
}

.preview-text {
  white-space: pre-wrap;
  word-wrap: break-word;
  background: #f8f9fa;
  padding: 16px;
  border-radius: 6px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 12px;
  line-height: 1.5;
  margin: 0;
}
</style>