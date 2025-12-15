/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/ban-types
  const component: DefineComponent<{}, {}, any>
  export default component
}

interface WindowAPI {
  openFile: (filePath: string) => Promise<{ success: boolean; error?: string }>
}

declare interface Window {
  electron: ElectronAPI
  api: WindowAPI
}
