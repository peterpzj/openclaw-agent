# Cherry Studio PPT 生成技能 📊

让Cherry Studio智能体具备生成专业PPT的能力！

## 🎯 这个技能能做什么？

- 检测到"生成PPT"、"做PPT"等关键词时自动触发
- 根据你的主题或提供的资料生成PPT内容
- 通过Python代码直接生成`.pptx`文件
- 支持封面页、内容页、结束页

---

## 📥 安装步骤（超简单！）

### 第一步：下载技能文件

把本仓库下载到本地：
```bash
# 如果你有git
git clone https://github.com/peterpzj/cherry-studio-ppt-skill.git

# 或者直接下载ZIP包解压
```

### 第二步：复制到Cherry Studio目录

将以下文件夹：
```
.agents/skills/ppt-generator/
```
复制到Cherry Studio的用户数据目录：

| 系统 | 路径 |
|------|------|
| Windows | `C:\Users\你的用户名\.cherrystudio\agents\skills\` |
| Mac | `~/.cherrystudio/agents/skills/` |
| Linux | `~/.cherrystudio/agents/skills/` |

### 第三步：重启Cherry Studio

关闭并重新打开Cherry Studio，技能就安装好了！

---

## 🚀 使用方法

### 方法1：创建专用智能体

1. 打开Cherry Studio → 智能体页面
2. 点击「创建智能体」
3. 名称随便填，比如"PPT助手"
4. 在提示词框加入：
   ```
   你是一个专业的PPT生成助手。当用户说"生成PPT"、"做PPT"、"制作演示文稿"等时，使用ppt-generator技能帮助用户创建专业的PowerPoint文件。生成后告诉用户文件保存路径。
   ```
5. 勾选「启用代码执行」
6. 保存

### 方法2：在现有智能体中使用

在任何智能体对话中直接说：
- "帮我生成一个关于[主题]的PPT"
- "制作一个介绍[内容]的演示文稿"
- "做PPT：[你的需求描述]"

---

## 💡 使用示例

**用户说：** "帮我做一个关于日间化疗的汇报PPT"

**技能响应：**
1. 询问具体内容要点
2. （如果知识库有相关资料，自动检索）
3. 生成PPT文件
4. 告知文件路径：`/tmp/日间化疗汇报.pptx`

---

## 📁 生成的文件

生成的PPT包含：
- 📄 **封面页** — 标题 + 副标题
- 📋 **内容页** — 根据你的要点生成
- 🙋 **结束页** — "谢谢观看"

你可以用Microsoft PowerPoint、WPS、或直接拖入Cherry Studio打开编辑。

---

## ⚠️ 注意事项

1. **首次使用**会提示安装`python-pptx`库，点击允许即可
2. **代码执行**需要开启工具权限才能生成文件
3. 生成的文件在`/tmp/`目录下，关闭电脑前记得复制出来
4. 如果生成失败，检查是否勾选了「代码执行」权限

---

## 🔧 技能结构

```
.agents/skills/ppt-generator/
└── SKILL.md    ← 这就是技能定义文件
```

技能文件格式：
```markdown
---
name: ppt-generator
description: 触发描述...
---

# 技能指令
...
```

---

## 🤝 反馈

遇到问题？在本GitHub仓库提交Issue！

---

*技能版本：v1.0.0 | 更新日期：2026-04-18*
