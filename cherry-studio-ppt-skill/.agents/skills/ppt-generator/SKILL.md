---
name: ppt-generator
description: 当用户说"生成PPT"、"制作PPT"、"做PPT"、"演示文稿"、"幻灯片"时触发。支持Mode A-从零创建（2种输出：PPTX文件或HTML演示稿）；Mode B-上传文件转换；Mode C-修改现有PPT。提供乔布斯极简风/专业商务/医疗健康等多种风格，支持图表生成、AI配图。
---

# PPT 生成助手 v4.0

专业级PPT生成技能，支持**PPTX文件**和**HTML演示稿**两种输出格式。

---

## 🎯 两种输出模式

| 输出模式 | 触发方式 | 说明 |
|----------|----------|------|
| **PPTX模式** | "生成PPT" | 输出`.pptx`文件，可用PowerPoint/WPS打开 |
| **HTML模式** | "生成HTML演示稿" | 输出单个`.html`文件，乔布斯极简科技风 |

**用户可二选一，或者由你根据内容推荐最佳格式：**
- 正式汇报/商务提案 → **PPTX**
- 演讲/分享/产品展示 → **HTML**（更有冲击力）

---

## 🎨 风格体系

### HTML演示稿风格（乔布斯风）

| 风格 | 特点 | 适用场景 |
|------|------|----------|
| **极简科技** | 深色背景+动态光斑+高对比文字 | 科技产品/创新主题 |
| **商务简约** | 深灰背景+白色文字+蓝色点缀 | 正式汇报/商业提案 |
| **清新自然** | 深绿背景+柔和光斑 | 健康/环保/生活方式 |

### PPTX风格（专业6种）

| 编号 | 风格 | 主色调 | 适用场景 |
|------|------|--------|----------|
| 1 | 商务专业 | 深海蓝 #1F5C99 | 正式汇报、工作总结 |
| 2 | 医疗健康 | 医疗绿 #2E8B57 | 医院汇报、健康宣教 |
| 3 | 教育培训 | 橙蓝撞色 | 学术报告、培训课件 |
| 4 | 简约现代 | 深蓝紫 #4A90D9 | 科技展示、产品发布 |
| 5 | 清新活泼 | 绿橙亮色 | 科普宣传、健康宣教 |
| 6 | 学术严谨 | 深蓝灰 | 论文答辩、研究汇报 |

---

## 📋 HTML演示稿：8种页面类型

| 类型 | 结构 | 示例场景 |
|------|------|----------|
| **封面页** | 超大标题 + 副标题 | 开场 |
| **标题冲击页** | 单行/双行大标题，无正文 | 章节分隔 |
| **金句强调页** | 大引号 + 金句 + 来源 | 核心观点 |
| **步骤说明页** | 编号 + 动词型大标题 | 方法论 |
| **对比页** | 左右/上下分栏对比 | 前后变化 |
| **数据展示页** | 超大数字 + 单位说明 | 关键成果 |
| **列表页** | 标题 + 3-5要点（每点≤10字）| 多点说明 |
| **结尾行动页** | 总结金句 + CTA | 结束呼吁 |

---

## 📋 PPTX页面类型

| 类型 | 说明 |
|------|------|
| 封面页 | 标题 + 副标题 + 日期/Logo |
| 目录页 | 带序号的章节列表 |
| 内容页 | 标题 + 要点列表 |
| 图表页 | 标题 + 图表（柱状/饼/折线） |
| 总结页 | 核心要点回顾 |
| 结束页 | 谢谢观看 |

---

## 🔄 Mode A 工作流程（从零创建）

### Step 1️⃣：确认基本信息

**必须收集：**

| 问题 | 示例 |
|------|------|
| 主题 | "日间化疗工作汇报" |
| 受众 | 给谁看？（领导/客户/患者） |
| 时长 | 5分钟/10分钟/20分钟 |
| 内容准备度 | A-有完整内容 / B-有大纲 / C-只有主题 |

**询问示例：**
> "好的！请确认：
> 1️⃣ **主题**：要做什么？（如：日间化疗季度汇报）
> 2️⃣ **受众**：给谁看？（如：科室主任）
> 3️⃣ **时长**：多久？（如：10分钟）
> 4️⃣ **内容**：准备好内容了吗？
>    - A：内容已准备好（直接给我）
>    - B：有大纲，帮我扩展
>    - C：只有主题，帮我规划"

---

### Step 2️⃣：确认输出格式

**询问示例：**
> "你希望输出什么格式？
>
> 📊 **PPTX文件** - 传统PPT格式
>    优点：可用PowerPoint/WPS打开编辑
>    适用：正式汇报、商务提案
>
> 🌐 **HTML演示稿** - 乔布斯极简科技风
>    优点：视觉效果强，支持动画
>    适用：产品展示、演讲分享"

---

### Step 3️⃣：内容提炼与大纲确认

**如果用户有内容：**
- 阅读理解，提取核心要点
- 生成PPT大纲（用户确认后继续）

**大纲确认示例：**
> "根据你的主题，我规划了以下结构（共X页）：
>
> **第1页** 📄 封面（日间化疗工作汇报 / 2026年Q1）
> **第2页** 📋 目录
> **第3页** 📌 Part 1：服务开展情况
> **第4页** 📊 Part 2：关键数据展示
> **第5页** 📈 Part 3：趋势分析
> **第6页** 📌 Part 4：问题与对策
> **第7页** 🙋 结尾：谢谢
>
> 请确认：
> - ✅ 结构是否合适？
> - ➕ 需要增减页面吗？
> - 📊 需要图表吗？"

---

### Step 4️⃣：选择具体风格

**PPTX风格（6选1）：**
> "请选择风格：
> 1️⃣ 商务专业 / 2️⃣ 医疗健康 / 3️⃣ 教育培训
> 4️⃣ 简约现代 / 5️⃣ 清新活泼 / 6️⃣ 学术严谨"

**HTML风格（3选1）：**
> "HTML演示稿风格：
> 1️⃣ **极简科技** - 深色背景+动态光斑（科技产品）
> 2️⃣ **商务简约** - 深灰+白色（正式汇报）
> 3️⃣ **清新自然** - 深绿+柔和（健康生活）"

---

### Step 5️⃣：生成图表（如需要）

> "需要生成图表吗？
> 📊 柱状图（对比数据）
> 🥧 饼图（占比分析）
> 📈 折线图（趋势变化）
> 🔄 流程图（工作流程）"

**图表生成代码：**
```python
import matplotlib.pyplot as plt
matplotlib.use('Agg')
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']

def create_bar_chart(data, labels, title, color='#4472C4'):
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, data, color=color)
    ax.set_title(title, fontsize=16, fontweight='bold')
    for bar, value in zip(bars, data):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(), 
                f'{value:.0f}', ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(f'/tmp/{title}.png', dpi=150, bbox_inches='tight')
    plt.close()
    return f'/tmp/{title}.png'

def create_pie_chart(sizes, labels, title, colors=None):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    ax.set_title(title, fontsize=16, fontweight='bold')
    plt.savefig(f'/tmp/{title}.png', dpi=150, bbox_inches='tight')
    plt.close()
    return f'/tmp/{title}.png'

def create_line_chart(x, y, title, xlabel='x', ylabel='y'):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, marker='o', linewidth=2, markersize=8)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'/tmp/{title}.png', dpi=150, bbox_inches='tight')
    plt.close()
    return f'/tmp/{title}.png'
```

---

### Step 6️⃣：最终确认 → 生成

> "所有信息已确认！
>
> 📋 **生成清单**：
> - ✅ 封面页
> - ✅ 目录页
> - ✅ 内容页（X页）
> - ✅ 图表（X个）
> - ✅ 总结页
> - ✅ 结束页
>
> 🎨 **风格**：医疗健康（PPTX）/ 极简科技（HTML）
>
> 请说"开始生成"，或告诉我需要修改的地方~"

---

## 🎨 HTML演示稿完整代码模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>演示文稿</title>
  <script src="https://lf26-cdn-tos.bytecdntp.com/cdn/expire-1-M/tailwindcss/3.0.23/tailwind.min.js"></script>
  <link href="https://fonts.loli.net/css2?family=Inter:wght@300;400;700;900&display=swap" rel="stylesheet">
  <link href="https://fonts.loli.net/css2?family=Noto+Sans+SC:wght@300;400;700;900&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Noto Sans SC', 'Inter', sans-serif; background: #000; color: #fff; overflow: hidden; }
    .slides-container { width: 100vw; height: 100vh; display: flex; align-items: center; justify-content: center; background: #0a0a0a; }
    
    .slide {
      width: 100%; height: 100%; max-width: 450px; max-height: 800px; aspect-ratio: 9/16;
      position: absolute; display: flex; flex-direction: column; align-items: center;
      justify-content: center; padding: 2rem; opacity: 0; transform: translateX(100%);
      transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden;
      background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%);
    }
    .slide.active { opacity: 1; transform: translateX(0); }
    .slide.prev { opacity: 0; transform: translateX(-100%); }
    
    .light-spot { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.3; pointer-events: none; }
    .light-spot-1 { width: 300px; height: 300px; background: #3b82f6; top: -100px; right: -100px; animation: float1 20s ease-in-out infinite; }
    .light-spot-2 { width: 250px; height: 250px; background: #8b5cf6; bottom: -80px; left: -80px; animation: float2 25s ease-in-out infinite; }
    .light-spot-3 { width: 200px; height: 200px; background: #06b6d4; top: 50%; left: 50%; transform: translate(-50%,-50%); animation: float3 18s ease-in-out infinite; }
    
    @keyframes float1 { 0%,100% { transform: translate(0,0); } 25% { transform: translate(-50px,30px); } 50% { transform: translate(30px,50px); } 75% { transform: translate(50px,-20px); } }
    @keyframes float2 { 0%,100% { transform: translate(0,0); } 33% { transform: translate(40px,-40px); } 66% { transform: translate(-30px,30px); } }
    @keyframes float3 { 0%,100% { transform: translate(-50%,-50%) scale(1); } 50% { transform: translate(-50%,-50%) scale(1.2); } }
    
    .slide-content { position: relative; z-index: 10; text-align: center; width: 100%; }
    .progress-bar { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 8px; z-index: 100; }
    .progress-dot { width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.3); cursor: pointer; transition: all 0.3s; }
    .progress-dot.active { background: #fff; transform: scale(1.3); }
    .progress-dot:hover { background: rgba(255,255,255,0.6); }
    .page-number { position: fixed; bottom: 50px; left: 50%; transform: translateX(-50%); font-size: 0.875rem; color: rgba(255,255,255,0.4); z-index: 100; }
  </style>
</head>
<body>
  <div class="slides-container">
    <!-- ========== 封面页 ========== -->
    <div class="slide active">
      <div class="light-spot light-spot-1"></div>
      <div class="light-spot light-spot-2"></div>
      <div class="slide-content">
        <h1 class="text-5xl font-black mb-6 leading-tight">主标题</h1>
        <p class="text-xl font-light text-gray-400">副标题</p>
      </div>
    </div>
    
    <!-- ========== 标题冲击页 ========== -->
    <div class="slide">
      <div class="light-spot light-spot-2"></div>
      <div class="light-spot light-spot-3"></div>
      <div class="slide-content">
        <h1 class="text-4xl font-black leading-tight">冲击力标题</h1>
      </div>
    </div>
    
    <!-- ========== 金句强调页 ========== -->
    <div class="slide">
      <div class="light-spot light-spot-1"></div>
      <div class="light-spot light-spot-3"></div>
      <div class="slide-content">
        <span class="text-6xl text-gray-600 block mb-2">"</span>
        <p class="text-2xl font-bold mb-6">金句内容</p>
        <span class="text-lg font-light text-gray-500">— 来源</span>
      </div>
    </div>
    
    <!-- ========== 数据展示页 ========== -->
    <div class="slide">
      <div class="light-spot light-spot-1"></div>
      <div class="light-spot light-spot-2"></div>
      <div class="slide-content">
        <span class="text-7xl font-black">10x</span>
        <p class="text-xl font-light text-gray-400 mt-4">效率提升</p>
      </div>
    </div>
    
    <!-- ========== 列表页 ========== -->
    <div class="slide">
      <div class="light-spot light-spot-2"></div>
      <div class="light-spot light-spot-3"></div>
      <div class="slide-content">
        <h2 class="text-2xl font-bold mb-8">三个原则</h2>
        <ul class="space-y-6 text-xl">
          <li class="text-gray-300">• 少即是多</li>
          <li class="text-gray-300">• 专注核心</li>
          <li class="text-gray-300">• 持续迭代</li>
        </ul>
      </div>
    </div>
    
    <!-- ========== 结尾行动页 ========== -->
    <div class="slide">
      <div class="light-spot light-spot-1"></div>
      <div class="light-spot light-spot-2"></div>
      <div class="light-spot light-spot-3"></div>
      <div class="slide-content">
        <h1 class="text-3xl font-bold mb-8">现在就开始改变</h1>
        <p class="text-xl font-light text-gray-400">扫码获取更多信息</p>
      </div>
    </div>
  </div>
  
  <div class="progress-bar" id="progressBar"></div>
  <div class="page-number" id="pageNumber">1 / 6</div>
  
  <script>
    const slides = document.querySelectorAll('.slide');
    const progressBar = document.getElementById('progressBar');
    const pageNumber = document.getElementById('pageNumber');
    let currentSlide = 0;
    
    slides.forEach((_, index) => {
      const dot = document.createElement('div');
      dot.className = `progress-dot ${index === 0 ? 'active' : ''}`;
      dot.addEventListener('click', () => goToSlide(index));
      progressBar.appendChild(dot);
    });
    
    function updateSlides() {
      slides.forEach((slide, index) => {
        slide.classList.remove('active', 'prev');
        if (index === currentSlide) slide.classList.add('active');
        else if (index < currentSlide) slide.classList.add('prev');
      });
      document.querySelectorAll('.progress-dot').forEach((dot, index) => {
        dot.classList.toggle('active', index === currentSlide);
      });
      pageNumber.textContent = `${currentSlide + 1} / ${slides.length}`;
    }
    
    function nextSlide() { if (currentSlide < slides.length - 1) { currentSlide++; updateSlides(); } }
    function prevSlide() { if (currentSlide > 0) { currentSlide--; updateSlides(); } }
    function goToSlide(index) { currentSlide = index; updateSlides(); }
    
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
      else if (e.key === 'ArrowLeft') prevSlide();
    });
    
    let touchStartX = 0;
    document.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; });
    document.addEventListener('touchend', (e) => {
      const diff = touchStartX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 50) { if (diff > 0) nextSlide(); else prevSlide(); }
    });
  </script>
</body>
</html>
```

---

## 📊 PPTX完整代码模板

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

STYLES = {
    "商务专业": {"primary": RGBColor(31,92,153), "secondary": RGBColor(66,133,244), "accent": RGBColor(0,121,191)},
    "医疗健康": {"primary": RGBColor(46,139,87), "secondary": RGBColor(67,160,71), "accent": RGBColor(0,150,136)},
    "教育培训": {"primary": RGBColor(255,143,0), "secondary": RGBColor(25,118,210), "accent": RGBColor(156,39,176)},
    "简约现代": {"primary": RGBColor(74,144,217), "secondary": RGBColor(224,27,108), "accent": RGBColor(156,136,255)},
    "清新活泼": {"primary": RGBColor(112,173,71), "secondary": RGBColor(255,192,0), "accent": RGBColor(0,150,136)},
    "学术严谨": {"primary": RGBColor(31,49,125), "secondary": RGBColor(70,130,180), "accent": RGBColor(105,105,105)},
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
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = c["primary"]
    p.alignment = PP_ALIGN.CENTER
    if subtitle:
        sub = slide.shapes.add_textbox(Inches(0.8), Inches(4.0), Inches(11.7), Inches(0.8))
        tf = sub.text_frame
        tf.paragraphs[0].text = subtitle
        tf.paragraphs[0].font.size = Pt(24)
        tf.paragraphs[0].font.color.rgb = c["secondary"]
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
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

def create_content(title, points, style="商务专业", image_path=None):
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
        p.font.color.rgb = RGBColor(33,33,33)
        p.space_after = Pt(14)
    if image_path and os.path.exists(image_path):
        slide.shapes.add_picture(image_path, Inches(9.5), Inches(2), width=Inches(3.5))
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

# 示例使用
if __name__ == "__main__":
    create_cover("日间化疗工作汇报", "2026年Q1季度总结", "日间化疗中心", "2026年4月", "医疗健康")
    create_toc(["服务开展情况", "质量安全分析", "下阶段计划"], "医疗健康")
    create_content("一、服务开展情况", ["Q1服务患者1256人次", "同比增长23.5%", "等候时间缩短至28分钟", "满意度96.8%"], "医疗健康")
    create_content("二、质量安全分析", ["不良事件：0例", "院感发生率：0.12%", "超时观察率：2.3%"], "医疗健康")
    create_summary(["服务量持续增长", "质量安全达标", "满意度提升", "优化服务流程"], "医疗健康")
    create_end("谢谢观看", "医疗健康")
    prs.save("/tmp/日间化疗工作汇报.pptx")
    print(f"✅ PPT已生成: /tmp/日间化疗工作汇报.pptx")
```

---

## ⚠️ 关键约束

1. **分步引导** — 不要一次性问完，逐步确认
2. **用户确认** — 每次确认后再继续
3. **内容精准** — 先确认主题、受众、时长
4. **格式推荐** — 根据场景推荐PPTX或HTML
5. **极简原则** — HTML模式每页只讲一件事

---

## 🎯 触发关键词

- 生成PPT / 制作PPT / 做PPT
- 创建演示文稿 / 制作幻灯片
- 生成HTML演示稿
- 乔布斯风PPT / 极简风演示
- 输出PPT文件 / HTML文件

---

## 📌 快速参考

| 场景 | 回复模板 |
|------|----------|
| 用户要新做PPT | "请确认：1)主题 2)受众 3)时长 4)内容准备度 5)输出格式（PPTX或HTML）" |
| 用户要HTML | "好的！HTML演示稿是乔布斯极简科技风，请告诉我主题和内容" |
| 用户选风格 | "PPTX：1商务/2医疗/3教育/4简约/5清新/6学术 | HTML：1极简科技/2商务简约/3清新自然" |
| 用户要图表 | "需要：1柱状图 2饼图 3折线图 4流程图？告诉我数据" |
