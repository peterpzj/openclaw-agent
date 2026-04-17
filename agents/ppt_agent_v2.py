"""
PPT Agent V2 - 三节点工作流
The Analyst → The Director → The Designer
"""
from typing import Dict, Any, Optional, List
from agents.base import BaseAgent
from core.engine import AgentEngine
import json
import re


class PPTAgenV2:
    """
    PPT 生成 Agent V2
    三阶段工作流：
    1. The Analyst  - 内容提炼（严谨，低温度）
    2. The Director - 大纲构建（结构化输出）
    3. The Designer - 幻灯片生成（高质量输出）
    """

    def __init__(self, engine: AgentEngine, output_dir: str = "/tmp/ppt_agent_v2"):
        self.engine = engine
        self.output_dir = output_dir
        self.analyst = AnalystNode(engine)
        self.director = DirectorNode(engine)
        self.designer = DesignerNode(engine)

    def run(self, source_material: str, topic: str, num_achievements: int = 3) -> Dict[str, Any]:
        """
        执行完整工作流
        source_material: 源文档内容
        topic: PPT主题
        num_achievements: 提炼的核心成就数量
        """
        result = {
            "topic": topic,
            "stages": {}
        }

        # Stage 1: 内容提炼
        print("🔬 Stage 1: The Analyst - 内容提炼...")
        analysis = self.analyst.extract(
            source_material=source_material,
            topic=topic,
            num_achievements=num_achievements
        )
        result["stages"]["analysis"] = analysis

        # Stage 2: 大纲构建
        print("🎬 Stage 2: The Director - 大纲构建...")
        outline = self.director.build_outline(
            analysis=analysis,
            topic=topic
        )
        result["stages"]["outline"] = outline

        # Stage 3: 幻灯片生成
        print("🎨 Stage 3: The Designer - 幻灯片生成...")
        slides = self.designer.generate_slides(
            outline=outline,
            analysis=analysis,
            topic=topic
        )
        result["stages"]["slides"] = slides
        result["final_slides"] = slides

        print("✅ 工作流完成！")
        return result


class AnalystNode:
    """
    第一阶段：内容提炼节点 (The Analyst)
    低温设置 (0.1-0.2)，确保事实严谨
    """

    SYSTEM_PROMPT = """你是一位顶级的学术传播专家和内容策略师。

你的任务是阅读用户提供的原始材料，并从中提取出最核心、最具说服力的信息，为演示文稿做准备。

【核心原则】
1. 你必须**严格且仅基于**提供的上下文进行提取
2. 绝不能捏造数据
3. 如果在源材料中找不到足够的信息来支撑某个要点，请在要点中标注【需要人工补充】
4. 保持客观，只提炼材料中真正存在的信息

【输出格式】
提炼结果必须以严格的 JSON 格式输出，包含：
- achievements: 核心成就数组
- key_themes: 关键主题
- evidence_quality: 证据质量评估"""

    USER_TEMPLATE = """请阅读以下源材料，并为接下来的演示文稿提取核心素材。

**目标**：准备一份专业的述职/成果汇报演示文稿。
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

    def __init__(self, engine: AgentEngine):
        self.engine = engine
        self.temperature = 0.15  # 低温确保严谨

    def extract(
        self,
        source_material: str,
        topic: str,
        num_achievements: int = 3
    ) -> Dict[str, Any]:
        """执行内容提炼"""
        user_prompt = self.USER_TEMPLATE.format(
            num_achievements=num_achievements,
            source_material=source_material
        )

        response = self.engine.chat(
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.temperature
        )

        # 解析 JSON
        return self._parse_json_response(response["content"])

    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """从响应中提取 JSON"""
        try:
            # 尝试直接解析
            return json.loads(content)
        except json.JSONDecodeError:
            # 尝试提取 JSON 块
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            return {
                "achievements": [],
                "error": "JSON解析失败",
                "raw": content[:500]
            }


class DirectorNode:
    """
    第二阶段：大纲构建节点 (The Director)
    金字塔原理，结构化 JSON 输出
    """

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

    USER_TEMPLATE = """基于以下提炼出的核心成就，请规划一份演示文稿大纲。

**主题**: {topic}

**核心成就**:
{achievements}

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

    def __init__(self, engine: AgentEngine):
        self.engine = engine
        self.temperature = 0.3

    def build_outline(
        self,
        analysis: Dict[str, Any],
        topic: str
    ) -> Dict[str, Any]:
        """构建演示大纲"""
        # 格式化成就信息
        achievements_text = json.dumps(
            analysis.get("achievements", []),
            ensure_ascii=False,
            indent=2
        )

        user_prompt = self.USER_TEMPLATE.format(
            topic=topic,
            achievements=achievements_text
        )

        response = self.engine.chat(
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.temperature
        )

        return self._parse_json_response(response["content"])

    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """解析 JSON 响应"""
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            return {"slides": [], "error": "JSON解析失败"}


class DesignerNode:
    """
    第三阶段：幻灯片生成节点 (The Designer)
    高质量输出，包含演讲稿和视觉建议
    """

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

    USER_TEMPLATE = """请根据以下大纲和核心信息，生成每一页幻灯片的详细内容。

**主题**: {topic}

**演示大纲**:
{outline}

**提炼的核心信息**:
{analysis}

**输出格式（严格JSON）**:
{{
  "slides": [
    {{
      "slide_number": 1,
      "title": "当前页面的主标题",
      "subtitle": "副标题（可选）",
      "bullet_points": ["要点1 (极简)", "要点2 (极简)", "要点3 (极简)"],
      "visual_suggestion": "详细描述该页面应该配什么样的图表或意象图（例如：一张展示工作流对比的左右结构流程图，配色以冷色调为主）",
      "speaker_notes": "该页面的口语化演讲逐字稿，需要过渡自然，充满自信。控制在100-150字。"
    }}
  ]
}}"""

    def __init__(self, engine: AgentEngine):
        self.engine = engine
        self.temperature = 0.65  # 适当提高温度，让语言更流畅

    def generate_slides(
        self,
        outline: Dict[str, Any],
        analysis: Dict[str, Any],
        topic: str
    ) -> List[Dict[str, Any]]:
        """生成幻灯片内容"""
        outline_text = json.dumps(outline, ensure_ascii=False, indent=2)
        analysis_text = json.dumps(analysis, ensure_ascii=False, indent=2)

        user_prompt = self.USER_TEMPLATE.format(
            topic=topic,
            outline=outline_text,
            analysis=analysis_text
        )

        response = self.engine.chat(
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.temperature
        )

        result = self._parse_json_response(response["content"])
        return result.get("slides", [])

    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """解析 JSON 响应"""
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            return {"slides": [], "error": "JSON解析失败"}


class PPTAgenV2Agent(BaseAgent):
    """
    封装为 BaseAgent 接口的 PPT Agent V2
    """

    def __init__(self, engine: AgentEngine, **kwargs):
        system_prompt = """你是一个专业的 PPT 制作助手。

你的工作流程分为三个独立的阶段：
1. The Analyst - 阅读源文档，提炼核心成就
2. The Director - 构建演示大纲
3. The Designer - 生成具体幻灯片内容

每个阶段都是独立的 API 调用，有不同的温度设置：
- Analyst: 0.15（严谨）
- Director: 0.3（结构化）
- Designer: 0.65（流畅）

【输入格式】
用户会提供：
- topic: PPT主题
- source_material: 源文档内容
- num_achievements: 提炼成就数量（默认3项）

【输出】
最终输出包含完整的三阶段结果和生成的幻灯片内容。"""

        super().__init__(
            name="PPT助手V2",
            engine=engine,
            system_prompt=system_prompt,
            **kwargs
        )

        self.ppt_agent = PPTAgenV2(engine=engine)

    def think(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """处理 PPT 生成请求"""
        # 从任务中提取参数
        # 格式：topic: xxx | source: xxx | achievements: 3
        params = self._parse_task(task)

        result = self.ppt_agent.run(
            source_material=params.get("source", ""),
            topic=params.get("topic", "演示文稿"),
            num_achievements=params.get("achievements", 3)
        )

        return result

    def _parse_task(self, task: str) -> Dict[str, str]:
        """解析任务参数"""
        params = {"topic": "演示文稿", "source": "", "achievements": "3"}

        # 简单解析：如果任务包含特定关键词
        if "topic:" in task.lower():
            match = re.search(r'topic:\s*(.+?)(?:\n|$)', task, re.IGNORECASE)
            if match:
                params["topic"] = match.group(1).strip()

        if "source:" in task.lower():
            match = re.search(r'source:\s*(.+?)(?:\n|$)', task, re.IGNORECASE | re.DOTALL)
            if match:
                params["source"] = match.group(1).strip()

        if "achievements:" in task.lower():
            match = re.search(r'achievements:\s*(\d+)', task, re.IGNORECASE)
            if match:
                params["achievements"] = int(match.group(1))

        # 如果没有明确指定，假设整个任务就是主题
        if not params["source"]:
            # 去掉参数部分，剩下的就是主题
            params["topic"] = task.split("source:")[0].replace("topic:", "").strip() or task

        return params
