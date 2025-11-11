"""
用户管理API端点
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.user_service import UserService

router = APIRouter()


@router.get("/current")
async def get_current_user(
    db: Session = Depends(get_db)
):
    """
    获取当前用户信息
    """
    try:
        user_service = UserService(db)
        user = await user_service.get_current_user()
        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户信息失败: {str(e)}")


@router.post("/")
async def create_user(
    db: Session = Depends(get_db)
):
    """
    创建用户
    """
    try:
        user_service = UserService(db)
        user = await user_service.create_user()
        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建用户失败: {str(e)}")