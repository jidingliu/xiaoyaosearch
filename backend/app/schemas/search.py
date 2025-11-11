"""
搜索相关的Pydantic模式
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """搜索请求模式"""
    query: str = Field(..., description="搜索查询")
    type: Optional[str] = Field(None, description="文件类型过滤")
    start_date: Optional[str] = Field(None, description="开始日期 YYYY-MM-DD")
    end_date: Optional[str] = Field(None, description="结束日期 YYYY-MM-DD")
    size: int = Field(20, ge=1, le=100, description="返回结果数量")
    page: int = Field(1, ge=1, description="页码")


class SearchResult(BaseModel):
    """搜索结果项模式"""
    id: str = Field(..., description="文件ID")
    title: str = Field(..., description="文件标题")
    path: str = Field(..., description="文件路径")
    size: int = Field(..., description="文件大小(字节)")
    modified_time: str = Field(..., description="修改时间")
    file_type: str = Field(..., description="文件类型")
    score: float = Field(..., description="相关性得分")
    summary: str = Field(..., description="文件摘要")
    highlights: List[str] = Field(default_factory=list, description="高亮关键词")


class SearchResponse(BaseModel):
    """搜索响应模式"""
    query: str = Field(..., description="搜索查询")
    total: int = Field(..., description="结果总数")
    results: List[SearchResult] = Field(..., description="搜索结果列表")
    search_time: float = Field(..., description="搜索耗时(秒)")
    suggestions: List[str] = Field(default_factory=list, description="搜索建议")