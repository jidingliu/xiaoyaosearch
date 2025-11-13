"""
Tag schemas for API request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class TagBase(BaseModel):
    """Base tag schema."""
    name: str = Field(..., description="Tag name")
    description: Optional[str] = Field(None, description="Tag description")
    color: str = Field("#007bff", pattern=r"^#[0-9A-Fa-f]{6}$", description="Hex color code")
    category: Optional[str] = Field(None, description="Tag category")


class TagCreate(TagBase):
    """Schema for creating a new tag."""
    is_system_tag: bool = Field(False, description="Whether this is a system-generated tag")


class TagUpdate(BaseModel):
    """Schema for updating tag information."""
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    category: Optional[str] = None


class Tag(TagBase):
    """Complete tag schema with all fields."""
    id: int
    is_system_tag: bool
    usage_count: int
    created_at: datetime
    last_used: Optional[datetime]

    class Config:
        from_attributes = True