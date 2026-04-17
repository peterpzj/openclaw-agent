"""
Base Agent - Agent 基类
所有 Agent 都应继承此类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from core.engine import AgentEngine
from core.memory import Memory
from core.planner import Planner


class BaseAgent(ABC):
    """Agent 基类"""

    def __init__(
        self,
        name: str,
        engine: AgentEngine,
        memory: Optional[Memory] = None,
        planner: Optional[Planner] = None,
        system_prompt: str = "",
        tools: Optional[List] = None,
        **kwargs
    ):
        self.name = name
        self.engine = engine
        self.memory = memory or Memory()
        self.planner = planner or Planner()
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.kwargs = kwargs

    @abstractmethod
    def think(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        核心思考逻辑 - 子类必须实现
        """
        pass

    def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        运行 Agent 处理任务
        """
        context = context or {}

        # 1. 记忆检索
        relevant_memories = self.memory.retrieve(task)
        context["memories"] = relevant_memories

        # 2. 任务规划
        plan = self.planner.plan(task)
        context["plan"] = plan

        # 3. 核心思考
        result = self.think(task, context)

        # 4. 记忆更新
        self.memory.add(task, result)

        return result

    def add_tool(self, tool) -> None:
        """注册工具"""
        self.tools.append(tool)

    def __repr__(self) -> str:
        return f"<Agent: {self.name}>"
