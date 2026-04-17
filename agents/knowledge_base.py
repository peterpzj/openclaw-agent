"""
知识库管理器 - 简化版
不依赖 ChromaDB，使用关键词匹配
文件存储 → 解析 → 索引 → 检索
"""
import os
import json
import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class Document:
    """知识库文档"""
    doc_id: str
    filename: str
    file_type: str
    content: str
    content_preview: str
    uploaded_at: str
    tags: List[str]
    char_count: int
    keywords: List[str]  # 提取的关键词

    def to_dict(self) -> Dict:
        return asdict(self)


class KnowledgeBase:
    """
    知识库管理器 - 简化版
    使用关键词索引，支持语义检索
    """

    def __init__(self, base_path: str = "/root/openclaw-agent/knowledge_base"):
        self.base_path = Path(base_path)
        self.documents_dir = self.base_path / "documents"
        self.metadata_file = self.base_path / "metadata.json"

        # 创建目录
        self.documents_dir.mkdir(parents=True, exist_ok=True)

        # 加载已有元数据
        self.metadata = self._load_metadata()

        # 关键词权重
        self.stop_words = set([
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
            '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
            '自己', '这', '那', '什么', '怎么', '为', '什么', '可以', '这个', '那个'
        ])

    def _load_metadata(self) -> Dict[str, Any]:
        """加载元数据"""
        if self.metadata_file.exists():
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"documents": [], "total_chars": 0}

    def _save_metadata(self):
        """保存元数据"""
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def _generate_id(self, content: str) -> str:
        """生成文档 ID"""
        return hashlib.md5(content[:500].encode()).hexdigest()[:16]

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 分词（简单基于空格和标点）
        words = re.findall(r'[\w]+', text.lower())

        # 过滤停用词，统计词频
        word_freq = {}
        for word in words:
            if len(word) >= 2 and word not in self.stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

        # 按频率排序，取前50个
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [w for w, _ in sorted_words[:50]]

    def _calculate_relevance(self, keywords: List[str], query_keywords: List[str]) -> float:
        """计算相关性分数"""
        if not keywords or not query_keywords:
            return 0

        match_count = sum(1 for qk in query_keywords if qk in keywords)
        return match_count / len(query_keywords)

    def add_document(
        self,
        filename: str,
        content: str,
        file_type: str = "text",
        tags: Optional[List[str]] = None
    ) -> Document:
        """
        添加文档到知识库
        """
        doc_id = self._generate_id(content)
        tags = tags or []

        # 提取关键词
        keywords = self._extract_keywords(content)

        # 检查是否已存在
        existing = next(
            (d for d in self.metadata["documents"] if d["doc_id"] == doc_id),
            None
        )

        if existing:
            # 更新
            existing["uploaded_at"] = datetime.now().isoformat()
            existing["char_count"] = len(content)
            existing["tags"] = tags
        else:
            # 新增
            doc_data = {
                "doc_id": doc_id,
                "filename": filename,
                "file_type": file_type,
                "content_preview": content[:500],
                "uploaded_at": datetime.now().isoformat(),
                "tags": tags,
                "char_count": len(content),
                "keywords": keywords
            }
            self.metadata["documents"].append(doc_data)
            self.metadata["total_chars"] = self.metadata.get("total_chars", 0) + len(content)

            # 保存内容到文件
            content_file = self.documents_dir / f"{doc_id}.txt"
            with open(content_file, "w", encoding="utf-8") as f:
                f.write(content)

        self._save_metadata()

        return Document(
            doc_id=doc_id,
            filename=filename,
            file_type=file_type,
            content=content,
            content_preview=content[:500],
            uploaded_at=datetime.now().isoformat(),
            tags=tags,
            char_count=len(content),
            keywords=keywords
        )

    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        检索相关文档
        基于关键词匹配
        """
        # 提取查询关键词
        query_keywords = self._extract_keywords(query)

        results = []
        for doc in self.metadata["documents"]:
            # 计算相关性
            doc_keywords = doc.get("keywords", [])
            relevance = self._calculate_relevance(doc_keywords, query_keywords)

            # 也检查内容是否包含查询词
            content_file = self.documents_dir / f"{doc['doc_id']}.txt"
            if content_file.exists():
                with open(content_file, "r", encoding="utf-8") as f:
                    full_content = f.read()
                    # 检查查询词在内容中的出现次数
                    query_lower = query.lower()
                    content_lower = full_content.lower()
                    match_count = content_lower.count(query_lower)
                    if match_count > 0:
                        relevance = max(relevance, min(1.0, match_count / 10))

            if relevance > 0:
                doc_copy = doc.copy()
                doc_copy["relevance_score"] = relevance
                results.append(doc_copy)

        # 按相关性排序
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

        return results[:top_k]

    def get_context(self, query: str, max_chars: int = 80000) -> str:
        """
        获取检索到的上下文
        合并为可发送给 LLM 的字符串
        """
        results = self.search(query, top_k=10)

        context_parts = []
        total_chars = 0

        context_parts.append("=" * 60)
        context_parts.append("【知识库内容】")
        context_parts.append(f"检索到 {len(results)} 个相关文档")
        context_parts.append("=" * 60)

        for doc in results:
            if total_chars >= max_chars:
                break

            content_file = self.documents_dir / f"{doc['doc_id']}.txt"
            if not content_file.exists():
                continue

            with open(content_file, "r", encoding="utf-8") as f:
                full_content = f.read()

            # 截断以控制长度
            remaining = max_chars - total_chars
            if len(full_content) > remaining:
                full_content = full_content[:remaining] + "\n...[内容截断]"

            context_parts.append("")
            context_parts.append("-" * 40)
            context_parts.append(f"📄 {doc['filename']} ({doc['file_type']})")
            context_parts.append(f"上传时间: {doc['uploaded_at']}")
            context_parts.append(f"相关度: {doc.get('relevance_score', 0):.2f}")
            context_parts.append("")
            context_parts.append(full_content)
            total_chars += len(full_content)

        context_parts.append("")
        context_parts.append("=" * 60)
        context_parts.append("【知识库内容结束】")
        context_parts.append("=" * 60)

        return "\n".join(context_parts)

    def list_documents(self) -> List[Dict[str, Any]]:
        """列出所有文档"""
        return self.metadata["documents"]

    def delete_document(self, doc_id: str) -> bool:
        """删除文档"""
        try:
            # 删除文件
            content_file = self.documents_dir / f"{doc_id}.txt"
            if content_file.exists():
                content_file.unlink()

            # 从元数据删除
            self.metadata["documents"] = [
                d for d in self.metadata["documents"] if d["doc_id"] != doc_id
            ]
            self._save_metadata()
            return True
        except:
            return False

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_documents": len(self.metadata["documents"]),
            "total_chars": self.metadata.get("total_chars", 0),
            "file_types": list(set(d.get("file_type", "") for d in self.metadata["documents"]))
        }


# 全局知识库实例
kb = KnowledgeBase()


def get_knowledge_base() -> KnowledgeBase:
    """获取知识库实例"""
    return kb
