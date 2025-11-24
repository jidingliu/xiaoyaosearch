<template>
  <div style="padding: 20px;">
    <h1>小遥搜索 - 图标测试页面</h1>
    <p>测试Ant Design Vue图标是否正常工作</p>

    <div style="margin: 20px 0;">
      <h3>基础图标测试：</h3>
      <Space size="large">
        <HomeOutlined />
        <SettingOutlined />
        <DatabaseOutlined />
        <QuestionCircleOutlined />
      </Space>
    </div>

    <div style="margin: 20px 0;">
      <h3>按钮图标测试：</h3>
      <Space>
        <a-button type="primary">
          <HomeOutlined />
          首页
        </a-button>
        <a-button>
          <SettingOutlined />
          设置
        </a-button>
      </Space>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Space } from 'ant-design-vue'
import {
  HomeOutlined,
  SettingOutlined,
  DatabaseOutlined,
  QuestionCircleOutlined
} from '@ant-design/icons-vue'
</script>