---
name: ppt-generator
description: 当用户说"生成PPT"、"制作PPT"、"做PPT"、"PPT"、"演示文稿"、"幻灯片"时触发此技能。此技能帮助用户根据主题或资料生成专业的PowerPoint演示文稿。
---

# PPT 生成助手

当用户请求生成PPT时，按照以下流程执行：

## 第一步：收集需求

询问用户以下信息（如果用户没有明确提供）：
1. **PPT主题**：关于什么的演示？
2. **内容要点**：需要包含哪些核心内容？
3. **页数/时长**：大概需要多少页？
4. **风格偏好**：正式/活泼/简约/专业？

## 第二步：资料检索（可选）

如果用户提供了文档或资料：
1. 先阅读理解用户提供的内容
2. 如果知识库中有相关资料，主动检索使用

如果用户没有提供资料但主题需要调研：
1. 使用网络搜索获取相关信息
2. 结合搜索结果组织内容

## 第三步：生成PPT

使用Python代码生成真实的PPT文件：

```python
# 安装必要的库（如果尚未安装）
# !pip install python-pptx Pillow

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RgbColor
from pptx.enum.text import PP_ALIGN
import os

# 创建演示文稿
prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9 宽屏
prs.slide_height = Inches(7.5)

# ===== 封面页 =====
slide_layout = prs.slide_layouts[6]  # 空白布局
slide = prs.slides.add_slide(slide_layout)

# 标题
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(12.333), Inches(1.5))
title_frame = title_box.text_frame
title_frame.paragraphs[0].text = "【你的PPT标题】"
title_frame.paragraphs[0].font.size = Pt(44)
title_frame.paragraphs[0].font.bold = True
title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

# 副标题
subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.2), Inches(12.333), Inches(0.8))
subtitle_frame = subtitle_box.text_frame
subtitle_frame.paragraphs[0].text = "副标题（如需要）"
subtitle_frame.paragraphs[0].font.size = Pt(24)
subtitle_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

# ===== 内容页模板 =====
def add_content_slide(prs, title, bullet_points):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # 标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12.333), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.paragraphs[0].text = title
    title_frame.paragraphs[0].font.size = Pt(32)
    title_frame.paragraphs[0].font.bold = True
    
    # 内容要点
    content_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(11.933), Inches(5.5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    for i, point in enumerate(bullet_points):
        if i == 0:
            p = content_frame.paragraphs[0]
        else:
            p = content_frame.add_paragraph()
        p.text = f"• {point}"
        p.font.size = Pt(20)
        p.space_after = Pt(12)
    
    return slide

# ===== 根据实际内容添加页面 =====
# 示例：根据用户提供的要点生成内容页
# 请根据实际需求修改以下内容

content_slides = [
    ("页面标题1", ["要点1", "要点2", "要点3"]),
    ("页面标题2", ["要点1", "要点2", "要点3"]),
    ("页面标题3", ["要点1", "要点2", "要点3"]),
]

for title, points in content_slides:
    add_content_slide(prs, title, points)

# ===== 结束页 =====
slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(slide_layout)

end_box = slide.shapes.add_textbox(Inches(0.5), Inches(3), Inches(12.333), Inches(1))
end_frame = end_box.text_frame
end_frame.paragraphs[0].text = "谢谢观看"
end_frame.paragraphs[0].font.size = Pt(36)
end_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

# ===== 保存文件 =====
output_path = "/tmp/生成的PPT文件.pptx"
prs.save(output_path)
print(f"PPT已生成: {output_path}")
print(f"文件大小: {os.path.getsize(output_path)} bytes")
```

## 第四步：提供下载

1. 代码执行完成后，PPT文件会保存到 `/tmp/` 目录
2. 告知用户文件路径，让用户下载
3. 如果Cherry Studio支持文件发送，直接发送文件给用户

## 注意事项

1. **代码执行**：使用Cherry Studio的Code Tools执行Python代码
2. **库安装**：首次使用时需要安装 `python-pptx`，使用 `!pip install python-pptx`
3. **内容组织**：根据用户的实际需求组织PPT内容，不要硬编码
4. **样式优化**：可以添加颜色、图片、图表等增强视觉效果
5. **文件交付**：生成后一定要告诉用户文件的完整路径

## 触发关键词

- 生成PPT
- 制作PPT
- 做PPT
- 帮我做演示文稿
- 创建幻灯片
- 输出PPT文件
