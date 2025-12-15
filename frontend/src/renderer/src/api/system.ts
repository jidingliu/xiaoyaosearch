// 系统状态API服务

import type { SystemHealth } from '@/types/api'
import { httpClient } from '@/utils/http'

// 系统状态服务
export class SystemService {
  // 获取系统健康状态
  static async getHealth() {
    return await httpClient.get('/api/system/health')
  }

  // 获取系统状态汇总（为底部状态栏设计）
  static async getStatus() {
    return await httpClient.get('/api/system/running-status')
  }
}