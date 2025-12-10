"""
应用设置服务
提供动态配置管理的核心功能
"""
import json
import logging
from typing import List, Dict, Any, Optional, Union
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.database import SessionLocal
from app.models.app_settings import AppSettingsModel

logger = logging.getLogger(__name__)


class SettingsService:
    """应用设置服务类"""

    def __init__(self):
        self._db: Optional[Session] = None

    def _get_db(self) -> Session:
        """获取数据库会话"""
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def _close_db(self):
        """关闭数据库会话"""
        if self._db is not None:
            self._db.close()
            self._db = None

    def get_all_settings(self) -> List[Dict[str, Any]]:
        """
        获取所有设置项

        Returns:
            List[Dict[str, Any]]: 设置项列表
        """
        try:
            db = self._get_db()
            settings = db.query(AppSettingsModel).all()
            return [setting.to_dict() for setting in settings]
        except Exception as e:
            logger.error(f"获取设置失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"获取设置失败: {str(e)}")
        finally:
            self._close_db()

    def get_setting(self, key: str) -> Optional[Dict[str, Any]]:
        """
        获取指定设置项

        Args:
            key: 设置键名

        Returns:
            Optional[Dict[str, Any]]: 设置项，不存在返回None
        """
        try:
            db = self._get_db()
            setting = db.query(AppSettingsModel).filter(
                AppSettingsModel.setting_key == key
            ).first()

            if setting:
                return setting.to_dict()
            return None
        except Exception as e:
            logger.error(f"获取设置 {key} 失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"获取设置失败: {str(e)}")
        finally:
            self._close_db()

    def get_setting_value(self, key: str, default: Any = None) -> Any:
        """
        获取设置值（解析后的原始值）

        Args:
            key: 设置键名
            default: 默认值

        Returns:
            Any: 解析后的设置值，不存在返回默认值
        """
        try:
            setting_dict = self.get_setting(key)
            if setting_dict:
                setting = AppSettingsModel()
                setting.setting_key = setting_dict['setting_key']
                setting.setting_value = setting_dict['setting_value']
                setting.setting_type = setting_dict['setting_type']
                return setting.get_parsed_value()
            return default
        except Exception as e:
            logger.error(f"获取设置值 {key} 失败: {str(e)}")
            return default

    def create_setting(
        self,
        key: str,
        value: Any,
        setting_type: str = "string",
        description: str = None
    ) -> Dict[str, Any]:
        """
        创建新的设置项

        Args:
            key: 设置键名
            value: 设置值
            setting_type: 值类型 (string/integer/boolean/float/json)
            description: 设置说明

        Returns:
            Dict[str, Any]: 创建的设置项
        """
        try:
            db = self._get_db()

            # 检查设置是否已存在
            existing = db.query(AppSettingsModel).filter(
                AppSettingsModel.setting_key == key
            ).first()

            if existing:
                raise HTTPException(status_code=400, detail=f"设置项 {key} 已存在")

            # 创建新设置
            setting = AppSettingsModel()
            setting.setting_key = key
            setting.setting_value = AppSettingsModel.parse_value_to_string(value, setting_type)
            setting.setting_type = setting_type
            setting.description = description

            db.add(setting)
            db.commit()
            db.refresh(setting)

            logger.info(f"创建设置项成功: {key}")
            return setting.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"创建设置项 {key} 失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"创建设置项失败: {str(e)}")
        finally:
            self._close_db()

    def update_setting(self, key: str, value: Any) -> Dict[str, Any]:
        """
        更新设置值

        Args:
            key: 设置键名
            value: 新的设置值

        Returns:
            Dict[str, Any]: 更新后的设置项
        """
        try:
            db = self._get_db()

            setting = db.query(AppSettingsModel).filter(
                AppSettingsModel.setting_key == key
            ).first()

            if not setting:
                raise HTTPException(status_code=404, detail=f"设置项 {key} 不存在")

            # 更新值
            setting.update_value(value)
            db.commit()
            db.refresh(setting)

            logger.info(f"更新设置项成功: {key} = {value}")
            return setting.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"更新设置项 {key} 失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"更新设置项失败: {str(e)}")
        finally:
            self._close_db()

    def delete_setting(self, key: str) -> bool:
        """
        删除设置项

        Args:
            key: 设置键名

        Returns:
            bool: 删除是否成功
        """
        try:
            db = self._get_db()

            setting = db.query(AppSettingsModel).filter(
                AppSettingsModel.setting_key == key
            ).first()

            if not setting:
                raise HTTPException(status_code=404, detail=f"设置项 {key} 不存在")

            db.delete(setting)
            db.commit()

            logger.info(f"删除设置项成功: {key}")
            return True
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"删除设置项 {key} 失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"删除设置项失败: {str(e)}")
        finally:
            self._close_db()

    def batch_create_settings(self, settings_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        批量创建设置项

        Args:
            settings_data: 设置数据列表，每个元素包含 key, value, type, description

        Returns:
            List[Dict[str, Any]]: 创建的设置项列表
        """
        try:
            db = self._get_db()
            created_settings = []

            for setting_data in settings_data:
                key = setting_data.get('key')
                value = setting_data.get('value')
                setting_type = setting_data.get('type', 'string')
                description = setting_data.get('description')

                if not key:
                    continue

                # 检查是否已存在
                existing = db.query(AppSettingsModel).filter(
                    AppSettingsModel.setting_key == key
                ).first()

                if existing:
                    continue

                # 创建设置
                setting = AppSettingsModel()
                setting.setting_key = key
                setting.setting_value = AppSettingsModel.parse_value_to_string(value, setting_type)
                setting.setting_type = setting_type
                setting.description = description

                db.add(setting)
                created_settings.append(setting)

            db.commit()

            # 刷新并返回创建的设置
            for setting in created_settings:
                db.refresh(setting)

            logger.info(f"批量创建设置项成功: {len(created_settings)} 个")
            return [setting.to_dict() for setting in created_settings]
        except Exception as e:
            logger.error(f"批量创建设置项失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"批量创建设置项失败: {str(e)}")
        finally:
            self._close_db()

    def reset_to_defaults(self, default_settings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        重置为默认设置

        Args:
            default_settings: 默认设置列表

        Returns:
            Dict[str, Any]: 重置结果统计
        """
        try:
            db = self._get_db()

            # 清除所有现有设置
            db.query(AppSettingsModel).delete()
            db.commit()

            # 创建默认设置
            created_count = 0
            for setting_data in default_settings:
                try:
                    setting = AppSettingsModel()
                    setting.setting_key = setting_data['setting_key']
                    setting.setting_value = setting_data['setting_value']
                    setting.setting_type = setting_data['setting_type']
                    setting.description = setting_data['description']

                    db.add(setting)
                    created_count += 1
                except Exception as e:
                    logger.warning(f"创建默认设置失败: {setting_data.get('setting_key')}, {str(e)}")
                    continue

            db.commit()

            logger.info(f"重置设置为默认值成功: {created_count} 个设置项")
            return {
                "total_defaults": len(default_settings),
                "created_count": created_count,
                "message": f"成功重置 {created_count} 个默认设置"
            }
        except Exception as e:
            logger.error(f"重置设置失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"重置设置失败: {str(e)}")
        finally:
            self._close_db()

    def export_settings(self) -> Dict[str, Any]:
        """
        导出所有设置为JSON格式

        Returns:
            Dict[str, Any]: 导出的设置数据
        """
        try:
            settings = self.get_all_settings()

            # 转换为键值对格式
            exported_data = {}
            for setting in settings:
                key = setting['setting_key']
                setting_obj = AppSettingsModel()
                setting_obj.setting_key = setting['setting_key']
                setting_obj.setting_value = setting['setting_value']
                setting_obj.setting_type = setting['setting_type']

                exported_data[key] = {
                    'value': setting_obj.get_parsed_value(),
                    'type': setting['setting_type'],
                    'description': setting['description'],
                    'updated_at': setting['updated_at']
                }

            return {
                "export_time": self._get_current_time(),
                "total_settings": len(settings),
                "settings": exported_data
            }
        except Exception as e:
            logger.error(f"导出设置失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"导出设置失败: {str(e)}")

    def import_settings(self, settings_data: Dict[str, Any], overwrite: bool = False) -> Dict[str, Any]:
        """
        从JSON数据导入设置

        Args:
            settings_data: 设置数据
            overwrite: 是否覆盖现有设置

        Returns:
            Dict[str, Any]: 导入结果统计
        """
        try:
            db = self._get_db()
            imported_count = 0
            skipped_count = 0

            for key, data in settings_data.items():
                try:
                    value = data.get('value')
                    setting_type = data.get('type', 'string')
                    description = data.get('description', '')

                    # 检查现有设置
                    existing = db.query(AppSettingsModel).filter(
                        AppSettingsModel.setting_key == key
                    ).first()

                    if existing and not overwrite:
                        skipped_count += 1
                        continue

                    if existing:
                        # 更新现有设置
                        existing.update_value(value)
                        existing.setting_type = setting_type
                        if description:
                            existing.description = description
                    else:
                        # 创建新设置
                        setting = AppSettingsModel()
                        setting.setting_key = key
                        setting.setting_value = AppSettingsModel.parse_value_to_string(value, setting_type)
                        setting.setting_type = setting_type
                        setting.description = description
                        db.add(setting)

                    imported_count += 1
                except Exception as e:
                    logger.warning(f"导入设置失败: {key}, {str(e)}")
                    skipped_count += 1
                    continue

            db.commit()

            logger.info(f"导入设置完成: 导入 {imported_count} 个，跳过 {skipped_count} 个")
            return {
                "imported_count": imported_count,
                "skipped_count": skipped_count,
                "message": f"成功导入 {imported_count} 个设置"
            }
        except Exception as e:
            logger.error(f"导入设置失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"导入设置失败: {str(e)}")
        finally:
            self._close_db()

    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().isoformat()


# 全局服务实例
settings_service = SettingsService()