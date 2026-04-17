"""
职场/科研汇报卡片数据框架
Presentation Card Schema - 基于潘潘设计的标准化 Schema
"""
from typing import Dict, Any, List, Optional, Literal
from dataclasses import dataclass, field, asdict
from enum import Enum


class CardType(Enum):
    """卡片类型"""
    PAIN_POINT = "pain_point"          # 痛点/挑战
    INNOVATION = "innovation"          # 创新/方案
    METRIC = "metric"                  # 量化指标
    CONTEXT = "context"                # 背景
    PROCESS = "process"               # 流程
    QUOTE = "quote"                   # 引言
    IMAGE = "image"                   # 图片
    BEFORE_AFTER = "before_after"     # 前后对比


class LayoutStyle(Enum):
    """布局类型"""
    THREE_COLUMN_CARDS = "three_column_cards"  # 三列卡片 ⭐
    TWO_COLUMN = "two_column"
    SINGLE_FULL = "single_full"
    COVER = "cover"
    TOC = "toc"
    SUMMARY = "summary"
    THANK_YOU = "thank_you"


class SlideType(Enum):
    """幻灯片类型"""
    COVER = "cover"
    TOC = "toc"
    ACHIEVEMENT_SHOWCASE = "achievement_showcase"  # 成果展示 ⭐
    CONTEXT_BACKGROUND = "context_background"
    SUMMARY = "summary"
    THANK_YOU = "thank_you"


@dataclass
class Card:
    """
    单个卡片数据模型
    """
    card_id: str = ""
    card_type: str = "pain_point"
    header: str = ""
    body_text: str = ""
    visual_placeholder: str = ""  # icon_warning, diagram_workflow, chart_upward_trend 等
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "card_id": self.card_id,
            "card_type": self.card_type,
            "header": self.header,
            "body_text": self.body_text,
            "visual_placeholder": self.visual_placeholder,
            **self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Card":
        """从字典创建卡片"""
        return cls(
            card_id=data.get("card_id", ""),
            card_type=data.get("card_type", "pain_point"),
            header=data.get("header", ""),
            body_text=data.get("body_text", ""),
            visual_placeholder=data.get("visual_placeholder", ""),
            metadata={k: v for k, v in data.items()
                     if k not in ["card_id", "card_type", "header", "body_text", "visual_placeholder"]}
        )


@dataclass
class Slide:
    """
    单页幻灯片数据模型
    """
    slide_number: int = 1
    slide_type: str = "achievement_showcase"
    title: str = ""
    layout_style: str = "three_column_cards"
    cards: List[Card] = field(default_factory=list)
    speaker_notes: str = ""
    subtitle: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "slide_number": self.slide_number,
            "slide_type": self.slide_type,
            "title": self.title,
            "layout_style": self.layout_style,
            "subtitle": self.subtitle,
            "cards": [card.to_dict() if isinstance(card, Card) else card for card in self.cards],
            "speaker_notes": self.speaker_notes
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Slide":
        """从字典创建幻灯片"""
        cards = [Card.from_dict(c) if isinstance(c, dict) else c for c in data.get("cards", [])]
        return cls(
            slide_number=data.get("slide_number", 1),
            slide_type=data.get("slide_type", "achievement_showcase"),
            title=data.get("title", ""),
            layout_style=data.get("layout_style", "three_column_cards"),
            subtitle=data.get("subtitle"),
            cards=cards,
            speaker_notes=data.get("speaker_notes", "")
        )


@dataclass
class GlobalSettings:
    """全局设置"""
    presentation_title: str = ""
    target_audience: str = ""
    total_slides: int = 5
    theme: str = "professional"  # professional, creative, academic
    language: str = "zh-CN"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "presentation_title": self.presentation_title,
            "target_audience": self.target_audience,
            "total_slides": self.total_slides,
            "theme": self.theme,
            "language": self.language
        }


@dataclass
class Presentation:
    """
    完整演示文稿数据模型
    """
    global_settings: GlobalSettings = field(default_factory=GlobalSettings)
    slides: List[Slide] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "global_settings": self.global_settings.to_dict(),
            "slides": [slide.to_dict() if isinstance(slide, Slide) else slide for slide in self.slides]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Presentation":
        """从字典创建演示文稿"""
        settings = GlobalSettings(**data.get("global_settings", {}))
        slides = [Slide.from_dict(s) if isinstance(s, dict) else s for s in data.get("slides", [])]
        return cls(global_settings=settings, slides=slides)

    def get_achievement_slides(self) -> List[Slide]:
        """获取所有成果展示页"""
        return [s for s in self.slides if s.slide_type == "achievement_showcase"]


class PresentationSchema:
    """
    演示文稿 JSON Schema 定义
    用于验证和指导 Agent 输出
    """

    # ============================================================
    # JSON Schema - 用于结构化输出验证
    # ============================================================

    @staticmethod
    def get_schema() -> Dict[str, Any]:
        """
        获取完整 JSON Schema
        """
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "PresentationSchema",
            "description": "职场/科研汇报演示文稿数据结构",
            "type": "object",
            "required": ["global_settings", "slides"],
            "properties": {
                "global_settings": {
                    "type": "object",
                    "required": ["presentation_title", "target_audience", "total_slides"],
                    "properties": {
                        "presentation_title": {
                            "type": "string",
                            "description": "演示文稿标题",
                            "maxLength": 100
                        },
                        "target_audience": {
                            "type": "string",
                            "description": "目标受众"
                        },
                        "total_slides": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 20
                        },
                        "theme": {
                            "type": "string",
                            "enum": ["professional", "creative", "academic"],
                            "default": "professional"
                        },
                        "language": {
                            "type": "string",
                            "default": "zh-CN"
                        }
                    }
                },
                "slides": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "$ref": "#/definitions/slide"
                    }
                }
            },
            "definitions": {
                "slide": {
                    "type": "object",
                    "required": ["slide_number", "slide_type", "title", "layout_style", "cards"],
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "minimum": 1
                        },
                        "slide_type": {
                            "type": "string",
                            "enum": [
                                "cover",
                                "toc",
                                "achievement_showcase",
                                "context_background",
                                "summary",
                                "thank_you"
                            ]
                        },
                        "title": {
                            "type": "string",
                            "description": "页面主标题",
                            "maxLength": 100
                        },
                        "subtitle": {
                            "type": "string"
                        },
                        "layout_style": {
                            "type": "string",
                            "enum": [
                                "three_column_cards",
                                "two_column",
                                "single_full",
                                "cover",
                                "toc",
                                "summary",
                                "thank_you"
                            ]
                        },
                        "cards": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/card"
                            }
                        },
                        "speaker_notes": {
                            "type": "string",
                            "description": "演讲逐字稿",
                            "maxLength": 500
                        }
                    }
                },
                "card": {
                    "type": "object",
                    "required": ["card_id", "card_type", "header", "body_text"],
                    "properties": {
                        "card_id": {
                            "type": "string",
                            "description": "卡片唯一标识符",
                            "pattern": "^(context_|action_|impact_|ctx_|act_|imp_)\\d+$"
                        },
                        "card_type": {
                            "type": "string",
                            "enum": [
                                "pain_point",
                                "innovation",
                                "metric",
                                "context",
                                "process",
                                "quote",
                                "image",
                                "before_after"
                            ]
                        },
                        "header": {
                            "type": "string",
                            "description": "卡片标题",
                            "maxLength": 30
                        },
                        "body_text": {
                            "type": "string",
                            "description": "卡片正文内容",
                            "maxLength": 80
                        },
                        "visual_placeholder": {
                            "type": "string",
                            "description": "视觉元素占位符",
                            "examples": [
                                "icon_warning",
                                "icon_target",
                                "diagram_workflow",
                                "icon_gear",
                                "chart_upward_trend",
                                "icon_chart",
                                "icon_image",
                                "icon_compare"
                            ]
                        }
                    }
                }
            }
        }

    # ============================================================
    # Prompt 模板 - 用于指导 Agent 生成
    # ============================================================

    @staticmethod
    def get_system_prompt(role: str = "achievement_report") -> str:
        """
        获取系统提示词模板

        Args:
            role: 场景角色
                - "achievement_report": 成果汇报
                - "academic_defense": 学术答辩
                - "project_review": 项目述职
        """

        prompts = {
            "achievement_report": """你是一位专业的职场汇报助手，擅长将工作成果转化为结构清晰、数据有力的演示文稿。

【核心原则】
1. 每页聚焦一个核心成果，不要贪多
2. 数据说话：必须包含量化的指标
3. 逻辑清晰：背景问题 → 核心方案 → 量化成果
4. 语言精炼：幻灯片上字不如表，表不如图

【三列卡片布局】
每一项成果用三列卡片展示：
- Context Card（背景/痛点）：为什么要做这件事？
- Action Card（方案/创新）：你做了什么独特贡献？
- Impact Card（成果/影响）：带来了什么可量化的价值？

【防幻觉规则】
如果你在源材料中找不到足够信息支撑某个要点，请标注【需要人工补充】，
绝对不要自行编造数据。""",

            "academic_defense": """你是一位资深的学术答辩顾问，擅长将科研成果转化为清晰、严谨的学术汇报。

【核心原则】
1. 学术严谨：每个结论必须有文献或数据支撑
2. 创新突出：明确区分你的原创贡献与已有工作
3. 逻辑严密：问题提出 → 方法创新 → 结果验证
4. 图表为主：能用图表示的不用文字

【三列卡片布局】
- Context：研究背景与关键问题
- Innovation：核心创新点与方法突破
- Impact：实验结果与学术影响

【防幻觉规则】
未在论文中明确报告的数据必须标注【待补充】。""",

            "project_review": """你是一位经验丰富的项目评审顾问，擅长总结项目执行情况与团队贡献。

【核心原则】
1. 结果导向：突出项目交付成果
2. 量化评估：进度、质量、成本的量化指标
3. 经验沉淀：成功因素与改进空间
4. 团队协作：明确个人与团队贡献

【三列卡片布局】
- Context：项目背景与关键挑战
- Action：核心举措与创新方法
- Impact：项目成果与业务价值"""
        }

        return prompts.get(role, prompts["achievement_report"])

    @staticmethod
    def get_user_prompt_template() -> str:
        """
        获取用户输入提示词模板
        """
        return """请根据以下材料，生成演示文稿结构。

【主题】
{topic}

【目标受众】
{target_audience}

【代表性成果数量】
{num_achievements} 项

【源材料】
{source_material}

【输出要求】
请生成包含以下内容的 JSON：
1. global_settings: 演示文稿全局设置
2. slides: 幻灯片数组
   - 第1页：封面
   - 第2页：目录
   - 第3-N页：成果展示（每项成果一页，使用三列卡片布局）
   - 最后：总结 + 致谢

【三列卡片格式】
每项成果页使用 layout_style="three_column_cards"，包含三张卡片：
- pain_point: 核心痛点与挑战（背景）
- innovation: 核心技术/方案突破（行动）
- metric: 可量化成果（影响）

【JSON 格式】
{
  "global_settings": {
    "presentation_title": "...",
    "target_audience": "...",
    "total_slides": N
  },
  "slides": [
    {
      "slide_number": 1,
      "slide_type": "cover",
      "title": "封面标题",
      "layout_style": "cover",
      "cards": [],
      "speaker_notes": "..."
    },
    {
      "slide_number": 2,
      "slide_type": "achievement_showcase",
      "title": "代表性成果一：XXX",
      "layout_style": "three_column_cards",
      "cards": [
        {
          "card_id": "context_01",
          "card_type": "pain_point",
          "header": "核心痛点与挑战",
          "body_text": "...",
          "visual_placeholder": "icon_warning"
        },
        {
          "card_id": "action_01",
          "card_type": "innovation",
          "header": "核心技术/方案突破",
          "body_text": "...",
          "visual_placeholder": "icon_gear"
        },
        {
          "card_id": "impact_01",
          "card_type": "metric",
          "header": "可量化成果",
          "body_text": "...",
          "visual_placeholder": "chart_upward_trend"
        }
      ],
      "speaker_notes": "..."
    }
  ]
}"""

    @staticmethod
    def get_card_type_hints() -> Dict[str, Dict[str, str]]:
        """
        获取各卡片类型的提示
        """
        return {
            "pain_point": {
                "name": "背景/痛点卡片",
                "header_hint": "核心痛点与挑战",
                "body_hint": "限制在50字以内，简述现有流程、技术或理论存在的局限性",
                "visual": "icon_warning / icon_target",
                "examples": [
                    "原有系统响应时间超过5秒，用户体验差",
                    "年物资损耗率达15%，成本控制压力大",
                    "跨部门协作流程混乱，沟通成本高"
                ]
            },
            "innovation": {
                "name": "方案/创新卡片",
                "header_hint": "核心技术/方案突破",
                "body_hint": "限制在60字以内，强调你引入的创新方法或独特贡献",
                "visual": "icon_gear / diagram_workflow",
                "examples": [
                    "引入微服务架构，系统响应降至200ms",
                    "设计三级评审机制，质量合格率达99%",
                    "开发智能调度算法，资源利用率提升40%"
                ]
            },
            "metric": {
                "name": "成果/影响卡片",
                "header_hint": "可量化成果",
                "body_hint": "必须包含数据！效率提升%、性能指标、业务价值等",
                "visual": "chart_upward_trend / icon_chart",
                "examples": [
                    "响应时间: 5s → 200ms (降低96%)",
                    "年节省成本: 120万元 (降低35%)",
                    "用户满意度: 68分 → 92分 (+24分)"
                ]
            },
            "context": {
                "name": "背景卡片",
                "header_hint": "背景与动机",
                "body_hint": "说明做这件事的背景和初衷",
                "visual": "icon_info"
            },
            "process": {
                "name": "流程卡片",
                "header_hint": "实施路径",
                "body_hint": "主要工作步骤和方法",
                "visual": "diagram_workflow"
            },
            "before_after": {
                "name": "对比卡片",
                "header_hint": "改善前后对比",
                "body_hint": "量化对比改善前后的差异",
                "visual": "icon_compare"
            }
        }


class PresentationRenderer:
    """
    演示文稿渲染器
    根据 JSON 数据生成渲染指令
    """

    def __init__(self, theme: Optional[Dict[str, str]] = None):
        self.theme = theme or {
            "primary": "#1a365d",
            "secondary": "#2c5282",
            "accent": "#3182ce",
            "light": "#bee3f8",
            "bg": "#ffffff",
            "text": "#2d3748",
            "success": "#38a169",
            "warning": "#dd6b20",
            "danger": "#e53e3e"
        }

    def render(self, presentation: Presentation) -> List[Dict[str, Any]]:
        """
        渲染整个演示文稿
        返回每页的渲染指令列表
        """
        pages = []

        for slide in presentation.slides:
            page = self._render_slide(slide)
            pages.append(page)

        return pages

    def _render_slide(self, slide: Slide) -> Dict[str, Any]:
        """渲染单页幻灯片"""

        layout = slide.layout_style

        if layout == "three_column_cards":
            return self._render_three_column(slide)
        elif layout == "cover":
            return self._render_cover(slide)
        elif layout == "toc":
            return self._render_toc(slide)
        elif layout == "summary":
            return self._render_summary(slide)
        elif layout == "thank_you":
            return self._render_thank_you(slide)
        else:
            return self._render_default(slide)

    def _render_three_column(self, slide: Slide) -> Dict[str, Any]:
        """
        渲染三列卡片布局
        这是成果展示的核心布局
        """
        cards = slide.cards

        # 按 card_type 分类
        context_card = None
        action_card = None
        impact_card = None

        for card in cards:
            if card.card_type == "pain_point":
                context_card = card
            elif card.card_type == "innovation":
                action_card = card
            elif card.card_type == "metric":
                impact_card = card

        return {
            "type": "slide",
            "slide_number": slide.slide_number,
            "layout": "three_column_grid",
            "background": self.theme["bg"],
            "header": {
                "title": slide.title,
                "subtitle": slide.subtitle
            },
            "columns": [
                self._render_card_column(context_card, "context", self.theme["warning"]),
                self._render_card_column(action_card, "action", self.theme["accent"]),
                self._render_card_column(impact_card, "impact", self.theme["success"])
            ],
            "speaker_notes": slide.speaker_notes
        }

    def _render_card_column(
        self,
        card: Optional[Card],
        position: str,
        accent_color: str
    ) -> Dict[str, Any]:
        """渲染单列卡片"""

        if card is None:
            return {
                "position": position,
                "type": "empty",
                "accent": accent_color,
                "content": {}
            }

        return {
            "position": position,
            "type": "card",
            "accent": accent_color,
            "header": card.header,
            "body": card.body_text,
            "visual": card.visual_placeholder,
            "card_type": card.card_type
        }

    def _render_cover(self, slide: Slide) -> Dict[str, Any]:
        """渲染封面"""
        return {
            "type": "slide",
            "slide_number": slide.slide_number,
            "layout": "cover",
            "background": self.theme["primary"],
            "title": slide.title,
            "subtitle": slide.subtitle,
            "speaker_notes": slide.speaker_notes
        }

    def _render_toc(self, slide: Slide) -> Dict[str, Any]:
        """渲染目录"""
        return {
            "type": "slide",
            "slide_number": slide.slide_number,
            "layout": "toc",
            "background": self.theme["bg"],
            "title": slide.title,
            "items": [c.body_text for c in slide.cards],
            "speaker_notes": slide.speaker_notes
        }

    def _render_summary(self, slide: Slide) -> Dict[str, Any]:
        """渲染总结"""
        return {
            "type": "slide",
            "slide_number": slide.slide_number,
            "layout": "summary",
            "background": self.theme["bg"],
            "title": slide.title,
            "points": [c.body_text for c in slide.cards],
            "speaker_notes": slide.speaker_notes
        }

    def _render_thank_you(self, slide: Slide) -> Dict[str, Any]:
        """渲染致谢"""
        return {
            "type": "slide",
            "slide_number": slide.slide_number,
            "layout": "thank_you",
            "background": self.theme["primary"],
            "title": slide.title,
            "subtitle": slide.subtitle,
            "speaker_notes": slide.speaker_notes
        }

    def _render_default(self, slide: Slide) -> Dict[str, Any]:
        """默认渲染"""
        return {
            "type": "slide",
            "slide_number": slide.slide_number,
            "layout": "unknown",
            "background": self.theme["bg"],
            "title": slide.title,
            "cards": [c.to_dict() for c in slide.cards],
            "speaker_notes": slide.speaker_notes
        }
