"""
Base Tool - 工具基类
所有工具都应继承此类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseTool(ABC):
    """工具基类"""

    name: str = ""           # 工具名称
    description: str = ""    # 工具描述
    parameters: Dict[str, Any] = {}  # 参数定义

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行工具 - 子类必须实现
        """
        pass

    def validate(self, **kwargs) -> bool:
        """
        验证参数是否合法
        """
        required = self.parameters.get("required", [])
        for param in required:
            if param not in kwargs:
                raise ValueError(f"Missing required parameter: {param}")
        return True

    def get_schema(self) -> Dict[str, Any]:
        """获取工具的 JSON Schema"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

    def __repr__(self) -> str:
        return f"<Tool: {self.name}>"


class ToolResult:
    """工具执行结果"""

    def __init__(
        self,
        success: bool,
        data: Any = None,
        error: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.success = success
        self.data = data
        self.error = error
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata
        }

    def __repr__(self) -> str:
        if self.success:
            return f"<ToolResult success=True data={self.data}>"
        return f"<ToolResult success=False error={self.error}>"
