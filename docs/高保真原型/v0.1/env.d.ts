/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// 环境变量类型声明
interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  readonly VITE_APP_VERSION: string
  readonly VITE_APP_DESCRIPTION: string
  readonly VITE_API_BASE_URL: string
  readonly VITE_API_TIMEOUT: string
  readonly VITE_DEV_TOOLS: string
  readonly VITE_SOURCE_MAP: string
  readonly VITE_ENABLE_MOCK_API: string
  readonly VITE_ENABLE_DEBUG_MODE: string
  readonly VITE_ENABLE_ANALYTICS: string
  readonly VITE_BUILD_SOURCEMAP: string
  readonly VITE_BUILD_MINIFY: string
  readonly VITE_ENABLE_CSP: string
  readonly VITE_ENABLE_HSTS: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

// 全局属性声明
declare global {
  interface Window {
    // Electron API
    api?: {
      openFile: (path: string) => void
      selectDirectory: () => Promise<string>
      showMessageBox: (options: any) => Promise<any>
    }

    // 自定义属性
    xiaoyaoSearch?: {
      version: string
      config: any
    }
  }
}

export {}