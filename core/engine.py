"""
Agent 执行引擎 - MiniMax 版本
"""
import os
import json
from typing import Dict, Any, Optional, List, Callable
import requests


# MiniMax API 配置
MINIMAX_API_KEY = "sk-cp-DedXYoutQtQyt-8PklSoeNfBoT5-dVagBUrNy07QLBwFDVEmHMjhLgJ7TDJoqUXXEIoHTUm4dGSKwq1pQcLdEUvp7ArIBRQtvycq-pdpPNYM6xf4TmrT-JY"
MINIMAX_BASE_URL = "https://api.minimaxi.com/anthropic"


class AgentEngine:
    """Agent 执行引擎 - MiniMax 版本"""

    def __init__(
        self,
        model: str = "MiniMax-M2.7",
        temperature: float = 0.3,
        max_tokens: int = 4096,
        **kwargs
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.kwargs = kwargs

        self._tools: Dict[str, Callable] = {}

    def _make_request(self, messages: List[Dict], temperature: float = None) -> Dict:
        """发送请求到 MiniMax API"""
        url = f"{MINIMAX_BASE_URL}/v1/messages"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "x-api-key": MINIMAX_API_KEY
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": temperature or self.temperature
        }

        response = requests.post(url, headers=headers, json=payload, timeout=120)
        return response.json()

    def _extract_content(self, result: Dict) -> str:
        """从 MiniMax 响应中提取内容"""
        if "content" in result:
            contents = result["content"]
            if isinstance(contents, list):
                # 可能有 thinking + text 两种内容
                text_parts = []
                for item in contents:
                    if item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                    elif item.get("type") == "thinking":
                        # 跳过推理过程，只在 debug 时使用
                        pass
                return "\n".join(text_parts)
            return str(contents)
        elif "error" in result:
            return f"[Error: {result.get('error', {}).get('message', str(result))}]"
        return str(result)

    def register_tool(self, name: str, func: Callable, description: str = "") -> None:
        """注册工具"""
        self._tools[name] = func

    def call(self, prompt: str, **kwargs) -> str:
        """调用模型"""
        messages = [{"role": "user", "content": prompt}]
        try:
            result = self._make_request(messages, kwargs.get("temperature"))
            return self._extract_content(result)
        except Exception as e:
            return f"[Error: {str(e)}]"

    def chat(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        tools: Optional[List[Dict]] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """对话接口"""
        # 构造完整消息
        full_messages = []

        if system:
            full_messages.append({"role": "system", "content": system})

        for msg in messages:
            if isinstance(msg, dict):
                full_messages.append(msg)
            elif isinstance(msg, str):
                full_messages.append({"role": "user", "content": msg})

        try:
            result = self._make_request(full_messages, temperature)
            content = self._extract_content(result)

            return {
                "content": content,
                "role": "assistant",
                "tool_calls": None
            }

        except Exception as e:
            return {
                "content": f"[Error: {str(e)}]",
                "role": "assistant",
                "tool_calls": None
            }

    def __repr__(self) -> str:
        return f"<AgentEngine model={self.model}>"
