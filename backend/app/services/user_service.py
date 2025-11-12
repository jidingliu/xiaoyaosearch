"""
用户服务
提供用户认证、授权和管理功能
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User
from app.core.config import settings
from app.api.exceptions import (
    AuthenticationError,
    NotFoundError,
    ConflictError
)

logger = logging.getLogger(__name__)

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """用户服务类"""

    def __init__(self, db: Session):
        self.db = db

    def _hash_password(self, password: str) -> str:
        """密码哈希"""
        return pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)

    def _create_access_token(self, user_id: str, expires_delta: Optional[timedelta] = None) -> str:
        """创建访问令牌"""
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        expire = datetime.utcnow() + expires_delta
        payload = {
            "sub": user_id,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }

        encoded_jwt = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm="HS256"
        )
        return encoded_jwt

    def _decode_token(self, token: str) -> Dict[str, Any]:
        """解码令牌"""
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )
            return payload
        except JWTError as e:
            logger.warning(f"JWT解码失败: {e}")
            raise AuthenticationError("无效的认证令牌")

    async def authenticate_user(self, username: str, password: str) -> User:
        """用户认证"""
        try:
            # 查找用户
            user = self.db.query(User).filter(User.username == username).first()
            if not user:
                raise AuthenticationError("用户名或密码错误")

            # 验证密码
            if not self._verify_password(password, user.hashed_password):
                raise AuthenticationError("用户名或密码错误")

            # 更新最后登录时间
            user.last_login = datetime.utcnow()
            self.db.commit()

            logger.info(f"用户认证成功: {username}")
            return user

        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"用户认证失败: {e}")
            raise AuthenticationError("认证失败")

    async def get_user_by_id(self, user_id: str) -> User:
        """根据用户ID获取用户"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise NotFoundError("用户不存在", resource_type="user", resource_id=user_id)
            return user

        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"获取用户失败: {e}")
            raise NotFoundError("获取用户信息失败")

    async def get_user_by_token(self, token: str) -> User:
        """根据令牌获取用户"""
        try:
            payload = self._decode_token(token)
            user_id = payload.get("sub")

            if not user_id:
                raise AuthenticationError("令牌无效")

            if payload.get("type") != "access":
                raise AuthenticationError("令牌类型错误")

            return await self.get_user_by_id(user_id)

        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"令牌验证失败: {e}")
            raise AuthenticationError("令牌验证失败")

    async def get_current_user(self) -> User:
        """获取当前用户（使用默认用户）"""
        try:
            # 对于单用户模式，返回默认用户
            user = self.db.query(User).filter(User.username == "默认用户").first()
            if not user:
                # 如果没有默认用户，创建一个
                user = await self.create_default_user()

            return user

        except Exception as e:
            logger.error(f"获取当前用户失败: {e}")
            # 创建默认用户作为后备
            try:
                return await self.create_default_user()
            except Exception as e2:
                logger.error(f"创建默认用户失败: {e2}")
                raise AuthenticationError("无法获取用户信息")

    async def create_user(self, username: str, password: str, email: Optional[str] = None) -> User:
        """创建用户"""
        try:
            # 检查用户名是否已存在
            existing_user = self.db.query(User).filter(User.username == username).first()
            if existing_user:
                raise ConflictError("用户名已存在", conflict_field="username")

            # 检查邮箱是否已存在
            if email:
                existing_email = self.db.query(User).filter(User.email == email).first()
                if existing_email:
                    raise ConflictError("邮箱已被使用", conflict_field="email")

            # 创建新用户
            hashed_password = self._hash_password(password)
            user_id = str(uuid.uuid4())

            user = User(
                id=user_id,
                username=username,
                email=email,
                hashed_password=hashed_password,
                is_active=True,
                created_at=datetime.utcnow(),
                last_login=datetime.utcnow()
            )

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            logger.info(f"用户创建成功: {username} (ID: {user_id})")
            return user

        except ConflictError:
            raise
        except Exception as e:
            logger.error(f"创建用户失败: {e}")
            self.db.rollback()
            raise ConflictError("创建用户失败")

    async def create_default_user(self) -> User:
        """创建默认用户"""
        try:
            # 检查是否已存在默认用户
            existing_user = self.db.query(User).filter(User.username == "默认用户").first()
            if existing_user:
                return existing_user

            # 创建默认用户（无需密码）
            user_id = str(uuid.uuid4())

            user = User(
                id=user_id,
                username="默认用户",
                email="user@xiaoyao.local",
                is_active=True,
                created_at=datetime.utcnow(),
                last_login=datetime.utcnow(),
                preferences='{"theme": "light", "language": "zh-CN"}'
            )

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            logger.info(f"默认用户创建成功 (ID: {user_id})")
            return user

        except Exception as e:
            logger.error(f"创建默认用户失败: {e}")
            self.db.rollback()
            raise ConflictError("创建默认用户失败")

    async def update_user(self, user_id: str, **kwargs) -> User:
        """更新用户信息"""
        try:
            user = await self.get_user_by_id(user_id)

            # 更新允许的字段
            for field, value in kwargs.items():
                if hasattr(user, field):
                    setattr(user, field, value)

            user.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(user)

            return user

        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"更新用户失败: {e}")
            self.db.rollback()
            raise ConflictError("更新用户信息失败")

    async def delete_user(self, user_id: str) -> bool:
        """删除用户（软删除）"""
        try:
            user = await self.get_user_by_id(user_id)
            user.is_active = False
            user.updated_at = datetime.utcnow()
            self.db.commit()

            logger.info(f"用户删除成功: {user.username}")
            return True

        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"删除用户失败: {e}")
            self.db.rollback()
            return False

    def _create_access_token(self, user_id: str, expires_delta: Optional[timedelta] = None) -> str:
        """创建访问令牌"""
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        expire = datetime.utcnow() + expires_delta
        payload = {
            "sub": user_id,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }

        encoded_jwt = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm="HS256"
        )
        return encoded_jwt