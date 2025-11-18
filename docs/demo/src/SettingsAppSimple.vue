<template>
  <div class="settings-simple">
    <h1>设置页面 - 简化版</h1>
    <p>这是一个测试页面，用于验证设置页面是否可以正常显示</p>

    <a-card title="LLM模型设置" style="margin: 20px 0;">
      <p>这里是LLM模型配置内容</p>
      <a-button type="primary">测试按钮</a-button>
    </a-card>

    <a-card title="语音识别设置" style="margin: 20px 0;">
      <p>这里是语音识别配置内容</p>
    </a-card>

    <a-card title="视觉模型设置" style="margin: 20px 0;">
      <p>这里是视觉模型配置内容</p>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

console.log('设置页面组件已加载')
</script>

<style scoped>
.settings-simple {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
}
</style>