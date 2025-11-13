"""
File schemas for API request/response validation.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class FileBase(BaseModel):
    """Base file schema."""
    path: str = Field(..., description="Full file path")
    filename: str = Field(..., description="File name")
    extension: str = Field(..., description="File extension")
    size: int = Field(..., ge=0, description="File size in bytes")
    mime_type: Optional[str] = Field(None, description="MIME type")
    content_type: Optional[str] = Field(None, description="Content type")


class FileCreate(FileBase):
    """Schema for creating a new file record."""
    directory_id: Optional[int] = Field(None, description="Directory ID")


class FileUpdate(BaseModel):
    """Schema for updating file information."""
    content_text: Optional[str] = None
    image_tags: Optional[str] = None
    audio_transcript: Optional[str] = None
    ocr_text: Optional[str] = None
    is_processed: Optional[bool] = None
    processing_status: Optional[str] = None
    metadata_json: Optional[str] = None


class File(FileBase):
    """Complete file schema with all fields."""
    id: int
    created_at: datetime
    modified_at: datetime
    indexed_at: datetime
    content_hash: Optional[str]
    text_vector: Optional[str]
    search_score: float
    access_count: int
    last_accessed: Optional[datetime]
    directory_id: Optional[int]
    is_deleted: bool
    is_processed: bool
    processing_status: str

    class Config:
        from_attributes = True


class FileSearchResult(BaseModel):
    """Schema for file search results."""
    id: int
    path: str
    filename: str
    extension: str
    size: int
    content_type: Optional[str]
    content_text: Optional[str]
    search_score: float
    highlights: Optional[List[str]] = []
    file_size_str: str
    modified_at_str: str

    @validator("file_size_str", pre=True, always=True)
    def format_file_size(cls, v, values):
        """Format file size as human-readable string."""
        size = values.get("size", 0)
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    @validator("modified_at_str", pre=True, always=True)
    def format_modified_time(cls, v, values):
        """Format modification time as readable string."""
        modified_at = values.get("modified_at")
        if isinstance(modified_at, datetime):
            return modified_at.strftime("%Y-%m-%d %H:%M")
        return str(modified_at) if modified_at else "Unknown"

    class Config:
        from_attributes = True