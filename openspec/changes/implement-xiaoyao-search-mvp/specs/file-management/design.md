# 文件管理模块设计

## 架构概述
文件管理模块提供文件预览、操作、安全控制等功能，是用户与本地文件交互的核心接口，确保安全、高效的文件操作体验。

## 核心组件设计

### 1. 文件预览器 (FilePreviewer)
**职责**: 支持多种文件格式的在线预览

**预览器架构**:
```python
class FilePreviewer(ABC):
    @abstractmethod
    def can_preview(self, file_path: Path) -> bool:
        pass

    @abstractmethod
    async def preview(self, file_path: Path, highlights: List[str] = None) -> PreviewResult:
        pass

class PDFPreviewer(FilePreviewer):
    def __init__(self):
        self.pdfjs_renderer = PDFJSRenderer()

    async def preview(self, file_path: Path, highlights: List[str] = None) -> PreviewResult:
        # 使用pdf.js渲染PDF
        # 支持分页、缩放、搜索高亮
        return PDFPreviewResult(
            pages=self.render_pages(file_path),
            highlights=highlights,
            metadata=self.extract_metadata(file_path)
        )

class ImagePreviewer(FilePreviewer):
    async def preview(self, file_path: Path, highlights: List[str] = None) -> PreviewResult:
        # 图片预览，支持缩放、旋转
        # EXIF信息提取
        return ImagePreviewResult(
            image_data=self.load_image(file_path),
            metadata=self.extract_exif(file_path),
            zoom_levels=[0.25, 0.5, 1.0, 2.0, 4.0]
        )

class VideoPreviewer(FilePreviewer):
    async def preview(self, file_path: Path, highlights: List[str] = None) -> PreviewResult:
        # 视频预览，支持播放控制
        # 关键帧导航
        return VideoPreviewResult(
            video_url=self.generate_stream_url(file_path),
            duration=self.get_duration(file_path),
            keyframes=self.extract_keyframes(file_path),
            subtitles=self.get_subtitles(file_path)
        )
```

**预览管理器**:
```python
class PreviewManager:
    def __init__(self):
        self.previewers = {
            '.pdf': PDFPreviewer(),
            '.jpg': ImagePreviewer(),
            '.jpeg': ImagePreviewer(),
            '.png': ImagePreviewer(),
            '.mp4': VideoPreviewer(),
            '.mp3': AudioPreviewer(),
            '.txt': TextPreviewer(),
            '.md': MarkdownPreviewer(),
        }

    async def get_preview(self, file_path: Path, search_query: str = None) -> PreviewResult:
        file_ext = file_path.suffix.lower()
        previewer = self.previewers.get(file_ext)

        if not previewer:
            return UnsupportedPreviewResult(file_path)

        highlights = self.extract_highlights(search_query) if search_query else None
        return await previewer.preview(file_path, highlights)
```

### 2. 文件操作器 (FileOperator)
**职责**: 安全地执行各种文件操作

**操作接口设计**:
```python
class FileOperator:
    def __init__(self):
        self.security_checker = SecurityChecker()
        self.permission_checker = PermissionChecker()

    async def open_file(self, file_path: Path) -> OperationResult:
        # 1. 安全检查
        if not self.security_checker.is_safe_to_open(file_path):
            return OperationResult(success=False, error="文件安全检查失败")

        # 2. 权限检查
        if not self.permission_checker.can_read(file_path):
            return OperationResult(success=False, error="无权限访问文件")

        # 3. 执行打开操作
        try:
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            else:  # Linux
                subprocess.run(["xdg-open", file_path])

            # 记录操作历史
            await self.record_operation("open", file_path)

            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    async def delete_file(self, file_path: Path, confirm: bool = False) -> OperationResult:
        if not confirm:
            return OperationResult(success=False, error="需要用户确认")

        # 安全检查：防止删除系统文件
        if self.security_checker.is_system_file(file_path):
            return OperationResult(success=False, error="不能删除系统文件")

        try:
            file_path.unlink()
            await self.record_operation("delete", file_path)
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    async def copy_path(self, file_path: Path) -> OperationResult:
        try:
            # 复制到系统剪贴板
            pyperclip.copy(str(file_path.absolute()))
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(success=False, error=str(e))
```

**安全检查器**:
```python
class SecurityChecker:
    def __init__(self):
        self.system_paths = self.get_system_paths()
        self.sensitive_extensions = {'.exe', '.bat', '.cmd', '.sh', '.scr'}

    def is_safe_to_open(self, file_path: Path) -> bool:
        # 检查是否为系统关键文件
        if self.is_system_file(file_path):
            return False

        # 检查文件扩展名
        if file_path.suffix.lower() in self.sensitive_extensions:
            return False

        # 检查文件路径
        if any(str(file_path).startswith(sys_path) for sys_path in self.system_paths):
            return False

        return True

    def is_system_file(self, file_path: Path) -> bool:
        # 检查是否为Windows系统文件
        system_patterns = [
            r"C:\\Windows\\",
            r"C:\\Program Files\\",
            r"C:\\Program Files (x86)\\",
            r"/System/",
            r"/usr/bin/",
            r"/bin/",
        ]

        return any(re.match(pattern, str(file_path), re.IGNORECASE)
                  for pattern in system_patterns)
```

### 3. 文件收藏管理器 (FavoritesManager)
**职责**: 管理用户收藏的文件

**收藏数据结构**:
```python
@dataclass
class FavoriteItem:
    id: str
    file_path: Path
    title: str
    description: Optional[str]
    category: Optional[str]
    tags: List[str]
    created_at: datetime
    accessed_at: datetime

class FavoritesManager:
    def __init__(self, db: Database):
        self.db = db

    async def add_favorite(self, file_path: Path, title: str = None, category: str = None) -> str:
        favorite_id = str(uuid.uuid4())

        favorite = FavoriteItem(
            id=favorite_id,
            file_path=file_path,
            title=title or file_path.name,
            category=category,
            tags=[],
            created_at=datetime.now(),
            accessed_at=datetime.now()
        )

        await self.db.insert("favorites", favorite.__dict__)
        return favorite_id

    async def get_favorites(self, category: str = None, limit: int = 50) -> List[FavoriteItem]:
        query = "SELECT * FROM favorites"
        params = []

        if category:
            query += " WHERE category = ?"
            params.append(category)

        query += " ORDER BY accessed_at DESC LIMIT ?"
        params.append(limit)

        rows = await self.db.fetch_all(query, params)
        return [FavoriteItem(**row) for row in rows]

    async def remove_favorite(self, favorite_id: str) -> bool:
        result = await self.db.execute(
            "DELETE FROM favorites WHERE id = ?",
            [favorite_id]
        )
        return result.rowcount > 0
```

### 4. 文件历史管理器 (HistoryManager)
**职责**: 记录和管理用户文件访问历史

**历史记录结构**:
```python
@dataclass
class FileHistoryItem:
    id: str
    file_path: Path
    operation: str  # open, preview, download
    search_query: Optional[str]
    timestamp: datetime
    duration: Optional[int]  # 访问时长（秒）

class HistoryManager:
    def __init__(self, db: Database):
        self.db = db

    async def record_access(self, file_path: Path, operation: str,
                          search_query: str = None, duration: int = None):
        history_item = FileHistoryItem(
            id=str(uuid.uuid4()),
            file_path=file_path,
            operation=operation,
            search_query=search_query,
            timestamp=datetime.now(),
            duration=duration
        )

        await self.db.insert("file_history", history_item.__dict__)

    async def get_recent_files(self, limit: int = 20,
                             operation: str = None) -> List[FileHistoryItem]:
        query = "SELECT * FROM file_history"
        params = []

        if operation:
            query += " WHERE operation = ?"
            params.append(operation)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        rows = await self.db.fetch_all(query, params)
        return [FileHistoryItem(**row) for row in rows]

    async def cleanup_old_history(self, days: int = 90):
        cutoff_date = datetime.now() - timedelta(days=days)
        await self.db.execute(
            "DELETE FROM file_history WHERE timestamp < ?",
            [cutoff_date]
        )
```

### 5. 文件导入导出管理器 (ImportExportManager)
**职责**: 处理文件的批量导入和导出

**导入处理流程**:
```python
class ImportExportManager:
    def __init__(self, index_manager: IndexManager, file_operator: FileOperator):
        self.index_manager = index_manager
        self.file_operator = file_operator

    async def import_files(self, file_paths: List[Path],
                          target_directory: Path = None) -> ImportResult:
        imported_files = []
        failed_files = []

        for file_path in file_paths:
            try:
                # 安全检查
                if not self.file_operator.security_checker.is_safe_to_open(file_path):
                    failed_files.append((file_path, "安全检查失败"))
                    continue

                # 复制到目标目录（如果指定）
                if target_directory:
                    dest_path = target_directory / file_path.name
                    shutil.copy2(file_path, dest_path)
                    file_path = dest_path

                # 添加到索引
                await self.index_manager.add_file_to_index(file_path)
                imported_files.append(file_path)

            except Exception as e:
                failed_files.append((file_path, str(e)))

        return ImportResult(
            success_count=len(imported_files),
            failed_count=len(failed_files),
            imported_files=imported_files,
            failed_files=failed_files
        )

    async def export_search_results(self, search_results: List[SearchResult],
                                  format: str = "csv") -> ExportResult:
        if format == "csv":
            return await self.export_to_csv(search_results)
        elif format == "json":
            return await self.export_to_json(search_results)
        else:
            raise ValueError(f"Unsupported export format: {format}")
```

### 6. 文件关系分析器 (FileRelationAnalyzer)
**职责**: 分析文件之间的关联关系

**关系分析算法**:
```python
class FileRelationAnalyzer:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service

    async def find_related_files(self, target_file: Path,
                               limit: int = 5) -> List[RelatedFile]:
        # 1. 获取目标文件的向量表示
        target_content = await self.extract_content(target_file)
        target_vector = await self.embedding_service.encode(target_content)

        # 2. 在索引中搜索相似文件
        similar_files = await self.search_similar_vectors(target_vector, limit * 2)

        # 3. 计算相似度并排序
        related_files = []
        for file_path, similarity in similar_files:
            if file_path != target_file and similarity > 0.3:  # 相似度阈值
                related_files.append(RelatedFile(
                    file_path=file_path,
                    similarity_score=similarity,
                    relation_type=self.detect_relation_type(target_file, file_path)
                ))

        # 4. 按相似度排序并限制数量
        related_files.sort(key=lambda x: x.similarity_score, reverse=True)
        return related_files[:limit]

    def detect_relation_type(self, file1: Path, file2: Path) -> str:
        # 基于文件路径和名称推断关系类型
        name1, name2 = file1.stem.lower(), file2.stem.lower()

        # 同一系列文档
        if self.is_same_series(name1, name2):
            return "series"

        # 同一项目文件
        if self.is_same_project(file1.parent, file2.parent):
            return "project"

        # 内容相似
        return "similar_content"
```

## 数据存储设计

### 收藏表
```sql
CREATE TABLE favorites (
    id TEXT PRIMARY KEY,
    file_path TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    tags TEXT, -- JSON数组
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_favorites_category ON favorites(category);
CREATE INDEX idx_favorites_accessed ON favorites(accessed_at);
```

### 文件历史表
```sql
CREATE TABLE file_history (
    id TEXT PRIMARY KEY,
    file_path TEXT NOT NULL,
    operation TEXT NOT NULL,
    search_query TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration INTEGER,
    INDEX(file_path, timestamp)
);

CREATE INDEX idx_history_timestamp ON file_history(timestamp DESC);
CREATE INDEX idx_history_operation ON file_history(operation);
```

### 文件关系表
```sql
CREATE TABLE file_relations (
    id TEXT PRIMARY KEY,
    source_file TEXT NOT NULL,
    target_file TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    similarity_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_file, target_file)
);

CREATE INDEX idx_relations_source ON file_relations(source_file);
CREATE INDEX idx_relations_score ON file_relations(similarity_score DESC);
```

## API接口设计

### 文件预览API
```
GET /api/v1/files/{file_id}/preview
Parameters:
- file_id: 文件唯一标识
- query: 搜索查询（用于高亮）

Response:
{
  "preview_type": "pdf",
  "content": "预览内容",
  "metadata": {},
  "highlights": []
}
```

### 文件操作API
```
POST /api/v1/files/{file_id}/open
POST /api/v1/files/{file_id}/delete
POST /api/v1/files/{file_id}/copy-path
GET /api/v1/files/{file_id}/show-in-folder
```

### 收藏管理API
```
POST /api/v1/favorites
{
  "file_id": "xxx",
  "title": "自定义标题",
  "category": "工作文档"
}

GET /api/v1/favorites
Parameters:
- category: 分类筛选
- limit: 返回数量限制

DELETE /api/v1/favorites/{favorite_id}
```

### 历史记录API
```
GET /api/v1/file-history
Parameters:
- operation: 操作类型筛选
- limit: 返回数量限制

DELETE /api/v1/file-history
Parameters:
- days: 保留天数
```

### 相关文件API
```
GET /api/v1/files/{file_id}/related
Parameters:
- limit: 相关文件数量限制

Response:
{
  "related_files": [
    {
      "file_id": "xxx",
      "file_name": "相关文档.pdf",
      "similarity_score": 0.85,
      "relation_type": "similar_content"
    }
  ]
}
```

## 性能优化策略

### 1. 预览缓存
- PDF页面渲染缓存
- 图片缩略图缓存
- 文本内容缓存

### 2. 懒加载
- 大文件分页加载
- 图片按需加载
- 视频关键帧预加载

### 3. 后台处理
- 文件关系分析后台计算
- 历史记录异步写入
- 缓存预清理

## 安全考虑

### 1. 路径验证
- 防止路径遍历攻击
- 限制可访问目录范围
- 验证文件路径合法性

### 2. 文件类型检查
- 基于魔数验证文件类型
- 防止恶意文件执行
- 限制可执行文件操作

### 3. 权限控制
- 最小权限原则
- 操作权限动态检查
- 敏感操作二次确认

## 用户体验设计

### 1. 操作反馈
- 操作进度提示
- 错误信息友好显示
- 成功操作确认

### 2. 快捷操作
- 右键菜单快捷操作
- 键盘快捷键支持
- 拖拽操作支持

### 3. 状态保持
- 预览位置记忆
- 窗口大小保持
- 操作历史恢复