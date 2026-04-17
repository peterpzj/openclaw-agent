"""
卡片式 PPT 生成框架
核心思路：内容生成与布局渲染解耦
- Agent 负责输出结构化卡片 JSON
- 框架负责根据卡片类型自动渲染
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
import json


class CardType(Enum):
    """卡片类型枚举"""
    # 封面类
    COVER = "cover"                    # 封面

    # 导航类
    TOC = "toc"                       # 目录
    SECTION_DIVIDER = "section"        # 章节分隔页

    # 内容类
    TITLE_ONLY = "title_only"          # 仅标题
    BULLET_LIST = "bullet_list"        # 要点列表
    DATA_POINT = "data_point"          # 数据点卡片
    BEFORE_AFTER = "before_after"       # 对比卡片（前后对比）
    TIMELINE = "timeline"              # 时间线卡片
    PROCESS_FLOW = "process_flow"       # 流程图卡片
    QUOTE = "quote"                    # 引言/金句卡片
    IMAGE_WITH_CAPTION = "image_with_caption"  # 图文卡片

    # 数据类
    CHART = "chart"                   # 图表卡片
    STATS_CARD = "stats_card"          # 统计数字卡片

    # 结束类
    SUMMARY = "summary"                # 总结页
    THANK_YOU = "thank_you"            # 致谢页


@dataclass
class BaseCard:
    """基础卡片"""
    type: str = ""
    title: str = ""
    subtitle: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CoverCard(BaseCard):
    """封面卡片"""
    type: str = "cover"
    title: str = ""
    subtitle: str = ""
    author: str = ""
    date: str = ""
    background_color: str = "#1a365d"


@dataclass
class TOCCard(BaseCard):
    """目录卡片"""
    type: str = "toc"
    title: str = "目录"
    items: List[str] = field(default_factory=list)


@dataclass
class SectionDividerCard(BaseCard):
    """章节分隔卡片"""
    type: str = "section"
    section_number: str = ""
    title: str = ""
    subtitle: str = ""


@dataclass
class BulletListCard(BaseCard):
    """要点列表卡片"""
    type: str = "bullet_list"
    title: str = ""
    bullets: List[str] = field(default_factory=list)
    emphasis: Optional[int] = None  # 第几个要点需要强调


@dataclass
class DataPointCard(BaseCard):
    """数据点卡片"""
    type: str = "data_point"
    title: str = ""
    metric_label: str = ""     # 指标名称
    metric_value: str = ""      # 数值
    metric_unit: str = ""       # 单位
    change: Optional[str] = None  # 变化（如 "+35%"）
    description: str = ""


@dataclass
class BeforeAfterCard(BaseCard):
    """对比卡片"""
    type: str = "before_after"
    title: str = ""
    before_label: str = "Before"
    before_content: str = ""
    after_label: str = "After"
    after_content: str = ""


@dataclass
class TimelineCard(BaseCard):
    """时间线卡片"""
    type: str = "timeline"
    title: str = ""
    events: List[Dict[str, str]] = field(default_factory=list)
    # [{"time": "2023.01", "event": "事件描述"}, ...]


@dataclass
class ProcessFlowCard(BaseCard):
    """流程卡片"""
    type: str = "process_flow"
    title: str = ""
    steps: List[Dict[str, str]] = field(default_factory=list)
    # [{"step": "1", "title": "步骤名", "description": "描述"}, ...]


@dataclass
class QuoteCard(BaseCard):
    """引言卡片"""
    type: str = "quote"
    quote_text: str = ""
    author: str = ""
    context: str = ""


@dataclass
class ImageCaptionCard(BaseCard):
    """图文卡片"""
    type: str = "image_with_caption"
    title: str = ""
    image_description: str = ""   # 图片内容描述
    caption: str = ""             # 图注
    layout: str = "left"         # 图片位置: left/right


@dataclass
class StatsCard(BaseCard):
    """统计卡片组"""
    type: str = "stats_card"
    title: str = ""
    stats: List[Dict[str, str]] = field(default_factory=list)
    # [{"value": "92", "label": "满意度", "unit": "分"}, ...]


@dataclass
class SummaryCard(BaseCard):
    """总结卡片"""
    type: str = "summary"
    title: str = "总结"
    key_points: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)


@dataclass
class ThankYouCard(BaseCard):
    """致谢卡片"""
    type: str = "thank_you"
    title: str = "感谢聆听"
    subtitle: str = ""
    contact: str = ""


class CardSchema:
    """
    卡片 JSON Schema 定义
    用于验证和指导 Agent 输出
    """

    @staticmethod
    def get_schema() -> Dict[str, Any]:
        """获取完整 Schema"""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "PPTCard",
            "description": "PPT 卡片数据模型",
            "type": "object",
            "required": ["type", "title"],
            "oneOf": [
                {"$ref": "#/definitions/cover"},
                {"$ref": "#/definitions/toc"},
                {"$ref": "#/definitions/section"},
                {"$ref": "#/definitions/bullet_list"},
                {"$ref": "#/definitions/data_point"},
                {"$ref": "#/definitions/before_after"},
                {"$ref": "#/definitions/timeline"},
                {"$ref": "#/definitions/process_flow"},
                {"$ref": "#/definitions/quote"},
                {"$ref": "#/definitions/image_with_caption"},
                {"$ref": "#/definitions/stats_card"},
                {"$ref": "#/definitions/summary"},
                {"$ref": "#/definitions/thank_you"},
            ],
            "definitions": {
                "cover": {
                    "type": "object",
                    "properties": {
                        "type": {"const": "cover"},
                        "title": {"type": "string", "maxLength": 50},
                        "subtitle": {"type": "string"},
                        "author": {"type": "string"},
                        "date": {"type": "string"}
                    },
                    "required": ["type", "title"]
                },
                "toc": {
                    "type": "object",
                    "properties": {
                        "type": {"const": "toc"},
                        "title": {"type": "string"},
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                            "maxItems": 6
                        }
                    }
                },
                "bullet_list": {
                    "type": "object",
                    "properties": {
                        "type": {"const": "bullet_list"},
                        "title": {"type": "string"},
                        "bullets": {
                            "type": "array",
                            "items": {"type": "string"},
                            "maxItems": 5
                        }
                    }
                },
                "data_point": {
                    "type": "object",
                    "properties": {
                        "type": {"const": "data_point"},
                        "title": {"type": "string"},
                        "metric_label": {"type": "string"},
                        "metric_value": {"type": "string"},
                        "metric_unit": {"type": "string"},
                        "change": {"type": "string"},
                        "description": {"type": "string"}
                    }
                },
                "before_after": {
                    "type": "object",
                    "properties": {
                        "type": {"const": "before_after"},
                        "title": {"type": "string"},
                        "before_label": {"type": "string"},
                        "before_content": {"type": "string"},
                        "after_label": {"type": "string"},
                        "after_content": {"type": "string"}
                    }
                },
                "timeline": {
                    "type": "object",
                    "properties": {
                        "type": {"const": "timeline"},
                        "title": {"type": "string"},
                        "events": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "time": {"type": "string"},
                                    "event": {"type": "string"}
                                }
                            }
                        }
                    }
                },
                "process_flow": {
                    "type": "object",
                    "properties": {
                        "type": {"const": "process_flow"},
                        "title": {"type": "string"},
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "step": {"type": "string"},
                                    "title": {"type": "string"},
                                    "description": {"type": "string"}
                                }
                            }
                        }
                    }
                },
                "quote": {
                    "type": "object",
                    "properties": {
                        "type": {"const": "quote"},
                        "quote_text": {"type": "string"},
                        "author": {"type": "string"},
                        "context": {"type": "string"}
                    }
                },
                "image_with_caption": {
                    "type": "object",
                    "properties": {
                        "type": {"const": "image_with_caption"},
                        "title": {"type": "string"},
                        "image_description": {"type": "string"},
                        "caption": {"type": "string"},
                        "layout": {"enum": ["left", "right"]}
                    }
                },
                "stats_card": {
                    "type": "object",
                    "properties": {
                        "type": {"const": "stats_card"},
                        "title": {"type": "string"},
                        "stats": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": "string"},
                                    "label": {"type": "string"},
                                    "unit": {"type": "string"}
                                }
                            }
                        }
                    }
                },
                "summary": {
                    "type": "object",
                    "properties": {
                        "type": {"const": "summary"},
                        "title": {"type": "string"},
                        "key_points": {"type": "array", "items": {"type": "string"}},
                        "next_steps": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "thank_you": {
                    "type": "object",
                    "properties": {
                        "type": {"const": "thank_you"},
                        "title": {"type": "string"},
                        "subtitle": {"type": "string"},
                        "contact": {"type": "string"}
                    }
                }
            }
        }

    @staticmethod
    def get_card_prompts() -> Dict[str, str]:
        """
        获取各类卡片的 Prompt 模板
        用于指导 Agent 生成特定类型的卡片
        """
        return {
            "cover": """生成封面卡片：
- title: 主标题（简洁有力，不超过50字）
- subtitle: 副标题（补充说明）
- author: 演讲者姓名
- date: 日期

示例输出：
{"type": "cover", "title": "2024年度工作述职", "subtitle": "门诊流程优化与质控提升", "author": "张三", "date": "2024年12月"}""",

            "toc": """生成目录卡片：
- title: 通常为"目录"或"CONTENTS"
- items: 3-6个章节目录项

示例输出：
{"type": "toc", "title": "目录", "items": ["背景与挑战", "核心成就", "实践案例", "总结展望"]}""",

            "bullet_list": """生成要点列表卡片：
- title: 页面标题
- bullets: 3-5个精炼要点（每条不超过20字）
- emphasis（可选）: 强调第几个要点

示例输出：
{"type": "bullet_list", "title": "门诊优化三大举措", "bullets": ["智能预约系统", "诊间结算", "分诊流程再造"], "emphasis": 1}""",

            "data_point": """生成数据点卡片（用于展示核心数据）：
- title: 卡片标题
- metric_label: 指标名称
- metric_value: 数值
- metric_unit: 单位
- change: 变化值（如 "+35%"）
- description: 一句话描述

示例输出：
{"type": "data_point", "title": "患者满意度", "metric_label": "满意度评分", "metric_value": "92", "metric_unit": "分", "change": "+24", "description": "较去年同期显著提升"}""",

            "before_after": """生成对比卡片（展示变革前后）：
- title: 对比主题
- before_label: "改善前"
- before_content: 改善前的问题描述
- after_label: "改善后"
- after_content: 改善后的效果

示例输出：
{"type": "before_after", "title": "就诊流程变革", "before_label": "改善前", "before_content": "平均等待45分钟", "after_label": "改善后", "after_content": "等待时间缩短至18分钟"}""",

            "timeline": """生成时间线卡片：
- title: 时间线标题
- events: 时间事件列表
  - time: 时间节点
  - event: 事件描述

示例输出：
{"type": "timeline", "title": "项目推进历程", "events": [{"time": "2024.01", "event": "启动调研"}, {"time": "2024.03", "event": "系统上线"}, {"time": "2024.06", "event": "全面推广"}]}""",

            "process_flow": """生成流程卡片：
- title: 流程名称
- steps: 步骤列表
  - step: 步骤编号
  - title: 步骤名称
  - description: 步骤描述

示例输出：
{"type": "process_flow", "title": "日间化疗流程", "steps": [{"step": "1", "title": "预约", "description": "线上预约"}, {"step": "2", "title": "评估", "description": "医生评估"}, {"step": "3", "title": "治疗", "description": "当日完成"}]}""",

            "quote": """生成引言卡片：
- quote_text: 引言内容
- author: 引言作者
- context: 引言背景

示例输出：
{"type": "quote", "quote_text": "以患者为中心的服务理念", "author": "科训理念", "context": "我们始终坚持以患者需求为导向"}""",

            "stats_card": """生成统计卡片组：
- title: 卡片标题
- stats: 统计数据列表
  - value: 数值
  - label: 标签
  - unit: 单位

示例输出：
{"type": "stats_card", "title": "年度成果一览", "stats": [{"value": "2000+", "label": "服务患者", "unit": "人次"}, {"value": "40%", "label": "能力提升", "unit": ""}, {"value": "62%", "label": "不良事件下降", "unit": ""}]}""",

            "summary": """生成总结卡片：
- title: 通常为"总结"或"小结"
- key_points: 核心要点（3-5条）
- next_steps: 下一步计划（可选）

示例输出：
{"type": "summary", "title": "总结与展望", "key_points": ["流程优化效果显著", "患者满意度大幅提升", "质控体系持续完善"], "next_steps": ["扩大试点范围", "优化信息系统"]}""",

            "thank_you": """生成致谢卡片：
- title: 通常为"感谢聆听"
- subtitle: 副标题
- contact: 联系方式

示例输出：
{"type": "thank_you", "title": "感谢聆听", "subtitle": "欢迎批评指正", "contact": "联系邮箱: xxx@hospital.com"}"""
        }


class CardRenderer:
    """
    卡片渲染器
    根据卡片类型和数据生成渲染指令
    """

    def __init__(self, theme: Optional[Dict[str, str]] = None):
        self.theme = theme or {
            "primary": "#1a365d",
            "secondary": "#2c5282",
            "accent": "#3182ce",
            "light": "#bee3f8",
            "bg": "#ffffff",
            "text": "#2d3748"
        }

    def render(self, card_data: Dict[str, Any]) -> Dict[str, Any]:
        """渲染单个卡片"""
        card_type = card_data.get("type", "")

        renderers = {
            "cover": self._render_cover,
            "toc": self._render_toc,
            "section": self._render_section,
            "bullet_list": self._render_bullet_list,
            "data_point": self._render_data_point,
            "before_after": self._render_before_after,
            "timeline": self._render_timeline,
            "process_flow": self._render_process_flow,
            "quote": self._render_quote,
            "stats_card": self._render_stats_card,
            "summary": self._render_summary,
            "thank_you": self._render_thank_you,
        }

        renderer = renderers.get(card_type, self._render_default)
        return renderer(card_data)

    def _render_cover(self, card: Dict) -> Dict:
        """渲染封面"""
        return {
            "layout": "full",
            "background": card.get("background_color", self.theme["primary"]),
            "elements": [
                {"type": "text", "content": card.get("title", ""), "style": "h1", "align": "center"},
                {"type": "text", "content": card.get("subtitle", ""), "style": "subtitle", "align": "center"},
                {"type": "text", "content": card.get("author", ""), "style": "body", "align": "center"},
                {"type": "text", "content": card.get("date", ""), "style": "body", "align": "center"},
            ]
        }

    def _render_toc(self, card: Dict) -> Dict:
        """渲染目录"""
        items = card.get("items", [])
        elements = [
            {"type": "text", "content": card.get("title", "目录"), "style": "h2"}
        ]
        for i, item in enumerate(items, 1):
            elements.append({
                "type": "text",
                "content": f"{i}. {item}",
                "style": "list_item",
                "index": i
            })

        return {
            "layout": "left_aligned",
            "background": self.theme["bg"],
            "elements": elements
        }

    def _render_bullet_list(self, card: Dict) -> Dict:
        """渲染要点列表"""
        bullets = card.get("bullets", [])
        emphasis_idx = card.get("emphasis", None)

        elements = [
            {"type": "text", "content": card.get("title", ""), "style": "h2"}
        ]

        for i, bullet in enumerate(bullets, 1):
            is_emphasis = (emphasis_idx is not None and i == emphasis_idx)
            elements.append({
                "type": "bullet",
                "content": bullet,
                "style": "emphasis" if is_emphasis else "normal",
                "index": i
            })

        return {
            "layout": "bullet_list",
            "background": self.theme["bg"],
            "elements": elements
        }

    def _render_data_point(self, card: Dict) -> Dict:
        """渲染数据点"""
        return {
            "layout": "centered",
            "background": self.theme["bg"],
            "elements": [
                {"type": "text", "content": card.get("title", ""), "style": "h3"},
                {"type": "metric", "content": card.get("metric_value", ""), "unit": card.get("metric_unit", ""), "style": "metric_large"},
                {"type": "text", "content": card.get("metric_label", ""), "style": "label"},
                {"type": "text", "content": card.get("change", ""), "style": "change_badge"} if card.get("change") else None,
                {"type": "text", "content": card.get("description", ""), "style": "body"},
            ]
        }

    def _render_before_after(self, card: Dict) -> Dict:
        """渲染对比卡片"""
        return {
            "layout": "two_column",
            "background": self.theme["bg"],
            "elements": [
                {"type": "text", "content": card.get("title", ""), "style": "h2"},
                {"type": "column", "label": card.get("before_label", "Before"), "content": card.get("before_content", ""), "side": "left"},
                {"type": "column", "label": card.get("after_label", "After"), "content": card.get("after_content", ""), "side": "right"},
            ]
        }

    def _render_summary(self, card: Dict) -> Dict:
        """渲染总结"""
        key_points = card.get("key_points", [])
        next_steps = card.get("next_steps", [])

        elements = [
            {"type": "text", "content": card.get("title", "总结"), "style": "h2"}
        ]

        if key_points:
            elements.append({"type": "text", "content": "核心要点", "style": "h3"})
            for point in key_points:
                elements.append({"type": "bullet", "content": point, "style": "normal"})

        if next_steps:
            elements.append({"type": "text", "content": "下一步", "style": "h3"})
            for step in next_steps:
                elements.append({"type": "bullet", "content": step, "style": "normal"})

        return {
            "layout": "summary",
            "background": self.theme["bg"],
            "elements": elements
        }

    def _render_thank_you(self, card: Dict) -> Dict:
        """渲染致谢"""
        return {
            "layout": "full",
            "background": self.theme["primary"],
            "elements": [
                {"type": "text", "content": card.get("title", "感谢聆听"), "style": "h1", "color": "white"},
                {"type": "text", "content": card.get("subtitle", ""), "style": "subtitle", "color": "white"},
                {"type": "text", "content": card.get("contact", ""), "style": "body", "color": "white"},
            ]
        }

    def _render_default(self, card: Dict) -> Dict:
        """默认渲染"""
        return {
            "layout": "unknown",
            "background": self.theme["bg"],
            "elements": [
                {"type": "text", "content": card.get("title", ""), "style": "h2"},
                {"type": "text", "content": str(card), "style": "body"},
            ]
        }

    # 其他渲染方法省略（保持简洁）...
    def _render_section(self, card): return self._render_default(card)
    def _render_timeline(self, card): return self._render_default(card)
    def _render_process_flow(self, card): return self._render_default(card)
    def _render_quote(self, card): return self._render_default(card)
    def _render_stats_card(self, card): return self._render_default(card)
