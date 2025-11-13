"""
User settings API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schemas.user_settings import UserSettings, UserSettingsCreate, UserSettingsUpdate

router = APIRouter()


@router.get("/", response_model=List[UserSettings])
async def list_user_settings(
    category: Optional[str] = Query(None, description="Filter by category"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all user settings or filter by category.
    """
    # TODO: Implement user settings listing
    return []


@router.get("/{key}", response_model=UserSettings)
async def get_user_setting(
    key: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific user setting by key.
    """
    # TODO: Implement user setting retrieval
    raise HTTPException(status_code=404, detail="Setting not found")


@router.post("/", response_model=UserSettings)
async def create_user_setting(
    setting: UserSettingsCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user setting.
    """
    # TODO: Implement user setting creation
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/{key}", response_model=UserSettings)
async def update_user_setting(
    key: str,
    setting_update: UserSettingsUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing user setting.
    """
    # TODO: Implement user setting update
    raise HTTPException(status_code=404, detail="Setting not found")


@router.delete("/{key}")
async def delete_user_setting(
    key: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a user setting.
    """
    # TODO: Implement user setting deletion
    return {"message": f"Setting '{key}' deleted"}