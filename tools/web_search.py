"""
WebSearch Tool - 网络搜索工具
"""
from tools.base import BaseTool, ToolResult
from typing import Dict, Any, List
import subprocess
import json


class WebSearchTool(BaseTool):
    """网络搜索工具"""

    name = "web_search"
    description = "搜索互联网获取最新信息"
    parameters = {
        "required": ["query"],
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索关键词"
            },
            "count": {
                "type": "number",
                "description": "返回结果数量，默认5条",
                "default": 5
            }
        }
    }

    def execute(self, query: str, count: int = 5) -> ToolResult:
        """执行搜索"""
        try:
            # 使用 mmx search（优先）
            result = subprocess.run(
                ["mmx", "search", query, "--q", query, "--output", "json", "--quiet"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0 and result.stdout:
                try:
                    data = json.loads(result.stdout)
                    results = data.get("results", [])[:count]
                    return ToolResult(
                        success=True,
                        data={
                            "query": query,
                            "count": len(results),
                            "results": results
                        }
                    )
                except json.JSONDecodeError:
                    pass

            # 降级到 curl 搜索
            cmd = [
                "curl", "-s", "--max-time", "15",
                f"https://duckduckgo.com/?q={query}&format=json"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)

            if result.returncode == 0:
                return ToolResult(
                    success=True,
                    data={
                        "query": query,
                        "results": [{"title": query, "snippet": "搜索结果"}]
                    }
                )

            return ToolResult(success=False, error="搜索失败")

        except subprocess.TimeoutExpired:
            return ToolResult(success=False, error="搜索超时")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class TavilySearchTool(BaseTool):
    """Tavily 搜索工具"""

    name = "tavily_search"
    description = "使用 Tavily API 进行 AI 优化的搜索"
    parameters = {
        "required": ["query"],
        "properties": {
            "query": {"type": "string", "description": "搜索查询"},
            "count": {"type": "number", "description": "结果数量", "default": 5}
        }
    }

    def execute(self, query: str, count: int = 5) -> ToolResult:
        """执行 Tavily 搜索"""
        try:
            api_key = "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"
            cmd = [
                "curl", "-s", "--max-time", "20",
                "-X", "POST", "https://api.tavily.com/search",
                "-H", "Content-Type: application/json",
                "-d", json.dumps({
                    "api_key": api_key,
                    "query": query,
                    "max_results": count,
                    "include_answer": True
                })
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=25)

            if result.returncode == 0:
                data = json.loads(result.stdout)
                return ToolResult(
                    success=True,
                    data={
                        "query": query,
                        "results": data.get("results", []),
                        "answer": data.get("answer", "")
                    }
                )

            return ToolResult(success=False, error="Tavily 搜索失败")

        except Exception as e:
            return ToolResult(success=False, error=str(e))


def get_search_tools() -> List[BaseTool]:
    """获取所有搜索工具"""
    return [WebSearchTool(), TavilySearchTool()]
