# 小遥搜索快速启动指南

## 🚀 环境要求

- **Node.js**: 18.x 或更高版本
- **Python**: 3.10 或更高版本
- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 18.04+

## 📦 快速安装

### 1. 安装依赖

```bash
# 安装根项目依赖
npm install

# 安装前端依赖
npm run setup:frontend

# 安装后端依赖
npm run setup:backend
```

### 2. 启动开发环境

```bash
# 同时启动前端和后端
npm run dev
```

或者分别启动：

```bash
# 启动后端服务 (端口 8000)
npm run dev:backend

# 启动前端开发服务器 (端口 3000)
npm run dev:frontend
```

### 3. 构建和运行

```bash
# 构建应用
npm run build

# 启动应用
npm start
```

## 🏗️ 项目结构

```
xiaoyaosearch/
├── frontend/                 # Electron + React 前端应用
│   ├── src/
│   │   ├── main/            # Electron 主进程
│   │   ├── renderer/        # React 渲染进程
│   │   └── shared/          # 共享类型和工具
│   ├── package.json
│   └── vite.config.ts
├── backend/                 # FastAPI 后端服务
│   ├── app/
│   │   ├── api/v1/          # API 路由
│   │   ├── core/            # 核心配置
│   │   ├── models/          # 数据模型
│   │   ├── services/        # 业务服务
│   │   └── schemas/         # Pydantic 模式
│   ├── main.py
│   └── requirements.txt
├── docs/                    # 项目文档
├── openspec/                # OpenSpec 规格文档
└── README.md
```

## 🛠️ 开发工具

### 代码格式化和检查

```bash
# 格式化所有代码
npm run format

# 检查代码风格
npm run lint

# 运行测试
npm test
```

### 前端开发

```bash
cd frontend
npm run dev          # 开发模式
npm run build        # 构建
npm run test         # 运行测试
npm run lint         # 代码检查
```

### 后端开发

```bash
cd backend
uvicorn main:app --reload  # 开发模式
pytest                    # 运行测试
mypy .                    # 类型检查
black .                   # 代码格式化
```

## 📋 当前状态

### ✅ 已完成
- [x] 项目环境搭建
- [x] 前端基础架构 (Electron + React + TypeScript)
- [x] 后端基础架构 (FastAPI + Python)
- [x] 基础页面组件 (搜索、索引管理、设置、收藏)
- [x] API 路由结构
- [x] 数据模型定义
- [x] 代码质量工具配置

### 🚧 进行中
- [ ] 数据库模式实现
- [ ] 搜索引擎核心功能
- [ ] AI 服务集成
- [ ] 文件索引系统

### 📅 计划中
- [ ] 用户系统完善
- [ ] 设置管理功能
- [ ] 性能优化
- [ ] 测试覆盖

## 🔧 API 接口

### 搜索接口
- `GET /api/v1/search` - 搜索文件
- `POST /api/v1/search/understand` - 理解查询
- `GET /api/v1/search/suggestions` - 获取建议

### 文件接口
- `GET /api/v1/files` - 获取文件列表
- `GET /api/v1/files/{id}` - 获取文件信息
- `GET /api/v1/files/{id}/preview` - 预览文件

### 目录接口
- `GET /api/v1/directories` - 获取目录列表
- `POST /api/v1/directories` - 添加目录
- `POST /api/v1/directories/{id}/scan` - 扫描目录

## 🐛 常见问题

### Q: 前端启动失败
A: 确保安装了所有依赖：`npm run setup:frontend`

### Q: 后端启动失败
A: 检查 Python 版本是否为 3.10+：`python --version`

### Q: API 请求失败
A: 确保后端服务运行在 http://localhost:8000

### Q: Electron 应用无法启动
A: 检查是否构建了前端资源：`npm run build:frontend`

## 📚 更多信息

- [OpenSpec 规格](./openspec/) - 详细的技术规格文档
- [项目文档](./docs/) - 更详细的项目说明
- [API 文档](http://localhost:8000/docs) - 后端 API 文档（需要后端运行）

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。