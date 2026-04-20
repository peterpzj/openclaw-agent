# openclaw-agent

> AI Agent 开发框架 - 专注于 Skill 开发

## 目录结构

```
openclaw-agent/
└── skills/
    └── pp-ppt-skill/     # PPT 制作技能 v5.0
        ├── SKILL.md      # 技能定义
        ├── _meta.json    # Cherry Studio 安装标识
        ├── scripts/
        │   └── create_ppt.py  # 三节点工作流脚本
        └── references/
            ├── slide-types.md   # 幻灯片类型参考
            └── design-guide.md  # 设计规范
```

## 核心技能

### pp-ppt-skill

AI 驱动的专业 PPT 制作技能，基于三节点工作流（Analyst → Director → Designer）。

**触发词：** 制作PPT、述职报告、学术汇报、项目汇报、工作汇报、成果展示...

**特点：**
- 三节点工作流：内容提炼 → 大纲构建 → 幻灯片生成
- 卡片式框架：三列布局（背景/痛点 | 方案/创新 | 成果/影响）
- 输出标准 PPTX 文件（PptxGenJS）

**安装（Cherry Studio）：**
```bash
npx skills add https://github.com/peterpzj/openclaw-agent
```

**安装（OpenClaw）：**
自动识别 `skills/` 目录下的 skill

## 技术栈

- **Python 3** - 核心脚本
- **PptxGenJS** - PPTX 文件生成
- **MiniMax API** - AI 模型调用

## 依赖

```bash
pip install markitdown python-pptx
npm install -g pptxgenjs
```
