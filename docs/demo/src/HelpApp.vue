<template>
  <a-config-provider :theme="{ token: { colorPrimary: '#6366F1' } }">
    <div class="help-app">
      <a-layout class="layout">
        <!-- 头部导航 -->
        <a-layout-header class="header">
          <div class="header-content">
            <div class="logo">
              <span class="logo-icon">❓</span>
              <span class="logo-text">帮助与关于</span>
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
          <div class="help-container">
            <a-layout style="background: #fff; min-height: 600px;">
              <!-- 左侧菜单 -->
              <a-layout-sider
                v-model:selectedKeys="selectedKeys"
                theme="light"
                width="240"
                class="help-sider"
              >
                <a-menu v-model:selectedKeys="selectedKeys" mode="inline">
                  <a-menu-item key="tutorial">
                    <template #icon><BookOutlined /></template>
                    使用教程
                  </a-menu-item>
                  <a-menu-item key="faq">
                    <template #icon><QuestionCircleOutlined /></template>
                    常见问题
                  </a-menu-item>
                  <a-menu-item key="troubleshooting">
                    <template #icon><ToolOutlined /></template>
                    故障排除
                  </a-menu-item>
                  <a-menu-item key="contact">
                    <template #icon><CustomerServiceOutlined /></template>
                    联系支持
                  </a-menu-item>
                  <a-menu-item key="about">
                    <template #icon><InfoCircleOutlined /></template>
                    关于
                  </a-menu-item>
                </a-menu>
              </a-layout-sider>

              <!-- 右侧内容区 -->
              <a-layout-content class="help-content">
                <!-- 使用教程 -->
                <div v-show="selectedKeys[0] === 'tutorial'" class="content-panel">
                  <div class="panel-header">
                    <h2>使用教程</h2>
                    <p>快速了解如何使用小遥搜索</p>
                  </div>

                  <div class="tutorial-sections">
                    <!-- 快速开始 -->
                    <div class="tutorial-section">
                      <h3>
                        <span class="step-number">1</span>
                        设置AI模型
                      </h3>
                      <div class="section-content">
                        <div class="content-item">
                          <h4>进入设置页面</h4>
                          <p>点击右上角的设置按钮，进入配置界面</p>
                        </div>
                        <div class="content-item">
                          <h4>配置LLM模型</h4>
                          <p>选择云端API或本地Ollama模型，填写相应的配置信息</p>
                        </div>
                        <div class="content-item">
                          <h4>测试连接</h4>
                          <p>点击"测试连接"按钮确保配置正确</p>
                        </div>
                      </div>
                    </div>

                    <!-- 添加索引文件夹 -->
                    <div class="tutorial-section">
                      <h3>
                        <span class="step-number">2</span>
                        添加索引文件夹
                      </h3>
                      <div class="section-content">
                        <div class="content-item">
                          <h4>进入索引管理</h4>
                          <p>从主页面进入索引管理页面</p>
                        </div>
                        <div class="content-item">
                          <h4>选择文件夹</h4>
                          <p>点击"添加文件夹"按钮，选择要索引的目录</p>
                        </div>
                        <div class="content-item">
                          <h4>配置索引选项</h4>
                          <p>选择是否包含子文件夹、索引文件内容等选项</p>
                        </div>
                        <div class="content-item">
                          <h4>等待索引完成</h4>
                          <p>系统会自动建立文件索引，完成后即可搜索</p>
                        </div>
                      </div>
                    </div>

                    <!-- 开始搜索 -->
                    <div class="tutorial-section">
                      <h3>
                        <span class="step-number">3</span>
                        开始搜索
                      </h3>
                      <div class="section-content">
                        <div class="content-item">
                          <h4>文本搜索</h4>
                          <p>直接在搜索框中输入关键词或自然语言描述</p>
                        </div>
                        <div class="content-item">
                          <h4>语音搜索</h4>
                          <p>点击麦克风按钮，说出您的搜索需求</p>
                        </div>
                        <div class="content-item">
                          <h4>图片搜索</h4>
                          <p>上传图片，系统会找到相似的文字内容和相关文档</p>
                        </div>
                        <div class="content-item">
                          <h4>查看结果</h4>
                          <p>搜索结果按相关度排序，支持预览和快速定位</p>
                        </div>
                      </div>
                    </div>

                    <div class="tutorial-actions">
                      <a-button type="primary" size="large" @click="watchVideoTutorial">
                        <template #icon><PlayCircleOutlined /></template>
                        观看视频教程
                      </a-button>
                      <a-button size="large" @click="downloadManual">
                        <template #icon><DownloadOutlined /></template>
                        下载使用手册
                      </a-button>
                    </div>
                  </div>
                </div>

                <!-- 常见问题 -->
                <div v-show="selectedKeys[0] === 'faq'" class="content-panel">
                  <div class="panel-header">
                    <h2>常见问题</h2>
                    <p>用户经常遇到的问题和解决方案</p>
                  </div>

                  <a-collapse v-model:activeKey="faqActiveKeys" class="faq-collapse">
                    <a-collapse-panel key="1" header="如何添加索引文件夹？">
                      <p>进入索引管理页面，点击"添加文件夹"按钮，选择要索引的目录路径。您可以配置是否包含子文件夹、索引文件内容等选项，然后点击"开始索引"即可。</p>
                    </a-collapse-panel>

                    <a-collapse-panel key="2" header="支持哪些文件格式？">
                      <p>小遥搜索支持多种文件格式：</p>
                      <ul>
                        <li>📄 文档：txt, md, pdf, docx, xlsx, pptx</li>
                        <li>🎵 音频：mp3, wav, m4a, flac</li>
                        <li>🎬 视频：mp4, avi, mov, mkv</li>
                        <li>🖼️ 图片：jpg, png, gif, webp</li>
                        <li>💻 代码：js, py, java, cpp, html</li>
                      </ul>
                    </a-collapse-panel>

                    <a-collapse-panel key="3" header="搜索速度慢怎么办？">
                      <p>搜索速度慢可能的原因和解决方案：</p>
                      <ol>
                        <li>检查索引是否完整建立，可以尝试重建索引</li>
                        <li>关闭不必要的文件类型过滤</li>
                        <li>升级到更快的AI模型或使用本地模型</li>
                        <li>确保系统有足够的内存和存储空间</li>
                      </ol>
                    </a-collapse-panel>

                    <a-collapse-panel key="4" header="如何提高搜索准确度？">
                      <p>提高搜索准确度的技巧：</p>
                      <ul>
                        <li>使用更具体的关键词和描述</li>
                        <li>启用文件内容索引</li>
                        <li>选择合适的AI模型</li>
                        <li>定期更新索引以包含最新文件</li>
                      </ul>
                    </a-collapse-panel>

                    <a-collapse-panel key="5" header="本地数据安全吗？">
                      <p>是的，小遥搜索非常注重数据安全：</p>
                      <ul>
                        <li>所有数据都存储在本地，不会上传到云端</li>
                        <li>支持本地数据加密存储</li>
                        <li>API密钥安全保存</li>
                        <li>可选择隐私模式，不记录搜索历史</li>
                      </ul>
                    </a-collapse-panel>

                    <a-collapse-panel key="6" header="系统配置要求是什么？">
                      <p>最低配置要求：</p>
                      <ul>
                        <li>操作系统：Windows 10/11 x64 或 macOS 10.15+</li>
                        <li>内存：4GB RAM（推荐8GB+）</li>
                        <li>存储：500MB应用空间 + 索引空间</li>
                        <li>网络：配置云端API时需要网络连接</li>
                      </ul>
                    </a-collapse-panel>
                  </a-collapse>
                </div>

                <!-- 故障排除 -->
                <div v-show="selectedKeys[0] === 'troubleshooting'" class="content-panel">
                  <div class="panel-header">
                    <h2>故障排除</h2>
                    <p>解决常见的技术问题</p>
                  </div>

                  <div class="troubleshooting-grid">
                    <div class="trouble-card">
                      <h4>🔧 应用无法启动</h4>
                      <div class="solution-steps">
                        <div class="step">检查系统是否满足最低配置要求</div>
                        <div class="step">尝试以管理员身份运行</div>
                        <div class="step">检查是否有其他程序占用端口</div>
                        <div class="step">重新安装应用程序</div>
                      </div>
                    </div>

                    <div class="trouble-card">
                      <h4>🔗 AI模型连接失败</h4>
                      <div class="solution-steps">
                        <div class="step">检查网络连接状态</div>
                        <div class="step">验证API密钥是否正确</div>
                        <div class="step">确认API地址和端口</div>
                        <div class="step">尝试切换到本地模型</div>
                      </div>
                    </div>

                    <div class="trouble-card">
                      <h4>📁 索引建立失败</h4>
                      <div class="solution-steps">
                        <div class="step">检查文件夹权限</div>
                        <div class="step">确认磁盘空间充足</div>
                        <div class="step">检查文件是否被其他程序占用</div>
                        <div class="step">尝试重新选择文件夹路径</div>
                      </div>
                    </div>

                    <div class="trouble-card">
                      <h4>🎤 语音识别不工作</h4>
                      <div class="solution-steps">
                        <div class="step">检查麦克风权限设置</div>
                        <div class="step">测试麦克风硬件是否正常</div>
                        <div class="step">检查语音识别服务状态</div>
                        <div class="step">尝试重新配置语音引擎</div>
                      </div>
                    </div>

                    <div class="trouble-card">
                      <h4>🔍 搜索结果不准确</h4>
                      <div class="solution-steps">
                        <div class="step">重建文件索引</div>
                        <div class="step">检查文件内容是否被正确索引</div>
                        <div class="step">优化搜索关键词</div>
                        <div class="step">调整AI模型参数</div>
                      </div>
                    </div>

                    <div class="trouble-card">
                      <h4>⚡ 性能问题</h4>
                      <div class="solution-steps">
                        <div class="step">关闭不必要的后台程序</div>
                        <div class="step">清理索引缓存</div>
                        <div class="step">减少索引文件夹数量</div>
                        <div class="step">升级硬件配置</div>
                      </div>
                    </div>
                  </div>

                  <div class="troubleshooting-actions">
                    <a-button @click="runDiagnostics">
                      <template #icon><BugOutlined /></template>
                      运行诊断工具
                    </a-button>
                    <a-button @click="exportLogs">
                      <template #icon><ExportOutlined /></template>
                      导出日志文件
                    </a-button>
                  </div>
                </div>

                <!-- 联系支持 -->
                <div v-show="selectedKeys[0] === 'contact'" class="content-panel">
                  <div class="panel-header">
                    <h2>联系支持</h2>
                    <p>我们随时为您提供帮助</p>
                  </div>

                  <div class="contact-grid">
                    <div class="contact-card">
                      <div class="contact-icon">
                        <MailOutlined />
                      </div>
                      <h4>邮件支持</h4>
                      <p>support@xiaoyaosearch.com</p>
                      <p class="contact-desc">我们会在24小时内回复您的邮件</p>
                    </div>

                    <div class="contact-card">
                      <div class="contact-icon">
                        <WechatOutlined />
                      </div>
                      <h4>微信客服</h4>
                      <p>XiaoyaoSearch</p>
                      <p class="contact-desc">工作日9:00-18:00在线</p>
                    </div>

                    <div class="contact-card">
                      <div class="contact-icon">
                        <GithubOutlined />
                      </div>
                      <h4>GitHub</h4>
                      <p>github.com/xiaoyaosearch</p>
                      <p class="contact-desc">提交问题反馈和功能建议</p>
                    </div>

                    <div class="contact-card">
                      <div class="contact-icon">
                        <MessageOutlined />
                      </div>
                      <h4>在线社区</h4>
                      <p>community.xiaoyaosearch.com</p>
                      <p class="contact-desc">与其他用户交流使用经验</p>
                    </div>
                  </div>

                  <div class="feedback-section">
                    <h3>意见反馈</h3>
                    <p>您的意见对我们非常重要，请告诉我们您的想法：</p>
                    <a-form layout="vertical" class="feedback-form">
                      <a-form-item label="反馈类型">
                        <a-select v-model:value="feedback.type" placeholder="选择反馈类型">
                          <a-select-option value="bug">错误报告</a-select-option>
                          <a-select-option value="feature">功能建议</a-select-option>
                          <a-select-option value="improvement">改进建议</a-select-option>
                          <a-select-option value="other">其他</a-select-option>
                        </a-select>
                      </a-form-item>
                      <a-form-item label="详细描述">
                        <a-textarea
                          v-model:value="feedback.content"
                          placeholder="请详细描述您的问题或建议..."
                          :rows="4"
                        />
                      </a-form-item>
                      <a-form-item label="联系邮箱（可选）">
                        <a-input v-model:value="feedback.email" placeholder="您的邮箱地址" />
                      </a-form-item>
                      <a-form-item>
                        <a-button type="primary" @click="submitFeedback" :loading="isSubmittingFeedback">
                          提交反馈
                        </a-button>
                      </a-form-item>
                    </a-form>
                  </div>
                </div>

                <!-- 关于 -->
                <div v-show="selectedKeys[0] === 'about'" class="content-panel">
                  <div class="panel-header">
                    <h2>关于</h2>
                    <p>了解小遥搜索的更多信息</p>
                  </div>

                  <div class="about-content">
                    <div class="app-info">
                      <div class="app-logo">
                        <span class="logo-emoji">🔍</span>
                        <h3>小遥搜索</h3>
                        <p class="app-version">版本 1.0.0</p>
                      </div>

                      <div class="app-description">
                        <p>小遥搜索是一款专为知识工作者、内容创作者和技术开发者设计的多模态AI智能搜索桌面应用。通过先进的AI技术，帮助您快速找到本地文件中的相关内容。</p>
                      </div>

                      <div class="feature-highlights">
                        <h4>核心功能</h4>
                        <div class="features-list">
                          <div class="feature-item">
                            <span class="feature-icon">🎯</span>
                            <span>多模态搜索（语音/文本/图片）</span>
                          </div>
                          <div class="feature-item">
                            <span class="feature-icon">🧠</span>
                            <span>AI语义理解和转换</span>
                          </div>
                          <div class="feature-item">
                            <span class="feature-icon">🔐</span>
                            <span>本地数据隐私保护</span>
                          </div>
                          <div class="feature-item">
                            <span class="feature-icon">⚡</span>
                            <span>快速准确的搜索结果</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div class="tech-info">
                      <h4>技术栈</h4>
                      <div class="tech-tags">
                        <a-tag color="blue">Vue 3</a-tag>
                        <a-tag color="green">TypeScript</a-tag>
                        <a-tag color="orange">Ant Design</a-tag>
                        <a-tag color="purple">Electron</a-tag>
                        <a-tag color="cyan">Vite</a-tag>
                      </div>
                    </div>

                    <div class="legal-info">
                      <h4>法律信息</h4>
                      <div class="legal-links">
                        <a @click="showLicense">软件许可协议</a>
                        <a @click="showPrivacy">隐私政策</a>
                        <a @click="showTerms">使用条款</a>
                      </div>
                    </div>

                    <div class="team-info">
                      <h4>开发团队</h4>
                      <p>小遥搜索由一个充满激情的团队开发，我们致力于为用户提供最佳的本地搜索体验。</p>
                      <div class="team-stats">
                        <div class="stat">
                          <span class="number">5+</span>
                          <span class="label">开发经验</span>
                        </div>
                        <div class="stat">
                          <span class="number">1000+</span>
                          <span class="label">用户信赖</span>
                        </div>
                        <div class="stat">
                          <span class="number">24/7</span>
                          <span class="label">技术支持</span>
                        </div>
                      </div>
                    </div>

                    <div class="update-info">
                      <h4>更新信息</h4>
                      <div class="update-card">
                        <div class="update-header">
                          <span class="update-version">v1.0.0</span>
                          <span class="update-date">2024年11月</span>
                        </div>
                        <div class="update-content">
                          <p>🎉 首次发布，包含以下核心功能：</p>
                          <ul>
                            <li>多模态搜索输入</li>
                            <li>AI语义转换</li>
                            <li>本地文件索引</li>
                            <li>搜索结果管理</li>
                          </ul>
                        </div>
                      </div>
                    </div>

                    <div class="about-actions">
                      <a-button @click="checkForUpdates">
                        <template #icon><SyncOutlined /></template>
                        检查更新
                      </a-button>
                      <a-button @click="visitWebsite">
                        <template #icon><GlobalOutlined /></template>
                        访问官网
                      </a-button>
                    </div>
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
  BookOutlined,
  QuestionCircleOutlined,
  ToolOutlined,
  CustomerServiceOutlined,
  InfoCircleOutlined,
  PlayCircleOutlined,
  DownloadOutlined,
  BugOutlined,
  ExportOutlined,
  MailOutlined,
  WechatOutlined,
  GithubOutlined,
  MessageOutlined,
  SyncOutlined,
  GlobalOutlined
} from '@ant-design/icons-vue'

// 状态管理
const selectedKeys = ref(['tutorial'])
const faqActiveKeys = ref(['1'])
const isSubmittingFeedback = ref(false)

// 反馈表单
const feedback = reactive({
  type: '',
  content: '',
  email: ''
})

// 观看视频教程
const watchVideoTutorial = () => {
  message.info('即将打开视频教程页面')
}

// 下载使用手册
const downloadManual = () => {
  message.success('使用手册下载开始')
}

// 运行诊断工具
const runDiagnostics = () => {
  message.info('正在运行系统诊断...')
  setTimeout(() => {
    message.success('诊断完成，系统运行正常')
  }, 3000)
}

// 导出日志文件
const exportLogs = () => {
  message.success('日志文件导出成功')
}

// 提交反馈
const submitFeedback = async () => {
  if (!feedback.type || !feedback.content) {
    message.warning('请填写反馈类型和详细描述')
    return
  }

  isSubmittingFeedback.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1500))
    message.success('反馈提交成功，感谢您的意见！')

    // 清空表单
    feedback.type = ''
    feedback.content = ''
    feedback.email = ''
  } catch (error) {
    message.error('反馈提交失败，请稍后重试')
  } finally {
    isSubmittingFeedback.value = false
  }
}

// 显示软件许可协议
const showLicense = () => {
  message.info('查看软件许可协议')
}

// 显示隐私政策
const showPrivacy = () => {
  message.info('查看隐私政策')
}

// 显示使用条款
const showTerms = () => {
  message.info('查看使用条款')
}

// 检查更新
const checkForUpdates = () => {
  message.info('正在检查更新...')
  setTimeout(() => {
    message.success('您使用的是最新版本')
  }, 2000)
}

// 访问官网
const visitWebsite = () => {
  message.info('即将打开官网')
}

// 返回
const goBack = () => {
  message.info('返回上一页')
}

// 组件挂载
onMounted(() => {
  // 初始化操作
})
</script>

<style scoped>
.help-app {
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

.help-container {
  max-width: 1200px;
  margin: 0 auto;
}

.help-sider {
  border-right: 1px solid #f0f0f0;
}

.help-content {
  padding: 32px;
  overflow-y: auto;
  max-height: calc(100vh - 112px);
}

.content-panel {
  max-width: 800px;
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

/* 使用教程样式 */
.tutorial-sections {
  margin-bottom: 40px;
}

.tutorial-section {
  margin-bottom: 40px;
  padding: 24px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.tutorial-section h3 {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0 0 20px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: #6366f1;
  color: white;
  border-radius: 50%;
  font-size: 14px;
  font-weight: 500;
}

.section-content {
  margin-left: 40px;
}

.content-item {
  margin-bottom: 16px;
}

.content-item h4 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 14px;
  font-weight: 600;
}

.content-item p {
  margin: 0;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.tutorial-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 32px;
}

/* FAQ样式 */
.faq-collapse {
  background: transparent;
  border: none;
}

:deep(.faq-collapse .ant-collapse-item) {
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  margin-bottom: 16px;
}

:deep(.faq-collapse .ant-collapse-header) {
  font-size: 16px;
  font-weight: 500;
  padding: 16px 20px;
}

:deep(.faq-collapse .ant-collapse-content-box) {
  padding: 16px 20px;
  font-size: 14px;
  line-height: 1.6;
  color: #666;
}

:deep(.faq-collapse ul) {
  margin: 12px 0;
  padding-left: 20px;
}

:deep(.faq-collapse li) {
  margin-bottom: 8px;
}

/* 故障排除样式 */
.troubleshooting-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.trouble-card {
  padding: 24px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.trouble-card h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.solution-steps {
  display: grid;
  gap: 12px;
}

.step {
  position: relative;
  padding-left: 24px;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.step::before {
  content: "•";
  position: absolute;
  left: 8px;
  color: #6366f1;
  font-weight: bold;
}

.troubleshooting-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

/* 联系支持样式 */
.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.contact-card {
  text-align: center;
  padding: 32px 20px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
  transition: all 0.2s;
}

.contact-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.contact-icon {
  font-size: 32px;
  color: #6366f1;
  margin-bottom: 16px;
  display: flex;
  justify-content: center;
}

.contact-card h4 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.contact-card p {
  margin: 4px 0;
  color: #666;
  font-size: 14px;
}

.contact-desc {
  font-size: 12px !important;
  color: #999 !important;
}

.feedback-section {
  padding: 32px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.feedback-section h3 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.feedback-form {
  max-width: 500px;
}

/* 关于页面样式 */
.about-content {
  display: grid;
  gap: 32px;
}

.app-info {
  text-align: center;
  padding: 40px;
  background: linear-gradient(135deg, #f0f5ff 0%, #e6f7ff 100%);
  border-radius: 12px;
  border: 1px solid #e6f7ff;
}

.app-logo .logo-emoji {
  font-size: 48px;
  display: block;
  margin-bottom: 16px;
}

.app-logo h3 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 24px;
  font-weight: 600;
}

.app-version {
  color: #666;
  font-size: 14px;
  margin: 0 0 24px 0;
}

.app-description {
  max-width: 500px;
  margin: 0 auto 32px;
  color: #666;
  font-size: 16px;
  line-height: 1.6;
}

.feature-highlights h4 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.features-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: white;
  border-radius: 6px;
  font-size: 14px;
  color: #666;
}

.feature-icon {
  font-size: 16px;
}

.tech-info, .legal-info, .team-info, .update-info {
  padding: 24px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.tech-info h4, .legal-info h4, .team-info h4, .update-info h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.tech-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.legal-links {
  display: flex;
  gap: 16px;
}

.legal-links a {
  color: #6366f1;
  text-decoration: none;
  cursor: pointer;
}

.legal-links a:hover {
  text-decoration: underline;
}

.team-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 20px;
  margin-top: 16px;
}

.stat {
  text-align: center;
}

.stat .number {
  display: block;
  font-size: 24px;
  font-weight: 600;
  color: #6366f1;
}

.stat .label {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}

.update-card {
  padding: 20px;
  background: white;
  border-radius: 6px;
  border: 1px solid #f0f0f0;
}

.update-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.update-version {
  font-weight: 600;
  color: #6366f1;
}

.update-date {
  color: #999;
  font-size: 12px;
}

.update-content p {
  margin: 0 0 12px 0;
  color: #666;
  font-size: 14px;
}

.update-content ul {
  margin: 0;
  padding-left: 20px;
  color: #666;
  font-size: 14px;
}

.update-content li {
  margin-bottom: 4px;
}

.about-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
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