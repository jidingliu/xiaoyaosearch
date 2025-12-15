/**
 * Electron API 测试工具
 * 用于测试 Electron 环境下的 API 功能
 */

export const testElectronAPI = () => {
  console.log('=== 测试 Electron API ===')

  // 检查环境
  console.log('当前环境:', {
    hasElectronAPI: !!(window as any).electron,
    hasAPI: !!(window as any).api,
    userAgent: navigator.userAgent
  })

  // 检查 window.api 是否存在
  if (!(window as any).api) {
    console.warn('❌ window.api 不存在')
    return
  }

  const api = (window as any).api
  console.log('✅ window.api 存在')

  // 检查可用的方法
  console.log('可用方法:', {
    hasOpenFile: typeof api.openFile === 'function',
    hasSelectFolder: typeof api.selectFolder === 'function'
  })

  // 测试文件夹选择功能
  const testSelectFolder = async () => {
    try {
      console.log('🔄 测试文件夹选择功能...')
      const result = await api.selectFolder()
      console.log('✅ 文件夹选择结果:', result)
    } catch (error) {
      console.error('❌ 文件夹选择失败:', error)
    }
  }

  return {
    testSelectFolder
  }
}

// 导出测试工具
export const electronTest = testElectronAPI()

// 在开发环境中自动执行测试
if (import.meta.env.DEV) {
  console.log('🧪 开发环境：Electron API 测试工具已加载')
}