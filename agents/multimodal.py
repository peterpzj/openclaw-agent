"""
多模态融合器
将文本 + 图片描述整合为标准格式
用于超长上下文或向量检索
"""
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from agents.parsers import ParsedDocument, DocumentChunk


@dataclass
class ImageDescription:
    """图片描述"""
    chunk_id: str
    original_content: str  # 原始占位符
    description: str      # 多模态模型生成的描述
    suggested_placement: str = ""  # "achievement_slide", "background", "process_diagram"
    confidence: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "chunk_id": self.chunk_id,
            "original_content": self.original_content,
            "description": self.description,
            "suggested_placement": self.suggested_placement,
            "confidence": self.confidence
        }


@dataclass
class FusedDocument:
    """融合后的文档"""
    source_documents: List[str] = field(default_factory=list)  # 原始文件名列表
    text_content: str = ""
    image_descriptions: List[ImageDescription] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "source_documents": self.source_documents,
            "text_content": self.text_content,
            "image_descriptions": [img.to_dict() for img in self.image_descriptions],
            "metadata": self.metadata
        }

    def to_llm_string(self, include_images: bool = True) -> str:
        """
        转换为 LLM 可读的字符串格式
        用于直接喂给超长上下文
        """
        parts = []
        parts.append("=" * 60)
        parts.append("【融合文档】")
        parts.append("=" * 60)

        # 文本内容
        if self.text_content.strip():
            parts.append("")
            parts.append("【文本内容】")
            parts.append(self.text_content)

        # 图片描述
        if include_images and self.image_descriptions:
            parts.append("")
            parts.append("【图片描述】")
            for img in self.image_descriptions:
                parts.append(f"\n[图片: {img.chunk_id}]")
                parts.append(f"描述: {img.description}")
                if img.suggested_placement:
                    parts.append(f"建议用途: {img.suggested_placement}")

        return "\n".join(parts)


class MultimodalFusion:
    """
    多模态融合器
    核心功能：
    1. 整合文本和图片描述
    2. 生成适合 LLM 理解的标准化格式
    3. 支持向量检索用的元数据
    """

    def __init__(self):
        self.image_descriptions: List[ImageDescription] = []

    def fuse(
        self,
        documents: List[ParsedDocument],
        image_descriptions: Optional[List[ImageDescription]] = None
    ) -> FusedDocument:
        """
        融合多个文档
        """
        # 合并文本内容
        text_parts = []
        source_files = []
        image_chunks = []

        for doc in documents:
            source_files.append(doc.filename)
            if doc.full_text.strip():
                text_parts.append(f"[来源: {doc.filename}]\n{doc.full_text}")

            # 收集图片 chunks
            for chunk in doc.chunks:
                if chunk.chunk_type == "image":
                    image_chunks.append(chunk)

        # 创建融合文档
        fused = FusedDocument(
            source_documents=source_files,
            text_content="\n\n".join(text_parts),
            image_descriptions=image_descriptions or [],
            metadata={
                "document_count": len(documents),
                "total_characters": sum(len(t) for t in text_parts),
                "image_count": len(image_chunks)
            }
        )

        return fused

    def generate_image_descriptions(
        self,
        documents: List[ParsedDocument],
        vision_func: Callable[[str], str],
        batch_size: int = 5
    ) -> List[ImageDescription]:
        """
        生成图片描述

        Args:
            documents: 解析后的文档列表
            vision_func: 视觉模型调用函数，输入图片路径/Base64，返回描述文字
            batch_size: 批量处理大小

        Returns:
            图片描述列表
        """
        # 收集所有图片 chunks
        image_chunks = []
        for doc in documents:
            for chunk in doc.chunks:
                if chunk.chunk_type == "image":
                    image_chunks.append(chunk)

        descriptions = []

        # 批量处理
        for i in range(0, len(image_chunks), batch_size):
            batch = image_chunks[i:i + batch_size]

            for chunk in batch:
                try:
                    description = self._describe_image(chunk, vision_func)
                    descriptions.append(description)
                except Exception as e:
                    print(f"描述图片失败 {chunk.chunk_id}: {e}")

        self.image_descriptions = descriptions
        return descriptions

    def _describe_image(
        self,
        chunk: DocumentChunk,
        vision_func: Callable[[str], str]
    ) -> ImageDescription:
        """
        生成单张图片的描述
        """
        # 获取图片路径或 Base64
        image_path = chunk.source

        # 调用视觉模型
        raw_description = vision_func(image_path)

        # 解析描述，提取建议用途
        placement, description = self._parse_description(raw_description)

        return ImageDescription(
            chunk_id=chunk.chunk_id,
            original_content=chunk.content,
            description=description,
            suggested_placement=placement,
            confidence=0.8  # 简化处理
        )

    def _parse_description(self, raw: str) -> tuple:
        """
        解析原始描述，提取建议用途

        Returns:
            (suggested_placement, cleaned_description)
        """
        lines = raw.strip().split("\n")

        placement = ""
        description_lines = []

        placement_keywords = {
            "achievement_slide": ["成果", "效果", "展示", "result", "achievement"],
            "background": ["背景", "场景", "现场", "background", "context"],
            "process_diagram": ["流程", "步骤", "架构", "process", "flow", "diagram"],
            "data_chart": ["图表", "数据", "曲线", "chart", "graph", "data"],
            "team_photo": ["团队", "合影", "人员", "team", "people"]
        }

        for line in lines:
            line_lower = line.lower()

            # 检测是否包含用途关键词
            for ptype, keywords in placement_keywords.items():
                if any(kw in line_lower for kw in keywords):
                    placement = ptype
                    break

            description_lines.append(line)

        description = "\n".join(description_lines)
        return placement, description

    def to_context_string(
        self,
        fused: FusedDocument,
        include_images: bool = True
    ) -> str:
        """
        转换为上下文字符串
        直接喂给 LLM
        """
        return fused.to_llm_string(include_images=include_images)


class SimpleContextBuilder:
    """
    简单上下文构建器
    不使用向量数据库，直接用超长上下文
    """

    @staticmethod
    def build(
        text_content: str,
        image_descriptions: Optional[List[Dict]] = None,
        topic: str = "",
        num_achievements: int = 3
    ) -> str:
        """
        构建上下文字符串

        用于直接发给 LLM，不需要向量检索
        """
        parts = []
        parts.append("=" * 60)
        parts.append("【源材料】")
        parts.append("=" * 60)

        if topic:
            parts.append(f"\n主题: {topic}")

        if text_content:
            parts.append(f"\n{text_content}")

        if image_descriptions:
            parts.append("\n" + "-" * 40)
            parts.append("【图片内容】")
            for img in image_descriptions:
                parts.append(f"\n[图片描述] {img.get('description', '')}")
                if img.get('suggested_placement'):
                    parts.append(f"[建议用途] {img['suggested_placement']}")

        parts.append("\n" + "=" * 60)
        parts.append("【任务】")
        parts.append("=" * 60)
        parts.append(f"""
请根据以上材料，提炼 {num_achievements} 项代表性成果。

要求：
1. 每项成果包含：背景痛点、核心方案、可量化成果
2. 数据必须来自材料，不自行编造
3. 语言精炼，适合口头汇报
""")

        return "\n".join(parts)
