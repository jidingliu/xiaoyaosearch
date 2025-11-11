"""
设置管理API端点
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.services.settings_service import SettingsService

router = APIRouter()


class SettingsUpdate(BaseModel):
    """设置更新模式"""
    search_mode: str = None
    results_per_page: int = None
    auto_suggestions: bool = None
    ai_mode: str = None
    theme: str = None
    language: str = None


@router.get("/")
async def get_settings(
    db: Session = Depends(get_db)
):
    """
    获取用户设置
    """
    try:
        settings_service = SettingsService(db)
        settings = await settings_service.get_settings()
        return settings

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取设置失败: {str(e)}")


@router.put("/")
async def update_settings(
    settings_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    更新用户设置
    """
    try:
        settings_service = SettingsService(db)
        settings = await settings_service.update_settings(settings_data)
        return settings

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新设置失败: {str(e)}")


@router.post("/reset")
async def reset_settings(
    db: Session = Depends(get_db)
):
    """
    重置用户设置
    """
    try:
        settings_service = SettingsService(db)
        settings = await settings_service.reset_settings()
        return {"message": "设置已重置", "settings": settings}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"重置设置失败: {str(e)}")


@router.post("/export")
async def export_settings(
    db: Session = Depends(get_db)
):
    """
    导出设置
    """
    try:
        settings_service = SettingsService(db)
        export_data = await settings_service.export_settings()
        return export_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出设置失败: {str(e)}")


@router.post("/import")
async def import_settings(
    settings_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    导入设置
    """
    try:
        settings_service = SettingsService(db)
        settings = await settings_service.import_settings(settings_data)
        return {"message": "设置导入成功", "settings": settings}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入设置失败: {str(e)}")