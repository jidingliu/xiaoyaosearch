import { defineStore } from 'pinia'
import { ref, computed, reactive } from 'vue'

// 定义接口类型
interface WindowSize {
  width: number
  height: number
}

interface SearchHistoryItem {
  id: string
  query: string
  inputType: 'text' | 'voice' | 'image'
  timestamp: Date
  resultCount: number
}

interface AppSettings {
  theme: 'dark' | 'light'
  language: 'zh-CN' | 'en-US'
  autoSave: boolean
  searchHistoryLimit: number
  enableNotifications: boolean
  enableSoundEffects: boolean
  animationEnabled: boolean
  compactMode: boolean
}

export const useAppStore = defineStore('app', () => {
  // 状态定义
  const theme = ref<AppSettings['theme']>('dark')
  const isLoading = ref(false)
  const pageVisible = ref(true)
  const searchFocus = ref(false)
  const shortcutHelpVisible = ref(false)
  const windowSize = reactive<WindowSize>({ width: 1920, height: 1080 })
  const searchHistory = ref<SearchHistoryItem[]>([])
  const notifications = ref<Array<{ id: string; message: string; type: 'success' | 'error' | 'warning' | 'info' }>>([])

  // 应用设置
  const settings = reactive<AppSettings>({
    theme: 'dark',
    language: 'zh-CN',
    autoSave: true,
    searchHistoryLimit: 50,
    enableNotifications: true,
    enableSoundEffects: true,
    animationEnabled: true,
    compactMode: false
  })

  // 计算属性
  const isDarkTheme = computed(() => theme.value === 'dark')
  const isMobile = computed(() => windowSize.width < 768)
  const isTablet = computed(() => windowSize.width >= 768 && windowSize.width < 1024)
  const isDesktop = computed(() => windowSize.width >= 1024)
  const hasSearchHistory = computed(() => searchHistory.value.length > 0)
  const recentSearches = computed(() =>
    searchHistory.value.slice(0, 5).map(item => item.query)
  )

  // 应用初始化
  const initializeApp = async () => {
    try {
      isLoading.value = true

      // 从本地存储加载设置
      await loadSettingsFromStorage()

      // 从本地存储加载搜索历史
      await loadSearchHistoryFromStorage()

      // 应用主题
      applyTheme()

      // 初始化通知系统
      if (settings.enableNotifications) {
        requestNotificationPermission()
      }

      console.log('应用初始化完成')
    } catch (error) {
      console.error('应用初始化失败:', error)
      addNotification('应用初始化失败', 'error')
    } finally {
      isLoading.value = false
    }
  }

  // 主题相关方法
  const setTheme = (newTheme: AppSettings['theme']) => {
    theme.value = newTheme
    settings.theme = newTheme
    applyTheme()
    saveSettingsToStorage()
  }

  const applyTheme = () => {
    document.documentElement.setAttribute('data-theme', theme.value)
    document.body.classList.toggle('dark-theme', theme.value === 'dark')
    document.body.classList.toggle('light-theme', theme.value === 'light')
  }

  const toggleTheme = () => {
    const newTheme = theme.value === 'dark' ? 'light' : 'dark'
    setTheme(newTheme)
    addNotification(`已切换到${newTheme === 'dark' ? '深色' : '浅色'}主题`, 'success')
  }

  // 窗口大小相关方法
  const setWindowSize = (size: WindowSize) => {
    Object.assign(windowSize, size)
  }

  // 搜索焦点相关方法
  const setSearchFocus = (focused: boolean) => {
    searchFocus.value = focused
  }

  // 快捷键帮助相关方法
  const toggleShortcutHelp = () => {
    shortcutHelpVisible.value = !shortcutHelpVisible.value
  }

  const hideShortcutHelp = () => {
    shortcutHelpVisible.value = false
  }

  // 页面可见性相关方法
  const setPageVisible = (visible: boolean) => {
    pageVisible.value = visible
  }

  // 搜索历史相关方法
  const addSearchHistory = (query: string, inputType: 'text' | 'voice' | 'image', resultCount: number) => {
    if (!query.trim()) return

    const historyItem: SearchHistoryItem = {
      id: Date.now().toString(),
      query: query.trim(),
      inputType,
      timestamp: new Date(),
      resultCount
    }

    // 避免重复记录
    const existingIndex = searchHistory.value.findIndex(item => item.query === query.trim())
    if (existingIndex > -1) {
      searchHistory.value.splice(existingIndex, 1)
    }

    // 添加到开头
    searchHistory.value.unshift(historyItem)

    // 限制历史记录数量
    if (searchHistory.value.length > settings.searchHistoryLimit) {
      searchHistory.value = searchHistory.value.slice(0, settings.searchHistoryLimit)
    }

    // 保存到本地存储
    saveSearchHistoryToStorage()
  }

  const clearSearchHistory = () => {
    searchHistory.value = []
    saveSearchHistoryToStorage()
    addNotification('搜索历史已清空', 'success')
  }

  const removeSearchHistoryItem = (id: string) => {
    const index = searchHistory.value.findIndex(item => item.id === id)
    if (index > -1) {
      searchHistory.value.splice(index, 1)
      saveSearchHistoryToStorage()
    }
  }

  // 通知相关方法
  const addNotification = (message: string, type: 'success' | 'error' | 'warning' | 'info' = 'info') => {
    const id = Date.now().toString()
    notifications.value.push({ id, message, type })

    // 自动移除通知
    setTimeout(() => {
      removeNotification(id)
    }, 5000)
  }

  const removeNotification = (id: string) => {
    const index = notifications.value.findIndex(notification => notification.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const clearNotifications = () => {
    notifications.value = []
  }

  // 设置相关方法
  const updateSettings = (newSettings: Partial<AppSettings>) => {
    Object.assign(settings, newSettings)
    saveSettingsToStorage()

    // 如果主题改变，应用新主题
    if (newSettings.theme) {
      theme.value = newSettings.theme
      applyTheme()
    }
  }

  const resetSettings = () => {
    const defaultSettings: AppSettings = {
      theme: 'dark',
      language: 'zh-CN',
      autoSave: true,
      searchHistoryLimit: 50,
      enableNotifications: true,
      enableSoundEffects: true,
      animationEnabled: true,
      compactMode: false
    }

    Object.assign(settings, defaultSettings)
    theme.value = defaultSettings.theme
    applyTheme()
    saveSettingsToStorage()
    addNotification('设置已重置为默认值', 'success')
  }

  // 本地存储相关方法
  const saveSettingsToStorage = () => {
    try {
      localStorage.setItem('xiaoyao-search-settings', JSON.stringify(settings))
    } catch (error) {
      console.error('保存设置失败:', error)
    }
  }

  const loadSettingsFromStorage = async () => {
    try {
      const savedSettings = localStorage.getItem('xiaoyao-search-settings')
      if (savedSettings) {
        const parsed = JSON.parse(savedSettings)
        Object.assign(settings, parsed)
        theme.value = settings.theme
      }
    } catch (error) {
      console.error('加载设置失败:', error)
    }
  }

  const saveSearchHistoryToStorage = () => {
    try {
      localStorage.setItem('xiaoyao-search-history', JSON.stringify(searchHistory.value))
    } catch (error) {
      console.error('保存搜索历史失败:', error)
    }
  }

  const loadSearchHistoryFromStorage = async () => {
    try {
      const savedHistory = localStorage.getItem('xiaoyao-search-history')
      if (savedHistory) {
        const parsed = JSON.parse(savedHistory)
        searchHistory.value = parsed.map((item: any) => ({
          ...item,
          timestamp: new Date(item.timestamp)
        }))
      }
    } catch (error) {
      console.error('加载搜索历史失败:', error)
    }
  }

  // 通知权限请求
  const requestNotificationPermission = async () => {
    if ('Notification' in window && Notification.permission === 'default') {
      try {
        const permission = await Notification.requestPermission()
        if (permission === 'granted') {
          addNotification('通知权限已启用', 'success')
        }
      } catch (error) {
        console.error('请求通知权限失败:', error)
      }
    }
  }

  // 浏览器通知
  const showBrowserNotification = (title: string, options?: NotificationOptions) => {
    if ('Notification' in window && Notification.permission === 'granted' && settings.enableNotifications) {
      new Notification(title, {
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        ...options
      })
    }
  }

  return {
    // 状态
    theme,
    isLoading,
    pageVisible,
    searchFocus,
    shortcutHelpVisible,
    windowSize,
    searchHistory,
    notifications,
    settings,

    // 计算属性
    isDarkTheme,
    isMobile,
    isTablet,
    isDesktop,
    hasSearchHistory,
    recentSearches,

    // 方法
    initializeApp,
    setTheme,
    toggleTheme,
    setWindowSize,
    setSearchFocus,
    toggleShortcutHelp,
    hideShortcutHelp,
    setPageVisible,
    addSearchHistory,
    clearSearchHistory,
    removeSearchHistoryItem,
    addNotification,
    removeNotification,
    clearNotifications,
    updateSettings,
    resetSettings,
    saveSettingsToStorage,
    loadSettingsFromStorage,
    requestNotificationPermission,
    showBrowserNotification
  }
})