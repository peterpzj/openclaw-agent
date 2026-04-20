#!/usr/bin/env python3
"""
PPT Maker - 智能幻灯片生成脚本 v5.0
三节点工作流：Analyst → Director → Designer → PPTX
"""
import argparse
import json
import os
import re
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional

# ============================================================
# 配置
# ============================================================

DEFAULT_THEME = {
    "primary": "1a365d",
    "secondary": "2c5282", 
    "accent": "3182ce",
    "light": "bee3f8",
    "bg": "ffffff"
}

STYLE_THEMES = {
    "professional": {
        "primary": "1a365d", "secondary": "2c5282", "accent": "3182ce", "light": "bee3f8", "bg": "ffffff"
    },
    "medical": {
        "primary": "2E8B57", "secondary": "43A047", "accent": "56C596", "light": "D4EDDA", "bg": "ffffff"
    },
    "education": {
        "primary": "1E3A5F", "secondary": "E65100", "accent": "FF8F00", "light": "FFF3E0", "bg": "ffffff"
    },
    "minimalist": {
        "primary": "2D3748", "secondary": "4A5568", "accent": "718096", "light": "EDF2F7", "bg": "ffffff"
    },
    "modern": {
        "primary": "1A1A2E", "secondary": "4A90D9", "accent": "7B68EE", "light": "E8E8FF", "bg": "ffffff"
    }
}

# ============================================================
# 工具函数
# ============================================================

def run_node(script_content: str, timeout: int = 30) -> str:
    """执行 Node.js 脚本并返回结果"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(script_content)
        f.flush()
        temp_path = f.name
    
    try:
        result = subprocess.run(
            ['node', temp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return ""
    finally:
        os.unlink(temp_path)


def parse_json_response(content: str) -> Dict[str, Any]:
    """解析 JSON 响应，支持各种格式"""
    content = content.strip()
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    
    patterns = [
        r'```json\s*([\s\S]*?)\s*```',
        r'```\s*([\s\S]*?)\s*```',
        r'\{[\s\S]*\}'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            try:
                return json.loads(match.group(1) if '```json' in pattern or '```' in pattern else match.group())
            except json.JSONDecodeError:
                continue
    
    return {"error": "JSON解析失败", "raw": content[:500]}


def ensure_pptxgenjs() -> bool:
    """确保 pptxgenjs 已安装"""
    result = subprocess.run(
        ['node', '-e', 'require("pptxgenjs")'],
        capture_output=True
    )
    if result.returncode != 0:
        print("Installing pptxgenjs...")
        install_result = subprocess.run(
            ['npm', 'install', '-g', 'pptxgenjs'],
            capture_output=True
        )
        return install_result.returncode == 0
    return True


# ============================================================
# 三节点工作流
# ============================================================

class AnalystNode:
    """Stage 1: 内容提炼节点（低温 0.15）"""
    
    SYSTEM_PROMPT = """你是一位顶级的学术传播专家和内容策略师。

你的任务是阅读用户提供的原始材料，并从中提取出最核心、最具说服力的信息，为演示文稿做准备。

【核心原则】
1. 你必须**严格且仅基于**提供的上下文进行提取
2. 绝不能捏造数据
3. 如果在源材料中找不到足够的信息来支撑某个要点，请在要点中标注【需要人工补充】
4. 保持客观，只提炼材料中真正存在的信息

【输出格式】
提炼结果必须以严格的 JSON 格式输出"""

    def __init__(self, model: str = "minimax-portal/MiniMax-M2.7"):
        self.model = model
        self.temperature = 0.15
    
    def extract(self, source_material: str, topic: str, num_achievements: int = 3) -> Dict[str, Any]:
        """执行内容提炼"""
        user_prompt = f"""请阅读以下源材料，并为接下来的演示文稿提取核心素材。

**目标**：准备一份专业的述职/成果汇报演示文稿。
**主题**：{topic}
**核心要求**：请从材料中提炼出 **{num_achievements} 项最具代表性的核心成就/突破**。

对于每一项成就，请提供：
1. 成就的简短命名（10字以内）
2. 核心痛点与挑战（原有的问题是什么）
3. 具体的解决方案与创新点
4. 可量化的结果或学术/业务影响

【源材料】
{source_material}

【输出JSON格式】
{{
  "achievements": [
    {{
      "name": "成就名称（10字内）",
      "challenge": "核心痛点与挑战",
      "solution": "解决方案与创新点",
      "result": "可量化结果或影响"
    }}
  ],
  "key_themes": ["主题1", "主题2"],
  "evidence_quality": "高/中/低"
}}"""

        return self._call_ai(self.SYSTEM_PROMPT, user_prompt)
    
    def _call_ai(self, system: str, user: str) -> Dict[str, Any]:
        """调用 AI 模型"""
        import urllib.request
        
        api_key = os.environ.get("MINIMAX_API_KEY", "")
        if not api_key:
            # 无 API key 时返回模拟数据
            return {
                "achievements": [
                    {"name": "流程优化", "challenge": "原有流程效率低下", "solution": "引入智能系统", "result": "效率提升40%"},
                    {"name": "质量提升", "challenge": "质量标准不统一", "solution": "建立质控体系", "result": "合格率99%"},
                    {"name": "服务扩展", "challenge": "服务能力不足", "solution": "扩展服务范围", "result": "服务人次翻倍"}
                ],
                "key_themes": ["效率提升", "质量改进"],
                "evidence_quality": "高"
            }
        
        url = "https://api.minimax.chat/v1/text/chatcompletion_pro"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "temperature": self.temperature
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "{}")
                return parse_json_response(content)
        except Exception as e:
            return {"achievements": [], "error": str(e)}


class DirectorNode:
    """Stage 2: 大纲构建节点（中温 0.30）"""
    
    SYSTEM_PROMPT = """你是一位经验丰富的演示文稿导演。

你的工作是将研究摘要转化为结构清晰的幻灯片大纲。遵循"金字塔原理"，确保逻辑层层递进。

【核心原则】
1. 逻辑清晰：背景 → 成就1 → 成就2 → 成就3 → 总结
2. 每页有明确的核心目的
3. 结构平衡：不要把所有内容堆在一页
4. 符合阅读习惯：先结论，后细节

【页面类型】
- Title Slide: 封面
- TOC: 目录
- Introduction: 背景引入
- Content: 内容页（每项成就一页）
- Summary: 总结展望
- Thank You: 致谢"""

    def __init__(self, model: str = "minimax-portal/MiniMax-M2.7"):
        self.model = model
        self.temperature = 0.30
    
    def build_outline(self, analysis: Dict[str, Any], topic: str) -> Dict[str, Any]:
        """构建演示大纲"""
        achievements_text = json.dumps(analysis.get("achievements", []), ensure_ascii=False, indent=2)
        
        user_prompt = f"""基于以下提炼出的核心成就，请规划一份演示文稿大纲。

**主题**: {topic}

**核心成就**:
{achievements_text}

**要求**:
- 8-10 页
- 结构：封面 → 目录 → 背景引入 → 成就1 → 成就2 → 成就3 → 总结展望 → 致谢
- 每页有明确的核心目的

**输出格式（严格JSON）**:
{{
  "presentation_title": "演示文稿标题",
  "subtitle": "副标题",
  "slides": [
    {{
      "slide_number": 1,
      "slide_type": "Title Slide | TOC | Introduction | Content | Summary | Thank You",
      "title": "页面标题",
      "core_purpose": "本页的核心目的（一句话）",
      "key_points": ["要点1", "要点2"]
    }}
  ]
}}"""

        import urllib.request
        
        api_key = os.environ.get("MINIMAX_API_KEY", "")
        if not api_key:
            num_slides = len(analysis.get("achievements", []))
            slides = [
                {"slide_number": 1, "slide_type": "Title Slide", "title": topic, "core_purpose": "封面", "key_points": []},
                {"slide_number": 2, "slide_type": "TOC", "title": "目录", "core_purpose": "导航", "key_points": ["背景", "核心成就", "总结"]},
            ]
            for i, ach in enumerate(analysis.get("achievements", []), 1):
                slides.append({
                    "slide_number": 2 + i,
                    "slide_type": "Content",
                    "title": f"成就{i}: {ach.get('name', '未命名')}",
                    "core_purpose": f"展示{ach.get('name', '成就')}",
                    "key_points": [ach.get('challenge', ''), ach.get('solution', ''), ach.get('result', '')]
                })
            slides.append({"slide_number": 2 + num_slides + 1, "slide_type": "Summary", "title": "总结与展望", "core_purpose": "收尾", "key_points": []})
            slides.append({"slide_number": 2 + num_slides + 2, "slide_type": "Thank You", "title": "感谢聆听", "core_purpose": "致谢", "key_points": []})
            
            return {"presentation_title": topic, "subtitle": "成果汇报", "slides": slides}
        
        url = "https://api.minimax.chat/v1/text/chatcompletion_pro"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": self.temperature
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "{}")
                return parse_json_response(content)
        except Exception as e:
            return {"slides": [], "error": str(e)}


class DesignerNode:
    """Stage 3: 幻灯片生成节点（高温 0.65）"""
    
    SYSTEM_PROMPT = """你是一位资深的幻灯片设计师。

你的工作是将大纲扩充为可以直接展示的幻灯片内容。

【核心原则】
1. 文字精炼：幻灯片上字不如表，表不如图
2. 每页控制在 3-5 个要点
3. 必须包含口语化逐字稿（演讲者备注）
4. 提供详细的视觉建议（配图、图表类型、配色）

【防幻觉规则】
如果你发现大纲中缺少某些信息来支撑内容，请在该处标注【需要人工补充】，
绝对不要自行编造事实。"""

    def __init__(self, model: str = "minimax-portal/MiniMax-M2.7"):
        self.model = model
        self.temperature = 0.65
    
    def generate_slides(self, outline: Dict[str, Any], analysis: Dict[str, Any], topic: str) -> List[Dict[str, Any]]:
        """生成幻灯片内容"""
        outline_text = json.dumps(outline, ensure_ascii=False, indent=2)
        analysis_text = json.dumps(analysis, ensure_ascii=False, indent=2)
        
        user_prompt = f"""请根据以下大纲和核心信息，生成每一页幻灯片的详细内容。

**主题**: {topic}

**演示大纲**:
{outline_text}

**提炼的核心信息**:
{analysis_text}

**输出格式（严格JSON）**:
{{
  "slides": [
    {{
      "slide_number": 1,
      "title": "当前页面的主标题",
      "subtitle": "副标题（可选）",
      "slide_type": "cover|toc|content|summary|thank_you",
      "bullet_points": ["要点1 (极简)", "要点2 (极简)", "要点3 (极简)"],
      "visual_suggestion": "详细描述该页面应该配什么样的图表或意象图",
      "speaker_notes": "该页面的口语化演讲逐字稿，需要过渡自然，充满自信。控制在100-150字。"
    }}
  ]
}}"""

        import urllib.request
        
        api_key = os.environ.get("MINIMAX_API_KEY", "")
        if not api_key:
            slides = []
            for sl in outline.get("slides", []):
                slides.append({
                    "slide_number": sl.get("slide_number", 1),
                    "title": sl.get("title", ""),
                    "subtitle": "",
                    "slide_type": sl.get("slide_type", "content").lower().replace(" ", "_"),
                    "bullet_points": sl.get("key_points", [])[:3],
                    "visual_suggestion": "建议配简洁的图标或示意图",
                    "speaker_notes": f"现在开始介绍{sl.get('title', '本页')}。"
                })
            return slides
        
        url = "https://api.minimax.chat/v1/text/chatcompletion_pro"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": self.temperature
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "{}")
                parsed = parse_json_response(content)
                return parsed.get("slides", [])
        except Exception as e:
            return []


# ============================================================
# PPTX 生成器
# ============================================================

class PPTXGenerator:
    """使用 PptxGenJS 生成 PPTX 文件"""
    
    def __init__(self, theme: Dict[str, str] = None):
        self.theme = theme or DEFAULT_THEME
    
    def generate(self, slides: List[Dict[str, Any]], output_path: str, title: str = "演示文稿") -> bool:
        """生成 PPTX 文件"""
        if not ensure_pptxgenjs():
            print("pptxgenjs install failed")
            return False
        
        output_dir = os.path.dirname(output_path) or "/tmp/ppt-maker"
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "output"), exist_ok=True)
        
        slide_files = []
        for i, slide in enumerate(slides, 1):
            slide_num = f"{i:02d}"
            slide_file = os.path.join(output_dir, f"slide-{slide_num}.js")
            content = self._generate_slide_js(slide, i, self.theme)
            with open(slide_file, 'w', encoding='utf-8') as f:
                f.write(content)
            slide_files.append(slide_file)
        
        compile_content = self._generate_compile_js(len(slides), self.theme, output_dir)
        compile_file = os.path.join(output_dir, "compile.js")
        with open(compile_file, 'w', encoding='utf-8') as f:
            f.write(compile_content)
        
        result = subprocess.run(['node', compile_file], capture_output=True, text=True, cwd=output_dir)
        
        if result.returncode == 0:
            src = os.path.join(output_dir, "output", "presentation.pptx")
            if os.path.exists(src):
                import shutil
                shutil.move(src, output_path)
                print(f"PPT generated: {output_path}")
                return True
        
        print(f"Compile failed: {result.stderr}")
        return False
    
    def _generate_slide_js(self, slide: Dict[str, Any], num: int, theme: Dict[str, str]) -> str:
        slide_type = slide.get("slide_type", "content")
        title = slide.get("title", "")
        subtitle = slide.get("subtitle", "")
        bullets = slide.get("bullet_points", [])
        
        if slide_type == "cover":
            return self._gen_cover(num, title, subtitle, theme)
        elif slide_type == "toc":
            return self._gen_toc(num, title, bullets, theme)
        elif slide_type == "thank_you":
            return self._gen_thank_you(num, title, subtitle, theme)
        elif slide_type == "summary":
            return self._gen_summary(num, title, bullets, theme)
        else:
            return self._gen_content(num, title, bullets, theme)
    
    def _gen_cover(self, num: int, title: str, subtitle: str, theme: Dict) -> str:
        return f'''const pptxgen = require("pptxgenjs");
const slideConfig = {{ type: 'cover', index: {num}, title: '{title}' }};
function createSlide(pres, theme) {{
  const slide = pres.addSlide();
  slide.background = {{ color: theme.primary }};
  slide.addShape(pres.shapes.OVAL, {{ x: -1.5, y: -1.5, w: 4, h: 4, fill: {{ color: theme.secondary, transparency: 60 }} }});
  slide.addShape(pres.shapes.OVAL, {{ x: 7.5, y: 3.5, w: 4, h: 4, fill: {{ color: theme.accent, transparency: 50 }} }});
  slide.addText("{title}", {{ x: 0.5, y: 1.8, w: 9, h: 1.5, fontSize: 44, fontFace: "Microsoft YaHei", color: "FFFFFF", bold: true, align: "center" }});
  slide.addText("{subtitle}", {{ x: 0.5, y: 3.4, w: 9, h: 0.8, fontSize: 22, fontFace: "Microsoft YaHei", color: theme.light, align: "center" }});
  return slide;
}}
if (require.main === module) {{
  const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9';
  createSlide(pres, {json.dumps(theme)});
  pres.writeFile({{ fileName: "./output/slide-{num:02d}.pptx" }});
}}
module.exports = {{ createSlide, slideConfig }};
'''
    
    def _gen_toc(self, num: int, title: str, items: List, theme: Dict) -> str:
        items_json = json.dumps(items, ensure_ascii=False)
        return f'''const pptxgen = require("pptxgenjs");
const slideConfig = {{ type: 'toc', index: {num}, title: '{title}' }};
function createSlide(pres, theme) {{
  const slide = pres.addSlide();
  slide.background = {{ color: theme.bg }};
  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 0, w: 0.15, h: 5.625, fill: {{ color: theme.primary }} }});
  slide.addText("{title}", {{ x: 0.5, y: 0.3, w: 9, h: 0.8, fontSize: 36, fontFace: "Microsoft YaHei", color: theme.primary, bold: true }});
  const items = {items_json};
  items.forEach((item, i) => {{
    slide.addShape(pres.shapes.OVAL, {{ x: 0.7, y: 1.4 + i * 0.8, w: 0.12, h: 0.12, fill: {{ color: theme.accent }} }});
    slide.addText(item, {{ x: 1.0, y: 1.25 + i * 0.8, w: 8, h: 0.5, fontSize: 20, fontFace: "Microsoft YaHei", color: theme.secondary }});
  }});
  slide.addShape(pres.shapes.OVAL, {{ x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: {{ color: theme.accent }} }});
  slide.addText("{num}", {{ x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" }});
  return slide;
}}
if (require.main === module) {{
  const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9';
  createSlide(pres, {json.dumps(theme)});
  pres.writeFile({{ fileName: "./output/slide-{num:02d}.pptx" }});
}}
module.exports = {{ createSlide, slideConfig }};
'''
    
    def _gen_content(self, num: int, title: str, bullets: List, theme: Dict) -> str:
        bullets_json = json.dumps(bullets, ensure_ascii=False)
        return f'''const pptxgen = require("pptxgenjs");
const slideConfig = {{ type: 'content', index: {num}, title: '{title}' }};
function createSlide(pres, theme) {{
  const slide = pres.addSlide();
  slide.background = {{ color: theme.bg }};
  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 0, w: 10, h: 0.08, fill: {{ color: theme.primary }} }});
  slide.addText("{title}", {{ x: 0.5, y: 0.3, w: 9, h: 0.8, fontSize: 28, fontFace: "Microsoft YaHei", color: theme.primary, bold: true }});
  const bullets = {bullets_json};
  bullets.forEach((point, i) => {{
    slide.addShape(pres.shapes.OVAL, {{ x: 0.6, y: 1.35 + i * 0.7, w: 0.15, h: 0.15, fill: {{ color: theme.accent }} }});
    slide.addText(point, {{ x: 0.9, y: 1.2 + i * 0.7, w: 8.5, h: 0.5, fontSize: 18, fontFace: "Microsoft YaHei", color: theme.secondary }});
  }});
  slide.addShape(pres.shapes.RECTANGLE, {{ x: 7, y: 1.2, w: 2.5, h: 3.8, fill: {{ color: theme.light, transparency: 60 }} }});
  slide.addShape(pres.shapes.OVAL, {{ x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: {{ color: theme.accent }} }});
  slide.addText("{num}", {{ x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" }});
  return slide;
}}
if (require.main === module) {{
  const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9';
  createSlide(pres, {json.dumps(theme)});
  pres.writeFile({{ fileName: "./output/slide-{num:02d}.pptx" }});
}}
module.exports = {{ createSlide, slideConfig }};
'''
    
    def _gen_summary(self, num: int, title: str, points: List, theme: Dict) -> str:
        points_json = json.dumps(points, ensure_ascii=False)
        return f'''const pptxgen = require("pptxgenjs");
const slideConfig = {{ type: 'summary', index: {num}, title: '{title}' }};
function createSlide(pres, theme) {{
  const slide = pres.addSlide();
  slide.background = {{ color: theme.bg }};
  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 0, w: 0.15, h: 5.625, fill: {{ color: theme.primary }} }});
  slide.addText("{title}", {{ x: 0.5, y: 0.3, w: 9, h: 0.8, fontSize: 32, fontFace: "Microsoft YaHei", color: theme.primary, bold: true }});
  const points = {points_json};
  points.forEach((point, i) => {{
    slide.addText("• " + point, {{ x: 0.8, y: 1.4 + i * 0.8, w: 8.5, h: 0.6, fontSize: 20, fontFace: "Microsoft YaHei", color: theme.secondary }});
  }});
  slide.addShape(pres.shapes.OVAL, {{ x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: {{ color: theme.accent }} }});
  slide.addText("{num}", {{ x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" }});
  return slide;
}}
if (require.main === module) {{
  const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9';
  createSlide(pres, {json.dumps(theme)});
  pres.writeFile({{ fileName: "./output/slide-{num:02d}.pptx" }});
}}
module.exports = {{ createSlide, slideConfig }};
'''
    
    def _gen_thank_you(self, num: int, title: str, subtitle: str, theme: Dict) -> str:
        return f'''const pptxgen = require("pptxgenjs");
const slideConfig = {{ type: 'thank_you', index: {num}, title: '{title}' }};
function createSlide(pres, theme) {{
  const slide = pres.addSlide();
  slide.background = {{ color: theme.primary }};
  slide.addShape(pres.shapes.OVAL, {{ x: 6, y: -2, w: 6, h: 6, fill: {{ color: theme.secondary, transparency: 60 }} }});
  slide.addText("{title}", {{ x: 0.5, y: 2, w: 9, h: 1.2, fontSize: 48, fontFace: "Microsoft YaHei", color: "FFFFFF", bold: true, align: "center" }});
  slide.addText("{subtitle}", {{ x: 0.5, y: 3.4, w: 9, h: 0.8, fontSize: 24, fontFace: "Microsoft YaHei", color: theme.light, align: "center" }});
  return slide;
}}
if (require.main === module) {{
  const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9';
  createSlide(pres, {json.dumps(theme)});
  pres.writeFile({{ fileName: "./output/slide-{num:02d}.pptx" }});
}}
module.exports = {{ createSlide, slideConfig }};
'''
    
    def _generate_compile_js(self, num_slides: int, theme: Dict, output_dir: str) -> str:
        return f'''const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
const theme = {json.dumps(theme)};
{chr(10).join([f"const slide{i:02d} = require('./slide-{i:02d}.js');" for i in range(1, num_slides + 1)])}
{chr(10).join([f"slide{i:02d}.createSlide(pres, theme);" for i in range(1, num_slides + 1)])}
pres.writeFile({{ fileName: './output/presentation.pptx' }}).then(() => console.log('PPT generated')).catch(err => console.error(err));
'''


# ============================================================
# 主工作流
# ============================================================

class PPTWorkflow:
    """完整的三节点工作流"""
    
    def __init__(self, style: str = "professional"):
        self.theme = STYLE_THEMES.get(style, STYLE_THEMES["professional"])
        self.analyst = AnalystNode()
        self.director = DirectorNode()
        self.designer = DesignerNode()
        self.generator = PPTXGenerator(self.theme)
    
    def run(self, topic: str, source_material: str, num_achievements: int = 3,
            output_path: str = "/tmp/ppt-maker/output/presentation.pptx") -> Dict[str, Any]:
        """执行完整工作流"""
        print(f"PPT Maker: {topic}")
        
        analysis = self.analyst.extract(source_material, topic, num_achievements)
        print(f"  Stage 1: {len(analysis.get('achievements', []))} achievements")
        
        outline = self.director.build_outline(analysis, topic)
        print(f"  Stage 2: {len(outline.get('slides', []))} slides planned")
        
        slides = self.designer.generate_slides(outline, analysis, topic)
        print(f"  Stage 3: {len(slides)} slides generated")
        
        success = self.generator.generate(slides, output_path, topic)
        
        return {
            "topic": topic,
            "analysis": analysis,
            "outline": outline,
            "slides": slides,
            "output_path": output_path if success else None,
            "success": success
        }


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="PPT Maker")
    parser.add_argument("--title", "-t", default="演示文稿", help="PPT title")
    parser.add_argument("--slides", "-s", default="", help="Slide content separated by |")
    parser.add_argument("--style", default="professional", choices=list(STYLE_THEMES.keys()), help="Style")
    parser.add_argument("--output", "-o", default="/tmp/ppt-maker/output/presentation.pptx", help="Output path")
    parser.add_argument("--source", "-i", default="", help="Source material file")
    parser.add_argument("--achievements", "-n", type=int, default=3, help="Number of achievements")
    
    args = parser.parse_args()
    
    source_material = args.source
    if args.source and os.path.exists(args.source):
        with open(args.source, 'r', encoding='utf-8') as f:
            source_material = f.read()
    
    if not source_material and args.slides:
        slides_list = args.slides.split("|")
        source_material = " | ".join([f"{i+1}. {s}" for i, s in enumerate(slides_list)])
    
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    workflow = PPTWorkflow(style=args.style)
    result = workflow.run(
        topic=args.title,
        source_material=source_material or args.title,
        num_achievements=args.achievements,
        output_path=args.output
    )
    
    if result["success"]:
        print(f"Success: {result['output_path']}")
    else:
        print("Failed to generate PPT")
        sys.exit(1)


if __name__ == "__main__":
    main()
