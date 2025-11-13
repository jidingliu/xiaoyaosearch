"""
Directory schemas for API request/response validation.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class DirectoryBase(BaseModel):
    """Base directory schema."""
    path: str = Field(..., description="Directory path")
    name: str = Field(..., description="Directory name")
    parent_id: Optional[int] = Field(None, description="Parent directory ID")


class DirectoryCreate(DirectoryBase):
    """Schema for creating a new directory record."""
    is_indexed: bool = Field(True, description="Whether to index this directory")
    scan_depth: int = Field(10, ge=1, le=100, description="Maximum scan depth")
    exclude_patterns: Optional[str] = Field(None, description="Exclude patterns")


class DirectoryUpdate(BaseModel):
    """Schema for updating directory information."""
    is_indexed: Optional[bool] = None
    scan_depth: Optional[int] = None
    exclude_patterns: Optional[str] = None


class Directory(DirectoryBase):
    """Complete directory schema with all fields."""
    id: int
    created_at: datetime
    modified_at: datetime
    last_scanned: Optional[datetime]
    is_indexed: bool
    scan_depth: int
    exclude_patterns: Optional[str]
    scan_status: str
    file_count: int
    total_size: int

    class Config:
        from_attributes = True


class DirectoryStatus(BaseModel):
    """Directory scanning status schema."""
    id: int
    name: str
    path: str
    scan_status: str
    file_count: int
    total_size: int
    last_scanned: Optional[datetime]
    scan_progress: float = Field(0.0, ge=0.0, le=1.0, description="Scan progress (0-1)")

    class Config:
        from_attributes = True