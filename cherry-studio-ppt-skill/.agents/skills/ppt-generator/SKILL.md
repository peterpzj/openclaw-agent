---
name: ppt-generator
description: 当用户说"生成PPT"、"制作PPT"、"做PPT"、"演示文稿"、"幻灯片"、或任何关于PPT/演示的需求时触发。此技能提供专业的PPT生成服务，包含多模板选择、图表生成、AI配图、分步确认等功能。
---

# PPT 生成助手

专业级PPT生成技能，提供多模板、图表、AI配图等能力。

---

## 核心能力

| 能力 | 说明 |
|------|------|
| 🎨 多模板 | 5种专业风格模板 |
| 📊 图表生成 | 支持柱状图、饼图、折线图、流程图 |
| 🖼️ AI配图 | 自动生成主题相关图片 |
| 🔄 分步确认 | 逐步确认，避免返工 |
| 📋 内容框架 | 精准确定受众与目标 |

---

## 工作流程

### Step 1️⃣：确认PPT基本信息

**必须收集：**

| 问题 | 选项/示例 |
|------|----------|
| **主题** | 你要做什么主题的PPT？ |
| **受众** | 给谁看？（领导/客户/同事/患者/学生） |
| **时长** | 演讲时长？（5分钟/10分钟/20分钟/更长） |

**询问示例：**
> "好的，我来帮你生成PPT！先确认几个基本信息：
> - 主题是什么？
> - 听众是谁？
> - 演讲大约多长时间？"

---

### Step 2️⃣：选择风格模板

**5种专业模板：**

| 编号 | 模板名 | 适用场景 | 配色 |
|------|--------|----------|------|
| 1 | **商务简约** | 正式汇报、工作总结 | 蓝白灰 |
| 2 | **医疗专业** | 医院汇报、健康宣教 | 白绿蓝 |
| 3 | **学术严谨** | 论文答辩、学术报告 | 深蓝米白 |
| 4 | **活泼清新** | 培训宣教、科普宣传 | 绿橙亮色 |
| 5 | **高端商务** | 客户提案、商业计划 | 黑金深灰 |

**询问示例：**
> "请选择PPT风格：
> 1️⃣ 商务简约（正式汇报）
> 2️⃣ 医疗专业（医院场景）
> 3️⃣ 学术严谨（论文答辩）
> 4️⃣ 活泼清新（培训科普）
> 5️⃣ 高端商务（客户提案）
> 请回复数字或风格名称~"

---

### Step 3️⃣：确认内容框架

**系统自动根据主题生成内容大纲，用户确认或修改：**

| 页面类型 | 内容说明 |
|----------|----------|
| 封面 | 标题 + 副标题 + 演讲人 |
| 目录 | 演讲大纲 |
| 内容页1 | [自动生成相关内容] |
| 内容页2 | [自动生成相关内容] |
| ... | ... |
| 总结页 | 核心要点回顾 |
| 结束页 | 谢谢观看 |

**询问示例：**
> "根据你的主题，我生成了以下PPT框架：
>
> 📄 **封面**：2026年日间化疗工作汇报
> 📋 **目录**：3部分内容
> 📌 **Part 1**：日间化疗开展情况
> 📌 **Part 2**：质量与安全分析
> 📌 **Part 3**：下阶段工作计划
> 📌 **总结**：核心要点
> 🙋 **结束**：谢谢
>
> 请确认：
> - 内容是否准确？
> - 需要增加或删除哪些部分？"

---

### Step 4️⃣：生成图表（可选）

**如果内容需要数据支撑，系统询问：**

> "你的PPT中包含数据吗？如果有，我可以帮你生成：
> - 📊 柱状图（对比数据）
> - 🥧 饼图（占比分析）
> - 📈 折线图（趋势变化）
> - 🔄 流程图（工作流程）
>
> 请告诉我需要生成哪些图表，以及对应的数据。"

**图表生成代码模板：**

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 无GUI后端
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 示例：柱状图
def create_bar_chart(data, labels, title, output_path):
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, data, color=['#4472C4', '#70AD47', '#FFC000', '#5B9BD5', '#ED7D31'])
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_ylabel('数值', fontsize=12)
    
    # 添加数值标签
    for bar, value in zip(bars, data):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{value:.0f}',
                ha='center', va='bottom', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"图表已保存: {output_path}")

# 使用示例
# create_bar_chart([85, 92, 78, 88], ['门诊', '住院', '急诊', '体检'], '各科室满意度', '/tmp/chart1.png')
```

---

### Step 5️⃣：生成配图（可选）

**系统自动判断并询问：**
> "需要为某些页面添加配图吗？比如：
> - 🏥 医疗场景图
> - 📊 数据展示图
> - 👥 人物示意
> - 🖼️ 背景装饰
>
> 请告诉我是哪一页需要配图，以及图片内容描述。"

**配图生成：**
- 使用AI绘图工具生成主题相关图片
- 保存到 `/tmp/ppt_images/` 目录
- 插入到对应页面

---

### Step 6️⃣：最终确认与生成

**确认无误后生成PPT：**

> "所有信息已确认！现在开始生成PPT...
> 
> 📝 生成中：
> - ✅ 封面页
> - ✅ 目录页
> - ✅ 内容页（5页）
> - ✅ 图表（2个）
> - ✅ 总结页
> - ✅ 结束页
> 
> 🎉 PPT生成完成！
> 📁 文件路径：`/tmp/你的PPT主题.pptx`
> 请在关闭电脑前复制出来~"

---

## PPT生成代码模板

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RgbColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import os

# 创建演示文稿
prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9 宽屏
prs.slide_height = Inches(7.5)

# ==================== 模板样式定义 ====================

TEMPLATES = {
    "商务简约": {
        "primary": RgbColor(0x00, 0x44, 0x82),   # 深蓝
        "secondary": RgbColor(0xFF, 0xFF, 0xFF), # 白色
        "accent": RgbColor(0x00, 0x70, 0xC0),     # 亮蓝
        "bg": RgbColor(0xF5, 0xF7, 0xFA),        # 浅灰蓝
        "font_title": "微软雅黑",
        "font_body": "微软雅黑"
    },
    "医疗专业": {
        "primary": RgbColor(0x00, 0x72, 0x4E),   # 医疗绿
        "secondary": RgbColor(0xFF, 0xFF, 0xFF), # 白色
        "accent": RgbColor(0x00, 0xA5, 0x69),     # 浅绿
        "bg": RgbColor(0xF0, 0xF8, 0xF5),        # 浅绿背景
        "font_title": "微软雅黑",
        "font_body": "微软雅黑"
    },
    "学术严谨": {
        "primary": RgbColor(0x1F, 0x49, 0x7D),   # 深蓝
        "secondary": RgbColor(0xFF, 0xF5, 0xE6), # 米白
        "accent": RgbColor(0x2E, 0x75, 0xB6),    # 中蓝
        "bg": RgbColor(0xFF, 0xFF, 0xFF),        # 白色
        "font_title": "宋体",
        "font_body": "宋体"
    },
    "活泼清新": {
        "primary": RgbColor(0x70, 0xAD, 0x47),   # 清新绿
        "secondary": RgbColor(0xFF, 0xFF, 0xFF), # 白色
        "accent": RgbColor(0xFF, 0xC0, 0x00),    # 亮橙
        "bg": RgbColor(0xF0, 0xF9, 0xEB),       # 浅绿背景
        "font_title": "微软雅黑",
        "font_body": "微软雅黑"
    },
    "高端商务": {
        "primary": RgbColor(0x1A, 0x1A, 0x1A),   # 黑色
        "secondary": RgbColor(0xFF, 0xD7, 0x00), # 金色
        "accent": RgbColor(0x40, 0x40, 0x40),     # 深灰
        "bg": RgbColor(0x26, 0x26, 0x26),        # 深灰背景
        "font_title": "微软雅黑",
        "font_body": "微软雅黑"
    }
}

# ==================== 页面生成函数 ====================

def set_shape_fill(shape, color):
    """设置形状填充颜色"""
    shape.fill.solid()
    shape.fill.fore_color.rgb = color

def add_title_bar(slide, template, text="标题"):
    """添加标题栏"""
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.2)
    )
    set_shape_fill(bar, template["primary"])
    bar.line.fill.background()
    
    # 标题文字
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(0.8))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = template["secondary"]
    p.font.name = template["font_title"]

def add_content_text(slide, template, points, start_y=1.8):
    """添加内容文本"""
    txBox = slide.shapes.add_textbox(Inches(0.7), Inches(start_y), Inches(11.9), Inches(5))
    tf = txBox.text_frame
    tf.word_wrap = True
    
    for i, point in enumerate(points):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"• {point}"
        p.font.size = Pt(22)
        p.font.color.rgb = template["primary"]
        p.font.name = template["font_body"]
        p.space_after = Pt(14)

# ==================== 封面页 ====================

def create_cover_slide(prs, template, title, subtitle="", author=""):
    """创建封面页"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # 背景色
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    set_shape_fill(bg, template["bg"])
    bg.line.fill.background()
    
    # 顶部装饰线
    top_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15)
    )
    set_shape_fill(top_bar, template["primary"])
    top_bar.line.fill.background()
    
    # 主标题
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(2.5), Inches(11.7), Inches(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = template["primary"]
    p.font.name = template["font_title"]
    p.alignment = PP_ALIGN.CENTER
    
    # 副标题
    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(4.2), Inches(11.7), Inches(0.8))
        tf = sub_box.text_frame
        p = tf.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(24)
        p.font.color.rgb = template["accent"]
        p.font.name = template["font_body"]
        p.alignment = PP_ALIGN.CENTER
    
    # 作者信息
    if author:
        author_box = slide.shapes.add_textbox(Inches(0.8), Inches(5.5), Inches(11.7), Inches(0.6))
        tf = author_box.text_frame
        p = tf.paragraphs[0]
        p.text = author
        p.font.size = Pt(18)
        p.font.color.rgb = template["primary"]
        p.font.name = template["font_body"]
        p.alignment = PP_ALIGN.CENTER
    
    return slide

# ==================== 目录页 ====================

def create_toc_slide(prs, template, items):
    """创建目录页"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    add_title_bar(slide, template, "目录")
    
    # 目录项
    toc_box = slide.shapes.add_textbox(Inches(1), Inches(1.8), Inches(11), Inches(5))
    tf = toc_box.text_frame
    
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"{i+1}. {item}"
        p.font.size = Pt(26)
        p.font.color.rgb = template["primary"]
        p.font.name = template["font_body"]
        p.space_after = Pt(20)
    
    return slide

# ==================== 内容页 ====================

def create_content_slide(prs, template, title, points, image_path=None):
    """创建内容页"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    add_title_bar(slide, template, title)
    add_content_text(slide, template, points)
    
    # 如果有配图，添加到右侧
    if image_path and os.path.exists(image_path):
        slide.shapes.add_picture(image_path, Inches(9.5), Inches(2), width=Inches(3.5))
    
    return slide

# ==================== 图表页 ====================

def create_chart_slide(prs, template, title, chart_image_path):
    """创建图表页"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    add_title_bar(slide, template, title)
    
    if os.path.exists(chart_image_path):
        slide.shapes.add_picture(chart_image_path, Inches(1.5), Inches(1.8), width=Inches(10))
    
    return slide

# ==================== 总结页 ====================

def create_summary_slide(prs, template, title, points):
    """创建总结页"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    add_title_bar(slide, template, title)
    
    # 总结要点框
    summary_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2)
    )
    set_shape_fill(summary_box, RgbColor(0xF5, 0xF7, 0xFA))
    summary_box.line.color.rgb = template["accent"]
    
    add_content_text(slide, template, points, start_y=2.0)
    
    return slide

# ==================== 结束页 ====================

def create_end_slide(prs, template, message="谢谢观看"):
    """创建结束页"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # 全屏背景
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    set_shape_fill(bg, template["primary"])
    bg.line.fill.background()
    
    # 结束语
    end_box = slide.shapes.add_textbox(Inches(0), Inches(3), Inches(13.333), Inches(1.5))
    tf = end_box.text_frame
    p = tf.paragraphs[0]
    p.text = message
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = template["secondary"]
    p.font.name = template["font_title"]
    p.alignment = PP_ALIGN.CENTER
    
    return slide

# ==================== 主程序 ====================

def generate_ppt(title, subtitle, author, template_name, toc_items, content_slides, chart_images, summary_points, output_filename):
    """
    生成完整PPT
    
    参数:
        title: 封面标题
        subtitle: 封面副标题
        author: 演讲人
        template_name: 模板名称（商务简约/医疗专业/学术严谨/活泼清新/高端商务）
        toc_items: 目录列表
        content_slides: [(标题, [要点列表]), ...]
        chart_images: [图表图片路径列表]
        summary_points: 总结要点列表
        output_filename: 输出文件名
    """
    template = TEMPLATES.get(template_name, TEMPLATES["商务简约"])
    
    # 创建封面
    create_cover_slide(prs, template, title, subtitle, author)
    
    # 创建目录
    create_toc_slide(prs, template, toc_items)
    
    # 创建内容页
    for i, (slide_title, points) in enumerate(content_slides):
        if i < len(chart_images) and chart_images[i]:
            create_content_slide(prs, template, slide_title, points, chart_images[i])
        else:
            create_content_slide(prs, template, slide_title, points)
    
    # 创建总结页
    create_summary_slide(prs, template, "核心要点", summary_points)
    
    # 创建结束页
    create_end_slide(prs, template)
    
    # 保存
    output_path = f"/tmp/{output_filename}.pptx"
    prs.save(output_path)
    print(f"✅ PPT已生成: {output_path}")
    print(f"📊 共 {len(prs.slides)} 页")
    return output_path

# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 示例：医疗工作汇报
    ppt = generate_ppt(
        title="2026年日间化疗工作汇报",
        subtitle="持续优化服务 提升患者体验",
        author="某某医院 日间化疗中心",
        template_name="医疗专业",
        toc_items=["日间化疗开展情况", "质量与安全分析", "下阶段工作计划"],
        content_slides=[
            ("一、日间化疗开展情况", [
                "2026年Q1共服务患者1256人次",
                "同比增长23.5%",
                "平均等候时间缩短至28分钟",
                "患者满意度达96.8%"
            ]),
            ("二、质量与安全分析", [
                "不良事件：0例",
                "院感发生率：0.12%（目标<0.5%）",
                "超时观察率：2.3%",
                "非计划再就诊率：0.8%"
            ]),
            ("三、下阶段工作计划", [
                "扩大日间病房容量50%",
                "引入智能化排程系统",
                "开展夜间化疗服务试点",
                "优化随访管理流程"
            ])
        ],
        chart_images=[],  # 如有图表图片路径填入
        summary_points=[
            "日间化疗服务量持续增长",
            "质量安全指标全部达标",
            "患者满意度稳步提升",
            "将继续优化服务流程"
        ],
        output_filename="日间化疗工作汇报"
    )
```

---

## 触发关键词

- 生成PPT
- 制作PPT
- 做PPT
- 创建演示文稿
- 制作幻灯片
- 帮我做PPT
- 做汇报
- 输出PPT文件

---

## 注意事项

1. **分步引导** — 不要一次性问完所有问题，逐步确认
2. **精准框架** — 先确认主题、受众、时长，再生成内容
3. **用户确认** — 每次确认后再继续，不要替用户做决定
4. **图表生成** — 使用matplotlib，保存为PNG后插入PPT
5. **配图生成** — 使用AI绘图工具生成主题相关图片
6. **文件交付** — 生成后告知完整路径
