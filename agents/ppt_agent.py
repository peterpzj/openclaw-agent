"""
PPT 生成 Agent
全流程：输入主题 → 搜索内容 → 构建框架 → 生成 PPT
"""
from typing import Dict, Any, Optional, List
from agents.base import BaseAgent
from core.engine import AgentEngine
from core.memory import Memory
from core.planner import Planner
import subprocess
import os
import json
import re


class PPTAgent(BaseAgent):
    """PPT 生成 Agent"""

    def __init__(self, engine: AgentEngine, output_dir: str = "/tmp/ppt_agent", **kwargs):
        system_prompt = """你是一个专业的 PPT 制作助手。

你的工作流程：
1. 理解用户需求（主题、场景、受众）
2. 搜索相关信息，构建内容框架
3. 生成专业 PPT

你的职责：
- 清晰理解用户描述的主题
- 规划合理的 PPT 结构（封面、目录、内容、总结）
- 为每一页填充有价值的内容
- 选择合适的配色和风格

输出要求：
- 内容准确、结构清晰
- 视觉风格专业统一
- 每一页有实质内容，不空洞"""

        super().__init__(
            name="PPT助手",
            engine=engine,
            system_prompt=system_prompt,
            **kwargs
        )

        self.output_dir = output_dir
        self.current_topic = ""
        self.search_results: List[Dict[str, str]] = []
        self.slide_outline: List[Dict[str, Any]] = []

    def think(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """处理 PPT 生成任务"""
        self.current_topic = task

        # Step 1: 理解主题，构建大纲
        outline = self._build_outline(task)

        # Step 2: 搜索补充内容
        self._search_content(task, outline)

        # Step 3: 生成 PPT
        result = self._generate_ppt(outline)

        return {
            "topic": task,
            "outline": outline,
            "slides_count": len(outline),
            "output_file": result.get("file_path", ""),
            "status": result.get("status", "completed")
        }

    def _build_outline(self, topic: str) -> List[Dict[str, Any]]:
        """构建 PPT 大纲"""
        # 使用 LLM 生成大纲
        prompt = f"""为主题「{topic}」设计一个 PPT 结构。

要求：
- 8-15 页
- 结构：封面 → 目录 → 背景/问题 → 核心内容（3-5页） → 案例/实践 → 总结
- 每页有明确的标题和要点

请以 JSON 格式输出，格式如下：
[
  {{"page": 1, "type": "cover", "title": "封面标题", "subtitle": "副标题"}},
  {{"page": 2, "type": "toc", "title": "目录"}},
  ...
]

只输出 JSON，不要其他文字。"""

        response = self.engine.chat(
            messages=[{"role": "user", "content": prompt}],
            system="你是一个 PPT 结构规划助手，擅长设计专业的演示文稿结构。"
        )

        try:
            # 提取 JSON
            content = response["content"]
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                outline = json.loads(json_match.group())
            else:
                outline = json.loads(content)
        except:
            # 默认大纲
            outline = [
                {"page": 1, "type": "cover", "title": topic, "subtitle": "主题演讲"},
                {"page": 2, "type": "toc", "title": "目录"},
                {"page": 3, "type": "content", "title": "背景介绍"},
                {"page": 4, "type": "content", "title": "核心内容"},
                {"page": 5, "type": "content", "title": "实践案例"},
                {"page": 6, "type": "summary", "title": "总结与展望"},
            ]

        self.slide_outline = outline
        return outline

    def _search_content(self, topic: str, outline: List[Dict[str, Any]]) -> None:
        """搜索内容补充大纲"""
        # 为每页内容搜索相关资料
        for slide in outline:
            if slide.get("type") == "content":
                title = slide.get("title", "")
                # 调用搜索（这里需要工具支持）
                self.search_results.append({
                    "page": slide["page"],
                    "title": title,
                    "query": f"{topic} {title}",
                    "content": ""  # 后续填充
                })

    def _generate_ppt(self, outline: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成 PPT 文件"""
        try:
            # 创建输出目录
            slides_dir = os.path.join(self.output_dir, "slides")
            output_dir = os.path.join(slides_dir, "output")
            os.makedirs(output_dir, exist_ok=True)

            # 生成 slides JS 文件
            for i, slide in enumerate(outline):
                slide_num = i + 1
                self._generate_slide_js(slides_dir, slide_num, slide)

            # 生成 compile.js
            self._generate_compile_js(slides_dir, len(outline))

            # 运行编译
            result = subprocess.run(
                ["node", "compile.js"],
                cwd=slides_dir,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                output_file = os.path.join(output_dir, "presentation.pptx")
                return {
                    "status": "success",
                    "file_path": output_file
                }
            else:
                return {
                    "status": "error",
                    "error": result.stderr
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def _generate_slide_js(self, slides_dir: str, num: int, slide: Dict[str, Any]) -> None:
        """生成单页 JS 文件"""
        page_type = slide.get("type", "content")
        title = slide.get("title", "")
        subtitle = slide.get("subtitle", "")

        # 选择主题配色
        theme = {
            "primary": "1a365d",    # 深蓝
            "secondary": "2c5282",  # 中蓝
            "accent": "3182ce",     # 亮蓝
            "light": "bee3f8",      # 浅蓝
            "bg": "ffffff"          # 白色背景
        }

        # 根据页面类型生成不同内容
        if page_type == "cover":
            content = self._gen_cover_slide(num, title, subtitle, theme)
        elif page_type == "toc":
            content = self._gen_toc_slide(num, title, theme)
        elif page_type == "summary":
            content = self._gen_summary_slide(num, title, theme)
        else:
            content = self._gen_content_slide(num, title, theme)

        # 写入文件
        filename = os.path.join(slides_dir, f"slide-{num:02d}.js")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    def _gen_cover_slide(self, num: int, title: str, subtitle: str, theme: Dict) -> str:
        return f'''const pptxgen = require("pptxgenjs");

const slideConfig = {{
  type: 'cover',
  index: {num},
  title: '{title}'
}};

function createSlide(pres, theme) {{
  const slide = pres.addSlide();
  slide.background = {{ color: theme.primary }};

  // 装饰圆形
  slide.addShape(pres.shapes.OVAL, {{
    x: -1, y: -1, w: 4, h: 4,
    fill: {{ color: theme.secondary, transparency: 50 }}
  }});
  slide.addShape(pres.shapes.OVAL, {{
    x: 7, y: 3, w: 5, h: 5,
    fill: {{ color: theme.accent, transparency: 40 }}
  }});

  // 主标题
  slide.addText("{title}", {{
    x: 0.5, y: 1.8, w: 9, h: 1.5,
    fontSize: 48, fontFace: "Microsoft YaHei",
    color: "FFFFFF", bold: true, align: "center"
  }});

  // 副标题
  slide.addText("{subtitle}", {{
    x: 0.5, y: 3.5, w: 9, h: 0.8,
    fontSize: 24, fontFace: "Microsoft YaHei",
    color: theme.light, align: "center"
  }});

  return slide;
}}

if (require.main === module) {{
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  createSlide(pres, {theme});
  pres.writeFile({{ fileName: "./output/slide-{num:02d}.pptx" }});
}}

module.exports = {{ createSlide, slideConfig }};
'''

    def _gen_toc_slide(self, num: int, title: str, theme: Dict) -> str:
        return f'''const pptxgen = require("pptxgenjs");

const slideConfig = {{
  type: 'toc',
  index: {num},
  title: '{title}'
}};

function createSlide(pres, theme) {{
  const slide = pres.addSlide();
  slide.background = {{ color: theme.bg }};

  // 左侧色块
  slide.addShape(pres.shapes.RECTANGLE, {{
    x: 0, y: 0, w: 0.15, h: 5.625,
    fill: {{ color: theme.primary }}
  }});

  // 标题
  slide.addText("{title}", {{
    x: 0.5, y: 0.3, w: 9, h: 0.8,
    fontSize: 36, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  }});

  // 目录项
  const items = [
    "背景介绍",
    "核心内容", 
    "实践案例",
    "总结展望"
  ];

  items.forEach((item, i) => {{
    slide.addText(`0{{i+1}}  ${{item}}`, {{
      x: 1, y: 1.5 + i * 0.9, w: 8, h: 0.7,
      fontSize: 24, fontFace: "Microsoft YaHei",
      color: theme.secondary
    }});
  }});

  // 页码
  slide.addText("{num}", {{
    x: 9.3, y: 5.1, w: 0.4, h: 0.4,
    fontSize: 12, fontFace: "Arial",
    color: theme.accent, align: "center", valign: "middle"
  }});

  return slide;
}}

if (require.main === module) {{
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  createSlide(pres, {theme});
  pres.writeFile({{ fileName: "./output/slide-{num:02d}.pptx" }});
}}

module.exports = {{ createSlide, slideConfig }};
'''

    def _gen_content_slide(self, num: int, title: str, theme: Dict) -> str:
        return f'''const pptxgen = require("pptxgenjs");

const slideConfig = {{
  type: 'content',
  index: {num},
  title: '{title}'
}};

function createSlide(pres, theme) {{
  const slide = pres.addSlide();
  slide.background = {{ color: theme.bg }};

  // 顶部色带
  slide.addShape(pres.shapes.RECTANGLE, {{
    x: 0, y: 0, w: 10, h: 0.08,
    fill: {{ color: theme.primary }}
  }});

  // 页面标题
  slide.addText("{title}", {{
    x: 0.5, y: 0.3, w: 9, h: 0.8,
    fontSize: 32, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  }});

  // 内容区域 - 左右布局
  // 左侧要点
  const points = [
    "要点一：清晰明了",
    "要点二：重点突出",
    "要点三：逻辑清晰"
  ];

  points.forEach((point, i) => {{
    // 圆点标记
    slide.addShape(pres.shapes.OVAL, {{
      x: 0.6, y: 1.4 + i * 0.7, w: 0.15, h: 0.15,
      fill: {{ color: theme.accent }}
    }});
    slide.addText(point, {{
      x: 0.9, y: 1.3 + i * 0.7, w: 4, h: 0.5,
      fontSize: 18, fontFace: "Microsoft YaHei",
      color: theme.secondary
    }});
  }});

  // 右侧色块装饰
  slide.addShape(pres.shapes.RECTANGLE, {{
    x: 5.5, y: 1.2, w: 4, h: 3.5,
    fill: {{ color: theme.light, transparency: 50 }}
  }});
  slide.addText("核心\\n观点", {{
    x: 5.5, y: 2.2, w: 4, h: 1.5,
    fontSize: 36, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true, align: "center", valign: "middle"
  }});

  // 页码
  slide.addShape(pres.shapes.OVAL, {{
    x: 9.3, y: 5.1, w: 0.4, h: 0.4,
    fill: {{ color: theme.accent }}
  }});
  slide.addText("{num}", {{
    x: 9.3, y: 5.1, w: 0.4, h: 0.4,
    fontSize: 12, fontFace: "Arial",
    color: "FFFFFF", bold: true,
    align: "center", valign: "middle"
  }});

  return slide;
}}

if (require.main === module) {{
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  createSlide(pres, {theme});
  pres.writeFile({{ fileName: "./output/slide-{num:02d}.pptx" }});
}}

module.exports = {{ createSlide, slideConfig }};
'''

    def _gen_summary_slide(self, num: int, title: str, theme: Dict) -> str:
        return f'''const pptxgen = require("pptxgenjs");

const slideConfig = {{
  type: 'summary',
  index: {num},
  title: '{title}'
}};

function createSlide(pres, theme) {{
  const slide = pres.addSlide();
  slide.background = {{ color: theme.primary }};

  // 装饰
  slide.addShape(pres.shapes.OVAL, {{
    x: 6, y: -2, w: 6, h: 6,
    fill: {{ color: theme.secondary, transparency: 60 }}
  }});

  // 标题
  slide.addText("{title}", {{
    x: 0.5, y: 0.5, w: 9, h: 1,
    fontSize: 36, fontFace: "Microsoft YaHei",
    color: "FFFFFF", bold: true, align: "center"
  }});

  // 总结要点
  const summaries = [
    "✓ 核心要点一",
    "✓ 核心要点二", 
    "✓ 核心要点三"
  ];

  summaries.forEach((item, i) => {{
    slide.addText(item, {{
      x: 2, y: 2 + i * 0.8, w: 6, h: 0.6,
      fontSize: 24, fontFace: "Microsoft YaHei",
      color: theme.light, align: "center"
    }});
  }});

  // 结束语
  slide.addText("感谢聆听", {{
    x: 0.5, y: 4.5, w: 9, h: 0.8,
    fontSize: 28, fontFace: "Microsoft YaHei",
    color: theme.accent, align: "center"
  }});

  return slide;
}}

if (require.main === module) {{
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  createSlide(pres, {theme});
  pres.writeFile({{ fileName: "./output/slide-{num:02d}.pptx" }});
}}

module.exports = {{ createSlide, slideConfig }};
'''

    def _generate_compile_js(self, slides_dir: str, total_slides: int) -> None:
        """生成编译脚本"""
        compile_js = '''const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

// 主题配置
const theme = {
  primary: "1a365d",
  secondary: "2c5282",
  accent: "3182ce",
  light: "bee3f8",
  bg: "ffffff"
};

// 加载并创建所有幻灯片
'''

        for i in range(total_slides):
            num = i + 1
            compile_js += f'''
const slide{num:02d} = require('./slide-{num:02d}.js');
slide{num:02d}.createSlide(pres, theme);
'''

        compile_js += '''
// 输出文件
pres.writeFile({ fileName: './output/presentation.pptx' })
  .then(() => console.log('PPT generated: ./output/presentation.pptx'))
  .catch(err => console.error('Error:', err));
'''

        with open(os.path.join(slides_dir, "compile.js"), "w", encoding="utf-8") as f:
            f.write(compile_js)

    def run_interactive(self, topic: str) -> Dict[str, Any]:
        """交互式运行"""
        print(f"📊 开始为「{topic}」生成 PPT...")
        print("=" * 50)

        # 1. 构建大纲
        print("📝 步骤1: 构建 PPT 结构...")
        outline = self._build_outline(topic)
        print(f"   已规划 {len(outline)} 页")

        # 2. 搜索内容
        print("🔍 步骤2: 搜索补充内容...")
        self._search_content(topic, outline)
        print("   内容搜索完成")

        # 3. 生成 PPT
        print("🎨 步骤3: 生成 PPT 文件...")
        result = self._generate_ppt(outline)

        if result.get("status") == "success":
            print(f"   ✅ 生成成功: {result.get('file_path')}")
        else:
            print(f"   ❌ 生成失败: {result.get('error')}")

        return self.think(topic, {})


if __name__ == "__main__":
    engine = AgentEngine()
    agent = PPTAgent(engine=engine)

    # 测试
    result = agent.run_interactive("人工智能在医疗领域的应用")
    print("\n结果:", result)
