# openclaw-agent
Agent 开发框架 - 用于快速构建和部署 AI Agent

## 项目结构

```
openclaw-agent/
├── agents/                    # Agent 实例定义
│   ├── base.py               # Agent 基类
│   ├── ppt_agent.py          # PPT Agent V1（基础版）
│   ├── ppt_agent_v2.py       # PPT Agent V2（三节点架构）⭐
│   ├── ppt_workflow.py       # 工作流运行器
│   └── cards.py              # 卡片式框架核心 ⭐⭐
├── core/                     # 核心引擎
│   ├── engine.py             # 模型调用引擎
│   ├── memory.py             # 记忆管理
│   └── planner.py            # 任务规划器
├── tools/                    # 工具集
│   ├── base.py               # 工具基类
│   └── web_search.py         # 网络搜索工具
├── prompts/                  # Prompt 模板
│   └── templates.py          # Prompt 模板管理
├── app/                      # Web 前端
│   └── streamlit_app.py      # Streamlit 原型界面 ⭐
├── examples/                 # 示例 Agent
│   └── qa_agent.py           # 问答助手示例
└── docs/                     # 文档
    └── DEVELOPMENT.md        # 开发指南
```

---

## 核心架构

### 三节点工作流 (The Analyst → Director → Designer)

```
┌─────────────────────────────────────────────────────────────────┐
│                    PPT 工作流（三节点架构）                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ The Analyst  │ →  │   The        │ →  │   The        │      │
│  │ 内容提炼节点  │    │   Director   │    │   Designer   │      │
│  │              │    │   大纲构建节点 │    │   幻灯片生成  │      │
│  │ Temp: 0.15   │    │  Temp: 0.30  │    │  Temp: 0.65  │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 卡片式框架 (Card-Based Architecture)

```
┌─────────────────────────────────────────────────────────────────┐
│                    卡片式 PPT 生成架构                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│   │   Agent     │ →   │  Card JSON  │ →   │  Renderer   │      │
│   │  内容生成    │     │  结构化输出  │     │  渲染展示   │      │
│   └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                 │
│   Agent 负责"内容"          JSON Schema 约束          前端负责"布局"│
│   - 提炼核心成就            - 类型定义                                         │
│   - 生成要点                - 字段校验                - Streamlit 预览│
│   - 输出结构化 JSON         - 模板提示                - PPTX 导出   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 快速开始

### 1. 卡片式框架核心

```python
from agents.cards import CardSchema, CardRenderer, CardType

# 获取卡片类型定义
schema = CardSchema.get_schema()

# 获取各类卡片的 Prompt 模板
prompts = CardSchema.get_card_prompts()
print(prompts["data_point"])  # 数据点卡片生成提示

# 渲染卡片
renderer = CardRenderer()
card_data = {
    "type": "data_point",
    "title": "患者满意度",
    "metric_value": "92",
    "metric_unit": "分",
    "change": "+24"
}
rendered = renderer.render(card_data)
```

### 2. 三阶段工作流

```python
from agents.ppt_workflow import PPTWorkflowRunner

runner = PPTWorkflowRunner()
result = runner.run_with_source(
    topic="2024年度述职报告",
    source_material="""
    成就1：门诊优化
    - 等待时间从45分钟降至18分钟
    - 患者满意度从68分提升至92分

    成就2：日间化疗
    - 服务能力提升40%
    - 服务患者超2000人次
    """,
    num_achievements=3,
    output_file="/tmp/result.json"
)
```

### 3. 启动 Streamlit 原型

```bash
cd app
streamlit run streamlit_app.py
```

---

## 卡片类型参考

| 类型 | 用途 | 核心字段 |
|------|------|----------|
| `cover` | 封面 | title, subtitle, author, date |
| `toc` | 目录 | items[] |
| `bullet_list` | 要点列表 | title, bullets[] |
| `data_point` | 数据点 | metric_value, metric_unit, change |
| `before_after` | 对比卡片 | before_content, after_content |
| `timeline` | 时间线 | events[{time, event}] |
| `process_flow` | 流程图 | steps[{step, title, description}] |
| `quote` | 引言 | quote_text, author |
| `stats_card` | 统计组 | stats[{value, label, unit}] |
| `summary` | 总结 | key_points[], next_steps[] |
| `thank_you` | 致谢 | title, contact |

---

## 技术选型建议

### 为什么 Python + Streamlit？

1. **生态融合** - LLM SDK 对 Python 支持最完善
2. **开发效率** - 用纯 Python 写前端，快速验证逻辑
3. **PPT 导出** - python-pptx 无缝衔接

### 卡片 Schema 设计原则

```
┌─────────────────────────────────────────────┐
│           The Contract (契约设计)            │
├─────────────────────────────────────────────┤
│                                             │
│  ❌ 作文题 (自由生成，容易跑偏)                │
│     "请生成一页关于成就的幻灯片"               │
│                                             │
│  ✅ 填空题 (结构约束，质量稳定)                │
│     {                                       │
│       "type": "data_point",                 │
│       "metric_value": "92",                 │
│       "metric_unit": "分",                  │
│       "change": "+24"                       │
│     }                                       │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 工程建议

### Temperature 设置

| 阶段 | Temperature | 原因 |
|------|-------------|------|
| 内容提炼 | 0.10 - 0.20 | 保证事实严谨性 |
| 大纲构建 | 0.25 - 0.35 | 适度创意 |
| 幻灯片生成 | 0.60 - 0.70 | 语言流畅自然 |

### 防幻觉规则

每个 System Prompt 都包含：
> "如果你在源材料中找不到足够的信息来支撑某个要点，请在要点中标注【需要人工补充】，绝对不要自行编造事实。"

### JSON Schema 验证

使用 `jsonschema` 库验证 Agent 输出：
```python
from jsonschema import validate, ValidationError

validate(instance=card_data, schema=CardSchema.get_schema())
```

---

## 依赖安装

```bash
# Python 依赖
pip install -r requirements.txt

# Node.js 依赖（PPT 渲染用）
npm install -g pptxgenjs

# 启动 Streamlit
cd app && streamlit run streamlit_app.py
```
