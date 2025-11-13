# 小遥搜索 UI设计规范文档

## 概述

小遥搜索是一个跨平台的本地文件智能搜索工具，通过AI多模态理解能力，为个人用户提供文本、语音、图片、视频等多种文件的语义化检索服务。

### 设计理念
- **智能化优先**：AI驱动的用户体验，智能理解用户需求
- **隐私保护**：本地优先，确保用户数据安全
- **简洁高效**：现代化界面设计，专注核心功能
- **无障碍设计**：支持键盘导航、屏幕阅读器等辅助功能

## 技术栈

### 前端技术
- **Vue 3.4+**：现代化前端框架，组合式API
- **TypeScript 5.3+**：类型安全的JavaScript超集
- **Ant Design Vue**：企业级UI组件库，自动导入支持，完整类型定义
- **Electron 28.0+**：跨平台桌面应用框架
- **electron-vite**：优化的构建工具和开发体验
- **Pinia**：Vue官方状态管理库

### 设计工具
- **Figma/Sketch**：UI设计稿制作
- **Adobe XD**：交互原型设计
- **Zeplin**：设计交付和协作

## 视觉系统

### 色彩规范

#### 主色调
```css
/* 主色调 */
--primary-blue: #2563EB;    /* 主要交互元素 */
--secondary-purple: #9333EA; /* 辅助强调色 */

/* 功能色彩 */
--success-green: #10B981;   /* 成功状态 */
--error-red: #EF4444;       /* 错误状态 */
--warning-yellow: #F59E0B;  /* 警告状态 */
--info-blue: #3B82F6;       /* 信息状态 */

/* 中性色彩 */
--gray-900: #111827;        /* 主要文本 */
--gray-700: #374151;        /* 次要文本 */
--gray-500: #6B7280;        /* 辅助文本 */
--gray-300: #D1D5DB;        /* 边框分割 */
--gray-100: #F3F4F6;        /* 背景色 */
```

### 字体系统

#### 字体族
```css
/* 主字体 */
--font-family-primary: 'Inter', system-ui, -apple-system, sans-serif;

/* 代码字体 */
--font-family-mono: 'JetBrains Mono', 'Consolas', monospace;
```

#### 字体层级
```css
/* 标题字体 */
--text-4xl: 2.25rem;    /* 36px - 页面标题 */
--text-3xl: 1.875rem;   /* 30px - 章节标题 */
--text-2xl: 1.5rem;     /* 24px - 子章节标题 */
--text-xl: 1.25rem;     /* 20px - 小标题 */

/* 正文字体 */
--text-lg: 1.125rem;    /* 18px - 重要正文 */
--text-base: 1rem;      /* 16px - 正文内容 */
--text-sm: 0.875rem;    /* 14px - 辅助文本 */
--text-xs: 0.75rem;     /* 12px - 标签文本 */
```

#### 字重规范
```css
--font-light: 300;      /* 轻量 */
--font-normal: 400;     /* 正常 */
--font-medium: 500;     /* 中等 */
--font-semibold: 600;   /* 半粗体 */
--font-bold: 700;       /* 粗体 */
```

### 间距系统

```css
/* 基础间距单位 */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

### 圆角规范
```css
--radius-sm: 0.25rem;   /* 4px - 小圆角 */
--radius-md: 0.5rem;    /* 8px - 中等圆角 */
--radius-lg: 0.75rem;   /* 12px - 大圆角 */
--radius-xl: 1rem;      /* 16px - 超大圆角 */
--radius-full: 9999px;  /* 完全圆角 */
```

## 页面设计

### 1. 搜索页面 (SearchPage)

#### 核心功能
- 多模态搜索输入（文本、语音、图片）
- 智能搜索建议和历史记录
- 搜索结果展示（卡片式布局）
- 批量操作和文件管理
- 高级搜索选项配置

#### 设计要点
- 搜索框突出显示，支持占位符提示
- 集成语音和图片搜索按钮
- 搜索结果卡片包含文件图标、标题、摘要、相关度评分
- 支持批量选择和操作
- 响应式布局适配

#### 关键组件
```html
<!-- 搜索输入框 -->
<div class="search-input-container">
  <input type="text" placeholder="输入搜索关键词，支持语义搜索...">
  <button class="voice-search-btn">
    <i class="fas fa-microphone"></i>
  </button>
  <button class="image-search-btn">
    <i class="fas fa-camera"></i>
  </button>
  <button class="advanced-options-btn">
    <i class="fas fa-sliders-h"></i>
  </button>
</div>

<!-- 搜索结果卡片 -->
<div class="search-result-card">
  <div class="file-icon">
    <i class="fas fa-file-word"></i>
  </div>
  <div class="file-info">
    <h3 class="file-title">文件名</h3>
    <p class="file-summary">文件摘要</p>
    <div class="file-meta">
      <span class="file-path">文件路径</span>
      <span class="file-size">文件大小</span>
      <span class="file-date">修改日期</span>
    </div>
  </div>
  <div class="file-actions">
    <button class="preview-btn"><i class="fas fa-eye"></i></button>
    <button class="open-btn"><i class="fas fa-external-link-alt"></i></button>
    <button class="favorite-btn"><i class="fas fa-star"></i></button>
    <button class="download-btn"><i class="fas fa-download"></i></button>
  </div>
</div>
```

### 2. 索引管理页面 (IndexPage)

#### 核心功能
- 索引统计概览（文件数量、目录数量、索引大小）
- 目录管理表格（添加、删除、重新扫描）
- 全局索引控制（开始、暂停、重建）
- 实时进度监控和状态显示
- 索引设置和性能配置

#### 设计要点
- 顶部显示索引统计概览卡片
- 目录列表采用表格形式展示
- 操作按钮突出显示，支持批量操作
- 索引进度条实时更新
- 状态标识清晰明确

#### 关键组件
```html
<!-- 统计卡片 -->
<div class="stat-card">
  <div class="stat-icon">
    <i class="fas fa-file"></i>
  </div>
  <div class="stat-content">
    <h3 class="stat-number">15,842</h3>
    <p class="stat-label">总文件数</p>
  </div>
</div>

<!-- 目录管理表格 -->
<table class="directory-table">
  <thead>
    <tr>
      <th>目录路径</th>
      <th>文件数量</th>
      <th>索引状态</th>
      <th>最后更新</th>
      <th>操作</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>目录信息</td>
      <td>文件数量</td>
      <td><span class="status-badge">状态</span></td>
      <td>更新时间</td>
      <td>操作按钮</td>
    </tr>
  </tbody>
</table>
```

### 3. 设置页面 (SettingsPage)

#### 核心功能
- 标签页式布局（搜索、索引、AI、界面、高级设置）
- 搜索设置（搜索模式、结果数量、自动建议）
- 索引管理设置（更新频率、文件类型限制）
- AI配置（本地/云端模式、GPU加速、模型管理）
- 界面设置（主题、语言、字体大小）

#### 设计要点
- 采用标签页式布局，清晰分类设置项
- 开关组件采用现代滑动条设计
- 下拉菜单和输入框统一样式
- 设置保存和重置功能突出显示

#### 关键组件
```html
<!-- 设置标签页 -->
<div class="settings-tabs">
  <button class="tab-btn active" data-tab="search">搜索设置</button>
  <button class="tab-btn" data-tab="index">索引管理</button>
  <button class="tab-btn" data-tab="ai">AI配置</button>
  <button class="tab-btn" data-tab="interface">界面设置</button>
</div>

<!-- 开关组件 -->
<div class="toggle-switch">
  <label class="toggle-label">功能名称</label>
  <div class="toggle-input">
    <input type="checkbox" checked>
    <span class="toggle-slider"></span>
  </div>
</div>
```

### 4. 收藏页面 (FavoritesPage)

#### 核心功能
- 网格/列表视图切换
- 收藏文件分类和标签管理
- 快速访问和批量操作
- 收藏统计概览
- 筛选和搜索功能

#### 设计要点
- 网格卡片式收藏展示
- 文件信息层次清晰
- 支持收藏分类和标签显示
- 快速操作按钮组

#### 关键组件
```html
<!-- 收藏卡片 -->
<div class="favorite-card">
  <div class="card-header">
    <div class="file-icon">
      <i class="fas fa-file-word"></i>
    </div>
    <button class="favorite-btn">
      <i class="fas fa-heart"></i>
    </button>
  </div>
  <div class="card-body">
    <h3 class="file-title">文件名</h3>
    <p class="file-description">文件描述</p>
    <div class="file-tags">
      <span class="tag">标签1</span>
      <span class="tag">标签2</span>
    </div>
  </div>
  <div class="card-actions">
    <button class="action-btn"><i class="fas fa-eye"></i></button>
    <button class="action-btn"><i class="fas fa-external-link-alt"></i></button>
    <button class="action-btn"><i class="fas fa-download"></i></button>
  </div>
</div>
```

## 组件规范

### SearchInput 搜索输入框组件

#### 属性
```typescript
interface SearchInputProps {
  placeholder?: string;        // 占位符文本
  value?: string;             // 输入值
  onSearch?: (value: string) => void; // 搜索回调
  onSuggestionSelect?: (suggestion: SearchSuggestion) => void; // 建议选择回调
  loading?: boolean;          // 加载状态
  suggestions?: SearchSuggestion[]; // 搜索建议
  showVoiceInput?: boolean;   // 显示语音输入
  showImageInput?: boolean;   // 显示图片输入
  showAdvancedOptions?: boolean; // 显示高级选项
  size?: 'small' | 'medium' | 'large'; // 尺寸
}
```

#### 样式状态
```css
.search-input {
  /* 默认状态 */
  border: 2px solid #E5E7EB;
  background-color: #F9FAFB;
}

.search-input:focus {
  /* 聚焦状态 */
  border-color: #2563EB;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.search-input.loading {
  /* 加载状态 */
  opacity: 0.7;
}
```

### FileIcon 文件图标组件

#### 支持的文件类型
```typescript
interface FileTypeMapping {
  // 文档类型
  doc: { icon: 'fa-file-word', color: '#2563EB' };
  docx: { icon: 'fa-file-word', color: '#2563EB' };
  pdf: { icon: 'fa-file-pdf', color: '#DC2626' };
  txt: { icon: 'fa-file-alt', color: '#6B7280' };

  // 表格类型
  xls: { icon: 'fa-file-excel', color: '#10B981' };
  xlsx: { icon: 'fa-file-excel', color: '#10B981' };
  csv: { icon: 'fa-file-csv', color: '#10B981' };

  // 演示类型
  ppt: { icon: 'fa-file-powerpoint', color: '#F59E0B' };
  pptx: { icon: 'fa-file-powerpoint', color: '#F59E0B' };

  // 图片类型
  jpg: { icon: 'fa-file-image', color: '#8B5CF6' };
  png: { icon: 'fa-file-image', color: '#8B5CF6' };
  gif: { icon: 'fa-file-image', color: '#8B5CF6' };

  // 视频类型
  mp4: { icon: 'fa-file-video', color: '#EC4899' };
  avi: { icon: 'fa-file-video', color: '#EC4899' };
  mov: { icon: 'fa-file-video', color: '#EC4899' };

  // 音频类型
  mp3: { icon: 'fa-file-audio', color: '#F97316' };
  wav: { icon: 'fa-file-audio', color: '#F97316' };

  // 代码类型
  js: { icon: 'fa-file-code', color: '#06B6D4' };
  py: { icon: 'fa-file-code', color: '#06B6D4' };
  java: { icon: 'fa-file-code', color: '#06B6D4' };

  // 压缩类型
  zip: { icon: 'fa-file-archive', color: '#6366F1' };
  rar: { icon: 'fa-file-archive', color: '#6366F1' };
}
```

### ActionBar 操作栏组件

#### 属性
```typescript
interface ActionItem {
  id: string;
  label: string;
  icon: string;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
  onClick?: () => void;
}

interface ActionBarProps {
  actions: ActionItem[];
  variant?: 'default' | 'icon' | 'vertical';
  size?: 'small' | 'medium' | 'large';
  maxVisible?: number;
}
```

## 交互设计

### 状态反馈
- **默认状态**：正常显示，使用标准色彩
- **悬停状态**：背景色变化，边框高亮
- **焦点状态**：蓝色边框，阴影效果
- **激活状态**：背景色加深，文字高亮
- **禁用状态**：透明度降低，不可交互

### 动画规范
```css
/* 缓动函数 */
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in: cubic-bezier(0.4, 0, 1, 1);

/* 动画时长 */
--duration-fast: 150ms;    /* 快速反馈 */
--duration-normal: 300ms;  /* 标准动画 */
--duration-slow: 500ms;    /* 复杂动画 */

/* 通用动画 */
.transition {
  transition: all var(--duration-normal) var(--ease-in-out);
}

.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
```

### 微交互
- **按钮点击**：轻微缩放效果 + 涟漪动画
- **卡片悬停**：上浮阴影 + 轻微放大
- **输入框聚焦**：边框高亮 + 外发光效果
- **加载状态**：旋转动画 + 进度指示器
- **切换开关**：滑动动画 + 状态色彩变化

## 响应式设计

### 断点规范
```css
/* 移动设备 */
@media (max-width: 640px) {
  /* 小屏幕样式 */
}

/* 平板设备 */
@media (min-width: 641px) and (max-width: 1024px) {
  /* 中等屏幕样式 */
}

/* 桌面设备 */
@media (min-width: 1025px) {
  /* 大屏幕样式 */
}
```

### 布局适配
- **移动端优先**：基础样式针对小屏幕设计
- **弹性网格**：使用Flexbox和Grid布局
- **响应式间距**：根据屏幕尺寸调整间距
- **触摸友好**：按钮和交互区域适合触摸操作

## 无障碍设计

### WCAG 2.1 AA 标准
- **色彩对比度**：至少 4.5:1 的对比度
- **键盘导航**：所有功能可通过键盘访问
- **屏幕阅读器**：语义化HTML标签 + ARIA属性
- **焦点管理**：清晰的焦点指示器
- **文字缩放**：支持200%文字缩放

### 实施要点
- 使用语义化HTML标签（header, nav, main, section等）
- 为图标按钮提供aria-label属性
- 表单元素关联正确的label标签
- 链接和按钮有明确的焦点状态
- 图片提供有意义的alt文本

## 设计资源

### 设计文件
- **Figma设计稿**：包含所有页面和组件设计
- **组件库**：可复用的UI组件集合
- **设计系统**：完整的视觉规范文档
- **图标库**：项目专用图标集合

### 开发资源
- **CSS框架**：Tailwind CSS配置文件
- **组件代码**：React/Vue组件示例
- **设计令牌**：CSS变量和设计系统配置
- **字体文件**：项目字体文件和图标字体

## 最佳实践

### 代码规范
- 使用语义化的HTML标签
- CSS类名采用BEM命名规范
- JavaScript代码模块化组织
- 注释清晰，便于维护

### 性能优化
- 图片资源压缩和懒加载
- CSS和JavaScript文件压缩
- 减少HTTP请求数量
- 使用CDN加速静态资源

### 测试要求
- 跨浏览器兼容性测试
- 响应式设计测试
- 无障碍功能测试
- 性能指标测试

## 更新日志

### v1.0.0 (2024-11-12)
- 初始设计规范文档
- 完整的UI组件库
- 响应式设计适配
- 无障碍设计支持

---

*本设计规范文档将随着项目发展持续更新，请关注最新版本。*