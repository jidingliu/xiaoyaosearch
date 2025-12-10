"""
应用设置管理API接口
提供动态配置的增删改查功能
"""
import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from app.services.settings_service import settings_service
from app.schemas.requests import (
    CreateSettingRequest,
    UpdateSettingRequest,
    BatchCreateRequest,
    ResetRequest
)
from app.schemas.responses import (
    SettingResponse,
    MessageResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/settings", tags=["设置管理"])


@router.get("/", response_model=List[SettingResponse])
async def get_all_settings():
    """
    获取所有设置项

    Returns:
        List[SettingResponse]: 所有设置项列表
    """
    try:
        settings = settings_service.get_all_settings()
        return [SettingResponse(**setting) for setting in settings]
    except Exception as e:
        logger.error(f"获取所有设置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取设置失败: {str(e)}")


@router.get("/{key}", response_model=SettingResponse)
async def get_setting(key: str):
    """
    获取指定设置项

    Args:
        key: 设置键名

    Returns:
        SettingResponse: 指定的设置项
    """
    try:
        setting = settings_service.get_setting(key)
        if not setting:
            raise HTTPException(status_code=404, detail=f"设置项 {key} 不存在")
        return SettingResponse(**setting)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取设置 {key} 失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取设置失败: {str(e)}")


@router.get("/{key}/value")
async def get_setting_value(
    key: str,
    default: Optional[str] = Query(None, description="默认值")
):
    """
    获取设置值（解析后的原始值）

    Args:
        key: 设置键名
        default: 默认值

    Returns:
        Dict[str, Any]: 包含设置值的响应
    """
    try:
        # 解析默认值
        parsed_default = default
        if default and default.lower() in ('true', 'false'):
            parsed_default = default.lower() == 'true'
        elif default and default.isdigit():
            parsed_default = int(default)
        elif default and '.' in default and default.replace('.', '').isdigit():
            parsed_default = float(default)

        value = settings_service.get_setting_value(key, parsed_default)
        return {
            "key": key,
            "value": value,
            "exists": settings_service.get_setting(key) is not None
        }
    except Exception as e:
        logger.error(f"获取设置值 {key} 失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取设置值失败: {str(e)}")


@router.post("/", response_model=SettingResponse)
async def create_setting(request: CreateSettingRequest):
    """
    创建新的设置项

    Args:
        request: 创建设置请求

    Returns:
        SettingResponse: 创建的设置项
    """
    try:
        # 验证设置类型
        valid_types = {"string", "integer", "boolean", "float", "json"}
        if request.type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"无效的设置类型: {request.type}，支持的类型: {valid_types}"
            )

        # 验证值与类型匹配
        if request.type == "boolean":
            if not isinstance(request.value, bool):
                raise HTTPException(status_code=400, detail="布尔类型值必须是 true 或 false")
        elif request.type == "integer":
            if not isinstance(request.value, int):
                raise HTTPException(status_code=400, detail="整数类型值必须是整数")
        elif request.type == "float":
            if not isinstance(request.value, (int, float)):
                raise HTTPException(status_code=400, detail="浮点类型值必须是数字")

        setting = settings_service.create_setting(
            key=request.key,
            value=request.value,
            setting_type=request.type,
            description=request.description
        )
        return SettingResponse(**setting)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建设置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建设置失败: {str(e)}")


@router.put("/{key}", response_model=SettingResponse)
async def update_setting(key: str, request: UpdateSettingRequest):
    """
    更新设置值

    Args:
        key: 设置键名
        request: 更新设置请求

    Returns:
        SettingResponse: 更新后的设置项
    """
    try:
        setting = settings_service.update_setting(key, request.value)
        return SettingResponse(**setting)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新设置 {key} 失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"更新设置失败: {str(e)}")


@router.delete("/{key}")
async def delete_setting(key: str):
    """
    删除设置项

    Args:
        key: 设置键名

    Returns:
        MessageResponse: 删除结果
    """
    try:
        success = settings_service.delete_setting(key)
        return MessageResponse(
            message=f"设置项 {key} 删除成功" if success else f"设置项 {key} 不存在"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除设置 {key} 失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除设置失败: {str(e)}")


@router.post("/batch", response_model=List[SettingResponse])
async def batch_create_settings(request: BatchCreateRequest):
    """
    批量创建设置项

    Args:
        request: 批量创建请求

    Returns:
        List[SettingResponse]: 创建的设置项列表
    """
    try:
        # 转换数据格式
        settings_data = []
        for setting in request.settings:
            settings_data.append({
                'key': setting.get('key'),
                'value': setting.get('value'),
                'type': setting.get('type', 'string'),
                'description': setting.get('description')
            })

        created_settings = settings_service.batch_create_settings(settings_data)
        return [SettingResponse(**setting) for setting in created_settings]
    except Exception as e:
        logger.error(f"批量创建设置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"批量创建设置失败: {str(e)}")


@router.post("/reset", response_model=MessageResponse)
async def reset_to_defaults(request: ResetRequest):
    """
    重置为默认设置

    Args:
        request: 重置请求，包含默认设置列表

    Returns:
        MessageResponse: 重置结果
    """
    try:
        result = settings_service.reset_to_defaults(request.default_settings)
        return MessageResponse(
            message=result.get("message", "重置完成"),
            data=result
        )
    except Exception as e:
        logger.error(f"重置设置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"重置设置失败: {str(e)}")

