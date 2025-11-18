<template>
  <div class="index-simple">
    <a-layout class="layout">
      <a-layout-header class="header">
        <div class="header-content">
          <div class="logo">
            <span class="logo-icon">📁</span>
            <span class="logo-text">索引管理</span>
          </div>
          <div class="header-actions">
            <a-button @click="goBack">
              <template #icon><ArrowLeftOutlined /></template>
              返回
            </a-button>
          </div>
        </div>
      </a-layout-header>

      <a-layout-content class="content">
        <div class="index-container">
          <a-card title="已索引文件夹" style="margin-bottom: 20px;">
            <div class="folder-item" v-for="(folder, index) in folders" :key="index">
              <h4>{{ folder.name }}</h4>
              <p>文件数: {{ folder.count }} | 大小: {{ folder.size }}</p>
              <a-space>
                <a-button size="small">重建</a-button>
                <a-button size="small" danger>删除</a-button>
              </a-space>
            </div>
          </a-card>

          <a-row :gutter="16">
            <a-col :span="6">
              <a-card>
                <div class="stat-item">
                  <div class="stat-number">{{ totalFiles }}</div>
                  <div class="stat-label">总文件数</div>
                </div>
              </a-card>
            </a-col>
            <a-col :span="6">
              <a-card>
                <div class="stat-item">
                  <div class="stat-number">{{ totalSize }}</div>
                  <div class="stat-label">总大小</div>
                </div>
              </a-card>
            </a-col>
            <a-col :span="6">
              <a-card>
                <div class="stat-item">
                  <div class="stat-number">{{ indexSize }}</div>
                  <div class="stat-label">索引大小</div>
                </div>
              </a-card>
            </a-col>
            <a-col :span="6">
              <a-card>
                <div class="stat-item">
                  <div class="stat-number">{{ progress }}%</div>
                  <div class="stat-label">完成进度</div>
                </div>
              </a-card>
            </a-col>
          </a-row>
        </div>
      </a-layout-content>
    </a-layout>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { ArrowLeftOutlined } from '@ant-design/icons-vue'

const folders = ref([
  { name: 'D:\\Documents', count: 1234, size: '2.3GB' },
  { name: 'D:\\Projects\\AI', count: 567, size: '1.8GB' },
  { name: 'E:\\Books\\技术', count: 2890, size: '5.6GB' }
])

const totalFiles = ref('4,691')
const totalSize = ref('9.7GB')
const indexSize = ref('234MB')
const progress = ref(85)

const goBack = () => {
  message.info('返回上一页')
}

onMounted(() => {
  console.log('索引管理页面已加载')
})
</script>

<style scoped>
.index-simple {
  min-height: 100vh;
  background: #f5f5f5;
}

.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #6366f1;
}

.content {
  padding: 24px;
}

.index-container {
  max-width: 1200px;
  margin: 0 auto;
}

.folder-item {
  padding: 16px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  margin-bottom: 12px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #6366f1;
}

.stat-label {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}
</style>