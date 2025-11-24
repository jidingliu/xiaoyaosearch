# 小遥搜索项目接口Mock数据集

## 📋 概述

本项目为小遥搜索(XiaoyaoSearch)提供完整的接口Mock数据集，支持前端开发和测试阶段使用，实现前后端并行开发。

### 🎯 项目目标

- **支持前后端并行开发**：前端团队可以基于Mock数据进行开发，无需等待后端API实现
- **完整的接口覆盖**：涵盖所有核心业务接口，包括正常、异常、边界等场景
- **真实的业务场景**：Mock数据基于真实业务需求设计，符合用户实际使用场景
- **易于集成使用**：提供详细的使用说明和集成示例

### 📊 数据统计

- **接口数量**：15个核心接口
- **Mock数据文件**：13个JSON文件
- **场景覆盖**：正常场景、异常场景、边界场景
- **消息类型**：REST API + WebSocket消息

## 🗂️ 文件结构

```
docs/接口mock数据集/
├── README.md                              # 本说明文档
├── 搜索服务/                              # 搜索相关接口Mock数据
│   ├── 文本搜索.json                      # POST /api/search
│   ├── 多模态搜索.json                    # POST /api/search/multimodal
│   └── 搜索历史.json                      # GET /api/search/history
├── 索引管理/                              # 索引管理接口Mock数据
│   ├── 创建索引.json                      # POST /api/index/create
│   ├── 索引状态查询.json                  # GET /api/index/status/{index_id}
│   ├── 删除索引.json                      # DELETE /api/index/{index_id}
│   └── 索引列表.json                      # GET /api/index/list
├── AI模型配置/                            # AI模型配置接口Mock数据
│   ├── 更新模型配置.json                  # POST /api/config/ai-model
│   ├── 获取模型列表.json                  # GET /api/config/ai-models
│   └── 测试模型.json                      # POST /api/config/ai-model/{model_id}/test
├── 系统管理/                              # 系统管理接口Mock数据
│   ├── 获取设置.json                      # GET /api/settings
│   ├── 更新设置.json                      # POST /api/settings
│   └── 系统健康检查.json                   # GET /api/system/health
└── WebSocket消息/                         # WebSocket实时消息Mock数据
    ├── 索引进度推送.json                   # ws://.../ws/index/{index_id}
    └── 搜索建议推送.json                   # ws://.../ws/search-suggest
```

## 🚀 快速开始

### 1. 开发环境集成

#### 方式一：文件直接读取
```typescript
// 前端项目中使用Mock数据
import mockSearchData from '@/mock/搜索服务/文本搜索.json';

// 使用Mock数据进行开发测试
const handleSearch = async (params: SearchParams) => {
  // 开发环境使用Mock数据
  if (process.env.NODE_ENV === 'development') {
    return mockSearchData;
  }

  // 生产环境调用真实API
  return await api.post('/api/search', params);
};
```

#### 方式二：Mock服务集成
```typescript
// 创建Mock服务类
class MockService {
  private static instance: MockService;

  static getInstance(): MockService {
    if (!MockService.instance) {
      MockService.instance = new MockService();
    }
    return MockService.instance;
  }

  // 模拟网络延迟
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // 文本搜索Mock
  async search(params: SearchRequest): Promise<any> {
    await this.delay(500); // 模拟网络延迟

    // 根据查询条件返回不同的Mock数据
    if (params.query === '人工智能发展趋势') {
      return require('@/mock/搜索服务/文本搜索.json');
    }

    // 返回默认成功响应
    return {
      success: true,
      data: {
        results: [],
        total: 0,
        search_time: 0.05
      }
    };
  }
}
```

### 2. 环境切换配置

```typescript
// api.config.ts
export const API_CONFIG = {
  development: {
    baseURL: 'http://127.0.0.1:8000',
    useMock: true,
    mockDelay: 500
  },
  production: {
    baseURL: 'http://127.0.0.1:8000',
    useMock: false
  }
};

// 根据环境自动选择
const currentConfig = API_CONFIG[process.env.NODE_ENV as keyof typeof API_CONFIG];
```

## 📱 接口分类详情

### 1. 搜索服务接口

#### 文本搜索 (`POST /api/search`)
- **功能**：支持语义搜索、全文搜索和混合搜索
- **文件**：`搜索服务/文本搜索.json`
- **场景覆盖**：正常搜索、无结果、参数错误、服务器错误
- **特色功能**：多文件类型搜索、相关度评分、结果高亮

#### 多模态搜索 (`POST /api/search/multimodal`)
- **功能**：支持语音输入和图像输入的智能搜索
- **文件**：`搜索服务/多模态搜索.json`
- **场景覆盖**：语音识别、图像理解、文件过大、格式错误
- **特色功能**：语音转文本、图像内容分析、多格式支持

#### 搜索历史 (`GET /api/search/history`)
- **功能**：获取用户搜索历史记录
- **文件**：`搜索服务/搜索历史.json`
- **场景覆盖**：分页查询、不同输入类型、空历史记录
- **特色功能**：搜索历史统计、性能指标、快速重搜

### 2. 索引管理接口

#### 创建索引 (`POST /api/index/create`)
- **功能**：创建文件索引任务
- **文件**：`索引管理/创建索引.json`
- **场景覆盖**：不同文件类型、权限错误、资源不足
- **特色功能**：递归索引、进度预估、错误处理

#### 索引状态查询 (`GET /api/index/status/{index_id}`)
- **功能**：查询索引任务状态和进度
- **文件**：`索引管理/索引状态查询.json`
- **场景覆盖**：处理中、已完成、失败、暂停状态
- **特色功能**：实时进度、错误统计、性能监控

#### 删除索引 (`DELETE /api/index/{index_id}`)
- **功能**：删除索引任务和相关文件
- **文件**：`索引管理/删除索引.json`
- **场景覆盖**：成功删除、权限不足、文件清理
- **特色功能**：空间释放、批量清理、错误恢复

#### 索引列表 (`GET /api/index/list`)
- **功能**：获取索引任务列表
- **文件**：`索引管理/索引列表.json`
- **场景覆盖**：状态过滤、分页查询、空列表
- **特色功能**：状态统计、批量操作、搜索过滤

### 3. AI模型配置接口

#### 更新模型配置 (`POST /api/config/ai-model`)
- **功能**：配置本地和云端AI模型
- **文件**：`AI模型配置/更新模型配置.json`
- **场景覆盖**：本地模型、云端API、配置验证
- **特色功能**：多模型支持、自动验证、性能优化

#### 获取模型列表 (`GET /api/config/ai-models`)
- **功能**：获取所有AI模型配置
- **文件**：`AI模型配置/获取模型列表.json`
- **场景覆盖**：按类型过滤、状态监控、性能指标
- **特色功能**：健康检查、使用统计、资源监控

#### 测试模型 (`POST /api/config/ai-model/{model_id}/test`)
- **功能**：测试AI模型连接和功能
- **文件**：`AI模型配置/测试模型.json`
- **场景覆盖**：功能测试、性能测试、错误诊断
- **特色功能**：详细测试报告、性能基准、故障排查

### 4. 系统管理接口

#### 获取设置 (`GET /api/settings`)
- **功能**：获取应用程序完整配置
- **文件**：`系统管理/获取设置.json`
- **场景覆盖**：完整设置、模块过滤、默认配置
- **特色功能**：分类管理、配置验证、备份恢复

#### 更新设置 (`POST /api/settings`)
- **功能**：更新应用程序配置
- **文件**：`系统管理/更新设置.json`
- **场景覆盖**：批量更新、冲突检测、权限控制
- **特色功能**：实时验证、冲突解决、自动备份

#### 系统健康检查 (`GET /api/system/health`)
- **功能**：检查系统各组件健康状态
- **文件**：`系统管理/系统健康检查.json`
- **场景覆盖**：健康状态、警告信息、错误诊断
- **特色功能**：综合评分、性能监控、故障预警

### 5. WebSocket消息

#### 索引进度推送 (`ws://.../ws/index/{index_id}`)
- **功能**：实时推送索引任务进度
- **文件**：`WebSocket消息/索引进度推送.json`
- **消息类型**：进度更新、文件处理、错误报告、完成通知
- **特色功能**：实时更新、断线重连、状态同步

#### 搜索建议推送 (`ws://.../ws/search-suggest`)
- **功能**：实时搜索建议和自动完成
- **文件**：`WebSocket消息/搜索建议推送.json`
- **消息类型**：搜索建议、热门查询、个性化推荐
- **特色功能**：智能推荐、多语言支持、用户偏好

## 🛠️ 高级用法

### 1. Mock数据动态生成

```typescript
// 动态生成Mock数据
class DynamicMockGenerator {
  static generateSearchResults(query: string, count: number = 20) {
    const results = [];
    const fileTypes = ['pdf', 'docx', 'txt', 'md'];
    const relevanceScore = 0.95;

    for (let i = 0; i < count; i++) {
      results.push({
        file_id: i + 1,
        file_name: `文件${i + 1}.${fileTypes[i % fileTypes.length]}`,
        file_path: `D:/Documents/文件${i + 1}.${fileTypes[i % fileTypes.length]}`,
        file_type: 'document',
        relevance_score: relevanceScore - (i * 0.02),
        preview_text: `包含查询词"${query}"的预览文本...`,
        highlight: `包含查询词"<em>${query}</em>"的预览文本`,
        created_at: new Date().toISOString(),
        modified_at: new Date().toISOString(),
        file_size: Math.floor(Math.random() * 10000000),
        match_type: 'semantic'
      });
    }

    return {
      success: true,
      data: {
        results,
        total: count,
        search_time: Math.random() * 0.5,
        query_used: query,
        input_processed: false
      }
    };
  }
}
```

### 2. Mock数据验证

```typescript
// Mock数据格式验证
class MockValidator {
  static validateSearchResponse(response: any): boolean {
    if (!response.success) return false;

    const { data } = response;
    if (!data.results || !Array.isArray(data.results)) return false;

    return data.results.every(item =>
      item.file_id &&
      item.file_name &&
      item.relevance_score >= 0 &&
      item.relevance_score <= 1
    );
  }

  static validateAllMockFiles() {
    // 验证所有Mock数据文件格式
    const mockFiles = [
      '搜索服务/文本搜索.json',
      '索引管理/创建索引.json',
      // ... 其他文件
    ];

    mockFiles.forEach(file => {
      const mockData = require(`@/mock/${file}`);
      console.log(`验证 ${file}:`, this.validateSearchResponse(mockData) ? '✅' : '❌');
    });
  }
}
```

### 3. 性能测试支持

```typescript
// 使用Mock数据进行性能测试
class PerformanceTester {
  static async testSearchPerformance(iterations: number = 1000) {
    const mockService = MockService.getInstance();
    const results = [];

    for (let i = 0; i < iterations; i++) {
      const startTime = performance.now();
      await mockService.search({
        query: `测试查询${i}`,
        limit: 20
      });
      const endTime = performance.now();

      results.push(endTime - startTime);
    }

    const avgResponseTime = results.reduce((a, b) => a + b, 0) / results.length;
    const maxResponseTime = Math.max(...results);
    const minResponseTime = Math.min(...results);

    console.log('性能测试结果:');
    console.log(`平均响应时间: ${avgResponseTime.toFixed(2)}ms`);
    console.log(`最大响应时间: ${maxResponseTime.toFixed(2)}ms`);
    console.log(`最小响应时间: ${minResponseTime.toFixed(2)}ms`);
  }
}
```

## 📊 Mock数据统计

### 按接口类型统计

| 接口类型 | 接口数量 | 文件数量 | 场景数量 | 覆盖率 |
|---------|---------|---------|---------|--------|
| 搜索服务 | 3 | 3 | 15 | 100% |
| 索引管理 | 4 | 4 | 20 | 100% |
| AI模型配置 | 3 | 3 | 18 | 100% |
| 系统管理 | 3 | 3 | 16 | 100% |
| WebSocket | 2 | 2 | 14 | 100% |
| **总计** | **15** | **15** | **83** | **100%** |

### 场景覆盖统计

| 场景类型 | 数量 | 占比 |
|---------|------|------|
| 正常场景 | 35 | 42.2% |
| 异常场景 | 28 | 33.7% |
| 边界场景 | 20 | 24.1% |
| **总计** | **83** | **100%** |

## 🔧 最佳实践

### 1. 开发阶段使用

- **初期开发**：使用Mock数据进行界面开发
- **功能测试**：验证各种边界情况和错误处理
- **性能优化**：测试前端的性能表现
- **用户验收**：展示完整的用户交互流程

### 2. 测试阶段使用

- **单元测试**：基于Mock数据进行组件测试
- **集成测试**：验证前后端数据交互
- **性能测试**：测试系统响应性能
- **用户体验测试**：验证交互逻辑

### 3. 维护和更新

- **定期更新**：根据接口文档更新Mock数据
- **场景扩展**：添加新的测试场景
- **数据验证**：确保Mock数据格式正确
- **文档同步**：保持文档与数据同步

## 📝 注意事项

### 1. 数据安全

- Mock数据中的敏感信息已做脱敏处理
- 生产环境不要使用Mock数据
- 定期清理测试数据

### 2. 性能考虑

- Mock数据文件大小控制在合理范围
- 避免过于复杂的Mock数据生成逻辑
- 使用缓存提高Mock数据访问速度

### 3. 版本管理

- Mock数据版本与接口版本保持一致
- 重大变更时需要更新Mock数据
- 维护变更历史和说明

## 🤝 贡献指南

### 1. 添加新Mock数据

1. 在对应分类目录下创建JSON文件
2. 按照现有格式编写Mock数据
3. 添加正常、异常、边界等场景
4. 更新本说明文档

### 2. 修改现有Mock数据

1. 确保修改符合接口文档规范
2. 保持数据格式的一致性
3. 添加必要的注释说明
4. 验证修改后的数据正确性

### 3. 报告问题

如果发现Mock数据的问题，请提交Issue并包含：
- 问题描述
- 期望的行为
- 建议的解决方案

## 📞 技术支持

- **文档维护**：AI助手
- **最后更新**：2024年1月20日
- **版本**：v1.0.0
- **联系方式**：通过项目Issue提交问题和建议

---

**项目地址**：`docs/接口mock数据集/`
**适用版本**：小遥搜索 v1.0.0
**开发环境**：Node.js + TypeScript + Vue 3
**测试环境**：Jest + Vitest