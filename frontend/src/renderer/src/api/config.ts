// AI模型配置API服务

import type {
  AIModelConfigRequest,
  AIModelTestRequest,
  AIModelInfo,
  AIModelTestResult
} from '@/types/api'
import { httpClient } from '@/utils/http'

// AI模型配置服务
export class AIModelConfigService {
  // 更新AI模型配置
  static async updateAIModelConfig(params: AIModelConfigRequest) {
    const requestData = {
      model_type: params.model_type,
      provider: params.provider,
      model_name: params.model_name,
      config: params.config
    }

    return await httpClient.post('/api/config/ai-model', requestData)
  }

  // 获取所有AI模型配置
  static async getAIModels(modelType?: string, provider?: string): Promise<{ success: boolean; data: AIModelInfo[]; message: string }> {
    const params = new URLSearchParams()
    if (modelType) params.append('model_type', modelType)
    if (provider) params.append('provider', provider)

    const url = params.toString() ? `/api/config/ai-models?${params}` : '/api/config/ai-models'
    return await httpClient.get(url)
  }

  // 测试AI模型
  static async testAIModel(modelId: number, request?: AIModelTestRequest): Promise<{ success: boolean; data: AIModelTestResult; message: string }> {
    const requestData = request || {}

    return await httpClient.post(`/api/config/ai-model/${modelId}/test`, requestData)
  }

  // 启用/禁用AI模型
  static async toggleAIModel(modelId: number) {
    return await httpClient.put(`/api/config/ai-model/${modelId}/toggle`)
  }

  // 删除AI模型配置
  static async deleteAIModelConfig(modelId: number) {
    return await httpClient.delete(`/api/config/ai-model/${modelId}`)
  }

  // 获取默认AI模型配置
  static async getDefaultAIModels(): Promise<{ success: boolean; data: AIModelInfo[]; message: string }> {
    return await httpClient.get('/api/config/ai-models/default')
  }

  // 辅助方法：解析模型配置JSON
  static parseModelConfig(configJson: string): Record<string, any> {
    try {
      return JSON.parse(configJson)
    } catch (error) {
      console.error('解析模型配置JSON失败:', error)
      return {}
    }
  }

  // 辅助方法：格式化模型类型显示名称
  static formatModelType(modelType: string): string {
    const typeMap: Record<string, string> = {
      'embedding': '文本嵌入',
      'speech': '语音识别',
      'vision': '图像理解',
      'llm': '大语言模型'
    }
    return typeMap[modelType] || modelType
  }

  // 辅助方法：格式化提供商显示名称
  static formatProvider(provider: string): string {
    const providerMap: Record<string, string> = {
      'local': '本地',
      'cloud': '云端'
    }
    return providerMap[provider] || provider
  }

  // 辅助方法：获取模型状态显示文本
  static getStatusText(isActive: boolean): string {
    return isActive ? '已启用' : '已禁用'
  }

  // 辅助方法：获取测试结果显示文本
  static getTestResultText(testPassed: boolean): string {
    return testPassed ? '测试通过' : '测试失败'
  }
}