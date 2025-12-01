"""
雪花算法ID生成器

用于生成全局唯一的索引ID，替代数据库自增ID方案。
支持时间有序、高性能、分布式部署。
"""

import time
import threading
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class SnowflakeIdGenerator:
    """雪花算法ID生成器

    生成64位唯一ID，结构如下：
    - 1位符号位（固定为0）
    - 41位时间戳（毫秒级，可用69年）
    - 10位机器ID（0-1023，支持1024个节点）
    - 12位序列号（0-4095，每毫秒4096个ID）
    """

    def __init__(self, machine_id: int = 1):
        """
        初始化雪花算法生成器

        Args:
            machine_id: 机器ID，范围0-1023
        """
        if machine_id < 0 or machine_id > 1023:
            raise ValueError(f"机器ID必须在0-1023范围内，当前值: {machine_id}")

        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1

        # 线程锁
        self.lock = threading.Lock()

        # 各部分的位数
        self.EPOCH_BITS = 41
        self.MACHINE_ID_BITS = 10
        self.SEQUENCE_BITS = 12

        # 各部分的最大值
        self.MAX_MACHINE_ID = (1 << self.MACHINE_ID_BITS) - 1  # 1023
        self.MAX_SEQUENCE = (1 << self.SEQUENCE_BITS) - 1      # 4095

        # 各部分的偏移量
        self.MACHINE_ID_SHIFT = self.SEQUENCE_BITS              # 12
        self.TIMESTAMP_SHIFT = self.SEQUENCE_BITS + self.MACHINE_ID_BITS  # 22

        # 起始时间戳（2024-01-01 00:00:00 UTC）
        self.EPOCH = int(time.mktime((2024, 1, 1, 0, 0, 0, 0, 0, 0))) * 1000

        logger.info(f"雪花算法生成器初始化完成 - 机器ID: {machine_id}")

    def _current_timestamp(self) -> int:
        """获取当前时间戳（毫秒）"""
        return int(time.time() * 1000)

    def _wait_next_millis(self, last_timestamp: int) -> int:
        """等待到下一毫秒"""
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp

    def next_id(self) -> int:
        """生成下一个雪花ID

        Returns:
            int: 64位唯一ID
        """
        with self.lock:
            timestamp = self._current_timestamp()

            # 处理时钟回拨
            if timestamp < self.last_timestamp:
                logger.warning(f"检测到时钟回拨！当前时间戳: {timestamp}, 上次时间戳: {self.last_timestamp}")
                # 等待时钟追上
                timestamp = self._wait_next_millis(self.last_timestamp)

            # 同一毫秒内，序列号递增
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
                # 序列号溢出，等待下一毫秒
                if self.sequence == 0:
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                # 新的一毫秒，序列号重置为0
                self.sequence = 0

            self.last_timestamp = timestamp

            # 组装ID
            id = ((timestamp - self.EPOCH) << self.TIMESTAMP_SHIFT) | \
                 (self.machine_id << self.MACHINE_ID_SHIFT) | \
                 self.sequence

            return id

    def parse_id(self, snowflake_id: int) -> dict:
        """解析雪花ID

        Args:
            snowflake_id: 雪花ID

        Returns:
            dict: 解析结果 {timestamp, machine_id, sequence, datetime}
        """
        timestamp = ((snowflake_id >> self.TIMESTAMP_SHIFT) + self.EPOCH) / 1000
        machine_id = (snowflake_id >> self.MACHINE_ID_SHIFT) & self.MAX_MACHINE_ID
        sequence = snowflake_id & self.MAX_SEQUENCE

        return {
            'id': snowflake_id,
            'timestamp': timestamp,
            'machine_id': machine_id,
            'sequence': sequence,
            'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        }

# 全局生成器实例
_snowflake_generator: Optional[SnowflakeIdGenerator] = None

def get_snowflake_generator(machine_id: int = 1) -> SnowflakeIdGenerator:
    """获取雪花算法生成器实例

    Args:
        machine_id: 机器ID，范围0-1023

    Returns:
        SnowflakeIdGenerator: 生成器实例
    """
    global _snowflake_generator

    if _snowflake_generator is None:
        _snowflake_generator = SnowflakeIdGenerator(machine_id)

    return _snowflake_generator

def generate_snowflake_id(machine_id: int = 1) -> int:
    """生成雪花ID（快捷函数）

    Args:
        machine_id: 机器ID，范围0-1023

    Returns:
        int: 64位唯一ID
    """
    generator = get_snowflake_generator(machine_id)
    return generator.next_id()

def parse_snowflake_id(snowflake_id: int) -> dict:
    """解析雪花ID（快捷函数）

    Args:
        snowflake_id: 雪花ID

    Returns:
        dict: 解析结果
    """
    generator = get_snowflake_generator()
    return generator.parse_id(snowflake_id)

# 兼容性别名
SnowflakeIDGenerator = SnowflakeIdGenerator