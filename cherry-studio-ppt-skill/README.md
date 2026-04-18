# Cherry Studio PPT 生成技能

让Cherry Studio智能体具备生成专业PPT的能力。

## 功能特点

- 🎯 智能识别PPT生成需求
- 📝 根据主题或资料自动生成PPT内容
- 🎨 支持多种风格和布局
- 💻 直接生成可编辑的 `.pptx` 文件

## 安装方法

### 方法一：从GitHub安装（推荐）

1. 打开Cherry Studio
2. 进入「智能体」页面
3. 点击右上角菜单 → 「导入技能」
4. 输入本仓库地址：
   ```
   https://github.com/peterpzj/cherry-studio-ppt-skill
   ```
5. 点击确认，等待安装完成

### 方法二：手动安装

1. 下载本仓库
2. 将 `.agents/skills/ppt-generator` 目录复制到Cherry Studio的对应目录：
   - Windows: `C:\Users\用户名\.cherrystudio\agents\skills\`
   - Mac/Linux: `~/.cherrystudio/agents/skills/`
3. 重启Cherry Studio

## 使用方法

1. 在Cherry Studio中创建一个新的智能体（Agent）
2. 启用「代码执行」工具权限
3. 在智能体的提示词中引用此技能：
   ```
   你是一个PPT生成专家。当用户请求生成PPT时，使用ppt-generator技能来帮助用户创建专业的演示文稿。
   ```
4. 开始对话，只需说：
   - "帮我生成一个关于XXX的PPT"
   - "制作一个介绍YYY的演示文稿"
   - "做PPT：主题是ZZZ"

## 技能工作原理

当检测到PPT相关关键词时，技能会：
1. 询问用户PPT的具体需求（主题、内容、风格）
2. 根据需要检索知识库或网络资料
3. 生成PPT内容并通过Python代码创建真实的`.pptx`文件
4. 提供文件下载

## 依赖要求

- Cherry Studio Agent模式
- 代码执行工具权限
- Python环境（内置）
- python-pptx库（首次使用自动安装）

## 示例输出

生成的PPT包含：
- 📄 封面页（标题 + 副标题）
- 📋 内容页（要点列表）
- 🙋 结束页（谢谢观看）

支持自定义：
- 页数
- 内容要点
- 文字大小和颜色
- 背景样式

## 文件结构

```
cherry-studio-ppt-skill/
└── .agents/
    └── skills/
        └── ppt-generator/
            └── SKILL.md    # 技能定义文件
```

## 反馈与支持

如有问题或建议，请在GitHub提交Issue。

## 更新日志

### v1.0.0 (2026-04-18)
- 初始版本
- 支持基础PPT生成功能
- 支持封面、内容页、结束页
- 支持自定义内容要点
