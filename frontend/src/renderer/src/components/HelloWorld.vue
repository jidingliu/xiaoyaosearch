<template>
  <div class="hello-world">
    <a-space direction="vertical" size="large">
      <h1>欢迎使用小遥搜索</h1>

      <a-alert
        message="这是 Ant Design Vue 4.1+ 的集成示例"
        type="success"
        show-icon
      />

      <a-row :gutter="16">
        <a-col :span="12">
          <a-input
            v-model:value="inputText"
            placeholder="请输入搜索内容"
            @pressEnter="handleSearch"
          >
            <template #suffix>
              <a-button type="primary" @click="handleSearch" :loading="loading">
                <template #icon>
                  <SearchOutlined />
                </template>
                搜索
              </a-button>
            </template>
          </a-input>
        </a-col>

        <a-col :span="12">
          <a-button type="default" @click="showMessage">
            显示消息
          </a-button>
          <a-button type="primary" @click="showModal">
            打开对话框
          </a-button>
        </a-col>
      </a-row>

      <a-table
        :columns="columns"
        :data-source="dataSource"
        :loading="tableLoading"
        size="small"
      />
    </a-space>

    <!-- 模态框 -->
    <a-modal
      v-model:open="modalVisible"
      title="小遥搜索"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
    >
      <p>这是一个使用 Ant Design Vue 构建的示例对话框。</p>
      <p>小遥搜索提供强大的AI驱动搜索功能。</p>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { message } from 'ant-design-vue'

// 响应式数据
const inputText = ref('')
const loading = ref(false)
const modalVisible = ref(false)
const tableLoading = ref(false)

// 表格数据
const dataSource = ref([
  {
    key: '1',
    name: '文档1.pdf',
    type: 'PDF文档',
    size: '2.3MB',
    modified: '2024-01-15'
  },
  {
    key: '2',
    name: '图片1.jpg',
    type: '图片文件',
    size: '1.5MB',
    modified: '2024-01-14'
  },
  {
    key: '3',
    name: '笔记.md',
    type: 'Markdown',
    size: '15KB',
    modified: '2024-01-13'
  }
])

// 表格列定义
const columns = reactive([
  {
    title: '文件名',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '类型',
    dataIndex: 'type',
    key: 'type',
  },
  {
    title: '大小',
    dataIndex: 'size',
    key: 'size',
  },
  {
    title: '修改时间',
    dataIndex: 'modified',
    key: 'modified',
  },
])

// 方法
const handleSearch = () => {
  if (!inputText.value.trim()) {
    message.warning('请输入搜索内容')
    return
  }

  loading.value = true
  message.info(`正在搜索: ${inputText.value}`)

  // 模拟搜索延迟
  setTimeout(() => {
    loading.value = false
    message.success('搜索完成!')
  }, 1000)
}

const showMessage = () => {
  message.success('这是小遥搜索的示例消息!')
}

const showModal = () => {
  modalVisible.value = true
}

const handleModalOk = () => {
  modalVisible.value = false
  message.info('对话框已确认')
}

const handleModalCancel = () => {
  modalVisible.value = false
  message.info('对话框已取消')
}
</script>

<style scoped>
.hello-world {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.hello-world h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #1890ff;
}
</style>