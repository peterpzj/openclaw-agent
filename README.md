# openclaw-agent
Agent 开发框架 - 用于快速构建和部署 AI Agent

## 项目结构

```
openclaw-agent/
├── agents/                    # Agent 实例定义
│   ├── base.py               # Agent 基类
│   ├── ppt_agent.py          # PPT Agent V1（基础版）
│   ├── ppt_agent_v2.py       # PPT Agent V2（三节点架构）⭐
│   └── ppt_workflow.py       # 工作流运行器
├── core/                     # 核心引擎
│   ├── engine.py             # 模型调用引擎
│   ├── memory.py             # 记忆管理
│   └── planner.py            # 任务规划器
├── tools/                    # 工具集
│   ├── base.py               # 工具基类
│   └── web_search.py         # 网络搜索工具
├── prompts/                  # Prompt 模板
│   └── templates.py          # Prompt 模板管理
├── examples/                 # 示例 Agent
│   └── qa_agent.py           # 问答助手示例
└── docs/                     # 文档
    └── DEVELOPMENT.md        # 开发指南
```

---

## 核心架构：三节点工作流

PPT Agent V2 采用**三阶段独立节点**设计，每个阶段有独立的 System Prompt 和 Temperature：

```
┌─────────────────────────────────────────────────────────────────┐
│                    PPT 工作流（三节点架构）                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ The Analyst  │ →  │   The        │ →  │   The        │      │
│  │ 内容提炼节点  │    │   Director   │    │   Designer   │      │
│  │              │    │   大纲构建节点 │    │   幻灯片生成  │      │
│  │              │    │              │    │              │      │
│  │ Temp: 0.15   │    │  Temp: 0.30  │    │  Temp: 0.65  │      │
│  │ 低温·严谨    │    │  结构化输出   │    │  流畅·自然   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         ↓                  ↓                   ↓               │
│    提炼核心成就         规划幻灯片结构        逐字稿+视觉建议       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 节点详解

| 节点 | 职责 | Temperature | 关键原则 |
|------|------|-------------|----------|
| **The Analyst** | 阅读源文档，提炼核心成就 | 0.15 | 严格基于上下文，不捏造 |
| **The Director** | 构建演示大纲 | 0.30 | 金字塔原理，逻辑递进 |
| **The Designer** | 生成幻灯片内容 | 0.65 | 字不如表，表不如图 |

---

## 快速开始

### 运行完整工作流

```python
from agents.ppt_workflow import PPTWorkflowRunner

runner = PPTWorkflowRunner()

result = runner.run_with_source(
    topic="2024年度工作述职报告",
    source_material="""
    【成就概述】
    1. 门诊流程优化：等待时间从45分钟降至18分钟
    2. 日间化疗扩展：服务能力提升40%
    3. 质控体系：不良事件下降62%
    """,
    num_achievements=3,
    output_file="/tmp/result.json"
)
```

### 独立运行各阶段（调试用）

```python
from agents.ppt_agent_v2 import AnalystNode, DirectorNode, DesignerNode
from core.engine import AgentEngine

engine = AgentEngine()

# Stage 1: 分析提炼
analyst = AnalystNode(engine)
analysis = analyst.extract(source_material="...", topic="述职报告", num_achievements=3)

# Stage 2: 大纲构建
director = DirectorNode(engine)
outline = director.build_outline(analysis=analysis, topic="述职报告")

# Stage 3: 幻灯片生成
designer = DesignerNode(engine)
slides = designer.generate_slides(outline=outline, analysis=analysis, topic="述职报告")
```

---

## 输出结构

```json
{
  "topic": "演示主题",
  "stages": {
    "analysis": {
      "achievements": [
        {
          "name": "成就名称",
          "challenge": "痛点",
          "solution": "方案",
          "result": "结果"
        }
      ],
      "key_themes": ["主题1", "主题2"]
    },
    "outline": {
      "presentation_title": "标题",
      "subtitle": "副标题",
      "slides": [
        {
          "slide_number": 1,
          "slide_type": "Title Slide",
          "title": "页面标题",
          "core_purpose": "核心目的"
        }
      ]
    },
    "slides": [
      {
        "slide_number": 1,
        "title": "主标题",
        "bullet_points": ["要点1", "要点2"],
        "visual_suggestion": "视觉建议：配图、配色等",
        "speaker_notes": "口语化逐字稿"
      }
    ]
  }
}
```

---

## 工程建议（来自最佳实践）

### Temperature 设置

| 阶段 | Temperature | 原因 |
|------|-------------|------|
| 内容提炼 | 0.10 - 0.20 | 保证事实严谨性 |
| 大纲构建 | 0.25 - 0.35 | 适度创意 |
| 幻灯片生成 | 0.60 - 0.70 | 语言流畅自然 |

### 防幻觉

每个 System Prompt 都包含：
> "如果你在源材料中找不到足够的信息来支撑某个要点，请在要点中标注【需要人工补充】，绝对不要自行编造事实。"

### 结构化输出

所有阶段都使用 **JSON Schema** 约束输出，确保代码可解析。

---

## 依赖

- Python 3.8+
- Node.js + pptxgenjs（用于最终PPT渲染）
- OpenAI API Key / Claude API Key（用于模型调用）

```bash
npm install -g pptxgenjs
```
