"""
搜索API端点
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.search import SearchRequest, SearchResponse, SearchResult
from app.services.search_service import SearchService

router = APIRouter()


@router.get("/", response_model=SearchResponse)
async def search_files(
    q: str = Query(..., description="搜索查询"),
    type: Optional[str] = Query(None, description="文件类型过滤"),
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    size: int = Query(20, ge=1, le=100, description="返回结果数量"),
    page: int = Query(1, ge=1, description="页码"),
    db: Session = Depends(get_db)
):
    """
    搜索文件
    """
    try:
        search_service = SearchService(db)

        request = SearchRequest(
            query=q,
            type=type,
            start_date=start_date,
            end_date=end_date,
            size=size,
            page=page
        )

        result = await search_service.search(request)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")


@router.post("/understand", response_model=dict)
async def understand_query(
    query: str = Query(..., description="用户查询"),
    db: Session = Depends(get_db)
):
    """
    理解用户查询意图
    """
    try:
        search_service = SearchService(db)
        understanding = await search_service.understand_query(query)
        return understanding

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询理解失败: {str(e)}")


@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., description="查询前缀"),
    limit: int = Query(5, ge=1, le=20, description="建议数量"),
    db: Session = Depends(get_db)
):
    """
    获取搜索建议
    """
    try:
        search_service = SearchService(db)
        suggestions = await search_service.get_suggestions(q, limit)
        return {"suggestions": suggestions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取建议失败: {str(e)}")