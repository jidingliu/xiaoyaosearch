"""
文件管理API端点
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.file import FileInfo, FilePreview
from app.services.file_service import FileService

router = APIRouter()


@router.get("/", response_model=List[FileInfo])
async def list_files(
    directory_id: Optional[str] = Query(None, description="目录ID"),
    type: Optional[str] = Query(None, description="文件类型过滤"),
    indexed_only: bool = Query(True, description="仅显示已索引文件"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(50, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取文件列表
    """
    try:
        file_service = FileService(db)
        files = await file_service.list_files(
            directory_id=directory_id,
            file_type=type,
            indexed_only=indexed_only,
            page=page,
            size=size
        )
        return files

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件列表失败: {str(e)}")


@router.get("/{file_id}", response_model=FileInfo)
async def get_file_info(
    file_id: str,
    db: Session = Depends(get_db)
):
    """
    获取文件详细信息
    """
    try:
        file_service = FileService(db)
        file_info = await file_service.get_file_info(file_id)
        if not file_info:
            raise HTTPException(status_code=404, detail="文件不存在")
        return file_info

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件信息失败: {str(e)}")


@router.get("/{file_id}/preview", response_model=FilePreview)
async def preview_file(
    file_id: str,
    highlights: Optional[str] = Query(None, description="高亮关键词"),
    db: Session = Depends(get_db)
):
    """
    预览文件内容
    """
    try:
        file_service = FileService(db)
        preview = await file_service.preview_file(
            file_id=file_id,
            highlights=highlights.split(",") if highlights else None
        )
        if not preview:
            raise HTTPException(status_code=404, detail="文件不存在或无法预览")
        return preview

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件预览失败: {str(e)}")


@router.post("/{file_id}/open")
async def open_file(
    file_id: str,
    db: Session = Depends(get_db)
):
    """
    使用系统默认应用打开文件
    """
    try:
        file_service = FileService(db)
        success = await file_service.open_file(file_id)
        if not success:
            raise HTTPException(status_code=404, detail="文件不存在")
        return {"message": "文件已打开"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"打开文件失败: {str(e)}")


@router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    db: Session = Depends(get_db)
):
    """
    删除文件
    """
    try:
        file_service = FileService(db)
        success = await file_service.delete_file(file_id)
        if not success:
            raise HTTPException(status_code=404, detail="文件不存在")
        return {"message": "文件已删除"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文件失败: {str(e)}")


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    directory_id: Optional[str] = Query(None, description="目标目录ID"),
    db: Session = Depends(get_db)
):
    """
    上传文件
    """
    try:
        file_service = FileService(db)
        file_info = await file_service.upload_file(file, directory_id)
        return file_info

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")