"""
图像理解标准提示词配置
确保索引构建和图片搜索使用完全一致的提示词
"""

# 图像理解标准提示词集合
IMAGE_UNDERSTANDING_PROMPTS = [
    "描述这张图片的内容",
    "这张图片展示了什么",
    "图片中的主要元素",
    "图片的整体主题"
]

# CLIP图像理解配置
CLIP_CONFIG = {
    "prompts": IMAGE_UNDERSTANDING_PROMPTS,
    "temperature": 0.7,
    "max_tokens": 150
}

def get_image_prompts() -> list:
    """获取图像理解标准提示词"""
    return IMAGE_UNDERSTANDING_PROMPTS.copy()

def get_clip_config() -> dict:
    """获取CLIP图像理解配置"""
    return CLIP_CONFIG.copy()