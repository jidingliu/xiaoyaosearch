# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**小遥搜索 (XiaoyaoSearch)** 是一个为知识工作者、内容创作者和开发者设计的多模态AI智能桌面搜索应用。该项目支持语音、文本和图像输入，对本地文件进行智能搜索。

**当前状态**: 高保真Vue.js原型已完成，完整实现待开发
**技术栈**: Vue 3 + TypeScript（前端原型），Python FastAPI + AI模型（计划后端）
**目标平台**: 跨平台桌面应用（Windows/macOS/Linux）

## 开发命令

### 前端原型 (docs/demo/)
```bash
# 安装依赖
cd docs/demo && npm install

# 启动开发服务器（默认打开navigation.html）
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

### 项目结构
- `docs/` - 完整项目文档（MRD、PRD、技术方案）
- `base/` - 规划文档模板

## 核心文档

**必读文档**：
- `docs/开发进度.md` - 当前项目开发进度文档
- `docs/00-mrd.md` - 市场需求和用户故事
- `docs/01-prd.md` - 详细产品需求
- `docs/02-原型.md` - 原型设计标准
- `docs/03-技术方案.md` - 完整技术架构
- `docs/04-开发任务清单.md` - 开发任务分解

## 前端原型架构

**页面结构**（多页面Vite应用）：
- `search.html` - 主搜索界面，支持多模态输入
- `settings.html` - AI模型配置（本地/云端切换）
- `index-manage.html` - 文件索引和文件夹管理
- `help.html` - 用户文档和支持

**核心组件**：
- `SearchApp.vue` - 多模态搜索（语音/文本/图像输入）
- `SettingsApp.vue` - AI模型配置界面
- `IndexApp.vue` - 文件索引管理
- `HelpApp.vue` - 文档和帮助界面

**技术栈**：
- Vue 3 with Composition API
- TypeScript 类型安全
- Ant Design Vue 4.x UI组件库
- Vite 开发构建工具

## 计划完整架构

**前端（计划）**: Electron + Vue 3 + TypeScript
**后端（计划）**: Python FastAPI + Uvicorn
**AI模型**: BGE-M3（文本）、FasterWhisper（语音）、CN-CLIP（视觉）、Ollama（大语言模型）
**搜索引擎**: Faiss（向量搜索）+ Whoosh（全文搜索）
**数据库**: SQLite 元数据和配置存储

## 核心功能（MVP）

1. **多模态输入**: 语音（30秒）、文本、图像上传支持
2. **AI智能搜索**: 语义理解，支持本地/云端AI模型切换
3. **本地文件索引**: 支持视频、音频、文档、图像格式
4. **混合搜索**: 向量相似度 + 全文搜索结合

## 开发指南

### 原型开发注意事项
- 当前代码库是**高保真原型**，用于演示目的
- 使用模拟数据和模拟AI响应
- 专注于UI/UX实现，而非实际AI功能
- 四个主要页面已完整实现，采用Material Design 3.0设计

### 代码风格
- Vue 3 Composition API 模式
- TypeScript 严格模式
- Ant Design Vue 组件保持一致性
- 响应式设计原则

### 文件组织
- 每个页面都有独立的HTML入口和Vue组件
- 共享TypeScript逻辑位于 `src/*.ts` 文件
- Vite多页面配置在 `vite.config.ts`

## 下一阶段开发步骤

根据技术文档，完整实现需要：

1. **后端搭建**: Python FastAPI服务器，集成AI模型
2. **桌面应用**: Electron包装Vue前端
3. **AI集成**: 本地模型部署（BGE-M3、FasterWhisper、CN-CLIP）
4. **搜索引擎**: Faiss + Whoosh混合搜索实现
5. **数据库**: SQLite文件元数据和配置模式

## 目标用户

- 管理文档集合的知识工作者
- 拥有多媒体文件的内容创作者
- 搜索代码和文档的开发者
- 需要文件整理的个人用户

## 重要说明

- 