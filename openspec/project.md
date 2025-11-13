# 小遥搜索项目上下文

## 项目目的
构建一个跨平台的本地文件智能搜索工具，通过AI多模态理解能力，实现文本、语音、图片、视频等多种文件的语义化检索，提升个人知识管理效率。

## 技术栈
### 前端
- **框架**: Vue 3.4+ (Composition API)
- **语言**: TypeScript 5.2+
- **构建工具**: Vite 5.0+
- **UI组件**: Ant Design Vue 4.1+
- **状态管理**: Zustand 4.4+
- **桌面框架**: Electron 27.0+

### 后端
- **框架**: FastAPI 0.104+
- **语言**: Python 3.11+
- **异步**: asyncio + uvicorn
- **数据库ORM**: SQLAlchemy 2.0+ (异步)
- **数据验证**: Pydantic 2.5+
- **AI/ML**: PyTorch, Transformers, FlagEmbedding
- **向量搜索**: Faiss
- **全文搜索**: Whoosh

### AI模型
- **文本嵌入**: BGE (BAAI General Embedding)
- **语音识别**: FastWhisper
- **图像理解**: Chinese-CLIP
- **大语言模型**: Ollama (本地) / OpenAI (云端)

## 项目规范

### 代码风格
#### 前端
- ESLint + Prettier代码格式化
- TypeScript严格模式
- Vue3组合式API规范
- 组件命名 PascalCase
- 文件命名 kebab-case

#### 后端
- Black代码格式化
- mypy类型检查
- flake8代码检查
- PEP 8编码规范
- 文档字符串规范

### 架构模式
- **前后端分离**: Electron + FastAPI架构
- **分层架构**: API层、服务层、核心逻辑层分离
- **模块化设计**: 按功能域组织代码
- **依赖注入**: 使用FastAPI的依赖注入系统
- **数据验证**: 使用Pydantic进行强类型验证

### 测试策略
#### 前端测试
- Jest单元测试
- Vue Test Utils组件测试
- Cypress端到端测试
- 测试覆盖率 > 80%

#### 后端测试
- pytest单元测试
- pytest-asyncio异步测试
- API集成测试
- 性能测试和压力测试

### Git工作流
- **分支策略**: GitFlow (main, develop, feature/*, hotfix/*)
- **提交规范**: Conventional Commits
- **代码审查**: 所有PR必须经过审查
- **自动化**: CI/CD pipeline自动测试和构建

## 领域上下文
小遥搜索是一个AI驱动的个人知识管理工具，专注于：
- **多模态搜索**: 支持文本、语音、图像输入
- **语义理解**: 理解查询意图，非精确匹配
- **本地优先**: 所有数据存储在用户本地，保护隐私
- **跨平台**: 支持Windows、Mac、Linux
- **实时索引**: 监控文件变化，增量更新索引

## 重要约束
- **隐私保护**: 所有数据存储在用户本地，不上传到云端
- **性能要求**: 支持1万文件规模，搜索响应时间<1秒
- **资源限制**: 内存使用<2GB，磁盘占用<10GB
- **跨平台兼容**: 必须在Windows、Mac、Linux上运行
- **离线工作**: 核心功能必须支持离线使用

## 外部依赖
- **AI模型**: 需要下载BGE、Whisper、Chinese-CLIP模型
- **系统工具**: LibreOffice (文档转换)、FFmpeg (音视频处理)
- **Python包**: 通过PyPI管理
- **Node.js包**: 通过npm管理
- **可选云服务**: OpenAI API (可选的云端LLM服务)
