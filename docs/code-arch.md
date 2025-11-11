
<project-structure>
## 代码架构
```markdown
ai-search/
├── frontend/                    # 前端项目（Electron + React）
│   ├── src/
│   │   ├── main/               # Electron主进程
│   │   │   ├── index.ts        # 主进程入口
│   │   │   ├── ipc/            # IPC通信处理
│   │   │   ├── window.ts       # 窗口管理
│   │   │   ├── menu.ts         # 菜单管理
│   │   │   ├── tray.ts         # 系统托盘
│   │   │   └── updater.ts      # 自动更新
│   │   │
│   │   ├── renderer/           # Electron渲染进程（React应用）
│   │   │   ├── App.tsx         # 应用根组件
│   │   │   ├── pages/          # 页面组件
│   │   │   │   ├── Search/     # 搜索页面
│   │   │   │   ├── Settings/   # 设置页面
│   │   │   │   ├── Preview/    # 文件预览页面
│   │   │   │   └── History/    # 历史记录页面
│   │   │   │
│   │   │   ├── components/     # 通用组件
│   │   │   │   ├── SearchBar/  # 搜索栏
│   │   │   │   ├── ResultList/ # 结果列表
│   │   │   │   ├── FilePreview/# 文件预览
│   │   │   │   ├── FilterPanel/# 筛选面板
│   │   │   │   └── VoiceInput/ # 语音输入
│   │   │   │
│   │   │   ├── stores/         # Zustand状态管理
│   │   │   │   ├── search.ts   # 搜索状态
│   │   │   │   ├── settings.ts # 设置状态
│   │   │   │   ├── user.ts     # 用户状态
│   │   │   │   └── index.ts    # 索引状态
│   │   │   │
│   │   │   ├── services/       # API服务
│   │   │   │   ├── api.ts      # API客户端封装
│   │   │   │   ├── search.ts   # 搜索服务
│   │   │   │   ├── index.ts    # 索引服务
│   │   │   │   └── file.ts     # 文件服务
│   │   │   │
│   │   │   ├── hooks/          # 自定义Hooks
│   │   │   │   ├── useSearch.ts
│   │   │   │   ├── useIndex.ts
│   │   │   │   └── useSettings.ts
│   │   │   │
│   │   │   ├── utils/          # 工具函数
│   │   │   │   ├── format.ts   # 格式化工具
│   │   │   │   ├── file.ts     # 文件工具
│   │   │   │   └── time.ts     # 时间工具
│   │   │   │
│   │   │   └── types/          # TypeScript类型定义
│   │   │       ├── search.ts
│   │   │       ├── file.ts
│   │   │       └── api.ts
│   │   │
│   │   └── preload/            # Preload脚本
│   │       └── index.ts        # 暴露安全的API给渲染进程
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts          # Vite配置
│   └── electron-builder.yml    # 打包配置
│
├── backend/                     # 后端项目（FastAPI）
│   ├── app/
│   │   ├── main.py             # FastAPI应用入口
│   │   │
│   │   ├── api/                # API路由
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── search.py   # 搜索接口
│   │   │   │   ├── index.py    # 索引管理接口
│   │   │   │   ├── files.py    # 文件操作接口
│   │   │   │   ├── settings.py # 设置接口
│   │   │   │   └── ai.py       # AI服务接口
│   │   │   └── deps.py         # 依赖注入
│   │   │
│   │   ├── core/               # 核心模块
│   │   │   ├── config.py       # 配置管理
│   │   │   ├── security.py     # 安全相关
│   │   │   ├── logging.py      # 日志配置
│   │   │   └── exceptions.py   # 自定义异常
│   │   │
│   │   ├── services/           # 业务服务
│   │   │   ├── search/         # 搜索服务
│   │   │   │   ├── engine.py   # 搜索引擎
│   │   │   │   ├── query_parser.py # 查询解析
│   │   │   │   └── ranker.py   # 结果排序
│   │   │   │
│   │   │   ├── index/          # 索引服务
│   │   │   │   ├── scanner.py  # 文件扫描
│   │   │   │   ├── processor.py# 文件处理
│   │   │   │   ├── indexer.py  # 索引构建
│   │   │   │   └── monitor.py  # 文件监控
│   │   │   │
│   │   │   ├── ai/             # AI服务
│   │   │   │   ├── llm.py      # LLM服务
│   │   │   │   ├── asr.py      # 语音识别
│   │   │   │   ├── vision.py   # 视觉理解
│   │   │   │   └── embedding.py# 向量化
│   │   │   │
│   │   │   └── file/           # 文件服务
│   │   │       ├── manager.py  # 文件管理
│   │   │       └── preview.py  # 文件预览
│   │   │
│   │   ├── models/             # 数据模型（SQLAlchemy）
│   │   │   ├── user.py         # 用户模型
│   │   │   ├── file.py         # 文件模型
│   │   │   ├── directory.py    # 目录模型
│   │   │   └── search_history.py # 搜索历史模型
│   │   │
│   │   ├── schemas/            # Pydantic Schema
│   │   │   ├── search.py       # 搜索Schema
│   │   │   ├── index.py        # 索引Schema
│   │   │   ├── file.py         # 文件Schema
│   │   │   └── common.py       # 通用Schema
│   │   │
│   │   ├── db/                 # 数据库操作
│   │   │   ├── sqlite.py       # SQLite操作
│   │   │   ├── faiss_db.py     # Faiss索引操作
│   │   │   └── whoosh_db.py    # Whoosh索引操作
│   │   │
│   │   └── utils/              # 工具函数
│   │       ├── file_utils.py   # 文件工具
│   │       ├── text_utils.py   # 文本工具
│   │       ├── cache.py        # 缓存工具
│   │       └── async_utils.py  # 异步工具
│   │
│   ├── tests/                  # 测试
│   │   ├── test_search.py
│   │   ├── test_index.py
│   │   └── test_ai.py
│   │
│   ├── requirements.txt        # Python依赖
│   ├── pyproject.toml          # 项目配置
│   └── pytest.ini              # 测试配置
│
├── models/                      # AI模型目录（本地）
│   ├── bge-base-zh-v1.5/       # BGE Embedding模型
│   ├── whisper-medium/         # Whisper ASR模型
│   └── chinese-clip/           # Chinese-CLIP视觉模型
│
├── docs/                        # 文档
│   ├── architecture.md         # 架构文档
│   ├── api.md                  # API文档
│   ├── development.md          # 开发文档
│   └── deployment.md           # 部署文档
│
├── scripts/                     # 脚本
│   ├── setup.sh                # 环境搭建脚本
│   ├── build.sh                # 构建脚本
│   ├── download_models.py      # 模型下载脚本
│   └── migrate.py              # 数据库迁移脚本
│
├── .github/                     # GitHub配置
│   └── workflows/              # CI/CD
│       ├── test.yml            # 测试工作流
│       └── release.yml         # 发布工作流
│
├── README.md                    # 项目说明
├── LICENSE                      # 开源协议
├── .gitignore                   # Git忽略文件
└── docker-compose.yml           # Docker配置（可选）

```
</project-structure>
