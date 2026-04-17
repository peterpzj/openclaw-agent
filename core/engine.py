"""
Agent 执行引擎
负责模型调用、工具执行、响应解析
"""
from typing import Dict, Any, Optional, List, Callable
import json


class AgentEngine:
    """Agent 执行引擎"""

    def __init__(
        self,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.kwargs = kwargs
        self._tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable, description: str = "") -> None:
        """注册工具"""
        self._tools[name] = func

    def call(self, prompt: str, **kwargs) -> str:
        """
        调用模型 - 目前是占位符
        实际使用时替换为 OpenAI / Claude / 本地模型等
        """
        # TODO: 接入实际模型
        return f"[模拟响应] 已收到任务: {prompt[:50]}..."

    def chat(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        对话接口
        """
        # 构造完整消息
        full_messages = []
        if system:
            full_messages.append({"role": "system", "content": system})

        for msg in messages:
            if isinstance(msg, dict):
                full_messages.append(msg)
            elif isinstance(msg, str):
                full_messages.append({"role": "user", "content": msg})

        # 调用模型
        response = self.call(
            prompt=full_messages[-1]["content"] if full_messages else "",
            **kwargs
        )

        return {
            "content": response,
            "role": "assistant",
            "tool_calls": None
        }

    def __repr__(self) -> str:
        return f"<AgentEngine model={self.model}>"
