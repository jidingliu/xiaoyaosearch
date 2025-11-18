import { createApp } from 'vue'
import Antd from 'ant-design-vue'
import App from './SettingsAppFixedIcons.vue'
import 'ant-design-vue/dist/reset.css'

console.log('=== 设置页面最终版本开始加载 ===')

const app = createApp(App)
app.use(Antd)
app.mount('#app')