# openclaw-agent
Agent 开发框架 - 用于快速构建和部署 AI Agent

## 项目结构

```
openclaw-agent/
├── agents/              # Agent 实例定义
│   ├── base.py          # Agent 基类
│   └── ppt_agent.py     # PPT 生成 Agent ⭐
├── core/                # 核心引擎
│   ├── engine.py        # 模型调用引擎
│   ├── memory.py        # 记忆管理
│   └── planner.py       # 任务规划器
├── tools/               # 工具集
│   ├── base.py          # 工具基类
│   └── web_search.py    # 网络搜索工具
├── prompts/             # Prompt 模板
│   └── templates.py     # Prompt 模板管理
├── scripts/             # 脚本和工具
├── tests/               # 单元测试
├── examples/            # 示例 Agent
│   └── qa_agent.py      # 问答助手示例
└── docs/                # 文档
    └── DEVELOPMENT.md   # 开发指南
```

## 核心模块

### BaseAgent
所有 Agent 的基类，定义统一接口：
```python
class MyAgent(BaseAgent):
    def think(self, task: str, context: Dict) -> Dict:
        return {"result": "处理结果"}
```

### PPTAgent ⭐
**PPT 全自动生成 Agent**

工作流程：
```
输入主题 → 搜索内容 → 构建框架 → 生成 PPT
```

使用示例：
```python
from agents.ppt_agent import PPTAgent
from core.engine import AgentEngine

engine = AgentEngine()
agent = PPTAgent(engine=engine, output_dir="/tmp/my_ppt")

# 交互式生成
result = agent.run_interactive("人工智能在医疗领域的应用")
# 或
result = agent.run("人工智能在医疗领域的应用")
```

### WebSearchTool
网络搜索工具，支持多源搜索：
```python
from tools.web_search import get_search_tools

tools = get_search_tools()
for tool in tools:
    result = tool.execute(query="搜索关键词")
```

## 快速开始

### 1. 创建 Agent
```python
from agents.base import BaseAgent
from core.engine import AgentEngine

class MyAgent(BaseAgent):
    def think(self, task: str, context: Dict) -> Dict:
        return {"response": f"处理了: {task}"}

engine = AgentEngine()
agent = MyAgent(name="我的Agent", engine=engine)
result = agent.run("Hello!")
```

### 2. 使用 PPTAgent
```python
from agents.ppt_agent import PPTAgent
from core.engine import AgentEngine

agent = PPTAgent(engine=AgentEngine())
result = agent.run_interactive("你的 PPT 主题")
print(result["output_file"])  # 输出文件路径
```

### 3. 注册自定义工具
```python
from tools.base import BaseTool, ToolResult

class MyTool(BaseTool):
    name = "my_tool"
    description = "我的工具"
    parameters = {"required": ["input"]}

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(success=True, data=kwargs["input"])

agent.add_tool(MyTool())
```

## 开发文档

详见 `docs/DEVELOPMENT.md`

## 依赖

- Python 3.8+
- pptxgenjs (用于 PPT 生成)
- Node.js (用于编译 PPT)

安装依赖：
```bash
npm install -g pptxgenjs
```
