"""
Tags API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schemas.tag import Tag, TagCreate, TagUpdate

router = APIRouter()


@router.get("/", response_model=List[Tag])
async def list_tags(
    category: Optional[str] = Query(None, description="Filter by category"),
    is_system_tag: Optional[bool] = Query(None, description="Filter system tags"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tags"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all tags or filter by criteria.
    """
    # TODO: Implement tag listing
    return []


@router.get("/{tag_id}", response_model=Tag)
async def get_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get tag information by ID.
    """
    # TODO: Implement tag retrieval
    raise HTTPException(status_code=404, detail="Tag not found")


@router.post("/", response_model=Tag)
async def create_tag(
    tag: TagCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new tag.
    """
    # TODO: Implement tag creation
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/{tag_id}", response_model=Tag)
async def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing tag.
    """
    # TODO: Implement tag update
    raise HTTPException(status_code=404, detail="Tag not found")


@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a tag.
    """
    # TODO: Implement tag deletion
    return {"message": f"Tag {tag_id} deleted"}