"""
分块服务

实现智能分块算法，支持500字符+50重叠策略。
提供透明分块处理，提升长文档搜索精度。
"""

import re
from typing import List, Dict, Any, Optional, Tuple
import logging
from dataclasses import dataclass
from app.core.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class ChunkInfo:
    """分块信息数据类"""
    content: str
    start_position: int
    end_position: int
    chunk_index: int
    content_length: int = 0

    def __post_init__(self):
        """初始化后处理"""
        self.content_length = len(self.content)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "content": self.content,
            "start_position": self.start_position,
            "end_position": self.end_position,
            "chunk_index": self.chunk_index,
            "content_length": self.content_length
        }


class ChunkService:
    """分块服务

    功能：
    - 智能分块：500字符+50重叠策略
    - 段落边界分割
    - 超长段落处理
    - 内容重装
    """

    def __init__(self, default_chunk_size: int = 500, default_overlap: int = 50):
        """初始化分块服务

        Args:
            default_chunk_size: 默认分块大小（字符数）
            default_overlap: 默认重叠大小（字符数）
        """
        self.default_chunk_size = default_chunk_size
        self.default_overlap = default_overlap

        # 段落分隔符（按优先级排序）
        self.paragraph_separators = [
            '\n\n\n',  # 三换行（章节分隔）
            '\n\n',   # 双换行（段落分隔）
            '\n',     # 单换行（行分隔）
            '。',     # 中文句号
            '！',     # 中文感叹号
            '？',     # 中文问号
            '；',     # 中文分号
            '. ',     # 英文句号+空格
            '! ',     # 英文感叹号+空格
            '? ',     # 英文问号+空格
            '; ',     # 英文分号+空格
        ]

        logger.info(f"分块服务初始化完成，默认分块大小: {default_chunk_size}，重叠: {default_overlap}")

    def intelligent_chunking(self, content: str, strategy: str = "500+50") -> List[ChunkInfo]:
        """智能分块：按语义边界分割

        Args:
            content: 原始内容
            strategy: 分块策略 "500+50" (大小+重叠)

        Returns:
            List[ChunkInfo]: 分块列表，包含位置和内容信息
        """
        if not content or not content.strip():
            logger.warning("内容为空，返回空分块列表")
            return []

        content = content.strip()

        # 如果内容较短，无需分块
        if len(content) <= self.default_chunk_size:
            logger.info(f"内容长度({len(content)})小于分块大小，返回单个分块")
            return [ChunkInfo(
                content=content,
                start_position=0,
                end_position=len(content),
                chunk_index=0
            )]

        # 解析策略
        chunk_size, overlap = self._parse_strategy(strategy)
        logger.info(f"开始智能分块，策略: {strategy}，分块大小: {chunk_size}，重叠: {overlap}")

        try:
            # 使用段落分隔符进行分块
            chunks = self._chunk_by_paragraphs(content, chunk_size, overlap)

            logger.info(f"分块完成，共生成 {len(chunks)} 个分块")
            return chunks

        except Exception as e:
            logger.error(f"智能分块失败: {e}")
            # 回退到简单分块
            return self._simple_chunking(content, chunk_size, overlap)

    def _parse_strategy(self, strategy: str) -> Tuple[int, int]:
        """解析分块策略

        Args:
            strategy: 策略字符串，如 "500+50"

        Returns:
            Tuple[int, int]: (分块大小, 重叠大小)
        """
        try:
            if '+' in strategy:
                parts = strategy.split('+')
                chunk_size = int(parts[0])
                overlap = int(parts[1])
            else:
                chunk_size = int(strategy)
                overlap = min(50, chunk_size // 10)  # 默认重叠为分块大小的10%

            # 验证参数
            chunk_size = max(100, min(chunk_size, 2000))  # 限制在100-2000字符
            overlap = max(0, min(overlap, chunk_size // 2))  # 重叠不超过分块大小的一半

            return chunk_size, overlap

        except Exception as e:
            logger.warning(f"解析分块策略失败 {strategy}: {e}，使用默认值")
            return self.default_chunk_size, self.default_overlap

    def _chunk_by_paragraphs(self, content: str, chunk_size: int, overlap: int) -> List[ChunkInfo]:
        """按段落边界分块

        Args:
            content: 原始内容
            chunk_size: 分块大小
            overlap: 重叠大小

        Returns:
            List[ChunkInfo]: 分块列表
        """
        chunks = []
        current_pos = 0
        chunk_index = 0

        while current_pos < len(content):
            # 确定当前分块的结束位置
            chunk_end = min(current_pos + chunk_size, len(content))

            # 如果不是最后一个分块，尝试在段落边界处分割
            if chunk_end < len(content):
                # 在当前分块范围内寻找最佳分割点
                best_split_pos = self._find_best_split_position(content, current_pos, chunk_end)

                if best_split_pos > current_pos:
                    chunk_end = best_split_pos
                else:
                    # 如果找不到合适的分割点，强制在分块大小处分割
                    logger.debug(f"在位置 {current_pos} 未找到合适的分割点，强制分割")

            # 提取分块内容
            chunk_content = content[current_pos:chunk_end].strip()

            if chunk_content:
                # 添加重叠内容（不是第一个分块）
                if chunk_index > 0 and overlap > 0:
                    overlap_content = self._get_overlap_content(
                        content, chunks, current_pos, overlap
                    )
                    if overlap_content:
                        chunk_content = overlap_content + "\n\n" + chunk_content
                        # 调整开始位置
                        current_pos = max(0, current_pos - len(overlap_content))

                chunk_info = ChunkInfo(
                    content=chunk_content,
                    start_position=current_pos,
                    end_position=chunk_end,
                    chunk_index=chunk_index
                )

                chunks.append(chunk_info)
                logger.debug(f"创建分块 {chunk_index}: 位置 {current_pos}-{chunk_end}, 长度 {len(chunk_content)}")

            # 移动到下一个分块（考虑重叠）
            current_pos = chunk_end
            chunk_index += 1

        return chunks

    def _find_best_split_position(self, content: str, start_pos: int, end_pos: int) -> int:
        """在指定范围内寻找最佳分割位置

        Args:
            content: 完整内容
            start_pos: 开始位置
            end_pos: 结束位置

        Returns:
            int: 最佳分割位置
        """
        # 搜索范围：从结束位置往前回溯20%的分块大小
        search_range = max(50, (end_pos - start_pos) // 5)
        search_start = max(start_pos, end_pos - search_range)

        best_pos = end_pos  # 默认使用原始结束位置
        best_priority = len(self.paragraph_separators) + 1  # 最低优先级

        for pos in range(end_pos - 1, search_start - 1, -1):
            # 检查当前位置是否是分隔符
            for i, separator in enumerate(self.paragraph_separators):
                if content.startswith(separator, pos):
                    # 找到更高优先级的分隔符
                    if i < best_priority:
                        best_pos = pos + len(separator)
                        best_priority = i
                        # 如果找到最高优先级，直接返回
                        if i == 0:
                            return best_pos
                    break

        return best_pos

    def _get_overlap_content(self, content: str, existing_chunks: List[ChunkInfo],
                           current_pos: int, overlap_size: int) -> str:
        """获取重叠内容

        Args:
            content: 完整内容
            existing_chunks: 已存在的分块列表
            current_pos: 当前位置
            overlap_size: 重叠大小

        Returns:
            str: 重叠内容
        """
        if not existing_chunks or overlap_size <= 0:
            return ""

        # 从上一个分块的末尾获取重叠内容
        last_chunk = existing_chunks[-1]

        # 计算重叠的起始位置
        overlap_start = max(last_chunk.end_position - overlap_size, last_chunk.start_position)
        overlap_end = last_chunk.end_position

        if overlap_start >= overlap_end:
            return ""

        overlap_content = content[overlap_start:overlap_end].strip()

        # 确保重叠内容是完整的句子
        overlap_content = self._ensure_complete_sentences(overlap_content)

        return overlap_content

    def _ensure_complete_sentences(self, content: str) -> str:
        """确保内容以完整句子结束

        Args:
            content: 原始内容

        Returns:
            str: 处理后的内容
        """
        if not content:
            return content

        # 寻找最后一个句子结束符
        sentence_endings = ['。', '！', '？', '.', '!', '?']

        for i in range(len(content) - 1, -1, -1):
            if content[i] in sentence_endings:
                return content[:i + 1]

        # 如果没有找到句子结束符，返回原内容
        return content

    def _simple_chunking(self, content: str, chunk_size: int, overlap: int) -> List[ChunkInfo]:
        """简单分块：固定大小分块（回退方案）

        Args:
            content: 原始内容
            chunk_size: 分块大小
            overlap: 重叠大小

        Returns:
            List[ChunkInfo]: 分块列表
        """
        logger.info("使用简单分块方案")

        chunks = []
        chunk_index = 0
        current_pos = 0

        while current_pos < len(content):
            # 计算分块范围
            start_pos = max(0, current_pos - overlap) if chunk_index > 0 else current_pos
            end_pos = min(current_pos + chunk_size, len(content))

            # 提取分块内容
            chunk_content = content[start_pos:end_pos]

            if chunk_content.strip():
                chunk_info = ChunkInfo(
                    content=chunk_content.strip(),
                    start_position=start_pos,
                    end_position=end_pos,
                    chunk_index=chunk_index
                )

                chunks.append(chunk_info)

            current_pos = end_pos
            chunk_index += 1

        return chunks

    def reassemble_content(self, chunks: List[ChunkInfo]) -> str:
        """重新组装内容

        Args:
            chunks: 分块列表

        Returns:
            str: 重新组装的内容
        """
        if not chunks:
            return ""

        try:
            # 按位置排序
            sorted_chunks = sorted(chunks, key=lambda x: x.start_position)

            # 去除重叠部分并组装内容
            content_parts = []
            last_end = 0

            for chunk in sorted_chunks:
                if chunk.start_position > last_end:
                    # 有间隔，添加间隔内容
                    content_parts.append(chunk.content)
                elif chunk.start_position <= last_end <= chunk.end_position:
                    # 有重叠，只添加非重叠部分
                    overlap_size = last_end - chunk.start_position
                    if overlap_size < len(chunk.content):
                        non_overlap_content = chunk.content[overlap_size:]
                        if non_overlap_content.strip():
                            content_parts.append(non_overlap_content)
                else:
                    # 完全不重叠
                    content_parts.append(chunk.content)

                last_end = chunk.end_position

            assembled_content = "\n\n".join(content_parts)
            logger.info(f"内容重装完成，原始分块数: {len(chunks)}，组装后长度: {len(assembled_content)}")

            return assembled_content

        except Exception as e:
            logger.error(f"内容重装失败: {e}")
            # 回退到简单拼接
            return "\n\n".join(chunk.content for chunk in sorted(chunks))

    def validate_chunks(self, chunks: List[ChunkInfo]) -> Dict[str, Any]:
        """验证分块质量

        Args:
            chunks: 分块列表

        Returns:
            Dict[str, Any]: 验证结果
        """
        if not chunks:
            return {
                "valid": False,
                "error": "分块列表为空",
                "stats": {}
            }

        try:
            stats = {
                "total_chunks": len(chunks),
                "total_length": sum(chunk.content_length for chunk in chunks),
                "avg_chunk_size": sum(chunk.content_length for chunk in chunks) / len(chunks),
                "min_chunk_size": min(chunk.content_length for chunk in chunks),
                "max_chunk_size": max(chunk.content_length for chunk in chunks),
                "chunks_too_small": sum(1 for chunk in chunks if chunk.content_length < 100),
                "chunks_too_large": sum(1 for chunk in chunks if chunk.content_length > 1000)
            }

            # 检查分块是否连续
            sorted_chunks = sorted(chunks, key=lambda x: x.start_position)
            gaps = []
            for i in range(len(sorted_chunks) - 1):
                current = sorted_chunks[i]
                next_chunk = sorted_chunks[i + 1]
                if next_chunk.start_position > current.end_position:
                    gaps.append({
                        "gap_size": next_chunk.start_position - current.end_position,
                        "between_chunks": (i, i + 1)
                    })

            stats["gaps"] = len(gaps)
            stats["gap_details"] = gaps[:5]  # 只保留前5个间隔详情

            # 评估分块质量
            valid = (
                stats["chunks_too_small"] == 0 and
                stats["chunks_too_large"] < len(chunks) * 0.1 and  # 少于10%的分块过大
                stats["gaps"] == 0  # 没有间隔
            )

            quality_score = 1.0
            if stats["chunks_too_large"] > 0:
                quality_score -= stats["chunks_too_large"] / len(chunks) * 0.3
            if stats["gaps"] > 0:
                quality_score -= 0.2

            return {
                "valid": valid,
                "quality_score": max(0.0, quality_score),
                "stats": stats,
                "recommendations": self._generate_recommendations(stats)
            }

        except Exception as e:
            logger.error(f"验证分块质量失败: {e}")
            return {
                "valid": False,
                "error": str(e),
                "stats": {}
            }

    def _generate_recommendations(self, stats: Dict[str, Any]) -> List[str]:
        """生成改进建议

        Args:
            stats: 统计信息

        Returns:
            List[str]: 建议列表
        """
        recommendations = []

        if stats["chunks_too_small"] > 0:
            recommendations.append(f"发现 {stats['chunks_too_small']} 个过小分块(<100字符)，建议调整分块策略")

        if stats["chunks_too_large"] > 0:
            recommendations.append(f"发现 {stats['chunks_too_large']} 个过大分块(>1000字符)，建议减小分块大小")

        if stats["avg_chunk_size"] < 200:
            recommendations.append("平均分块大小过小，建议增加分块大小以提升性能")

        if stats["avg_chunk_size"] > 800:
            recommendations.append("平均分块大小过大，建议减小分块大小以提升精度")

        if stats["gaps"] > 0:
            recommendations.append("分块间存在间隔，可能丢失内容，请检查分块算法")

        return recommendations

    def get_chunking_stats(self) -> Dict[str, Any]:
        """获取分块服务统计信息

        Returns:
            Dict[str, Any]: 统计信息
        """
        return {
            "default_chunk_size": self.default_chunk_size,
            "default_overlap": self.default_overlap,
            "supported_strategies": [
                "500+50",
                "300+30",
                "800+80",
                "1000+100"
            ],
            "paragraph_separators_count": len(self.paragraph_separators)
        }


# 创建全局分块服务实例
_chunk_service: Optional[ChunkService] = None


def get_chunk_service() -> ChunkService:
    """获取分块服务实例"""
    global _chunk_service
    if _chunk_service is None:
        _chunk_service = ChunkService()
    return _chunk_service


def reload_chunk_service(chunk_size: int = 500, overlap: int = 50):
    """重新加载分块服务"""
    global _chunk_service
    _chunk_service = ChunkService(chunk_size, overlap)