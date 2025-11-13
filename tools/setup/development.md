# 开发环境设置指南

## 系统要求

- **操作系统**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: 3.9+ (推荐使用 3.11)
- **Node.js**: 18.0+ (推荐使用 LTS 版本)
- **Git**: 2.30+

## 必需的系统依赖

### Windows
1. **Microsoft Visual C++ 14.0 or greater**
   - 安装 Visual Studio 2019/2022 或 Visual Studio Build Tools
   - 确保 "C++ build tools" 已安装

2. **Git**
   ```powershell
   # 使用 winget 安装
   winget install Git.Git

   # 或从官网下载安装
   # https://git-scm.com/download/win
   ```

3. **FFmpeg** (用于音视频处理)
   ```powershell
   # 使用 chocolatey 安装
   choco install ffmpeg

   # 或手动下载并添加到 PATH
   # https://ffmpeg.org/download.html
   ```

4. **LibreOffice** (用于 Office 文档处理)
   ```powershell
   # 使用 chocolatey 安装
   choco install libreoffice
   ```

### macOS
1. **Xcode Command Line Tools**
   ```bash
   xcode-select --install
   ```

2. **Homebrew** (包管理器)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **系统依赖**
   ```bash
   brew install git ffmpeg libreoffice
   ```

### Linux (Ubuntu/Debian)
1. **系统更新和基础依赖**
   ```bash
   sudo apt update
   sudo apt install -y git curl wget build-essential
   ```

2. **Python 和相关依赖**
   ```bash
   sudo apt install -y python3.11 python3.11-venv python3.11-dev
   ```

3. **音视频处理**
   ```bash
   sudo apt install -y ffmpeg
   ```

4. **文档处理**
   ```bash
   sudo apt install -y libreoffice
   ```

## 项目设置

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/xiaoyaosearch.git
cd xiaoyaosearch
```

### 2. 设置 Python 环境
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装 Poetry (如果尚未安装)
curl -sSL https://install.python-poetry.org | python3 -

# 安装后端依赖
cd backend
poetry install
```

### 3. 设置 Node.js 环境
```bash
# 检查 Node.js 版本
node --version
npm --version

# 如果需要安装 Node.js，推荐使用 nvm
# macOS/Linux
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20

# Windows
# 使用 winget 安装
winget install OpenJS.NodeJS

# 安装前端依赖
cd frontend
npm install
```

### 4. 设置开发工具
```bash
# 安装 pre-commit hooks
pre-commit install

# 设置 Git hooks (可选)
cp tools/scripts/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

## AI 模型设置

### 1. 下载基础模型
```bash
cd tools
python setup/download_models.py
```

### 2. 设置 Ollama (本地 LLM)
```bash
# 安装 Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 下载模型
ollama pull llama2
ollama pull qwen:7b
```

### 3. 配置 OpenAI (可选)
```bash
# 创建环境变量文件
cp .env.example .env

# 编辑 .env 文件，添加 OpenAI API Key
echo "OPENAI_API_KEY=your_api_key_here" >> .env
```

## 数据库设置

### 1. 创建数据库目录
```bash
mkdir -p data
mkdir -p indexes/vectors
mkdir -p indexes/fulltext
```

### 2. 初始化数据库
```bash
cd backend
poetry run alembic upgrade head
```

## 运行项目

### 开发模式

1. **启动后端服务**
   ```bash
   cd backend
   poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **启动前端 Electron 应用 (electron-vite)**
   ```bash
   cd frontend
   npm run dev
   ```

   这个命令会同时启动渲染进程开发服务器和 Electron 应用。

3. **分步启动 (可选)**
   ```bash
   # 启动渲染进程开发服务器
   cd frontend
   npm run dev:renderer

   # 在另一个终端启动 Electron
   npm run dev:electron
   ```

### 生产模式

1. **构建后端**
   ```bash
   cd backend
   poetry build
   ```

2. **构建前端和打包 Electron 应用**
   ```bash
   cd frontend
   npm run build
   ```

   这个命令会进行类型检查，构建前端，并打包 Electron 应用。

3. **单独打包不同平台**
   ```bash
   # Windows
   cd frontend
   npm run build:win

   # macOS
   cd frontend
   npm run build:mac

   # Linux
   cd frontend
   npm run build:linux
   ```

4. **仅构建不打包**
   ```bash
   cd frontend
   npm run build:unpack
   ```

## 开发工具配置

### VS Code
推荐安装以下扩展：
- Python
- TypeScript and JavaScript Language Features
- Vue Language Features (Volar)
- Prettier - Code formatter
- ESLint
- GitLens

### PyCharm
1. 安装 Python 插件
2. 配置 Poetry 解释器
3. 安装 Vue.js 插件

### 调试配置

#### VS Code launch.json
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/backend/app/main.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/backend"
      }
    },
    {
      "name": "Electron: Main",
      "type": "node",
      "request": "launch",
      "cwd": "${workspaceFolder}/frontend",
      "runtimeExecutable": "${workspaceFolder}/frontend/node_modules/.bin/electron",
      "windows": {
        "runtimeExecutable": "${workspaceFolder}/frontend/node_modules/.bin/electron.cmd"
      },
      "args": ["--inspect=5858", "--remote-debugging-port=9223", "out/main/index.js"],
      "outputCapture": "std"
    },
    {
      "name": "Electron: Renderer",
      "type": "chrome",
      "request": "attach",
      "port": 9223,
      "webRoot": "${workspaceFolder}/frontend/src/renderer/src",
      "timeout": 30000
    }
  ],
  "compounds": [
    {
      "name": "Electron: All",
      "configurations": ["Electron: Main", "Electron: Renderer"]
    }
  ]
}
```

## 常见问题

### Q: Poetry 安装依赖失败
A: 尝试清除缓存并重新安装
```bash
poetry cache clear pypi --all
poetry install --no-dev
```

### Q: Node.js 依赖安装失败
A: 清除 npm 缓存并重新安装
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Q: AI 模型下载失败
A: 检查网络连接并使用镜像源
```bash
# 设置 Hugging Face 镜像
export HF_ENDPOINT=https://hf-mirror.com
```

### Q: 权限问题 (Linux/macOS)
A: 确保文件权限正确
```bash
chmod +x tools/scripts/*.sh
```

### Q: electron-vite 构建失败
A: 检查 TypeScript 配置和依赖
```bash
# 重新安装依赖
cd frontend
rm -rf node_modules package-lock.json
npm install

# 检查类型错误
npm run typecheck
```

### Q: Electron 应用无法启动
A: 检查主进程和预加载脚本
```bash
# 检查主进程编译
npm run build:main

# 检查预加载脚本编译
npm run build:preload

# 查看详细错误日志
DEBUG=electron:* npm run dev
```

## 性能优化建议

### 开发环境
1. 使用 SSD 硬盘
2. 至少 16GB RAM
3. 多核 CPU (AI 模型推理)

### 生产环境
1. GPU 支持 (NVIDIA CUDA)
2. 更多 RAM 用于向量索引
3. 快速存储设备

## 测试

### 运行测试
```bash
# 后端测试
cd backend
poetry run pytest

# 前端测试
cd frontend
npm run test
```

### 测试覆盖率
```bash
# 后端
poetry run pytest --cov=app --cov-report=html

# 前端
npm run test:coverage
```