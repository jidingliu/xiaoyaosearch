# AI服务模块设计

## 架构概述
AI服务模块提供统一的AI能力接口，集成多种AI模型和服务，支持本地和云端两种部署模式，为搜索和索引功能提供智能化的底层支持。

## 核心组件设计

### 1. AI服务管理器 (AIServiceManager)
**职责**: 统一管理所有AI服务的加载、调用和资源管理

**关键方法**:
```python
class AIServiceManager:
    def __init__(self):
        self.llm_service = LLMService()
        self.embedding_service = EmbeddingService()
        self.asr_service = ASRService()
        self.vision_service = VisionService()
        self.model_manager = ModelManager()

    async def initialize(self):
        # 并行加载所有AI模型
        # 检查硬件资源
        # 配置运行模式

    async def shutdown(self):
        # 释放模型资源
        # 清理缓存
```

### 2. LLM查询理解服务 (LLMService)
**职责**: 使用大语言模型理解用户查询意图

**支持的模型**:
- **本地**: Ollama (qwen2, llama3等)
- **云端**: OpenAI GPT-4/GPT-3.5

**提示词模板**:
```python
class LLMPromptTemplates:
    QUERY_UNDERSTANDING = """
你是一个文件搜索助手，负责解析用户的搜索查询。

用户查询: {query}

请提取以下信息（JSON格式）:
1. keywords: 关键词列表
2. semantic_query: 语义化查询描述
3. time_range: 时间范围 {{"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD"}}
4. file_types: 文件类型列表

示例:
输入: "上周的产品设计PPT"
输出: {{
  "keywords": ["产品设计", "PPT"],
  "semantic_query": "产品设计相关的演示文稿",
  "time_range": {{"start_date": "2024-11-03", "end_date": "2024-11-09"}},
  "file_types": ["ppt", "pptx"]
}}
"""
```

**查询理解流程**:
```python
class LLMService:
    async def understand_query(self, query: str) -> QueryUnderstanding:
        # 1. 预处理查询文本
        cleaned_query = self.preprocess_query(query)

        # 2. 生成提示词
        prompt = self.build_prompt(cleaned_query)

        # 3. 调用LLM模型
        response = await self.call_llm(prompt)

        # 4. 解析响应
        result = self.parse_response(response)

        # 5. 后处理和时间解析
        result.time_range = self.parse_time_range(query)

        return result
```

### 3. Embedding向量化服务 (EmbeddingService)
**职责**: 文本向量化，支持语义相似度搜索

**模型配置**:
```python
class EmbeddingConfig:
    MODEL_NAME = "BAAI/bge-base-zh-v1.5"
    VECTOR_DIM = 768
    MAX_SEQUENCE_LENGTH = 512
    BATCH_SIZE = 32
    DEVICE = "auto"  # 自动选择CPU/GPU

class EmbeddingService:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.cache = LRUCache(maxsize=1000)

    async def initialize(self):
        # 加载BGE模型
        self.model = AutoModel.from_pretrained(EmbeddingConfig.MODEL_NAME)
        self.tokenizer = AutoTokenizer.from_pretrained(EmbeddingConfig.MODEL_NAME)

        # GPU加速检测
        if torch.cuda.is_available():
            self.model = self.model.cuda()

    async def encode(self, texts: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        # 检查缓存
        if isinstance(texts, str):
            cache_key = hashlib.md5(texts.encode()).hexdigest()
            if cache_key in self.cache:
                return self.cache[cache_key]

        # 批量处理
        if isinstance(texts, str):
            texts = [texts]

        # 文本预处理
        encoded_input = self.tokenizer(texts, padding=True, truncation=True,
                                     max_length=EmbeddingConfig.MAX_SEQUENCE_LENGTH,
                                     return_tensors='pt')

        # 模型推理
        with torch.no_grad():
            model_output = self.model(**encoded_input)
            embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
            embeddings = F.normalize(embeddings, p=2, dim=1)

        result = embeddings.cpu().numpy()

        # 缓存结果
        for i, text in enumerate(texts):
            cache_key = hashlib.md5(text.encode()).hexdigest()
            self.cache[cache_key] = result[i]

        return result[0] if len(result) == 1 else result
```

### 4. ASR语音识别服务 (ASRService)
**职责**: 语音转文字，支持实时语音和音频文件处理

**支持的模型**:
- **本地**: OpenAI Whisper (medium/base)
- **云端**: OpenAI Whisper API

**音频处理流程**:
```python
class ASRService:
    def __init__(self):
        self.model = None
        self.sample_rate = 16000

    async def initialize(self):
        # 加载Whisper模型
        self.model = whisper.load_model("medium")

    async def transcribe_audio(self, audio_path: str, language: str = None) -> TranscriptionResult:
        # 1. 音频预处理
        audio = self.preprocess_audio(audio_path)

        # 2. 语言检测（如果未指定）
        if language is None:
            language = self.detect_language(audio)

        # 3. 语音识别
        result = self.model.transcribe(audio, language=language)

        # 4. 后处理
        return self.postprocess_result(result)

    def preprocess_audio(self, audio_path: str):
        # 使用FFmpeg转换音频格式
        # 统一采样率为16kHz
        # 转换为单声道
```

**实时语音处理**:
```python
class RealTimeASR:
    def __init__(self, asr_service: ASRService):
        self.asr_service = asr_service
        self.audio_buffer = []
        self.is_recording = False

    async def start_recording(self):
        self.is_recording = True
        # 启动音频流捕获
        # 30秒分段处理

    async def process_audio_chunk(self, audio_chunk):
        self.audio_buffer.append(audio_chunk)

        # 30秒分段
        if len(self.audio_buffer) >= 30 * self.sample_rate:
            segment = np.concatenate(self.audio_buffer)
            self.audio_buffer = []

            # 异步转录
            asyncio.create_task(self.transcribe_segment(segment))
```

### 5. 视觉理解服务 (VisionService)
**职责**: 图片和视频内容理解，支持OCR和标签生成

**图片处理流程**:
```python
class VisionService:
    def __init__(self):
        self.clip_model = None
        self.clip_processor = None
        self.ocr_engine = None
        self.labels = self.load_predefined_labels()

    async def initialize(self):
        # 加载Chinese-CLIP模型
        self.clip_model = ChineseCLIPModel.from_pretrained("OFA-Sys/chinese-clip-vit-base-patch16")
        self.clip_processor = ChineseCLIPProcessor.from_pretrained("OFA-Sys/chinese-clip-vit-base-patch16")

        # 初始化OCR引擎
        self.ocr_engine = PaddleOCR(use_angle_cls=True, lang="ch")

    async def analyze_image(self, image_path: str) -> ImageAnalysisResult:
        # 1. OCR文字提取
        ocr_result = self.extract_text(image_path)

        # 2. 图像标签生成
        labels = self.generate_labels(image_path)

        # 3. 图像向量化
        embedding = await self.encode_image(image_path)

        return ImageAnalysisResult(
            text=ocr_result.text,
            labels=labels,
            embedding=embedding,
            confidence=ocr_result.confidence
        )

    def generate_labels(self, image_path: str) -> List[str]:
        # 使用Chinese-CLIP生成图像标签
        image = Image.open(image_path)
        inputs = self.clip_processor(images=image, return_tensors="pt")

        with torch.no_grad():
            image_features = self.clip_model.get_image_features(**inputs)

        # 与预定义标签库匹配
        similarities = self.compute_similarities(image_features, self.label_embeddings)
        top_labels = self.get_top_labels(similarities, top_k=10)

        return [label for label, score in top_labels if score > 0.3]
```

**视频处理流程**:
```python
class VideoProcessor:
    def extract_keyframes(self, video_path: str, num_frames: int = 15) -> List[str]:
        # 使用FFmpeg提取关键帧
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vf', f'select=eq(n\\,0)+if(eq(pict_type\\,I),1,0)',
            '-vsync', 'vfr', '-frames:v', str(num_frames),
            'keyframe_%03d.jpg'
        ]
        subprocess.run(cmd)

        return [f'keyframe_{i:03d}.jpg' for i in range(num_frames)]

    async def analyze_video(self, video_path: str) -> VideoAnalysisResult:
        # 1. 提取关键帧
        keyframes = self.extract_keyframes(video_path)

        # 2. 分析每个关键帧
        frame_results = []
        for frame_path in keyframes:
            result = await self.vision_service.analyze_image(frame_path)
            frame_results.append(result)

        # 3. 提取音频并转录
        audio_result = await self.asr_service.transcribe_audio(video_path)

        # 4. 合并结果
        return self.merge_video_results(frame_results, audio_result)
```

### 6. 模型管理器 (ModelManager)
**职责**: 管理AI模型的下载、加载、版本控制

```python
class ModelManager:
    def __init__(self):
        self.models_dir = Path("~/.xiaoyao/models").expanduser()
        self.model_registry = self.load_model_registry()

    async def download_model(self, model_name: str, force: bool = False):
        # 检查模型是否已存在
        model_path = self.models_dir / model_name
        if model_path.exists() and not force:
            return

        # 下载模型
        await self.download_from_huggingface(model_name, model_path)

        # 验证模型完整性
        self.verify_model(model_path)

    async def load_model(self, model_name: str):
        # 检查内存使用情况
        if not self.check_memory_available(model_name):
            self.unload_least_used_model()

        # 加载模型
        model_info = self.model_registry[model_name]
        model = await self.load_model_from_path(model_info)

        return model

    def check_memory_available(self, model_name: str) -> bool:
        # 检查可用内存是否足够加载模型
        model_info = self.model_registry[model_name]
        required_memory = model_info['memory requirement']
        available_memory = self.get_available_memory()

        return available_memory > required_memory
```

## 运行模式设计

### 混合模式架构
```python
class HybridAIService:
    def __init__(self):
        self.local_service = LocalAIService()
        self.cloud_service = CloudAIService()
        self.mode = "hybrid"  # local, cloud, hybrid

    async def process_query(self, query: str) -> QueryResult:
        if self.mode == "local":
            return await self.local_service.process_query(query)
        elif self.mode == "cloud":
            return await self.cloud_service.process_query(query)
        else:  # hybrid
            # 本地处理，云端增强
            local_result = await self.local_service.process_query(query)
            if local_result.confidence < 0.8:
                enhanced_result = await self.cloud_service.enhance_result(local_result)
                return enhanced_result
            return local_result
```

## 服务接口设计

### REST API
```python
# 查询理解
POST /api/v1/ai/understand-query
{
  "query": "上周的产品设计PPT"
}

# 文本向量化
POST /api/v1/ai/embed
{
  "texts": ["文本1", "文本2"]
}

# 语音转录
POST /api/v1/ai/transcribe
Content-Type: multipart/form-data
file: audio.wav

# 图像分析
POST /api/v1/ai/analyze-image
Content-Type: multipart/form-data
file: image.jpg
```

### WebSocket接口
```python
# 实时语音识别
/ws/ai/realtime-asr

# 长任务处理状态
/ws/ai/task-status/{task_id}
```

## 性能优化策略

### 1. 模型预加载
- 系统启动时预加载常用模型
- 根据用户使用模式智能预加载
- 后台异步加载，不阻塞启动

### 2. 批量处理
- Embedding服务支持批量处理
- 图像分析支持批量处理
- 合理的批次大小优化

### 3. 缓存策略
- 文本向量缓存 (LRU, 1000条)
- OCR结果缓存
- 查询理解结果缓存

### 4. 硬件加速
- 自动检测并使用GPU
- 多模型并行处理
- 内存映射大文件

## 错误处理与降级

### 服务降级策略
```python
class ServiceDegradation:
    def __init__(self):
        self.fallback_chain = [
            'local_llm',
            'cloud_llm',
            'keyword_search'
        ]

    async def process_with_fallback(self, query: str):
        for service in self.fallback_chain:
            try:
                result = await self.call_service(service, query)
                if result.confidence > self.threshold:
                    return result
            except ServiceUnavailable:
                continue

        # 最终降级到基础搜索
        return await self.basic_keyword_search(query)
```

### 错误监控
- 实时监控服务可用性
- 自动故障检测和恢复
- 详细的错误日志记录

## 资源管理

### 内存管理
```python
class MemoryManager:
    def __init__(self):
        self.max_memory = 2 * 1024 * 1024 * 1024  # 2GB
        self.current_usage = 0
        self.loaded_models = {}

    async def load_model_with_memory_check(self, model_name: str):
        model_info = self.get_model_info(model_name)

        if not self.check_memory_available(model_info['memory']):
            await self.free_memory(model_info['memory'])

        model = await self.load_model(model_name)
        self.loaded_models[model_name] = {
            'model': model,
            'memory': model_info['memory'],
            'last_used': time.time()
        }

        return model
```

### GPU资源管理
- 自动检测GPU可用性
- 动态分配GPU内存
- 多模型GPU共享