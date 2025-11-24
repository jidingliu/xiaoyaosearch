import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import type { RouteLocationNormalized } from 'vue-router'

// 路由懒加载
const HomePage = () => import('@/pages/HomePage.vue')
const SettingsPage = () => import('@/pages/SettingsPage.vue')
const IndexManagePage = () => import('@/pages/IndexManagePage.vue')
const HelpPage = () => import('@/pages/HelpPage.vue')
const NotFoundPage = () => import('@/pages/NotFoundPage.vue')

// 路由配置
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
    meta: {
      title: '小遥搜索 - 多模态AI智能搜索',
      depth: 1,
      keepAlive: true,
      icon: 'SearchOutlined'
    }
  },
  {
    path: '/search',
    redirect: '/'
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsPage,
    meta: {
      title: '设置 - 小遥搜索',
      depth: 2,
      icon: 'SettingOutlined'
    }
  },
  {
    path: '/index',
    name: 'IndexManage',
    component: IndexManagePage,
    meta: {
      title: '索引管理 - 小遥搜索',
      depth: 2,
      icon: 'DatabaseOutlined'
    }
  },
  {
    path: '/help',
    name: 'Help',
    component: HelpPage,
    meta: {
      title: '帮助与关于 - 小遥搜索',
      depth: 2,
      icon: 'QuestionCircleOutlined'
    }
  },
  {
    path: '/404',
    name: 'NotFound',
    component: NotFoundPage,
    meta: {
      title: '页面未找到 - 小遥搜索',
      depth: 1,
      hideFromNav: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 如果有保存的位置（浏览器前进后退），恢复到那个位置
    if (savedPosition) {
      return savedPosition
    }

    // 如果是跳转到同一个页面，保持当前滚动位置
    if (to.path === from.path) {
      return false
    }

    // 否则滚动到顶部
    return { top: 0, left: 0 }
  }
})

// 全局前置守卫
router.beforeEach(
  (
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: any
  ) => {
    // 设置页面标题
    if (to.meta?.title) {
      document.title = to.meta.title as string
    }

    // 路由切换前的处理
    next()
  }
)

// 全局后置钩子
router.afterEach((to: RouteLocationNormalized, from: RouteLocationNormalized) => {
  // 路由切换后的处理
  console.log(`路由切换: ${from.path} -> ${to.path}`)
})

// 导航错误处理
router.onError((error) => {
  console.error('路由错误:', error)
})

// 路由工具方法
export const useRouterUtils = () => {
  const goToSearch = () => {
    router.push('/')
  }

  const goToSettings = () => {
    router.push('/settings')
  }

  const goToIndexManage = () => {
    router.push('/index')
  }

  const goToHelp = () => {
    router.push('/help')
  }

  const goBack = () => {
    router.go(-1)
  }

  const goForward = () => {
    router.go(1)
  }

  const isActiveRoute = (path: string): boolean => {
    return router.currentRoute.value.path === path
  }

  const isChildRouteActive = (parentPath: string): boolean => {
    return router.currentRoute.value.path.startsWith(parentPath)
  }

  return {
    goToSearch,
    goToSettings,
    goToIndexManage,
    goToHelp,
    goBack,
    goForward,
    isActiveRoute,
    isChildRouteActive
  }
}

export default router