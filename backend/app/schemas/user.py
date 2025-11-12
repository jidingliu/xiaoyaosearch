"""
用户相关的Pydantic模式
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    """用户基础模式"""
    username: str = Field(..., min_length=1, max_length=100, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱地址")


class UserCreate(UserBase):
    """创建用户模式"""
    password: Optional[str] = Field(None, min_length=6, max_length=100, description="密码")
    preferences: Optional[str] = Field(None, description="用户偏好设置(JSON格式)")


class UserUpdate(BaseModel):
    """更新用户模式"""
    username: Optional[str] = Field(None, min_length=1, max_length=100, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    preferences: Optional[str] = Field(None, description="用户偏好设置(JSON格式)")
    is_active: Optional[bool] = Field(None, description="是否激活")


class UserLogin(BaseModel):
    """用户登录模式"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserResponse(UserBase):
    """用户响应模式"""
    id: str = Field(..., description="用户ID")
    created_at: datetime = Field(..., description="创建时间")
    last_login: datetime = Field(..., description="最后登录时间")
    is_active: bool = Field(..., description="是否激活")
    preferences: Optional[str] = Field(None, description="用户偏好设置")

    class Config:
        from_attributes = True


class UserToken(BaseModel):
    """用户令牌模式"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(..., description="令牌过期时间(秒)")


class UserAuth(BaseModel):
    """用户认证信息"""
    user_id: str = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    is_active: bool = Field(..., description="是否激活")