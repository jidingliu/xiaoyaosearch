# 小遥搜索 - 索引管理接口测试数据
# backend/app/api/index.py 接口手动测试数据
# 使用方法: 使用 curl 或 Postman 等工具发送以下请求

# ==============================================
# 基础信息
# API基础URL: http://127.0.0.1:8000
# Content-Type: application/json
# ==============================================

# ==============================================
# 1. 创建索引 (POST)
# ==============================================

# 1.1 创建完整索引
curl -X POST "http://127.0.0.1:8000/api/index/create" \
  -H "Content-Type: application/json" \
  -d '{
    "folder_path": "D:\\MyWorkProjects\\freelance\\indiehacker\\xiaoyaosearch\\docs\\测试数据",
    "file_types": ["txt", "md", "pdf", "docx", "mp3", "mp4"],
    "recursive": true
  }'

# 1.2 创建非递归索引
curl -X POST "http://127.0.0.1:8000/api/index/create" \
  -H "Content-Type: application/json" \
  -d '{
    "folder_path": "D:\\MyWorkProjects\\freelance\\indiehacker\\xiaoyaosearch\\docs\\测试数据",
    "file_types": ["txt", "md"],
    "recursive": false
  }'

# 1.3 使用默认文件类型创建索引
curl -X POST "http://127.0.0.1:8000/api/index/create" \
  -H "Content-Type: application/json" \
  -d '{
    "folder_path": "D:\\MyWorkProjects\\freelance\\indiehacker\\xiaoyaosearch\\docs\\测试数据",
    "recursive": true
  }'

# ==============================================
# 2. 更新索引 (POST)
# ==============================================

# 2.1 增量更新索引
curl -X POST "http://127.0.0.1:8000/api/index/update" \
  -H "Content-Type: application/json" \
  -d '{
    "folder_path": "D:\\MyWorkProjects\\freelance\\indiehacker\\xiaoyaosearch\\docs\\测试数据",
    "recursive": true
  }'

# 2.2 非递归增量更新
curl -X POST "http://127.0.0.1:8000/api/index/update" \
  -H "Content-Type: application/json" \
  -d '{
    "folder_path": "D:\\MyWorkProjects\\freelance\\indiehacker\\xiaoyaosearch\\docs\\测试数据",
    "recursive": false
  }'

# ==============================================
# 3. 获取索引系统状态 (GET)
# ==============================================
curl -X GET "http://127.0.0.1:8000/api/index/status"

# ==============================================
# 4. 查询索引状态 (GET)
# ==============================================
# 注意: 需要将 {index_id} 替换为实际的索引ID

# 4.1 查询指定索引状态
curl -X GET "http://127.0.0.1:8000/api/index/status/1"

# 4.2 查询其他索引状态
curl -X GET "http://127.0.0.1:8000/api/index/status/2"
curl -X GET "http://127.0.0.1:8000/api/index/status/3"

# ==============================================
# 5. 获取索引列表 (GET)
# ==============================================

# 5.1 获取所有索引列表
curl -X GET "http://127.0.0.1:8000/api/index/list"

# 5.2 分页获取索引列表
curl -X GET "http://127.0.0.1:8000/api/index/list?limit=5&offset=0"

# 5.3 按状态过滤索引列表
curl -X GET "http://127.0.0.1:8000/api/index/list?status=completed&limit=10"

# 5.4 获取运行中的索引任务
curl -X GET "http://127.0.0.1:8000/api/index/list?status=processing"

# 5.5 获取失败的索引任务
curl -X GET "http://127.0.0.1:8000/api/index/list?status=failed"

# 5.6 获取待处理的索引任务
curl -X GET "http://127.0.0.1:8000/api/index/list?status=pending"

# ==============================================
# 6. 删除索引 (DELETE)
# ==============================================
# 注意: 需要将 {index_id} 替换为实际的索引ID

# 6.1 删除指定索引
curl -X DELETE "http://127.0.0.1:8000/api/index/1"

# 6.2 删除其他索引
curl -X DELETE "http://127.0.0.1:8000/api/index/2"

# ==============================================
# 7. 停止索引 (POST)
# ==============================================
# 注意: 需要将 {index_id} 替换为实际的索引ID

# 7.1 停止正在运行的索引
curl -X POST "http://127.0.0.1:8000/api/index/1/stop"

# 7.2 停止其他正在运行的索引
curl -X POST "http://127.0.0.1:8000/api/index/2/stop"

# ==============================================
# 8. 备份索引 (POST)
# ==============================================

# 8.1 创建默认命名的索引备份
curl -X POST "http://127.0.0.1:8000/api/index/backup"

# 8.2 创建指定名称的索引备份
curl -X POST "http://127.0.0.1:8000/api/index/backup?backup_name=backup_2025_11_28"

# 8.3 创建带时间戳的索引备份
curl -X POST "http://127.0.0.1:8000/api/index/backup?backup_name=xiaoyao_search_backup"

# ==============================================
# 9. 获取已索引文件列表 (GET)
# ==============================================

# 9.1 获取所有已索引文件
curl -X GET "http://127.0.0.1:8000/api/index/files"

# 9.2 按文件夹路径过滤
curl -X GET "http://127.0.0.1:8000/api/index/files?folder_path=D:\\MyWorkProjects\\freelance\\indiehacker\\xiaoyaosearch\\docs\\测试数据"

# 9.3 按文件类型过滤
curl -X GET "http://127.0.0.1:8000/api/index/files?file_type=txt"
curl -X GET "http://127.0.0.1:8000/api/index/files?file_type=pdf"
curl -X GET "http://127.0.0.1:8000/api/index/files?file_type=mp3"

# 9.4 按索引状态过滤
curl -X GET "http://127.0.0.1:8000/api/index/files?index_status=indexed"
curl -X GET "http://127.0.0.1:8000/api/index/files?index_status=pending"

# 9.5 分页获取已索引文件
curl -X GET "http://127.0.0.1:8000/api/index/files?limit=20&offset=0"

# 9.6 组合过滤条件
curl -X GET "http://127.0.0.1:8000/api/index/files?folder_path=D:\\MyWorkProjects\\freelance\\indiehacker\\xiaoyaosearch\\docs\\测试数据&file_type=txt&limit=10"

# ==============================================
# 10. 删除文件索引 (DELETE)
# ==============================================
# 注意: 需要将 {file_id} 替换为实际的文件ID

# 10.1 删除指定文件的索引
curl -X DELETE "http://127.0.0.1:8000/api/index/files/1"

# 10.2 删除其他文件索引
curl -X DELETE "http://127.0.0.1:8000/api/index/files/2"
curl -X DELETE "http://127.0.0.1:8000/api/index/files/3"

# ==============================================
# 11. 错误测试用例
# ==============================================

# 11.1 创建索引 - 文件夹不存在
curl -X POST "http://127.0.0.1:8000/api/index/create" \
  -H "Content-Type: application/json" \
  -d '{
    "folder_path": "D:\\nonexistent\\folder",
    "recursive": true
  }'

# 11.2 创建索引 - 路径不是文件夹
curl -X POST "http://127.0.0.1:8000/api/index/create" \
  -H "Content-Type: application/json" \
  -d '{
    "folder_path": "D:\\MyWorkProjects\\freelance\\indiehacker\\xiaoyaosearch\\docs\\测试数据\\test.txt",
    "recursive": true
  }'

# 11.3 创建索引 - 缺少必要参数
curl -X POST "http://127.0.0.1:8000/api/index/create" \
  -H "Content-Type: application/json" \
  -d '{
    "recursive": true
    # 缺少 folder_path 参数
  }'

# 11.4 查询索引状态 - 索引ID不存在
curl -X GET "http://127.0.0.1:8000/api/index/status/99999"

# 11.5 删除索引 - 索引ID不存在
curl -X DELETE "http://127.0.0.1:8000/api/index/99999"

# 11.6 停止索引 - 索引ID不存在
curl -X POST "http://127.0.0.1:8000/api/index/99999/stop"

# 11.7 停止索引 - 任务未在运行
curl -X POST "http://127.0.0.1:8000/api/index/1/stop"

# 11.8 删除文件索引 - 文件ID不存在
curl -X DELETE "http://127.0.0.1:8000/api/index/files/99999"

# 11.9 分页参数错误 - 负数limit
curl -X GET "http://127.0.0.1:8000/api/index/list?limit=-1&offset=0"

# 11.10 分页参数错误 - 负数offset
curl -X GET "http://127.0.0.1:8000/api/index/files?limit=10&offset=-1"

# ==============================================
# 使用说明
# ==============================================

# Windows PowerShell 中使用 curl 的注意事项:
# 1. 如果需要在 PowerShell 中使用，请将单引号 ' 改为双引号 "
# 2. 或者使用 Invoke-RestMethod 命令替代 curl
# 3. JSON 中的双引号需要转义为 \"
# 4. 路径中的反斜杠需要转义为 \\

# Postman 使用步骤:
# 1. 新建请求，选择对应的 HTTP 方法 (GET/POST/PUT/DELETE)
# 2. 输入完整的 URL
# 3. 如果是 POST/PUT 请求，在 Body 选项卡中选择 raw 和 JSON 格式
# 4. 粘贴对应的 JSON 数据
# 5. 点击 Send 发送请求

# 索引ID获取方法:
# 1. 先调用 "获取索引列表" 接口 (/api/index/list)
# 2. 从返回结果中的 data.indexes 数组里找到对应的 index_id 字段
# 3. 将这个 index_id 替换到需要 {index_id} 的请求中

# 文件ID获取方法:
# 1. 先调用 "获取已索引文件列表" 接口 (/api/index/files)
# 2. 从返回结果中的 data.files 数组里找到对应的 id 字段
# 3. 将这个 id 替换到需要 {file_id} 的请求中

# 测试建议顺序:
# 1. 先测试创建索引 (1.1, 1.2)
# 2. 测试获取索引系统状态 (3)
# 3. 测试查询索引状态 (4.1)
# 4. 测试获取索引列表 (5.1)
# 5. 测试获取已索引文件列表 (9.1)
# 6. 测试更新索引 (2.1)
# 7. 测试备份索引 (8.1)
# 8. 测试删除索引 (6.1)
# 9. 最后测试错误用例 (11)

# 常见响应状态码:
# 200: 成功
# 400: 请求参数错误
# 404: 资源不存在
# 422: 参数验证失败
# 500: 服务器内部错误

# 测试数据准备建议:
# 1. 在 D:\MyWorkProjects\freelance\indiehacker\xiaoyaosearch\data\test-data\ 创建测试文件夹
# 2. 在测试文件夹中放入不同类型的文件:
#    - 文本文件 (.txt)
#    - Markdown文件 (.md)
#    - PDF文件 (.pdf)
#    - Word文档 (.docx)
#    - 音频文件 (.mp3)
#    - 视频文件 (.mp4)
# 3. 确保文件夹结构包含子文件夹，用于测试递归索引功能

# 索引任务状态说明:
# - pending: 等待执行
# - processing: 正在执行
# - completed: 执行完成
# - failed: 执行失败

# 文件索引状态说明:
# - pending: 等待索引
# - processing: 正在索引
# - indexed: 索引完成
# - failed: 索引失败