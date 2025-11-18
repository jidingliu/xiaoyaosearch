<template>
  <div style="padding: 20px;">
    <h1>设置页面测试</h1>
    <p>如果您能看到这个页面，说明Vue组件正常工作</p>

    <a-card title="基础测试" style="margin-top: 20px;">
      <p>Ant Design 组件测试</p>
      <a-button type="primary" @click="showMessage">测试按钮</a-button>
    </a-card>

    <div style="margin-top: 20px;">
      <h2>调试信息：</h2>
      <p>组件挂载状态: {{ mountedStatus }}</p>
      <p>当前时间: {{ currentTime }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'

console.log('=== SettingsAppBasic 组件开始创建 ===')

const mountedStatus = ref('未挂载')
const currentTime = ref('')

const showMessage = () => {
  message.success('测试按钮点击成功！')
  console.log('测试按钮被点击')
}

onMounted(() => {
  console.log('=== SettingsAppBasic 组件已挂载 ===')
  mountedStatus.value = '已挂载'
  currentTime.value = new Date().toLocaleTimeString()

  // 每秒更新时间
  setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString()
  }, 1000)
})
</script>