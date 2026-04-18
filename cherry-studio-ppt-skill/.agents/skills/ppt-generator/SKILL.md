---
name: ppt-generator
description: 当用户说"生成PPT"、"制作PPT"、"做PPT"、"演示文稿"、"幻灯片"时触发。支持Mode A-从零创建（PPTX文件或HTML演示稿）；Mode B-上传文件转换；Mode C-修改现有PPT。提供36种HTML主题、14种完整模板、图表生成、AI配图。
---

# PPT 生成助手 v5.0

专业级PPT生成技能，支持**PPTX文件**和**HTML演示稿**两种输出格式。

---

## 🎯 两种输出模式

| 输出模式 | 触发方式 | 说明 |
|----------|----------|------|
| **PPTX模式** | "生成PPT" | 输出`.pptx`文件，可用PowerPoint/WPS打开 |
| **HTML模式** | "生成HTML演示稿" | 输出单个`.html`文件，36种主题+动画效果 |

---

## 🎨 HTML演示稿：36种专业主题

### 简约专业（Light & Calm）

| 主题 | 风格 | 适用场景 |
|------|------|----------|
| `minimal-white` | 极简白，克制高级 | 内部汇报、技术评审 |
| `editorial-serif` | 杂志风衬线+奶油底 | 品牌故事、文字密度大 |
| `soft-pastel` | 柔和马卡龙三色渐变 | 产品发布、消费者向 |
| `xiaohongshu-white` | 小红书白底+暖红accent | 小红书图文、生活美学 |
| `academic-paper` | 论文白+衬线正文 | 学术报告、研究分享 |
| `corporate-clean` | 纯白+海军蓝accent | 董事会汇报、B2B销售 |

### 酷炫暗色（Cool & Dark）

| 主题 | 风格 | 适用场景 |
|------|------|----------|
| `tokyo-night` | Tokyo Night蓝夜 | 基础设施、技术分享 |
| `dracula` | 经典Dracula紫红 | 代码密集技术分享 |
| `catppuccin-mocha` | catppuccin深色 | 开发者内部分享 |
| `nord` | 北欧清冷蓝白 | 云产品、基础设施 |
| `gruvbox-dark` | 温暖复古深色 | Terminal/vim/*nix |
| `glassmorphism` | 毛玻璃+多色光斑 | Apple式发布会 |

### 强烈视觉（BOLD & Statement）

| 主题 | 风格 | 适用场景 |
|------|------|----------|
| `neo-brutalism` | 厚描边+硬阴影+明黄 | 创业路演、敢说敢做 |
| `bauhaus` | 几何+红黄蓝原色 | 设计talk、艺术史 |
| `swiss-grid` | 瑞士网格+Helvetica感 | 严肃排版、设计行业 |
| `cyberpunk-neon` | 纯黑+霓虹粉青黄发光 | 黑客、赛博talk |
| `vaporwave` | 深紫+粉红青蓝渐变 | 潮流艺术、Aesthetic |

### 温暖活力（Warm & Vibrant）

| 主题 | 风格 | 适用场景 |
|------|------|----------|
| `sunset-warm` | 橘/珊瑚/琥珀三色渐变 | 生活方式、奖项颁发 |
| `midcentury` | 奶油底+芥末/青/焦橙 | 设计史、复古品牌 |
| `retro-tv` | 暖奶油+CRT扫描线 | 怀旧叙事、八零九零后 |

### 效果丰富（Effect-Heavy）

| 主题 | 风格 | 适用场景 |
|------|------|----------|
| `aurora` | 极光渐变+blur | 封面/CTA/结语 |
| `blueprint` | 蓝图工程+网格底纹 | 系统架构、工程蓝图 |
| `terminal-green` | 绿屏终端+等宽发光 | CLI/复古朋克 |
| `pitch-deck-vc` | YC风白底+蓝紫渐变 | 融资路演、VC meeting |

### 小红书专属（XHS）

| 主题 | 风格 | 适用场景 |
|------|------|----------|
| `xhs-white-editorial` | 白底杂志风+彩虹条 | 小红书图文+横屏deck |
| `xhs-pastel-card` | 柔和马卡龙慢生活 | 生活/个人成长/情感 |

---

## 📦 14种完整Deck模板（开箱即用）

| 模板 | 页数 | 风格 | 适用场景 |
|------|------|------|----------|
| `pitch-deck` | 10 | YC风白底+蓝紫渐变 | 融资路演 |
| `product-launch` | 8 | 暗英雄+亮内容+橙桃渐变 | 产品发布 |
| `tech-sharing` | 10+ | 代码友好深色 | 技术分享 |
| `weekly-report` | 5 | 商务白+图表 | 周报/月报 |
| `course-module` | 8 | 教育蓝+步骤卡片 | 培训课件 |
| `xhs-post` | 6 | 小红书3:4竖版 | 小红书图文 |
| `graphify-dark-graph` | 8 | 暗底+知识图谱+光球 | 开发者工具 |
| `knowledge-arch-blueprint` | 8 | 奶油蓝图+工程感 | 系统架构 |
| `hermes-cyber-terminal` | 8 | 暗终端+命令风格 | 工具评测 |
| `obsidian-claude-gradient` | 8 | GitHub暗紫渐变 | 开发教程 |

---

## 📋 工作流程（三种模式）

### Mode A：从零创建

**Step 1️⃣：确认基本信息**
> "好的！请确认：
> 1️⃣ **主题**：要做什么？（如：日间化疗季度汇报）
> 2️⃣ **受众**：给谁看？（如：科室主任）
> 3️⃣ **时长**：多久？（如：10分钟）
> 4️⃣ **内容**：准备好内容了吗？"

**Step 2️⃣：确认输出格式**
> "输出格式：
> 📊 **PPTX** - 传统PPT，可用PowerPoint打开
> 🌐 **HTML** - 36种主题+动画效果，更精美"

**Step 3️⃣：选择具体风格（HTML模式）**
> "HTML主题（选一个）：
> - 正式汇报：`minimal-white` / `corporate-clean` / `academic-paper`
> - 技术分享：`tokyo-night` / `dracula` / `blueprint`
> - 产品发布：`glassmorphism` / `aurora` / `soft-pastel`
> - 小红书：`xhs-white-editorial` / `xhs-pastel-card`
> - 路演融资：`pitch-deck-vc` / `neo-brutalism`"

**Step 4️⃣：确认内容大纲 → 生成**

---

### Mode B：文件转换

**上传文件 → 提取内容 → 选择风格 → 生成**

支持：Word / PDF / PPT / Markdown文件

---

### Mode C：修改PPT

**接收文件 → 分析现有 → 询问修改 → 执行**

---

## 🎨 HTML模板核心代码

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" id="theme-link" href="../assets/themes/minimal-white.css">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap" rel="stylesheet">
  <style>/* 基础变量由theme接管 */</style>
</head>
<body class="overflow-hidden">

  <!-- 幻灯片1: 封面 -->
  <section class="slide flex items-center justify-center" data-theme="minimal-white">
    <div class="text-center max-w-2xl">
      <h1 class="text-5xl font-black mb-4">主标题</h1>
      <p class="text-xl text-gray-500">副标题</p>
    </div>
  </section>

  <!-- 幻灯片2: 大数字展示 -->
  <section class="slide flex items-center justify-center" data-theme="minimal-white">
    <div class="text-center">
      <span class="text-8xl font-black text-blue-600">10x</span>
      <p class="text-2xl text-gray-600 mt-4">效率提升</p>
    </div>
  </section>

  <!-- 幻灯片3: 列表页 -->
  <section class="slide flex items-center justify-center" data-theme="minimal-white">
    <div class="max-w-2xl">
      <h2 class="text-3xl font-bold mb-8">三个核心要点</h2>
      <ul class="space-y-4 text-xl">
        <li>• 第一要点</li>
        <li>• 第二要点</li>
        <li>• 第三要点</li>
      </ul>
    </div>
  </section>

  <!-- 幻灯片4: 结束页 -->
  <section class="slide flex items-center justify-center" data-theme="minimal-white">
    <div class="text-center">
      <h2 class="text-4xl font-bold">谢谢观看</h2>
      <p class="text-xl text-gray-500 mt-4">欢迎提问</p>
    </div>
  </section>

  <script src="../assets/runtime.js"></script>
</body>
</html>
```

**键盘控制：** `← →` 翻页 | `F` 全屏 | `T` 切换主题 | `S` 演讲者备注 | `O` 幻灯片概览

---

## 📊 PPTX：6种专业风格

| 编号 | 风格 | 主色调 | 适用场景 |
|------|------|--------|----------|
| 1 | 商务专业 | 深海蓝 #1F5C99 | 正式汇报、工作总结 |
| 2 | 医疗健康 | 医疗绿 #2E8B57 | 医院汇报、健康宣教 |
| 3 | 教育培训 | 橙蓝撞色 | 学术报告、培训课件 |
| 4 | 简约现代 | 深蓝紫 #4A90D9 | 科技展示、产品发布 |
| 5 | 清新活泼 | 绿橙亮色 | 科普宣传、健康宣教 |
| 6 | 学术严谨 | 深蓝灰 | 论文答辩、研究汇报 |

---

## 📊 PPTX代码模板

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

STYLES = {
    "商务专业": {"primary": RGBColor(31,92,153), "secondary": RGBColor(66,133,244)},
    "医疗健康": {"primary": RGBColor(46,139,87), "secondary": RGBColor(67,160,71)},
    "教育培训": {"primary": RGBColor(255,143,0), "secondary": RGBColor(25,118,210)},
    "简约现代": {"primary": RGBColor(74,144,217), "secondary": RGBColor(224,27,108)},
    "清新活泼": {"primary": RGBColor(112,173,71), "secondary": RGBColor(255,192,0)},
    "学术严谨": {"primary": RGBColor(31,49,125), "secondary": RGBColor(70,130,180)},
}

def set_fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color

def create_cover(title, subtitle="", author="", date="", style="商务专业"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    c = STYLES[style]
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    set_fill(bg, RGBColor(250,250,250))
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.3))
    set_fill(bar, c["primary"])
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(2.5), Inches(11.7), Inches(1.5))
    p = txBox.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = c["primary"]
    p.alignment = PP_ALIGN.CENTER
    if subtitle:
        sub = slide.shapes.add_textbox(Inches(0.8), Inches(4.0), Inches(11.7), Inches(0.8))
        sub.text_frame.paragraphs[0].text = subtitle
        sub.text_frame.paragraphs[0].font.size = Pt(24)
        sub.text_frame.paragraphs[0].font.color.rgb = c["secondary"]
        sub.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    return slide

def create_toc(items, style="商务专业"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    c = STYLES[style]
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.2))
    set_fill(bar, c["primary"])
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.35), Inches(12), Inches(0.8))
    txBox.text_frame.paragraphs[0].text = "目录"
    txBox.text_frame.paragraphs[0].font.size = Pt(32)
    txBox.text_frame.paragraphs[0].font.bold = True
    txBox.text_frame.paragraphs[0].font.color.rgb = RGBColor(255,255,255)
    for i, item in enumerate(items):
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1), Inches(1.8+i*0.9), Inches(0.5), Inches(0.5))
        set_fill(circle, c["secondary"])
        txBox = slide.shapes.add_textbox(Inches(1.8), Inches(1.8+i*0.9), Inches(10), Inches(0.5))
        txBox.text_frame.paragraphs[0].text = item
        txBox.text_frame.paragraphs[0].font.size = Pt(22)
    return slide

def create_content(title, points, style="商务专业"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    c = STYLES[style]
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.2))
    set_fill(bar, c["primary"])
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.35), Inches(12), Inches(0.8))
    txBox.text_frame.paragraphs[0].text = title
    txBox.text_frame.paragraphs[0].font.size = Pt(28)
    txBox.text_frame.paragraphs[0].font.bold = True
    txBox.text_frame.paragraphs[0].font.color.rgb = RGBColor(255,255,255)
    content = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(5.2))
    tf = content.text_frame
    tf.word_wrap = True
    for i, point in enumerate(points):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {point}"
        p.font.size = Pt(20)
        p.space_after = Pt(14)
    return slide

def create_summary(points, style="商务专业"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    c = STYLES[style]
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.2))
    set_fill(bar, c["secondary"])
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.35), Inches(12), Inches(0.8))
    txBox.text_frame.paragraphs[0].text = "核心要点"
    txBox.text_frame.paragraphs[0].font.size = Pt(28)
    txBox.text_frame.paragraphs[0].font.bold = True
    txBox.text_frame.paragraphs[0].font.color.rgb = RGBColor(255,255,255)
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    set_fill(box, RGBColor(245,247,250))
    box.line.color.rgb = c["accent"]
    content = slide.shapes.add_textbox(Inches(1.2), Inches(2), Inches(11), Inches(4.5))
    tf = content.text_frame
    for i, point in enumerate(points):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"✓ {point}"
        p.font.size = Pt(22)
        p.font.color.rgb = c["primary"]
        p.space_after = Pt(16)
    return slide

def create_end(message="谢谢观看", style="商务专业"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    c = STYLES[style]
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    set_fill(bg, c["primary"])
    txBox = slide.shapes.add_textbox(Inches(0), Inches(3), Inches(13.333), Inches(1.5))
    tf = txBox.text_frame
    tf.paragraphs[0].text = message
    tf.paragraphs[0].font.size = Pt(48)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(255,255,255)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    return slide

# 示例
if __name__ == "__main__":
    create_cover("2026年日间化疗工作汇报", "Q1季度总结", "日间化疗中心", "2026年4月", "医疗健康")
    create_toc(["服务开展情况", "质量安全分析", "下阶段计划"], "医疗健康")
    create_content("一、服务开展情况", ["Q1服务1256人次", "同比增长23.5%", "等候时间缩短至28分钟", "满意度96.8%"], "医疗健康")
    create_summary(["服务量持续增长", "质量安全达标", "满意度提升"], "医疗健康")
    create_end("谢谢观看", "医疗健康")
    prs.save("/tmp/日间化疗工作汇报.pptx")
```

---

## ⚠️ 关键约束

1. **分步引导** — 不要一次性问完，逐步确认
2. **用户确认** — 每次确认后再继续
3. **格式推荐** — 根据场景推荐PPTX或HTML
4. **HTML主题丰富** — 36种主题可选，详细见上方列表

---

## 🎯 触发关键词

- 生成PPT / 制作PPT / 做PPT
- 创建演示文稿 / 制作幻灯片
- 生成HTML演示稿
- 输出PPT文件 / HTML文件
- 小红书图文 / 小红书PPT

---

## 📌 快速参考

| 场景 | 推荐格式/主题 |
|------|---------------|
| 正式汇报 | PPTX商务专业 / HTML: minimal-white |
| 技术分享 | HTML: tokyo-night / dracula / blueprint |
| 产品发布 | HTML: glassmorphism / aurora / soft-pastel |
| 小红书图文 | HTML: xhs-white-editorial / xhs-pastel-card |
| 融资路演 | HTML: pitch-deck-vc / neo-brutalism |
| 周报月报 | PPTX商务专业 / HTML: weekly-report |
| 学术报告 | PPTX学术严谨 / HTML: academic-paper |
