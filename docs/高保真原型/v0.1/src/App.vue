<template>
  <div id="app" class="app-container" :data-theme="theme">
    <!-- 背景装饰 -->
    <div class="background-decoration">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="noise-overlay"></div>
    </div>

    <!-- 主应用容器 -->
    <div class="app-layout">
      <!-- 顶部导航栏 -->
      <AppHeader />

      <!-- 主内容区域 -->
      <main class="main-content">
        <router-view v-slot="{ Component, route }">
          <transition
            :name="getTransitionName(route)"
            mode="out-in"
            appear
          >
            <component :is="Component" :key="route.path" />
          </transition>
        </router-view>
      </main>
    </div>

    <!-- 全局消息容器 -->
    <div class="global-message-container">
      <!-- 这里可以放置全局消息提示 -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/useAppStore'
import AppHeader from '@/components/layout/AppHeader.vue'

const route = useRoute()
const appStore = useAppStore()

// 主题状态
const theme = computed(() => appStore.theme)

// 页面切换动画名称
const getTransitionName = (currentRoute: any) => {
  // 根据路由层级决定动画方向
  const routeDepth = currentRoute.meta?.depth || 1

  if (routeDepth > 1) {
    return 'slide-left'
  } else if (routeDepth < 1) {
    return 'slide-right'
  }

  return 'fade'
}

// 全局键盘快捷键
const handleKeydown = (event: KeyboardEvent) => {
  // Ctrl/Cmd + K 快速搜索
  if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
    event.preventDefault()
    // 触发全局搜索框聚焦
    appStore.setSearchFocus(true)
  }

  // ESC 清除搜索或关闭弹窗
  if (event.key === 'Escape') {
    appStore.setSearchFocus(false)
    appStore.clearSearchQuery()
  }

  // Ctrl/Cmd + / 显示快捷键帮助
  if ((event.ctrlKey || event.metaKey) && event.key === '/') {
    event.preventDefault()
    appStore.toggleShortcutHelp()
  }
}

// 页面可见性变化处理
const handleVisibilityChange = () => {
  if (document.hidden) {
    // 页面隐藏时暂停一些操作
    appStore.setPageVisible(false)
  } else {
    // 页面显示时恢复操作
    appStore.setPageVisible(true)
  }
}

// 窗口大小变化处理
const handleResize = () => {
  appStore.setWindowSize({
    width: window.innerWidth,
    height: window.innerHeight
  })
}

onMounted(() => {
  // 初始化窗口大小
  handleResize()

  // 添加事件监听
  document.addEventListener('keydown', handleKeydown)
  document.addEventListener('visibilitychange', handleVisibilityChange)
  window.addEventListener('resize', handleResize)

  // 初始化应用
  appStore.initializeApp()
})

onUnmounted(() => {
  // 清理事件监听
  document.removeEventListener('keydown', handleKeydown)
  document.removeEventListener('visibilitychange', handleVisibilityChange)
  window.removeEventListener('resize', handleResize)
})
</script>

<style lang="scss" scoped>
.app-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: var(--surface-primary);
  color: var(--text-primary);
  font-family: var(--font-display);
}

// 背景装饰
.background-decoration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: float 20s ease-in-out infinite;

  &.orb-1 {
    top: -20%;
    left: -10%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, var(--accent-cyan) 0%, transparent 70%);
    animation-delay: 0s;
  }

  &.orb-2 {
    top: 60%;
    right: -15%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, var(--accent-magenta) 0%, transparent 70%);
    animation-delay: 5s;
  }

  &.orb-3 {
    bottom: -25%;
    left: 50%;
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, var(--primary-core) 0%, transparent 70%);
    animation-delay: 10s;
  }
}

.noise-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.03;
  background-image:
    repeating-linear-gradient(45deg, transparent, transparent 2px, rgba(255,255,255,.1) 2px, rgba(255,255,255,.1) 4px);
  pointer-events: none;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(30px, -40px) scale(1.1);
  }
  50% {
    transform: translate(-20px, 30px) scale(0.9);
  }
  75% {
    transform: translate(-30px, -20px) scale(1.05);
  }
}

// 应用布局
.app-layout {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

.main-content {
  flex: 1;
  overflow: hidden;
  position: relative;
}

// 路由过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s var(--ease-out-cubic);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-left-enter-active,
.slide-left-leave-active {
  transition: all 0.4s var(--ease-out-cubic);
}

.slide-left-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-left-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.4s var(--ease-out-cubic);
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.slide-right-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

// 全局消息容器
.global-message-container {
  position: fixed;
  top: var(--header-height, 72px);
  right: var(--space-4);
  z-index: var(--z-toast);
  pointer-events: none;

  > * {
    pointer-events: auto;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .gradient-orb {
    filter: blur(60px);

    &.orb-1 {
      width: 400px;
      height: 400px;
    }

    &.orb-2 {
      width: 350px;
      height: 350px;
    }

    &.orb-3 {
      width: 500px;
      height: 500px;
    }
  }

  .slide-left-enter-from,
  .slide-right-leave-to {
    transform: translateX(20px);
  }

  .slide-left-leave-to,
  .slide-right-enter-from {
    transform: translateX(-20px);
  }
}

// 高对比度模式
@media (prefers-contrast: high) {
  .noise-overlay {
    opacity: 0;
  }

  .gradient-orb {
    opacity: 0.2;
    filter: blur(40px);
  }
}

// 减少动画模式
@media (prefers-reduced-motion: reduce) {
  .gradient-orb {
    animation: none;
  }

  .fade-enter-active,
  .fade-leave-active,
  .slide-left-enter-active,
  .slide-left-leave-active,
  .slide-right-enter-active,
  .slide-right-leave-active {
    transition-duration: 0.01ms;
  }
}
</style>