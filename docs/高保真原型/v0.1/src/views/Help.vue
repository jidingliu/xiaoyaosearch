<template>
  <div class="help-container">
    <div class="help-header">
      <h2>帮助与关于</h2>
      <p>了解如何使用小遥搜索，解决常见问题</p>
    </div>

    <a-tabs v-model:activeKey="activeTab" type="card" class="help-tabs">
      <!-- 快速入门 -->
      <a-tab-pane key="guide" tab="快速入门">
        <div class="guide-section">
          <div class="guide-step">
            <div class="step-number">1</div>
            <div class="step-content">
              <h3>配置AI模型</h3>
              <p>进入设置页面的模型配置，选择云端API或本地模型</p>
              <a-button type="primary" @click="$router.push('/settings')">前往设置</a-button>
            </div>
          </div>

          <div class="guide-step">
            <div class="step-number">2</div>
            <div class="step-content">
              <h3>添加索引文件夹</h3>
              <p>进入索引管理页面，添加需要搜索的文件夹并创建文件索引</p>
              <a-button type="primary" @click="$router.push('/index')">前往索引</a-button>
            </div>
          </div>

          <div class="guide-step">
            <div class="step-number">3</div>
            <div class="step-content">
              <h3>开始搜索</h3>
              <p>在主页面使用多种方式输入搜索内容，查看智能搜索结果</p>
              <a-button type="primary" @click="$router.push('/')">开始搜索</a-button>
            </div>
          </div>
        </div>

        <div class="feature-highlights">
          <h3>核心功能介绍</h3>
          <a-row :gutter="16">
            <a-col :span="8">
              <a-card class="feature-card">
                <template #cover>
                  <div class="feature-icon">
                    <AudioOutlined />
                  </div>
                </template>
                <a-card-meta title="语音搜索" description="支持最长30秒的语音输入，自动转换为搜索查询" />
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card class="feature-card">
                <template #cover>
                  <div class="feature-icon">
                    <PictureOutlined />
                  </div>
                </template>
                <a-card-meta title="图片搜索" description="上传图片，AI分析内容后进行相关文件搜索" />
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card class="feature-card">
                <template #cover>
                  <div class="feature-icon">
                    <RobotOutlined />
                  </div>
                </template>
                <a-card-meta title="AI增强" description="利用大语言模型提供更智能的搜索理解" />
              </a-card>
            </a-col>
          </a-row>
        </div>
      </a-tab-pane>

      <!-- 使用教程 -->
      <a-tab-pane key="tutorial" tab="使用教程">
        <div class="tutorial-section">
          <a-collapse v-model:activeKey="tutorialActiveKeys" :bordered="false">
            <a-collapse-panel key="1" header="如何进行语音搜索？">
              <div class="tutorial-content">
                <h4>语音搜索步骤：</h4>
                <ol>
                  <li>点击搜索框上方的语音输入按钮</li>
                  <li>允许浏览器访问麦克风</li>
                  <li>点击"开始录音"按钮</li>
                  <li>说出您的搜索内容（最长30秒）</li>
                  <li>系统自动转换语音为文字并执行搜索</li>
                </ol>
                <div class="tip-box">
                  <BulbOutlined />
                  <span>小贴士：在安静环境下录音效果更佳，语速适中</span>
                </div>
              </div>
            </a-collapse-panel>

            <a-collapse-panel key="2" header="如何使用图片搜索？">
              <div class="tutorial-content">
                <h4>图片搜索步骤：</h4>
                <ol>
                  <li>切换到图片输入模式</li>
                  <li>拖拽图片到上传区域或点击选择文件</li>
                  <li>支持 JPG、PNG、WEBP 格式，最大10MB</li>
                  <li>点击"开始分析"让AI理解图片内容</li>
                  <li>系统根据图片内容搜索相关文件</li>
                </ol>
                <div class="tip-box">
                  <BulbOutlined />
                  <span>小贴士：清晰的图片和文字图片搜索效果更佳</span>
                </div>
              </div>
            </a-collapse-panel>

            <a-collapse-panel key="3" header="如何优化搜索结果？">
              <div class="tutorial-content">
                <h4>优化搜索技巧：</h4>
                <ul>
                  <li><strong>关键词选择</strong>：使用核心概念和关键词</li>
                  <li><strong>搜索类型</strong>：根据需要选择语义搜索、全文搜索或混合搜索</li>
                  <li><strong>文件类型过滤</strong>：指定搜索特定类型的文件</li>
                  <li><strong>相似度调节</strong>：调整相似度阈值控制结果精确度</li>
                  <li><strong>使用引号</strong>：用引号括起短语进行精确匹配</li>
                </ul>
              </div>
            </a-collapse-panel>

            <a-collapse-panel key="4" header="如何管理文件索引？">
              <div class="tutorial-content">
                <h4>索引管理指南：</h4>
                <ul>
                  <li><strong>添加文件夹</strong>：选择包含文档、图片、音频等文件的文件夹</li>
                  <li><strong>索引选项</strong>：选择是否包含子文件夹和隐藏文件</li>
                  <li><strong>文件类型</strong>：指定需要建立索引的文件类型</li>
                  <li><strong>监控进度</strong>：在索引管理页面查看索引任务状态</li>
                  <li><strong>重建索引</strong>：文件更新后可以重建索引保持同步</li>
                </ul>
              </div>
            </a-collapse-panel>
          </a-collapse>
        </div>
      </a-tab-pane>

      <!-- 常见问题 -->
      <a-tab-pane key="faq" tab="常见问题">
        <div class="faq-section">
          <a-collapse v-model:activeKey="faqActiveKeys" :bordered="false">
            <a-collapse-panel key="1" header="语音识别准确率不高怎么办？">
              <div class="faq-content">
                <p><strong>可能的原因：</strong></p>
                <ul>
                  <li>环境噪音较大</li>
                  <li>语速过快或过慢</li>
                  <li>麦克风质量不佳</li>
                  <li>网络连接不稳定</li>
                </ul>
                <p><strong>解决方法：</strong></p>
                <ul>
                  <li>在安静环境下进行语音输入</li>
                  <li>保持适中的语速和音量</li>
                  <li>使用质量较好的麦克风</li>
                  <li>检查网络连接状态</li>
                </ul>
              </div>
            </a-collapse-panel>

            <a-collapse-panel key="2" header="搜索结果不够精确怎么办？">
              <div class="faq-content">
                <p><strong>优化建议：</strong></p>
                <ul>
                  <li>使用更具体的关键词</li>
                  <li>尝试不同的搜索类型（语义/全文/混合）</li>
                  <li>调整相似度阈值</li>
                  <li>使用文件类型过滤</li>
                  <li>检查文件是否已正确索引</li>
                </ul>
              </div>
            </a-collapse-panel>

            <a-collapse-panel key="3" header="文件索引速度很慢？">
              <div class="faq-content">
                <p><strong>影响因素：</strong></p>
                <ul>
                  <li>文件夹中文件数量较多</li>
                  <li>文件体积较大</li>
                  <li>电脑性能限制</li>
                  <li>同时运行多个索引任务</li>
                </ul>
                <p><strong>建议：</strong></p>
                <ul>
                  <li>分批建立索引，避免一次索引过多文件</li>
                  <li>关闭不必要的程序释放系统资源</li>
                  <li>考虑在夜间进行大量文件的索引</li>
                </ul>
              </div>
            </a-collapse-panel>

            <a-collapse-panel key="4" header="如何备份数据？">
              <div class="faq-content">
                <p><strong>数据位置：</strong></p>
                <ul>
                  <li>配置文件：用户目录下的.xiaoyaosearch文件夹</li>
                  <li>索引文件：用户选择的数据目录</li>
                  <li>搜索历史：数据库文件</li>
                </ul>
                <p><strong>备份方法：</strong></p>
                <ul>
                  <li>定期复制数据目录到其他位置</li>
                  <li>导出重要配置和索引</li>
                  <li>使用云存储进行异地备份</li>
                </ul>
              </div>
            </a-collapse-panel>
          </a-collapse>
        </div>
      </a-tab-pane>

      <!-- 关于 -->
      <a-tab-pane key="about" tab="关于">
        <div class="about-section">
          <div class="about-header">
            <div class="app-logo">
              <span class="logo-text">◤小遥搜索◢</span>
            </div>
            <h3>XiaoyaoSearch v2.0</h3>
            <p class="app-description">
              一款支持多模态AI智能搜索的本地桌面应用，为知识工作者提供语音、文本、图像输入的智能文件检索能力。
            </p>
          </div>

          <a-row :gutter="24" class="info-grid">
            <a-col :span="12">
              <a-card title="技术特性" class="info-card">
                <ul class="feature-list">
                  <li>🎯 多模态AI搜索</li>
                  <li>🔊 语音识别支持</li>
                  <li>🖼️ 图像内容理解</li>
                  <li>🔍 智能语义搜索</li>
                  <li>📁 本地文件管理</li>
                  <li>⚡ 高速索引检索</li>
                </ul>
              </a-card>
            </a-col>
            <a-col :span="12">
              <a-card title="技术栈" class="info-card">
                <ul class="tech-list">
                  <li>前端：Vue 3 + TypeScript</li>
                  <li>UI框架：Ant Design Vue</li>
                  <li>桌面端：Electron</li>
                  <li>后端：Python + FastAPI</li>
                  <li>AI模型：BGE-M3, Whisper, CLIP</li>
                  <li>搜索引擎：Faiss + Whoosh</li>
                </ul>
              </a-card>
            </a-col>
          </a-row>

          <div class="version-info">
            <a-descriptions title="版本信息" :column="2" bordered>
              <a-descriptions-item label="版本号">
                v2.0.0 (Beta)
              </a-descriptions-item>
              <a-descriptions-item label="构建日期">
                2024-01-20
              </a-descriptions-item>
              <a-descriptions-item label="运行平台">
                Windows 11+ / macOS 10.15+ / Linux
              </a-descriptions-item>
              <a-descriptions-item label="最低配置">
                4GB RAM / 2GB 磁盘空间
              </a-descriptions-item>
              <a-descriptions-item label="推荐配置">
                8GB RAM / 10GB 磁盘空间
              </a-descriptions-item>
              <a-descriptions-item label="开源许可">
                MIT License
              </a-descriptions-item>
            </a-descriptions>
          </div>

          <div class="contact-info">
            <h4>联系我们</h4>
            <div class="contact-links">
              <a-space size="large">
                <a href="https://github.com/xiaoyaosearch" target="_blank">
                  <GithubOutlined />
                  GitHub
                </a>
                <a href="mailto:support@xiaoyaosearch.com">
                  <MailOutlined />
                  邮箱支持
                </a>
                <a href="https://docs.xiaoyaosearch.com" target="_blank">
                  <ReadOutlined />
                  文档中心
                </a>
              </a-space>
            </div>
          </div>

          <div class="acknowledgments">
            <h4>致谢</h4>
            <p>
              感谢开源社区的贡献，特别是以下项目的支持：
            </p>
            <div class="opensource-projects">
              <a-tag color="blue">Vue.js</a-tag>
              <a-tag color="green">Ant Design</a-tag>
              <a-tag color="orange">FastAPI</a-tag>
              <a-tag color="red">Transformers</a-tag>
              <a-tag color="purple">Faiss</a-tag>
            </div>
          </div>
        </div>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  AudioOutlined,
  PictureOutlined,
  RobotOutlined,
  BulbOutlined,
  GithubOutlined,
  MailOutlined,
  ReadOutlined
} from '@ant-design/icons-vue'

const router = useRouter()

// 响应式数据
const activeTab = ref('guide')
const tutorialActiveKeys = ref(['1'])
const faqActiveKeys = ref(['1'])
</script>

<style scoped>
.help-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: var(--space-6);
}

.help-header {
  text-align: center;
  margin-bottom: var(--space-8);
}

.help-header h2 {
  margin: 0 0 var(--space-3);
  color: var(--text-primary);
}

.help-header p {
  margin: 0;
  color: var(--text-secondary);
}

.help-tabs {
  background: var(--surface-01);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-base);
  overflow: hidden;
}

/* 快速入门样式 */
.guide-section {
  padding: var(--space-6);
}

.guide-step {
  display: flex;
  align-items: flex-start;
  margin-bottom: var(--space-8);
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  border-radius: 50%;
  margin-right: var(--space-6);
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-content h3 {
  margin: 0 0 var(--space-2);
  color: var(--text-primary);
}

.step-content p {
  margin: 0 0 var(--space-4);
  color: var(--text-secondary);
}

.feature-highlights {
  margin-top: var(--space-8);
  padding-top: var(--space-6);
  border-top: 1px solid var(--border-light);
}

.feature-highlights h3 {
  text-align: center;
  margin-bottom: var(--space-6);
  color: var(--text-primary);
}

.feature-card {
  text-align: center;
  border-radius: var(--radius-lg);
  transition: transform var(--transition-base);
}

.feature-card:hover {
  transform: translateY(-2px);
}

.feature-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 80px;
  background: linear-gradient(135deg, var(--primary-50), var(--accent-light));
  font-size: 2rem;
  color: var(--primary-600);
}

/* 教程样式 */
.tutorial-section,
.faq-section {
  padding: var(--space-6);
}

.tutorial-content,
.faq-content {
  color: var(--text-secondary);
}

.tutorial-content h4,
.faq-content h4 {
  color: var(--text-primary);
  margin-bottom: var(--space-3);
}

.tutorial-content ol,
.tutorial-content ul,
.faq-content ul {
  margin-bottom: var(--space-4);
  padding-left: var(--space-6);
}

.tutorial-content li,
.faq-content li {
  margin-bottom: var(--space-2);
}

.tip-box {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3);
  background: var(--warning-light);
  border-left: 4px solid var(--warning);
  border-radius: var(--radius-base);
  color: var(--warning-dark);
}

/* 关于样式 */
.about-section {
  padding: var(--space-6);
}

.about-header {
  text-align: center;
  margin-bottom: var(--space-8);
}

.app-logo {
  margin-bottom: var(--space-4);
}

.logo-text {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-600), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.about-header h3 {
  margin: var(--space-2) 0;
  color: var(--text-primary);
}

.app-description {
  max-width: 600px;
  margin: 0 auto;
  color: var(--text-secondary);
  line-height: 1.6;
}

.info-grid {
  margin-bottom: var(--space-6);
}

.info-card {
  height: 100%;
}

.feature-list,
.tech-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li,
.tech-list li {
  padding: var(--space-2) 0;
  border-bottom: 1px solid var(--border-light);
}

.feature-list li:last-child,
.tech-list li:last-child {
  border-bottom: none;
}

.version-info {
  margin-bottom: var(--space-6);
}

.contact-info {
  text-align: center;
  margin-bottom: var(--space-6);
}

.contact-info h4 {
  margin-bottom: var(--space-4);
  color: var(--text-primary);
}

.contact-links a {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  color: var(--primary-600);
}

.acknowledgments {
  text-align: center;
}

.acknowledgments h4 {
  margin-bottom: var(--space-3);
  color: var(--text-primary);
}

.opensource-projects {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-top: var(--space-3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .help-container {
    padding: var(--space-4);
  }

  .guide-step {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .step-number {
    margin-right: 0;
    margin-bottom: var(--space-4);
  }

  .info-grid .ant-col {
    margin-bottom: var(--space-4);
  }

  .contact-links {
    flex-direction: column;
    align-items: center;
  }
}
</style>