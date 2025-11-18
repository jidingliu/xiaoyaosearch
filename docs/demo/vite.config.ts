import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 3000,
    open: 'navigation.html'  // 默认打开导航页面
  },
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        search: resolve(__dirname, 'search.html'),
        settings: resolve(__dirname, 'settings.html'),
        indexManage: resolve(__dirname, 'index-manage.html'),
        help: resolve(__dirname, 'help.html')
      }
    }
  }
})