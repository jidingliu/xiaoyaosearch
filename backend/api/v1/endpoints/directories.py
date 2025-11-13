"""
Directory management API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schemas.directory import Directory, DirectoryCreate, DirectoryUpdate, DirectoryStatus

router = APIRouter()


@router.post("/", response_model=Directory)
async def create_directory(
    directory: DirectoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Add a new directory for indexing.
    """
    # TODO: Implement directory creation
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/", response_model=List[Directory])
async def list_directories(
    skip: int = Query(0, ge=0, description="Number of directories to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of directories"),
    indexed_only: bool = Query(False, description="Only return indexed directories"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all configured directories.
    """
    # TODO: Implement directory listing
    return []


@router.get("/{directory_id}", response_model=Directory)
async def get_directory(
    directory_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get directory information by ID.
    """
    # TODO: Implement directory retrieval
    raise HTTPException(status_code=404, detail="Directory not found")


@router.put("/{directory_id}", response_model=Directory)
async def update_directory(
    directory_id: int,
    directory_update: DirectoryUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update directory configuration.
    """
    # TODO: Implement directory update
    raise HTTPException(status_code=404, detail="Directory not found")


@router.delete("/{directory_id}")
async def delete_directory(
    directory_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Remove directory from indexing (removes directory record, not files on disk).
    """
    # TODO: Implement directory deletion
    return {"message": f"Directory {directory_id} removed from indexing"}


@router.get("/status/{directory_id}", response_model=DirectoryStatus)
async def get_directory_status(
    directory_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get directory scanning status and progress.
    """
    # TODO: Implement directory status retrieval
    raise HTTPException(status_code=404, detail="Directory not found")


@router.post("/{directory_id}/scan")
async def start_directory_scan(
    directory_id: int,
    full_scan: bool = Query(False, description="Perform full scan instead of incremental"),
    db: AsyncSession = Depends(get_db)
):
    """
    Start scanning directory for files.
    """
    # TODO: Implement directory scanning
    return {"message": f"Scanning started for directory {directory_id}"}


@router.post("/{directory_id}/stop")
async def stop_directory_scan(
    directory_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Stop ongoing directory scan.
    """
    # TODO: Implement scan stopping
    return {"message": f"Scanning stopped for directory {directory_id}"}