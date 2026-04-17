"""
Memory - Agent 记忆管理
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class Memory:
    """Agent 记忆模块"""

    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self._memories: List[Dict[str, Any]] = []

    def add(self, task: str, result: Dict[str, Any]) -> None:
        """添加记忆"""
        memory = {
            "task": task,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self._memories.append(memory)

        # 限制记忆长度
        if len(self._memories) > self.max_size:
            self._memories = self._memories[-self.max_size:]

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        检索相关记忆
        简单实现：基于关键词匹配
        """
        query_words = set(query.lower().split())
        scored = []

        for mem in self._memories:
            score = 0
            mem_text = (mem.get("task", "") + " " + json.dumps(mem.get("result", ""))).lower()
            for word in query_words:
                if word in mem_text:
                    score += 1
            if score > 0:
                scored.append((score, mem))

        # 排序返回 top_k
        scored.sort(key=lambda x: x[0], reverse=True)
        return [mem for _, mem in scored[:top_k]]

    def clear(self) -> None:
        """清空记忆"""
        self._memories = []

    def all(self) -> List[Dict[str, Any]]:
        """获取所有记忆"""
        return self._memories.copy()

    def __len__(self) -> int:
        return len(self._memories)
