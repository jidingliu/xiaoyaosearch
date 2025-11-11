"""
目录管理API端点
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.schemas.directory import DirectoryInfo, DirectoryCreate
from app.services.directory_service import DirectoryService

router = APIRouter()


@router.get("/", response_model=List[DirectoryInfo])
async def list_directories(
    db: Session = Depends(get_db)
):
    """
    获取所有索引目录
    """
    try:
        directory_service = DirectoryService(db)
        directories = await directory_service.list_directories()
        return directories

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取目录列表失败: {str(e)}")


@router.post("/", response_model=DirectoryInfo)
async def add_directory(
    directory_data: DirectoryCreate,
    db: Session = Depends(get_db)
):
    """
    添加索引目录
    """
    try:
        directory_service = DirectoryService(db)
        directory = await directory_service.add_directory(directory_data)
        return directory

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加目录失败: {str(e)}")


@router.get("/{directory_id}", response_model=DirectoryInfo)
async def get_directory(
    directory_id: str,
    db: Session = Depends(get_db)
):
    """
    获取目录详细信息
    """
    try:
        directory_service = DirectoryService(db)
        directory = await directory_service.get_directory(directory_id)
        if not directory:
            raise HTTPException(status_code=404, detail="目录不存在")
        return directory

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取目录信息失败: {str(e)}")


@router.post("/{directory_id}/scan")
async def scan_directory(
    directory_id: str,
    full_scan: bool = Query(False, description="是否进行全量扫描"),
    db: Session = Depends(get_db)
):
    """
    扫描目录
    """
    try:
        directory_service = DirectoryService(db)
        result = await directory_service.scan_directory(directory_id, full_scan)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"目录扫描失败: {str(e)}")


@router.delete("/{directory_id}")
async def remove_directory(
    directory_id: str,
    remove_files: bool = Query(False, description="是否同时删除相关文件索引"),
    db: Session = Depends(get_db)
):
    """
    移除索引目录
    """
    try:
        directory_service = DirectoryService(db)
        success = await directory_service.remove_directory(directory_id, remove_files)
        if not success:
            raise HTTPException(status_code=404, detail="目录不存在")
        return {"message": "目录已移除"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"移除目录失败: {str(e)}")


@router.get("/{directory_id}/status")
async def get_directory_status(
    directory_id: str,
    db: Session = Depends(get_db)
):
    """
    获取目录扫描状态
    """
    try:
        directory_service = DirectoryService(db)
        status = await directory_service.get_scan_status(directory_id)
        return status

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取目录状态失败: {str(e)}")