import { createApp } from 'vue'
import Antd from 'ant-design-vue'
import App from './IndexAppSimple.vue'
import 'ant-design-vue/dist/reset.css'

console.log('=== 索引管理页面入口文件加载 ===')

const app = createApp(App)
app.use(Antd)
app.mount('#app')