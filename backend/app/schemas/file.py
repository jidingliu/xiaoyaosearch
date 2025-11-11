"""
文件相关的Pydantic模式
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class FileInfo(BaseModel):
    """文件信息模式"""
    id: str = Field(..., description="文件ID")
    file_name: str = Field(..., description="文件名")
    file_path: str = Field(..., description="文件路径")
    size: int = Field(..., description="文件大小(字节)")
    file_type: str = Field(..., description="文件类型")
    mime_type: Optional[str] = Field(None, description="MIME类型")
    modified_time: str = Field(..., description="修改时间")
    created_at: str = Field(..., description="创建时间")
    indexed_at: str = Field(..., description="索引时间")
    status: str = Field(..., description="状态")
    is_deleted: bool = Field(False, description="是否已删除")


class FilePreview(BaseModel):
    """文件预览模式"""
    file_id: str = Field(..., description="文件ID")
    file_name: str = Field(..., description="文件名")
    file_type: str = Field(..., description="文件类型")
    preview_type: str = Field(..., description="预览类型")
    content: Optional[str] = Field(None, description="文本内容")
    metadata: Optional[Dict[str, Any]] = Field(None, description="文件元数据")
    highlights: List[str] = Field(default_factory=list, description="高亮关键词")
    preview_url: Optional[str] = Field(None, description="预览URL")


class FileCreate(BaseModel):
    """文件创建模式"""
    file_name: str = Field(..., description="文件名")
    file_path: str = Field(..., description="文件路径")
    directory_id: Optional[str] = Field(None, description="目录ID")
    file_type: str = Field(..., description="文件类型")
    file_size: int = Field(..., description="文件大小")


class FileUpdate(BaseModel):
    """文件更新模式"""
    file_name: Optional[str] = Field(None, description="文件名")
    status: Optional[str] = Field(None, description="状态")
    error_message: Optional[str] = Field(None, description="错误信息")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")