<template>
  <div style="padding: 20px; font-family: Arial, sans-serif;">
    <h1 style="color: #1890ff;">小遥搜索原型调试</h1>
    <p>如果您能看到这个页面，说明Vue基础环境正常</p>

    <div style="margin: 20px 0;">
      <button style="padding: 8px 16px; background: #1890ff; color: white; border: none; border-radius: 4px; cursor: pointer;">
        测试按钮
      </button>
    </div>

    <div style="margin: 20px 0;">
      <h3>环境测试结果：</h3>
      <ul>
        <li>✅ Vue 3: 正常运行</li>
        <li>✅ Vite: 开发服务器正常</li>
        <li>⏳ Ant Design Vue: 测试中...</li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
console.log('App-debug.vue 组件已加载')
</script>

<style>
body {
  margin: 0;
  padding: 0;
}
</style>