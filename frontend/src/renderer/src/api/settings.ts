// 设置和AI模型配置API服务 - 包含真实API和Mock服务

import type {
  AIModelConfig,
  AIModelConfigRequest,
  AppSettings
} from '@/types/api'

// 真实API服务
export class SettingsService {
  // AI模型配置相关
  static async getAIModels() {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.getAIModels()
  }

  static async updateAIModel(params: AIModelConfigRequest) {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.updateAIModel(params)
  }

  static async testAIModel(id: number) {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.testAIModel(id)
  }

  static async toggleAIModel(id: number) {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.toggleAIModel(id)
  }

  static async deleteAIModel(id: number) {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.deleteAIModel(id)
  }

  static async getDefaultAIModels() {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.getDefaultAIModels()
  }

  // AI模型管理相关
  static async getAIModelStatus() {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.getAIModelStatus()
  }

  static async getAvailableModels() {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.getAvailableModels()
  }

  static async loadAIModel(id: number) {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.loadAIModel(id)
  }

  static async unloadAIModel(id: number) {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.unloadAIModel(id)
  }

  static async loadAllAIModels() {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.loadAllAIModels()
  }

  static async unloadAllAIModels() {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.unloadAllAIModels()
  }

  static async checkAIModelHealth() {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.checkAIModelHealth()
  }

  static async benchmarkAIModels() {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.benchmarkAIModels()
  }

  static async testTextEmbedding(text: string) {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.testTextEmbedding(text)
  }

  // 系统设置相关
  static async getSettings() {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.getSettings()
  }

  static async updateSettings(params: Partial<AppSettings>) {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.updateSettings(params)
  }

  static async getSystemInfo() {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.getSystemInfo()
  }

  static async restartSystem() {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.restartSystem()
  }

  static async getSystemLogs(level?: string, limit = 100, offset = 0) {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.getSystemLogs(level, limit, offset)
  }

  static async downloadSystemLogs(date?: string) {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.downloadSystemLogs(date)
  }

  static async getSystemHealth() {
    // TODO: 替换为真实API调用
    return await SettingsServiceMock.getSystemHealth()
  }
}

// Mock 数据服务
export class SettingsServiceMock {
  private static mockAIModels: Array<AIModelConfig & { id: number }> = [
    {
      id: 1,
      model_type: 'embedding',
      provider: 'local',
      model_name: 'bge-m3',
      config_json: JSON.stringify({
        model_path: '/models/bge-m3',
        device: 'cpu',
        embedding_dim: 768,
        max_length: 8192,
        batch_size: 32
      }),
      is_active: true,
      created_at: '2024-01-10T08:00:00Z',
      updated_at: '2024-01-15T14:30:00Z'
    },
    {
      id: 2,
      model_type: 'speech',
      provider: 'local',
      model_name: 'faster-whisper',
      config_json: JSON.stringify({
        model_size: 'base',
        device: 'cpu',
        compute_type: 'float32',
        language: 'zh'
      }),
      is_active: true,
      created_at: '2024-01-10T08:30:00Z',
      updated_at: '2024-01-15T14:30:00Z'
    },
    {
      id: 3,
      model_type: 'vision',
      provider: 'local',
      model_name: 'cn-clip',
      config_json: JSON.stringify({
        model_name: 'OFA-Sys/chinese-clip-vit-base-patch16',
        device: 'cpu',
        image_size: 224,
        max_length: 77
      }),
      is_active: true,
      created_at: '2024-01-10T09:00:00Z',
      updated_at: '2024-01-15T14:30:00Z'
    },
    {
      id: 4,
      model_type: 'llm',
      provider: 'local',
      model_name: 'qwen2-7b-instruct',
      config_json: JSON.stringify({
        model_path: '/models/qwen2-7b-instruct',
        device: 'cpu',
        temperature: 0.7,
        max_new_tokens: 2048
      }),
      is_active: false,
      created_at: '2024-01-10T09:30:00Z',
      updated_at: '2024-01-15T14:30:00Z'
    },
    {
      id: 5,
      model_type: 'embedding',
      provider: 'cloud',
      model_name: 'text-embedding-ada-002',
      config_json: JSON.stringify({
        api_key: 'sk-***hidden***',
        api_base: 'https://api.openai.com/v1',
        model: 'text-embedding-ada-002',
        dimensions: 1536
      }),
      is_active: false,
      created_at: '2024-01-10T10:00:00Z',
      updated_at: '2024-01-15T14:30:00Z'
    },
    {
      id: 6,
      model_type: 'llm',
      provider: 'cloud',
      model_name: 'gpt-4',
      config_json: JSON.stringify({
        api_key: 'sk-***hidden***',
        api_base: 'https://api.openai.com/v1',
        model: 'gpt-4',
        temperature: 0.7,
        max_tokens: 4096
      }),
      is_active: false,
      created_at: '2024-01-10T10:30:00Z',
      updated_at: '2024-01-15T14:30:00Z'
    }
  ]

  private static nextModelId = 7

  private static mockSettings: AppSettings = {
    app_name: '小遥搜索',
    version: '1.0.0',
    search: {
      default_limit: 20,
      default_threshold: 0.7,
      max_file_size: 52428800 // 50MB
    },
    indexing: {
      max_concurrent_jobs: 3,
      supported_formats: ['pdf', 'txt', 'md', 'docx', 'xlsx', 'pptx', 'mp3', 'mp4', 'wav'],
      auto_rebuild: false
    },
    ui: {
      theme: 'light',
      language: 'zh-CN'
    }
  }

  private static loadedModels: Set<number> = new Set([1, 2, 3]) // 默认加载前3个模型

  // AI模型配置相关
  static async getAIModels() {
    await new Promise(resolve => setTimeout(resolve, 200))

    return {
      success: true,
      data: this.mockAIModels
    }
  }

  static async updateAIModel(params: AIModelConfigRequest) {
    await new Promise(resolve => setTimeout(resolve, 300))

    // 创建新模型配置
    const newModel: AIModelConfig & { id: number } = {
      id: this.nextModelId++,
      model_type: params.model_type,
      provider: params.provider,
      model_name: params.model_name,
      config_json: JSON.stringify(params.config),
      is_active: false, // 新创建的模型默认不激活
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }

    this.mockAIModels.push(newModel)

    return {
      success: true,
      message: 'AI模型配置创建成功',
      data: {
        id: newModel.id,
        model_name: newModel.model_name
      }
    }
  }

  static async testAIModel(id: number) {
    await new Promise(resolve => setTimeout(resolve, 1200 + Math.random() * 800))

    const model = this.mockAIModels.find(m => m.id === id)

    if (!model) {
      return {
        success: false,
        error: {
          code: 'MODEL_NOT_FOUND',
          message: 'AI模型配置不存在',
          details: `模型ID ${id} 未找到`
        }
      }
    }

    // 模拟测试结果
    const testPassed = Math.random() > 0.1 // 90%的测试通过率
    const responseTime = 0.1 + Math.random() * 0.5 // 0.1-0.6秒响应时间

    if (testPassed) {
      return {
        success: true,
        data: {
          model_id: id,
          test_passed: true,
          response_time: responseTime,
          test_message: `${model.model_name} 测试成功，响应时间：${(responseTime * 1000).toFixed(0)}ms`
        }
      }
    } else {
      return {
        success: false,
        error: {
          code: 'MODEL_TEST_FAILED',
          message: 'AI模型测试失败',
          details: `${model.model_name} 测试未通过，请检查配置参数`
        }
      }
    }
  }

  static async toggleAIModel(id: number) {
    await new Promise(resolve => setTimeout(resolve, 200))

    const model = this.mockAIModels.find(m => m.id === id)

    if (!model) {
      return {
        success: false,
        error: {
          code: 'MODEL_NOT_FOUND',
          message: 'AI模型配置不存在',
          details: `模型ID ${id} 未找到`
        }
      }
    }

    const previousStatus = model.is_active
    model.is_active = !model.is_active
    model.updated_at = new Date().toISOString()

    return {
      success: true,
      message: 'AI模型状态切换成功',
      data: {
        model_id: id,
        is_active: model.is_active,
        previous_status: previousStatus
      }
    }
  }

  static async deleteAIModel(id: number) {
    await new Promise(resolve => setTimeout(resolve, 150))

    const modelIndex = this.mockAIModels.findIndex(m => m.id === id)

    if (modelIndex === -1) {
      return {
        success: false,
        error: {
          code: 'MODEL_NOT_FOUND',
          message: 'AI模型配置不存在',
          details: `模型ID ${id} 未找到`
        }
      }
    }

    this.mockAIModels.splice(modelIndex, 1)

    // 从已加载模型中移除
    this.loadedModels.delete(id)

    return {
      success: true,
      message: 'AI模型配置删除成功'
    }
  }

  static async getDefaultAIModels() {
    await new Promise(resolve => setTimeout(resolve, 150))

    const defaultModels = this.mockAIModels.filter(model =>
      (model.model_type === 'embedding' && model.id === 1) ||
      (model.model_type === 'speech' && model.id === 2) ||
      (model.model_type === 'vision' && model.id === 3) ||
      (model.model_type === 'llm' && model.id === 4)
    )

    return {
      success: true,
      data: defaultModels
    }
  }

  // AI模型管理相关
  static async getAIModelStatus() {
    await new Promise(resolve => setTimeout(resolve, 250))

    const models = this.mockAIModels.map(model => ({
      id: model.id,
      model_type: model.model_type,
      model_name: model.model_name,
      status: this.loadedModels.has(model.id) ? 'loaded' : 'not_loaded',
      memory_usage: this.loadedModels.has(model.id) ?
        `${(Math.random() * 3 + 0.5).toFixed(1)}GB` : null,
      load_time: this.loadedModels.has(model.id) ?
        '2025-01-01T10:00:00Z' : null
    }))

    return {
      success: true,
      data: {
        models: models
      }
    }
  }

  static async getAvailableModels() {
    await new Promise(resolve => setTimeout(resolve, 200))

    return {
      success: true,
      data: {
        available_models: [
          {
            model_type: 'embedding',
            models: ['bge-m3', 'text-embedding-ada-002', 'text-embedding-3-small', 'text-embedding-3-large']
          },
          {
            model_type: 'speech',
            models: ['faster-whisper', 'whisper-1', 'aliyun-asr', 'azure-speech']
          },
          {
            model_type: 'vision',
            models: ['cn-clip', 'gpt-4-vision', 'claude-3-vision', 'gemini-pro-vision']
          },
          {
            model_type: 'llm',
            models: ['qwen2-7b-instruct', 'gpt-4', 'claude-3', 'gemini-pro', 'llama-3']
          }
        ]
      }
    }
  }

  static async loadAIModel(id: number) {
    await new Promise(resolve => setTimeout(resolve, 2000 + Math.random() * 3000))

    const model = this.mockAIModels.find(m => m.id === id)

    if (!model) {
      return {
        success: false,
        error: {
          code: 'MODEL_NOT_FOUND',
          message: 'AI模型配置不存在',
          details: `模型ID ${id} 未找到`
        }
      }
    }

    if (this.loadedModels.has(id)) {
      return {
        success: false,
        error: {
          code: 'MODEL_ALREADY_LOADED',
          message: '模型已加载',
          details: `${model.model_name} 已经在内存中`
        }
      }
    }

    this.loadedModels.add(id)

    return {
      success: true,
      message: '模型加载成功',
      data: {
        model_id: id,
        model_name: model.model_name,
        load_time: (2 + Math.random() * 3).toFixed(1),
        memory_usage: `${(Math.random() * 3 + 0.5).toFixed(1)}GB`
      }
    }
  }

  static async unloadAIModel(id: number) {
    await new Promise(resolve => setTimeout(resolve, 500))

    const model = this.mockAIModels.find(m => m.id === id)

    if (!model) {
      return {
        success: false,
        error: {
          code: 'MODEL_NOT_FOUND',
          message: 'AI模型配置不存在',
          details: `模型ID ${id} 未找到`
        }
      }
    }

    if (!this.loadedModels.has(id)) {
      return {
        success: false,
        error: {
          code: 'MODEL_NOT_LOADED',
          message: '模型未加载',
          details: `${model.model_name} 不在内存中`
        }
      }
    }

    const memoryUsage = `${(Math.random() * 3 + 0.5).toFixed(1)}GB`
    this.loadedModels.delete(id)

    return {
      success: true,
      message: '模型卸载成功',
      data: {
        model_id: id,
        freed_memory: memoryUsage
      }
    }
  }

  static async loadAllAIModels() {
    await new Promise(resolve => setTimeout(resolve, 5000 + Math.random() * 3000))

    const modelsToLoad = this.mockAIModels.filter(m => !this.loadedModels.has(m.id))
    const loadedCount = modelsToLoad.length

    modelsToLoad.forEach(model => {
      this.loadedModels.add(model.id)
    })

    return {
      success: true,
      message: '所有模型加载完成',
      data: {
        loaded_count: loadedCount,
        total_memory_usage: `${(this.loadedModels.size * (Math.random() * 2 + 1)).toFixed(1)}GB`,
        load_time: (5 + Math.random() * 3).toFixed(1)
      }
    }
  }

  static async unloadAllAIModels() {
    await new Promise(resolve => setTimeout(resolve, 1000))

    const unloadedCount = this.loadedModels.size
    const totalMemoryUsage = `${(unloadedCount * (Math.random() * 2 + 1)).toFixed(1)}GB`

    this.loadedModels.clear()

    return {
      success: true,
      message: '所有模型卸载完成',
      data: {
        unloaded_count: unloadedCount,
        freed_memory: totalMemoryUsage
      }
    }
  }

  static async checkAIModelHealth() {
    await new Promise(resolve => setTimeout(resolve, 800))

    const models = this.mockAIModels.map(model => ({
      id: model.id,
      model_name: model.model_name,
      status: this.loadedModels.has(model.id) ?
        (Math.random() > 0.05 ? 'healthy' : 'degraded') : 'not_loaded',
      response_time: this.loadedModels.has(model.id) ?
        (Math.random() * 0.3 + 0.05).toFixed(3) : null,
      last_check: new Date().toISOString()
    }))

    const overallStatus = models.some(m => m.status === 'degraded') ? 'degraded' :
      models.some(m => m.status === 'healthy') ? 'healthy' : 'unhealthy'

    return {
      success: true,
      data: {
        overall_status: overallStatus,
        models: models
      }
    }
  }

  static async benchmarkAIModels() {
    await new Promise(resolve => setTimeout(resolve, 10000 + Math.random() * 5000))

    const loadedModels = this.mockAIModels.filter(m => this.loadedModels.has(m.id))

    const testResults = loadedModels.map(model => ({
      model_id: model.id,
      model_name: model.model_name,
      model_type: model.model_type,
      test_type: model.model_type === 'embedding' ? 'embedding' :
                model.model_type === 'speech' ? 'speech' :
                model.model_type === 'vision' ? 'vision' : 'llm',
      avg_response_time: Math.random() * 0.2 + 0.05,
      throughput: model.model_type === 'embedding' ?
        `${Math.floor(Math.random() * 2000 + 500)} vectors/sec` :
        model.model_type === 'speech' ?
        `${Math.floor(Math.random() * 10 + 5)} files/sec` :
        model.model_type === 'vision' ?
        `${Math.floor(Math.random() * 5 + 2)} images/sec` :
        `${Math.floor(Math.random() * 50 + 10)} requests/sec`,
      accuracy: `${(Math.random() * 5 + 93).toFixed(1)}%`
    }))

    return {
      success: true,
      message: '基准测试完成',
      data: {
        test_results: testResults,
        test_duration: (10 + Math.random() * 5).toFixed(1)
      }
    }
  }

  static async testTextEmbedding(text: string) {
    await new Promise(resolve => setTimeout(resolve, 300 + Math.random() * 200))

    const embeddingModel = this.mockAIModels.find(m =>
      m.model_type === 'embedding' && this.loadedModels.has(m.id)
    )

    if (!embeddingModel) {
      return {
        success: false,
        error: {
          code: 'NO_EMBEDDING_MODEL_LOADED',
          message: '没有已加载的文本嵌入模型',
          details: '请先加载一个文本嵌入模型'
        }
      }
    }

    // 生成模拟的嵌入向量 (768维)
    const embedding = Array.from({ length: 768 }, () => Math.random() * 2 - 1)

    return {
      success: true,
      data: {
        text: text,
        embedding: embedding,
        model_used: embeddingModel.model_name,
        embedding_dim: embedding.length,
        processing_time: (0.3 + Math.random() * 0.2).toFixed(3)
      }
    }
  }

  // 系统设置相关
  static async getSettings() {
    await new Promise(resolve => setTimeout(resolve, 150))

    return {
      success: true,
      data: this.mockSettings
    }
  }

  static async updateSettings(params: Partial<AppSettings>) {
    await new Promise(resolve => setTimeout(resolve, 200))

    // 更新设置
    if (params.search) {
      Object.assign(this.mockSettings.search, params.search)
    }
    if (params.indexing) {
      Object.assign(this.mockSettings.indexing, params.indexing)
    }
    if (params.ui) {
      Object.assign(this.mockSettings.ui, params.ui)
    }

    return {
      success: true,
      message: '设置更新成功'
    }
  }

  static async getSystemInfo() {
    await new Promise(resolve => setTimeout(resolve, 200))

    return {
      success: true,
      data: {
        system_info: {
          platform: 'Windows',
          arch: 'x64',
          node_version: '21.0.0',
          electron_version: '28.0.0',
          app_version: '1.0.0',
          uptime: Math.floor(Math.random() * 86400) + 3600, // 1-25小时
          memory_usage: {
            total: Math.floor(Math.random() * 4000000000) + 4000000000, // 4-8GB
            used: Math.floor(Math.random() * 2000000000) + 1000000000, // 1-3GB
            free: Math.floor(Math.random() * 2000000000) + 2000000000  // 2-4GB
          },
          cpu_usage: Math.floor(Math.random() * 30) + 10, // 10-40%
          disk_usage: Math.floor(Math.random() * 40) + 20 // 20-60%
        }
      }
    }
  }

  static async restartSystem() {
    await new Promise(resolve => setTimeout(resolve, 1000))

    return {
      success: true,
      message: '系统重启指令已发送，将在3秒后重启'
    }
  }

  static async getSystemLogs(level = 'info', limit = 100, offset = 0) {
    await new Promise(resolve => setTimeout(resolve, 300))

    const levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
    const modules = ['app.search', 'app.index', 'app.config', 'app.system', 'app.api']

    const mockLogs = Array.from({ length: 50 }, (_, i) => ({
      timestamp: new Date(Date.now() - (i * 60000)).toISOString(),
      level: levels[Math.floor(Math.random() * levels.length)] as any,
      logger: modules[Math.floor(Math.random() * modules.length)],
      message: [
        '搜索请求处理完成',
        '索引创建成功',
        '模型配置更新',
        '系统状态检查正常',
        '文件处理完成',
        'WebSocket连接建立',
        '缓存清理完成',
        '数据库连接正常',
        '模型加载完成',
        '用户配置保存成功'
      ][Math.floor(Math.random() * 10)],
      module: ['search', 'index', 'config', 'system', 'api'][Math.floor(Math.random() * 5)],
      details: {
        query: Math.random() > 0.7 ? '人工智能' : undefined,
        processing_time: Math.random() > 0.8 ? (Math.random() * 0.5).toFixed(3) : undefined,
        file_count: Math.random() > 0.8 ? Math.floor(Math.random() * 100) : undefined
      }
    }))

    // 按级别过滤
    let filteredLogs = mockLogs
    if (level && level !== 'all') {
      filteredLogs = mockLogs.filter(log => log.level === level.toUpperCase())
    }

    const limitedLogs = filteredLogs.slice(offset, offset + limit)

    return {
      success: true,
      data: {
        logs: limitedLogs,
        total: filteredLogs.length,
        has_more: offset + limit < filteredLogs.length
      }
    }
  }

  static async downloadSystemLogs(date?: string) {
    await new Promise(resolve => setTimeout(resolve, 500))

    const targetDate = date || new Date().toISOString().split('T')[0]
    const fileName = `xiaoyao-search-${targetDate}.log`

    return {
      success: true,
      data: {
        download_url: `/api/download/logs/${fileName}`,
        file_name: fileName,
        file_size: Math.floor(Math.random() * 10000000) + 1000000, // 1-11MB
        created_at: new Date().toISOString()
      }
    }
  }

  static async getSystemHealth() {
    await new Promise(resolve => setTimeout(resolve, 400))

    const loadedModels = this.mockAIModels.filter(m => this.loadedModels.has(m.id))

    return {
      success: true,
      data: {
        status: 'healthy',
        database: {
          status: 'connected',
          response_time: 0.002
        },
        ai_models: {
          [loadedModels[0]?.model_name || 'bge-m3']: {
            status: 'loaded',
            memory_usage: '2.1GB',
            error: null
          },
          [loadedModels[1]?.model_name || 'faster-whisper']: {
            status: 'not_loaded',
            memory_usage: null,
            error: null
          }
        },
        indexes: {
          faiss_index: {
            status: 'ready',
            document_count: Math.floor(Math.random() * 20000) + 10000
          },
          whoosh_index: {
            status: 'ready',
            document_count: Math.floor(Math.random() * 20000) + 10000
          }
        },
        timestamp: new Date().toISOString()
      }
    }
  }
}