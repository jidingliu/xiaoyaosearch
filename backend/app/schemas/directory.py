"""
目录相关的Pydantic模式
"""

from typing import Optional, List
from pydantic import BaseModel, Field, validator


class DirectoryCreate(BaseModel):
    """目录创建模式"""
    path: str = Field(..., description="目录路径")
    name: Optional[str] = Field(None, description="目录名称")

    @validator('path')
    def validate_path(cls, v):
        if not v or v.strip() == "":
            raise ValueError("目录路径不能为空")
        return v.strip()


class DirectoryInfo(BaseModel):
    """目录信息模式"""
    id: str = Field(..., description="目录ID")
    path: str = Field(..., description="目录路径")
    name: str = Field(..., description="目录名称")
    status: str = Field(..., description="状态: active, inactive, error")
    file_count: int = Field(..., description="文件数量")
    indexed_count: int = Field(..., description="已索引文件数量")
    last_scan_time: Optional[str] = Field(None, description="最后扫描时间")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")
    error_message: Optional[str] = Field(None, description="错误信息")


class DirectoryUpdate(BaseModel):
    """目录更新模式"""
    name: Optional[str] = Field(None, description="目录名称")
    status: Optional[str] = Field(None, description="状态")


class ScanStatus(BaseModel):
    """扫描状态模式"""
    directory_id: str = Field(..., description="目录ID")
    is_scanning: bool = Field(..., description="是否正在扫描")
    progress: float = Field(..., description="扫描进度(0-1)")
    current_file: Optional[str] = Field(None, description="当前扫描文件")
    total_files: int = Field(..., description="总文件数")
    scanned_files: int = Field(..., description="已扫描文件数")
    error_count: int = Field(..., description="错误文件数")
    start_time: Optional[str] = Field(None, description="开始时间")
    estimated_completion: Optional[str] = Field(None, description="预计完成时间")