// 索引管理API服务 - 包含真实API和Mock服务

import type {
  IndexCreateRequest,
  IndexStatus
} from '@/types/api'

// 真实API服务
export class IndexService {
  // 创建索引
  static async createIndex(params: IndexCreateRequest) {
    // TODO: 替换为真实API调用
    return await IndexServiceMock.createIndex(params)
  }

  // 查询索引状态
  static async getIndexStatus(id: number) {
    // TODO: 替换为真实API调用
    return await IndexServiceMock.getIndexStatus(id)
  }

  // 索引列表
  static async getIndexList(status?: string, limit = 10) {
    // TODO: 替换为真实API调用
    return await IndexServiceMock.getIndexList(status, limit)
  }

  // 删除索引
  static async deleteIndex(id: number) {
    // TODO: 替换为真实API调用
    return await IndexServiceMock.deleteIndex(id)
  }

  // 停止索引
  static async stopIndex(id: number) {
    // TODO: 替换为真实API调用
    return await IndexServiceMock.stopIndex(id)
  }

  // 更新索引
  static async updateIndex(id: number, params: Partial<IndexCreateRequest>) {
    // TODO: 替换为真实API调用
    return await IndexServiceMock.updateIndex(id, params)
  }

  // 备份索引
  static async backupIndex(id: number) {
    // TODO: 替换为真实API调用
    return await IndexServiceMock.backupIndex(id)
  }

  // 获取已索引文件列表
  static async getIndexedFiles(indexId?: number, limit = 50) {
    // TODO: 替换为真实API调用
    return await IndexServiceMock.getIndexedFiles(indexId, limit)
  }

  // 删除文件索引
  static async deleteFileIndex(fileId: number) {
    // TODO: 替换为真实API调用
    return await IndexServiceMock.deleteFileIndex(fileId)
  }

  // 获取系统索引状态
  static async getSystemIndexStatus() {
    // TODO: 替换为真实API调用
    return await IndexServiceMock.getSystemIndexStatus()
  }
}

// Mock 数据服务
export class IndexServiceMock {
  private static mockIndexes: Array<IndexStatus & { id: number }> = [
    {
      id: 1,
      index_id: 1,
      folder_path: 'D:\\Documents',
      status: 'completed',
      progress: 100,
      total_files: 156,
      processed_files: 154,
      error_count: 2,
      started_at: '2024-01-15T09:00:00Z',
      completed_at: '2024-01-15T09:25:00Z',
      error_message: null
    },
    {
      id: 2,
      index_id: 2,
      folder_path: 'D:\\Downloads',
      status: 'processing',
      progress: 65,
      total_files: 234,
      processed_files: 152,
      error_count: 1,
      started_at: '2024-01-20T10:30:00Z',
      completed_at: null,
      error_message: null
    },
    {
      id: 3,
      index_id: 3,
      folder_path: 'D:\\Projects',
      status: 'failed',
      progress: 30,
      total_files: 89,
      processed_files: 27,
      error_count: 5,
      started_at: '2024-01-19T14:00:00Z',
      completed_at: '2024-01-19T14:08:00Z',
      error_message: '部分文件权限不足，无法访问'
    },
    {
      id: 4,
      index_id: 4,
      folder_path: 'D:\\Desktop',
      status: 'pending',
      progress: 0,
      total_files: 45,
      processed_files: 0,
      error_count: 0,
      started_at: null,
      completed_at: null,
      error_message: null
    }
  ]

  private static nextIndexId = 5

  static async createIndex(params: IndexCreateRequest) {
    // 模拟网络延迟
    await new Promise(resolve => setTimeout(resolve, 500))

    // 检查是否已有相同路径的索引
    const existingIndex = this.mockIndexes.find(
      index => index.folder_path === params.folder_path &&
      (index.status === 'pending' || index.status === 'processing')
    )

    if (existingIndex) {
      return {
        success: false,
        error: {
          code: 'INDEX_ALREADY_EXISTS',
          message: '该文件夹正在索引中或等待处理',
          details: `文件夹 ${params.folder_path} 已存在索引任务 (ID: ${existingIndex.id})`
        }
      }
    }

    // 创建新索引任务
    const newIndex = {
      id: this.nextIndexId++,
      index_id: this.nextIndexId - 1,
      folder_path: params.folder_path,
      status: 'pending' as const,
      progress: 0,
      total_files: Math.floor(Math.random() * 200) + 50, // 随机50-250个文件
      processed_files: 0,
      error_count: 0,
      started_at: null,
      completed_at: null,
      error_message: null
    }

    this.mockIndexes.push(newIndex)

    // 模拟索引开始处理
    setTimeout(() => {
      const index = this.mockIndexes.find(i => i.id === newIndex.id)
      if (index && index.status === 'pending') {
        index.status = 'processing'
        index.started_at = new Date().toISOString()
        this.simulateIndexProgress(index)
      }
    }, 2000)

    return {
      success: true,
      data: {
        index_id: newIndex.id,
        status: 'pending',
        message: '索引任务已创建，等待开始处理'
      }
    }
  }

  // 模拟索引进度更新
  private static simulateIndexProgress(index: typeof IndexServiceMock.mockIndexes[0]) {
    const progressInterval = setInterval(() => {
      if (index.status === 'processing') {
        const increment = Math.random() * 15 + 5 // 5-20的进度增量
        index.progress = Math.min(index.progress + increment, 100)

        // 更新已处理文件数
        index.processed_files = Math.floor((index.progress / 100) * index.total_files)

        // 随机产生一些错误
        if (Math.random() < 0.05 && index.error_count < 3) {
          index.error_count++
        }

        // 检查是否完成
        if (index.progress >= 100) {
          index.status = 'completed'
          index.completed_at = new Date().toISOString()
          index.processed_files = index.total_files - index.error_count
          clearInterval(progressInterval)
        } else if (Math.random() < 0.02) { // 2%的概率失败
          index.status = 'failed'
          index.completed_at = new Date().toISOString()
          index.error_message = '索引过程中发生未知错误'
          clearInterval(progressInterval)
        }
      } else {
        clearInterval(progressInterval)
      }
    }, 1000) // 每秒更新一次进度
  }

  static async getIndexStatus(id: number) {
    await new Promise(resolve => setTimeout(resolve, 200))

    const index = this.mockIndexes.find(i => i.id === id)

    if (!index) {
      return {
        success: false,
        error: {
          code: 'INDEX_NOT_FOUND',
          message: '索引任务不存在',
          details: `索引ID ${id} 未找到`
        }
      }
    }

    return {
      success: true,
      data: index
    }
  }

  static async getIndexList(status?: string, limit = 10) {
    await new Promise(resolve => setTimeout(resolve, 150))

    let filteredIndexes = this.mockIndexes

    if (status && status !== 'all') {
      filteredIndexes = filteredIndexes.filter(index => index.status === status)
    }

    // 按创建时间倒序排序（ID大的代表新创建的）
    filteredIndexes.sort((a, b) => b.id - a.id)

    const limitedIndexes = filteredIndexes.slice(0, limit)

    return {
      success: true,
      data: {
        indexes: limitedIndexes,
        total: filteredIndexes.length
      }
    }
  }

  static async deleteIndex(id: number) {
    await new Promise(resolve => setTimeout(resolve, 300))

    const index = this.mockIndexes.find(i => i.id === id)

    if (!index) {
      return {
        success: false,
        error: {
          code: 'INDEX_NOT_FOUND',
          message: '索引任务不存在',
          details: `索引ID ${id} 未找到`
        }
      }
    }

    if (index.status === 'processing') {
      return {
        success: false,
        error: {
          code: 'INDEX_IS_PROCESSING',
          message: '无法删除正在处理的索引任务',
          details: '请先停止索引任务后再删除'
        }
      }
    }

    const indexToDelete = this.mockIndexes.findIndex(i => i.id === id)
    this.mockIndexes.splice(indexToDelete, 1)

    return {
      success: true,
      message: '索引删除成功'
    }
  }

  static async stopIndex(id: number) {
    await new Promise(resolve => setTimeout(resolve, 400))

    const index = this.mockIndexes.find(i => i.id === id)

    if (!index) {
      return {
        success: false,
        error: {
          code: 'INDEX_NOT_FOUND',
          message: '索引任务不存在',
          details: `索引ID ${id} 未找到`
        }
      }
    }

    if (index.status !== 'processing') {
      return {
        success: false,
        error: {
          code: 'INDEX_NOT_PROCESSING',
          message: '索引任务未在处理中',
          details: `当前状态: ${index.status}`
        }
      }
    }

    index.status = 'failed'
    index.completed_at = new Date().toISOString()
    index.error_message = '用户手动停止索引任务'

    return {
      success: true,
      message: '索引任务已停止'
    }
  }

  static async updateIndex(id: number, params: Partial<IndexCreateRequest>) {
    await new Promise(resolve => setTimeout(resolve, 350))

    const index = this.mockIndexes.find(i => i.id === id)

    if (!index) {
      return {
        success: false,
        error: {
          code: 'INDEX_NOT_FOUND',
          message: '索引任务不存在',
          details: `索引ID ${id} 未找到`
        }
      }
    }

    if (index.status === 'processing') {
      return {
        success: false,
        error: {
          code: 'INDEX_IS_PROCESSING',
          message: '无法更新正在处理的索引任务',
          details: '请先停止索引任务后再更新'
        }
      }
    }

    // 只允许更新已完成或失败的索引
    if (params.folder_path) {
      index.folder_path = params.folder_path
    }

    // 重置索引状态
    index.status = 'pending'
    index.progress = 0
    index.processed_files = 0
    index.error_count = 0
    index.started_at = null
    index.completed_at = null
    index.error_message = null

    // 重新模拟索引进度
    setTimeout(() => {
      if (index.status === 'pending') {
        index.status = 'processing'
        index.started_at = new Date().toISOString()
        this.simulateIndexProgress(index)
      }
    }, 1000)

    return {
      success: true,
      message: '索引更新成功，将重新开始处理'
    }
  }

  static async backupIndex(id: number) {
    await new Promise(resolve => setTimeout(resolve, 800))

    const index = this.mockIndexes.find(i => i.id === id)

    if (!index) {
      return {
        success: false,
        error: {
          code: 'INDEX_NOT_FOUND',
          message: '索引任务不存在',
          details: `索引ID ${id} 未找到`
        }
      }
    }

    if (index.status !== 'completed') {
      return {
        success: false,
        error: {
          code: 'INDEX_NOT_COMPLETED',
          message: '只能备份已完成的索引',
          details: `当前状态: ${index.status}`
        }
      }
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    const backupName = `index_backup_${id}_${timestamp}`

    return {
      success: true,
      message: '索引备份成功',
      data: {
        backup_name: backupName,
        backup_path: `D:\\xiaoyao_search\\backups\\${backupName}.zip`,
        backup_size: Math.floor(Math.random() * 100000000) + 10000000 // 10MB-110MB
      }
    }
  }

  static async getIndexedFiles(indexId?: number, limit = 50) {
    await new Promise(resolve => setTimeout(resolve, 250))

    // 模拟文件数据
    const mockFiles = [
      { id: 1, file_name: 'AI技术文档.pdf', file_path: 'D:\\Documents\\AI技术文档.pdf', file_size: 2048576, file_type: 'pdf', indexed_at: '2024-01-15T09:05:00Z' },
      { id: 2, file_name: '机器学习入门.docx', file_path: 'D:\\Documents\\机器学习入门.docx', file_size: 1048576, file_type: 'docx', indexed_at: '2024-01-15T09:06:00Z' },
      { id: 3, file_name: '数据分析教程.md', file_path: 'D:\\Documents\\数据分析教程.md', file_size: 524288, file_type: 'md', indexed_at: '2024-01-15T09:07:00Z' },
      { id: 4, file_name: '深度学习笔记.txt', file_path: 'D:\\Documents\\深度学习笔记.txt', file_size: 262144, file_type: 'txt', indexed_at: '2024-01-15T09:08:00Z' },
      { id: 5, file_name: 'Python代码示例.py', file_path: 'D:\\Documents\\Python代码示例.py', file_size: 131072, file_type: 'py', indexed_at: '2024-01-15T09:09:00Z' },
      { id: 6, file_name: '项目计划.xlsx', file_path: 'D:\\Documents\\项目计划.xlsx', file_size: 3145728, file_type: 'xlsx', indexed_at: '2024-01-15T09:10:00Z' },
      { id: 7, file_name: '会议记录.pptx', file_path: 'D:\\Documents\\会议记录.pptx', file_size: 4194304, file_type: 'pptx', indexed_at: '2024-01-15T09:11:00Z' },
      { id: 8, file_name: 'API文档.pdf', file_path: 'D:\\Documents\\API文档.pdf', file_size: 1572864, file_type: 'pdf', indexed_at: '2024-01-15T09:12:00Z' },
      { id: 9, file_name: '用户手册.doc', file_path: 'D:\\Documents\\用户手册.doc', file_size: 2097152, file_type: 'doc', indexed_at: '2024-01-15T09:13:00Z' },
      { id: 10, file_name: '配置文件.json', file_path: 'D:\\Documents\\配置文件.json', file_size: 65536, file_type: 'json', indexed_at: '2024-01-15T09:14:00Z' }
    ]

    // 如果指定了indexId，只返回该索引的文件
    let filteredFiles = mockFiles
    if (indexId) {
      // 根据indexId筛选文件（这里简化处理）
      const startIndex = (indexId - 1) * 10
      filteredFiles = mockFiles.slice(startIndex, startIndex + 10)
    }

    const limitedFiles = filteredFiles.slice(0, limit)

    return {
      success: true,
      data: {
        files: limitedFiles,
        total: filteredFiles.length
      }
    }
  }

  static async deleteFileIndex(fileId: number) {
    await new Promise(resolve => setTimeout(resolve, 200))

    // 模拟文件删除
    return {
      success: true,
      message: `文件索引删除成功 (文件ID: ${fileId})`
    }
  }

  static async getSystemIndexStatus() {
    await new Promise(resolve => setTimeout(resolve, 300))

    const totalIndexes = this.mockIndexes.length
    const completedIndexes = this.mockIndexes.filter(i => i.status === 'completed').length
    const processingIndexes = this.mockIndexes.filter(i => i.status === 'processing').length
    const pendingIndexes = this.mockIndexes.filter(i => i.status === 'pending').length
    const failedIndexes = this.mockIndexes.filter(i => i.status === 'failed').length

    const totalDocuments = this.mockIndexes.reduce((sum, index) => sum + (index.total_files || 0), 0)
    const processedDocuments = this.mockIndexes.reduce((sum, index) => sum + (index.processed_files || 0), 0)
    const totalErrors = this.mockIndexes.reduce((sum, index) => sum + (index.error_count || 0), 0)

    return {
      success: true,
      data: {
        system_status: processingIndexes > 0 ? 'processing' : 'healthy',
        indexes: {
          total: totalIndexes,
          completed: completedIndexes,
          processing: processingIndexes,
          pending: pendingIndexes,
          failed: failedIndexes
        },
        documents: {
          total: totalDocuments,
          processed: processedDocuments,
          errors: totalErrors,
          success_rate: totalDocuments > 0 ? ((processedDocuments / totalDocuments) * 100).toFixed(1) : '0'
        },
        storage: {
          used_size: Math.floor(Math.random() * 1000000000) + 500000000, // 500MB-1.5GB
          available_size: Math.floor(Math.random() * 5000000000) + 1000000000 // 1GB-6GB
        },
        last_updated: new Date().toISOString()
      }
    }
  }
}