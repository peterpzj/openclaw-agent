# Agent 开发指南

## 架构概览

```
┌─────────────────────────────────────────┐
│               BaseAgent                  │
│  (定义 Agent 行为: think/run/add_tool)  │
└──────────────┬──────────────────────────┘
               │
       ┌───────┼───────┐
       ▼       ▼       ▼
┌─────────┐┌─────────┐┌──────────┐
│ Engine  ││ Memory  ││ Planner  │
│ 模型调用││ 记忆管理││ 任务规划 │
└─────────┘└─────────┘└──────────┘
               │
               ▼
         ┌───────────┐
         │   Tools   │
         │  工具集   │
         └───────────┘
```

## 开发步骤

### 1. 创建 Agent

```python
from agents.base import BaseAgent
from core.engine import AgentEngine

class MyAgent(BaseAgent):
    def think(self, task: str, context: Dict) -> Dict:
        # 你的 Agent 逻辑
        return {"response": f"处理了: {task}"}

# 使用
engine = AgentEngine(model="gpt-4")
agent = MyAgent(name="我的Agent", engine=engine)
result = agent.run("Hello!")
```

### 2. 注册工具

```python
from tools.base import BaseTool, ToolResult

class MyTool(BaseTool):
    name = "my_tool"
    description = "我的工具"
    parameters = {
        "required": ["input"],
        "properties": {
            "input": {"type": "string", "description": "输入"}
        }
    }

    def execute(self, **kwargs) -> ToolResult:
        result = kwargs["input"].upper()
        return ToolResult(success=True, data=result)

# 注册
agent.add_tool(MyTool())
```

### 3. 配置 Prompt

```python
from prompts.templates import get_template

template = get_template("agent_system")
prompt = template.render(
    agent_name="我的Agent",
    role_description="助手",
    capabilities="- 问答\n- 写作",
    current_time="2024-01-01"
)
```

## 示例 Agent

见 `examples/` 目录（可自行添加）

## 测试

```bash
cd tests
python -m pytest
```

## 部署

待补充：容器化部署方案
