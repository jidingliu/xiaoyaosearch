import { contextBridge, ipcRenderer } from 'electron'
import { ElectronAPI } from '@/shared/types'

// 定义暴露给渲染进程的API
const electronAPI: ElectronAPI = {
  // 应用控制
  app: {
    getVersion: () => ipcRenderer.invoke('app:getVersion'),
    quit: () => ipcRenderer.invoke('app:quit'),
    minimize: () => ipcRenderer.invoke('app:minimize'),
    maximize: () => ipcRenderer.invoke('app:maximize')
  },

  // 窗口控制
  window: {
    close: () => ipcRenderer.invoke('window:close')
  },

  // 配置存储
  store: {
    get: (key: string) => ipcRenderer.invoke('store:get', key),
    set: (key: string, value: any) => ipcRenderer.invoke('store:set', key, value),
    delete: (key: string) => ipcRenderer.invoke('store:delete', key)
  },

  // 文件对话框
  dialog: {
    showOpenDialog: (options: any) => ipcRenderer.invoke('dialog:showOpenDialog', options),
    showSaveDialog: (options: any) => ipcRenderer.invoke('dialog:showSaveDialog', options)
  },

  // 事件监听
  on: (channel: string, callback: Function) => {
    ipcRenderer.on(channel, (_event, ...args) => callback(...args))
  },

  // 移除事件监听
  off: (channel: string, callback: Function) => {
    ipcRenderer.removeListener(channel, callback)
  }
}

// 暴露API到渲染进程
contextBridge.exposeInMainWorld('electronAPI', electronAPI)