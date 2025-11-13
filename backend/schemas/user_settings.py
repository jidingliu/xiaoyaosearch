"""
User settings schemas for API request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserSettingsBase(BaseModel):
    """Base user settings schema."""
    key: str = Field(..., description="Setting key")
    value: Optional[str] = Field(None, description="Setting value")
    description: Optional[str] = Field(None, description="Setting description")
    category: Optional[str] = Field(None, description="Setting category")
    data_type: str = Field("string", pattern="^(string|integer|boolean|json)$", description="Data type")


class UserSettingsCreate(UserSettingsBase):
    """Schema for creating user settings."""
    pass


class UserSettingsUpdate(BaseModel):
    """Schema for updating user settings."""
    value: Optional[str] = None
    description: Optional[str] = None


class UserSettings(UserSettingsBase):
    """Complete user settings schema."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True