# Electron API 使用说明

## 概述

小遥搜索桌面应用中集成了 Electron 原生功能，包括文件夹选择和文件操作等。

## 可用的 API

### 1. 文件夹选择 (`window.api.selectFolder`)

调用系统原生的文件夹选择对话框，让用户选择要索引的文件夹。

```typescript
// 示例用法
const result = await window.api.selectFolder()

if (result.success) {
  console.log('选择的文件夹:', result.folderPath)
} else if (result.canceled) {
  console.log('用户取消了选择')
} else {
  console.error('选择失败:', result.error)
}
```

**返回值格式:**
```typescript
{
  success: boolean;
  folderPath?: string;  // 成功时返回选择的文件夹路径
  canceled?: boolean;   // 用户取消时为 true
  error?: string;        // 错误信息
}
```

### 2. 打开文件 (`window.api.openFile`)

使用系统默认程序打开指定文件。

```typescript
// 示例用法
const result = await window.api.openFile('C:\\path\\to\\file.pdf')

if (result.success) {
  console.log('文件打开成功')
} else {
  console.error('打开失败:', result.error)
}
```

**返回值格式:**
```typescript
{
  success: boolean;
  error?: string;  // 错误信息
}
```

## 环境检测

在浏览器环境中，这些 API 不可用。可以使用以下代码进行环境检测：

```typescript
// 检查是否在 Electron 环境中
const isElectron = !!(window as any).api

if (isElectron) {
  // 可以使用 Electron API
  const result = await window.api.selectFolder()
} else {
  // 浏览器环境，使用替代方案或提示用户
  console.warn('请在桌面应用中使用此功能')
}
```

## 使用示例

### 在 Vue 组件中使用

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { message } from 'ant-design-vue'

const selectedFolder = ref('')

const selectFolder = async () => {
  // 检查环境
  if (!window.api) {
    message.warning('请在桌面应用中使用文件夹选择功能')
    return
  }

  try {
    const result = await window.api.selectFolder()

    if (result.success && result.folderPath) {
      selectedFolder.value = result.folderPath
      message.success(`已选择: ${result.folderPath}`)
    } else if (result.canceled) {
      // 用户取消，不显示错误
    } else {
      message.error(result.error || '选择文件夹失败')
    }
  } catch (error) {
    console.error('调用失败:', error)
    message.error('文件夹选择功能不可用')
  }
}
</script>

<template>
  <div>
    <button @click="selectFolder">选择文件夹</button>
    <div v-if="selectedFolder">已选择: {{ selectedFolder }}</div>
  </div>
</template>
```

## 注意事项

1. **环境限制**: 这些 API 只能在 Electron 桌面应用中使用，在浏览器环境中不可用。
2. **错误处理**: 始终要进行错误处理和用户提示。
3. **权限**: 某些操作可能需要系统权限，确保应用有足够的权限。
4. **异步操作**: 所有 API 都是异步的，需要使用 `await` 或 `.then()` 处理。
5. **类型安全**: 在 TypeScript 项目中，类型定义已在 `src/preload/index.d.ts` 中声明。

## 调试

在开发过程中，可以使用测试工具来验证 API 是否正常工作：

```typescript
import { electronTest } from '@/utils/testElectronAPI'

// 测试文件夹选择
await electronTest.testSelectFolder()
```

检查浏览器控制台是否有相关的调试信息。