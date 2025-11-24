import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// 样式导入
import './styles/global.scss'
import 'ant-design-vue/dist/reset.css'

// Ant Design Vue 按需导入配置
import Antd from 'ant-design-vue'
import {
  ConfigProvider
} from 'ant-design-vue'

// 创建应用实例
const app = createApp(App)

// 配置Ant Design Vue主题
app.use(ConfigProvider, {
  theme: {
    token: {
      // 主色彩配置
      colorPrimary: '#00E5FF',
      colorSuccess: '#4ADE80',
      colorWarning: '#F59E0B',
      colorError: '#EF4444',
      colorInfo: '#3B82F6',

      // 字体配置
      fontFamily: "'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif",
      fontSize: 14,
      fontSizeHeading1: 48,
      fontSizeHeading2: 36,
      fontSizeHeading3: 30,
      fontSizeHeading4: 24,
      fontSizeHeading5: 20,

      // 圆角配置
      borderRadius: 6,
      borderRadiusLG: 12,
      borderRadiusSM: 2,

      // 阴影配置
      boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
      boxShadowSecondary: '0 2px 8px rgba(0, 0, 0, 0.3)',

      // 动画配置
      motionDurationSlow: '0.4s',
      motionDurationMid: '0.3s',
      motionDurationFast: '0.2s',

      // 控件配置
      controlHeight: 40,
      controlHeightSM: 32,
      controlHeightLG: 48,

      // 间距配置
      paddingXS: 8,
      paddingSM: 12,
      padding: 16,
      paddingMD: 20,
      paddingLG: 24,
      paddingXL: 32,

      // 背景配置
      colorBgContainer: 'rgba(26, 31, 75, 0.8)',
      colorBgElevated: 'rgba(37, 43, 78, 0.95)',
      colorBgLayout: '#0A0E27',

      // 边框配置
      colorBorder: 'rgba(255, 255, 255, 0.2)',
      colorBorderSecondary: 'rgba(255, 255, 255, 0.1)',

      // 文字配置
      colorText: '#FFFFFF',
      colorTextSecondary: '#B8BCC8',
      colorTextTertiary: '#7A8299',
      colorTextQuaternary: '#4A5568',

      // 悬停配置
      colorPrimaryHover: '#00B8D4',
      colorPrimaryActive: '#00ACC1'
    },
    algorithm: 'darkAlgorithm'
  }
})

// 使用插件
app.use(createPinia())
app.use(router)
app.use(Antd)

// 全局属性
app.config.globalProperties.$ELEMENT_SIZE = 'large'

// 挂载应用
app.mount('#app')