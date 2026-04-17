"""
Prompt 模板管理
"""
from typing import Dict, Optional


class PromptTemplate:
    """Prompt 模板"""

    def __init__(
        self,
        template: str,
        name: str = "",
        description: str = "",
        variables: Optional[Dict[str, str]] = None
    ):
        self.template = template
        self.name = name
        self.description = description
        self.variables = variables or {}

    def render(self, **kwargs) -> str:
        """渲染模板"""
        result = self.template
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            result = result.replace(placeholder, str(value))
        return result

    def __repr__(self) -> str:
        return f"<PromptTemplate: {self.name or 'anonymous'}>"


# 预设模板
TEMPLATES: Dict[str, PromptTemplate] = {
    "agent_system": PromptTemplate(
        name="agent_system",
        description="Agent 系统提示词",
        template="""你是一个专业的 {agent_name}。
你的角色是：{role_description}

核心能力：
{capabilities}

当前时间：{current_time}

请根据用户需求，提供专业、高效的帮助。"""
    ),

    "task_decomposition": PromptTemplate(
        name="task_decomposition",
        description="任务分解提示词",
        template="""请将以下任务分解为可执行的子任务：

任务：{task}

要求：
1. 识别任务的关键步骤
2. 确定任务间的依赖关系
3. 估算每个子任务的难度

以列表形式输出每个子任务。"""
    ),

    "reasoning": PromptTemplate(
        name="reasoning",
        description="推理思考提示词",
        template="""请仔细思考以下问题：

问题：{question}

请按以下步骤推理：
1. 理解问题 - 明确目标和约束
2. 分析方案 - 列出可能的解决路径
3. 评估选项 - 权衡利弊
4. 给出结论 - 推荐最佳方案

你的推理过程："""
    ),

    "tool_call": PromptTemplate(
        name="tool_call",
        description="工具调用提示词",
        template="""你需要使用工具来完成以下任务：

任务：{task}

可用工具：
{available_tools}

请选择合适的工具并给出调用参数。

工具名称：{tool_name}
调用参数：{tool_args}

如果你认为不需要工具，请直接回答。"""
    )
}


def get_template(name: str) -> PromptTemplate:
    """获取模板"""
    return TEMPLATES.get(name, PromptTemplate(template=""))
