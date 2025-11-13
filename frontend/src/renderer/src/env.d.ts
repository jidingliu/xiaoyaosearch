/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/ban-types
  const component: DefineComponent<{}, {}, any>
  export default component
}

// Auto-import APIs for Vue, Vue Router and Pinia
declare global {
  const defineStore: typeof import('pinia')['defineStore']
  const storeToRefs: typeof import('pinia')['storeToRefs']
  const useRouter: typeof import('vue-router')['useRouter']
  const useRoute: typeof import('vue-router')['useRoute']
}

// Auto-import APIs for Ant Design Vue
declare global {
  const message: typeof import('ant-design-vue')['message']
  const notification: typeof import('ant-design-vue')['notification']
  const Modal: typeof import('ant-design-vue')['Modal']
}

export {}
