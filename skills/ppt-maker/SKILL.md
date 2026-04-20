---
name: ppt-maker
description: "AI驱动的专业PPT制作技能。基于三节点工作流（内容提炼→大纲构建→幻灯片生成），支持述职报告、学术汇报、工作汇报等场景。通过卡片式框架生成结构清晰的演示文稿，输出标准PPTX文件。触发词：制作PPT、创建幻灯片、做PPT、述职报告、工作汇报、学术答辩、项目汇报、成果展示、演示文稿、PPT模板、生成PPT、帮我做PPT、把内容做成PPT。"
license: MIT
metadata:
  version: "5.0.0"
  category: productivity
  author: "小胖 AI 助手"
  language: "zh-CN"
  sources:
    - https://github.com/peterpzj/openclaw-agent
---

# 🎴 PPT Maker - 智能幻灯片制作技能 v5.0

基于三节点工作流的 AI PPT 生成系统，支持 36 种主题 + 14 种模板，可生成专业级述职/汇报/学术演示文稿。

## 核心能力

1. **三节点工作流** — Analyst（内容提炼）→ Director（大纲构建）→ Designer（幻灯片生成）
2. **卡片式框架** — 三列卡片布局（背景/痛点 | 方案/创新 | 成果/影响）
3. **多场景支持** — 述职报告、学术答辩、项目汇报、成果展示
4. **36 主题 + 14 模板** — 涵盖商务、学术、科技、小红书等风格
5. **输出标准 PPTX** — 使用 PptxGenJS 生成可编辑的 .pptx 文件

## 触发词（Keywords）

当用户说以下内容时激活此技能：
- "制作PPT"、"创建幻灯片"、"做PPT"、"帮我做PPT"
- "述职报告"、"述职PPT"、"工作述职"
- "学术汇报"、"学术答辩"、"论文答辩"
- "项目汇报"、"项目述职"、"工作汇报"
- "成果展示"、"展示PPT"、"演示文稿"
- "PPT模板"、"生成PPT"、"把内容做成PPT"
- "做一份演示稿"、"做一份slides"

## 工作流程

```
用户输入主题/材料
       ↓
┌─────────────────────────────┐
│  Stage 1: The Analyst       │
│  内容提炼（低温 0.15）       │
│  - 提取核心成就             │
│  - 识别关键主题             │
│  - 评估证据质量             │
└─────────────────────────────┘
       ↓
┌─────────────────────────────┐
│  Stage 2: The Director      │
│  大纲构建（中温 0.30）       │
│  - 规划幻灯片结构           │
│  - 确定页面类型             │
│  - 设计逻辑流程             │
└─────────────────────────────┘
       ↓
┌─────────────────────────────┐
│  Stage 3: The Designer      │
│  幻灯片生成（高温 0.65）     │
│  - 生成卡片内容             │
│  - 编写演讲逐字稿           │
│  - 提供视觉建议             │
└─────────────────────────────┘
       ↓
   生成 .pptx 文件
```

## 快速使用

### 方式一：自然语言触发（推荐）

```
用户：帮我做一份述职报告
助手：请提供你的工作材料或主要成就，我来帮你生成专业PPT。

用户：（粘贴材料）
助手：收到！正在为你生成述职报告PPT...
（自动执行三节点工作流）
```

### 方式二：直接指定主题

```bash
# 基本用法
python3 /root/.openclaw/workspace/skills/ppt-maker/scripts/create_ppt.py \
  --title "2024年度工作述职" \
  --slides "封面|目录|背景介绍|核心成就1|核心成就2|核心成就3|总结|致谢" \
  --style professional

# 指定主题配色
python3 /root/.openclaw/workspace/skills/ppt-maker/scripts/create_ppt.py \
  --title "项目汇报" \
  --slides "项目背景|技术方案|实施成果|总结" \
  --theme blue \
  --output /tmp/project_report.pptx
```

## 脚本参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--title` | PPT标题 | `"2024年度工作述职"` |
| `--slides` | 幻灯片内容，用`\|`分隔 | `"封面\|目录\|内容\|总结"` |
| `--style` | 风格：professional/medical/education/minimalist/modern | `professional` |
| `--theme` | 主题配色：blue/green/purple/orange/custom | `blue` |
| `--output` | 输出文件路径 | `"/tmp/output.pptx"` |
| `--layout` | 布局模式 | 详见下方 |

### 支持的布局模式

| 布局 | 说明 |
|------|------|
| `three_column` | 三列卡片（成果展示专用） |
| `cover` | 封面 |
| `toc` | 目录 |
| `content` | 标准内容页 |
| `summary` | 总结页 |
| `thank_you` | 致谢页 |

## 三列卡片布局（成果展示页）

每项核心成果使用三列卡片展示：

```
┌─────────────────┬─────────────────┬─────────────────┐
│   🟠 背景/痛点   │   🔵 方案/创新   │   🟢 成果/影响   │
│                 │                 │                 │
│  原有流程等待    │  引入智能预约    │  等待时间缩短    │
│  时间超过45分钟  │  系统+诊间结算  │  至18分钟        │
│                 │                 │                 │
│  患者满意度仅68分│                 │  满意度提升至92分 │
└─────────────────┴─────────────────┴─────────────────┘
```

### 卡片类型说明

| 类型 | 用途 | 关键字段 |
|------|------|----------|
| `pain_point` | 背景/痛点 | header, body_text, visual_placeholder |
| `innovation` | 方案/创新 | header, body_text, visual_placeholder |
| `metric` | 成果/量化 | header, body_text, visual_placeholder |

## 主题配色

### 内置主题（36种）

| 主题 | 风格 | 适用场景 |
|------|------|----------|
| professional | 商务蓝 | 企业汇报、述职 |
| medical | 医疗绿 | 医疗健康主题 |
| education | 学术橙 | 教育培训 |
| minimalist | 简约灰 | 极简风格 |
| modern | 科技紫 | 科技感演示 |
| ... | ... | ... |

详细 36 种主题列表见 [references/themes.md](references/themes.md)

### 配色规范

```
主色系：
- 蓝色系: #1F5C99, #2E7D32, #1565C0
- 绿色系: #2E8B57, #43A047, #388E3C  
- 橙色系: #FF8F00, #F57C00, #E65100
- 紫色系: #7B1FA2, #9C27B0, #6A1B9A

背景色：
- 浅色: #FFFFFF, #F5F5F5, #FAFAFA
- 深色: #263238, #37474F, #1A1A2E
```

## 场景化模板（14种）

| 模板 | 适用场景 |
|------|----------|
| `pitch-deck` | 融资路演 |
| `product-launch` | 产品发布 |
| `tech-sharing` | 技术分享 |
| `weekly-report` | 周报/月报 |
| `academic-defense` | 学术答辩 |
| `project-review` | 项目述职 |
| `achievement-report` | 成果汇报 |
| `xhs-post` | 小红书图文 |

详细模板说明见 [references/templates.md](references/templates.md)

## 输出文件

```
/tmp/
└── ppt-maker/
    ├── slide-01.js      # 每页幻灯片模块
    ├── slide-02.js
    ├── ...
    ├── compile.js       # 编译脚本
    └── output/
        └── presentation.pptx   # 最终文件
```

## 设计规范

### 字体

| 用途 | 中文字体 | 英文字体 |
|------|----------|----------|
| 标题 | Microsoft YaHei | Arial |
| 正文 | Microsoft YaHei | Arial |
| 强调 | Microsoft YaHei Bold | Arial Bold |

### 尺寸

- 标准尺寸：10" x 5.625" (16:9)
- 页码位置：x: 9.3", y: 5.1"

### 颜色格式

- PptxGenJS 使用 6 位十六进制，不带 `#`
- 例如：`"FF0000"` 表示红色

## 依赖安装

```bash
# Python 依赖
pip install markitdown python-pptx

# Node.js 依赖（必需）
npm install -g pptxgenjs

# 验证安装
node -e "require('pptxgenjs'); console.log('OK')"
```

## 参考文档

| 文件 | 内容 |
|------|------|
| [references/slide-types.md](references/slide-types.md) | 5种幻灯片类型详解 |
| [references/design-system.md](references/design-system.md) | 配色系统、字体规范 |
| [references/templates.md](references/templates.md) | 14种场景模板 |
| [references/pptxgenjs-api.md](references/pptxgenjs-api.md) | PptxGenJS API 参考 |

## 常见问题

**Q: 生成的PPT打不开？**
A: 确保已安装 `pptxgenjs`，运行 `npm install -g pptxgenjs`

**Q: 中文显示乱码？**
A: 确保使用 `Microsoft YaHei` 字体，并安装中文字体

**Q: 如何修改已有PPT？**
A: 使用 `python -m markitdown` 提取内容后重新生成

---

*PPT Maker v5.0 - 基于三节点工作流的智能PPT生成系统*
*GitHub: https://github.com/peterpzj/openclaw-agent*
