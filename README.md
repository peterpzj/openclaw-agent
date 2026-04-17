# openclaw-agent
Agent 开发框架 - 用于快速构建和部署 AI Agent

## 项目结构

```
openclaw-agent/
├── agents/          # Agent 实例定义
│   └── base.py      # Agent 基类
├── core/            # 核心引擎
│   ├── engine.py    # Agent 执行引擎
│   ├── memory.py    # 记忆管理
│   └── planner.py   # 任务规划器
├── tools/           # 工具集
│   └── base.py      # 工具基类
├── prompts/         # Prompt 模板
│   └── templates.py # Prompt 模板管理
├── scripts/         # 脚本和工具
├── tests/           # 单元测试
└── docs/            # 文档
```

## 快速开始

```bash
# 创建 Agent
from agents.base import BaseAgent
from core.engine import AgentEngine

# 初始化引擎
engine = AgentEngine()

# 创建 Agent
agent = BaseAgent(name="MyAgent", engine=engine)

# 运行
result = agent.run("你的任务描述")
```

## 开发流程

1. **定义 Agent** - 继承 `BaseAgent`
2. **注册工具** - 在 `tools/` 中添加工具
3. **配置 Prompt** - 在 `prompts/` 中管理模板
4. **测试部署** - 在 `tests/` 中编写测试

## 开发文档

详见 `docs/DEVELOPMENT.md`
