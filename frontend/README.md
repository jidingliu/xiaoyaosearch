<h1 align="center">小遥搜索 - 前端应用</h1>

<p align="center">AI驱动的桌面搜索应用前端 (Electron + Vue3 + TypeScript)</p>

<p align="center">
<img src="https://img.shields.io/github/package-json/dependency-version/alex8088/electron-vite-boilerplate/dev/electron" alt="electron-version">
<img src="https://img.shields.io/github/package-json/dependency-version/alex8088/electron-vite-boilerplate/dev/electron-vite" alt="electron-vite-version" />
<img src="https://img.shields.io/github/package-json/dependency-version/alex8088/electron-vite-boilerplate/dev/electron-builder" alt="electron-builder-version" />
<img src="https://img.shields.io/github/package-json/dependency-version/alex8088/electron-vite-boilerplate/dev/vite" alt="vite-version" />
<img src="https://img.shields.io/github/package-json/dependency-version/alex8088/electron-vite-boilerplate/dev/vue" alt="vue-version" />
<img src="https://img.shields.io/github/package-json/dependency-version/alex8088/electron-vite-boilerplate/dev/typescript" alt="typescript-version" />
</p>

<p align='center'>
<img src='./build/electron-vite-vue-ts.png'/>
</p>

## 功能特性

- 🔍 **多模态搜索**: 支持文本、语音、图像三种搜索方式
- 🤖 **AI智能理解**: 基于大语言模型的查询意图识别
- 📁 **全文件类型支持**: 文档、图片、音频、视频全覆盖
- ⚡ **高性能搜索**: 向量搜索 + 全文搜索 + 元数据搜索
- 🔒 **隐私保护**: 所有数据存储在本地，保护用户隐私
- 🖥️ **跨平台支持**: Windows、macOS、Linux

## 技术架构

- **框架**: Electron 28.0+ + Vue 3.4+ + TypeScript 5.3+
- **构建工具**: electron-vite 2.0+ (优化的开发体验)
- **状态管理**: Pinia (Vue官方推荐)
- **UI组件**: Ant Design Vue 4.1+
- **后端服务**: FastAPI (Python) + AI模型服务

## 开发指南

### 环境要求
- Node.js 18.0+
- Python 3.9+ (后端服务)
- 系统要求: Windows 10+, macOS 10.15+, Linux

### 快速开始

1. **安装依赖**
   ```bash
   npm install
   ```

2. **启动开发服务器**
   ```bash
   # 同时启动渲染进程和Electron
   npm run dev

   # 或分步启动
   npm run dev:renderer  # 仅渲染进程
   npm run dev:electron   # 仅Electron主进程
   ```

3. **启动后端服务** (在另一个终端)
   ```bash
   cd ../backend
   poetry run uvicorn app.main:app --reload
   ```

### 构建打包

```bash
# 构建所有平台
npm run build

# 构建特定平台
npm run build:win    # Windows
npm run build:mac    # macOS
npm run build:linux  # Linux

# 仅构建不打包
npm run build:unpack
```

### 开发工具

- **代码检查**: `npm run lint`
- **代码格式化**: `npm run format`
- **类型检查**: `npm run typecheck`
- **测试**: `npm run test`

### Ant Design Vue 集成

本项目已集成 Ant Design Vue 4.1+，提供企业级UI组件：

- **自动导入**: 使用 `unplugin-vue-components` 自动按需导入组件
- **类型支持**: 完整的 TypeScript 类型定义
- **主题定制**: 支持主题配置和样式定制
- **国际化**: 支持中文和其他语言

#### 使用示例

```vue
<template>
  <a-button type="primary" @click="handleClick">
    主要按钮
  </a-button>

  <a-input v-model:value="inputValue" placeholder="请输入内容" />

  <a-table :columns="columns" :data-source="data" />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { message } from 'ant-design-vue'

const inputValue = ref('')
const columns = ref([
  { title: '姓名', dataIndex: 'name', key: 'name' },
  { title: '年龄', dataIndex: 'age', key: 'age' },
])
const data = ref([
  { key: '1', name: '张三', age: 32 },
  { key: '2', name: '李四', age: 42 },
])

const handleClick = () => {
  message.success('按钮点击成功！')
}
</script>
```

详细文档请参考:
- [electron-vite 官方文档](https://electron-vite.org/)
- [项目架构文档](../docs/code-arch.md)
- [技术选型文档](../docs/tech-stack.md)
- [Ant Design Vue 官方文档](https://antdv.com/components/overview-cn)

## Recommended IDE Setup

- [VSCode](https://code.visualstudio.com/) + [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) + [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin)

## Project Setup

### Install

```bash
$ npm install
```

### Development

```bash
$ npm run dev
```

### Build

```bash
# For windows
$ npm run build:win

# For macOS
$ npm run build:mac

# For Linux
$ npm run build:linux
```

## Examples

- [electron-vite-bytecode-example](https://github.com/alex8088/electron-vite-bytecode-example), source code protection
- [electron-vite-decorator-example](https://github.com/alex8088/electron-vite-decorator-example), typescipt decorator
- [electron-vite-worker-example](https://github.com/alex8088/electron-vite-worker-example), worker and fork
