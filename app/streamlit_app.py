"""
PPT Agent 卡片式框架 - Streamlit 前端
快速原型开发，用于验证 Agent 逻辑
"""
import streamlit as st
import json
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.ppt_agent_v2 import PPTAgenV2, AnalystNode, DirectorNode, DesignerNode
from agents.cards import CardSchema, CardRenderer, CardType
from core.engine import AgentEngine


# 页面配置
st.set_page_config(
    page_title="PPT Agent - 卡片式生成框架",
    page_icon="📊",
    layout="wide"
)


# 侧边栏配置
with st.sidebar:
    st.title("⚙️ 配置")

    api_mode = st.selectbox(
        "模型模式",
        ["demo", "openai", "gemini", "claude"],
        index=0,
        help="选择使用的模型提供商"
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.05,
        help="较低的temperature更确定性输出"
    )

    st.divider()

    st.markdown("### 📋 工作流程")
    st.markdown("""
    1. **输入材料** - 粘贴源文档
    2. **提炼成就** - 分析3项核心成就
    3. **构建大纲** - 规划幻灯片结构
    4. **生成卡片** - 输出卡片式内容
    5. **预览渲染** - 实时预览效果
    """)


# 主界面
st.title("📊 PPT Agent - 卡片式生成框架")
st.markdown("基于三节点工作流的智能 PPT 生成系统")

# 初始化引擎
engine = AgentEngine()

# 输入区域
st.markdown("## 📥 输入")

col1, col2 = st.columns([1, 1])

with col1:
    topic = st.text_input(
        "PPT 主题",
        value="2024年度工作述职报告",
        help="输入本次汇报的主题"
    )

    num_achievements = st.number_input(
        "提炼核心成就数量",
        min_value=1,
        max_value=5,
        value=3,
        help="从材料中提炼的代表性成就数量"
    )

with col2:
    source_material = st.text_area(
        "源材料",
        value="",
        placeholder="粘贴你的工作材料、述职内容、项目文档...",
        height=200,
        help="输入原始材料，Agent 将从中提炼核心内容"
    )

# 示例材料按钮
if st.button("📋 加载示例材料"):
    source_material = """
    【2024年度工作总结】

    一、门诊流程优化
    - 原有门诊流程平均等待时间超过45分钟，患者满意度评分仅68分
    - 引入智能预约系统，优化分诊流程，实施诊间结算
    - 结果：等待时间缩短至18分钟，满意度提升至92分

    二、日间化疗服务扩展
    - 化疗床位紧张，住院化疗患者平均等待床位时间3.5天
    - 建立日间化疗中心，增加6个专用床位，实施标准化治疗路径
    - 结果：日均服务能力提升40%，服务患者超2000人次

    三、医疗质量安全管理
    - 原有质控体系分散，缺乏统一标准
    - 建立多学科质控团队，实施PDCA循环管理
    - 结果：医疗不良事件下降62%，达到三甲评审标准
    """
    st.session_state.source_material = source_material

if 'source_material' in st.session_state:
    source_material = st.session_state.source_material

# 执行按钮
st.markdown("---")
run_workflow = st.button("🚀 运行完整工作流", type="primary", use_container_width=True)

if run_workflow and source_material:
    st.markdown("## 🔄 执行工作流")

    progress_bar = st.progress(0)
    status_text = st.empty()

    # Stage 1: 分析提炼
    status_text.text("🔬 Stage 1: The Analyst - 内容提炼中...")
    progress_bar.progress(20)

    analyst = AnalystNode(engine)
    analysis = analyst.extract(
        source_material=source_material,
        topic=topic,
        num_achievements=num_achievements
    )

    st.session_state.analysis = analysis

    # Stage 2: 大纲构建
    status_text.text("🎬 Stage 2: The Director - 大纲构建中...")
    progress_bar.progress(50)

    director = DirectorNode(engine)
    outline = director.build_outline(
        analysis=analysis,
        topic=topic
    )

    st.session_state.outline = outline

    # Stage 3: 卡片生成
    status_text.text("🎨 Stage 3: The Designer - 卡片生成中...")
    progress_bar.progress(80)

    designer = DesignerNode(engine)
    slides = designer.generate_slides(
        outline=outline,
        analysis=analysis,
        topic=topic
    )

    st.session_state.slides = slides
    progress_bar.progress(100)
    status_text.text("✅ 工作流完成！")

# 显示结果
if 'slides' in st.session_state:
    st.markdown("---")
    st.markdown("## 📤 生成结果")

    tab1, tab2, tab3 = st.tabs(["📋 提炼结果", "🎬 大纲", "🎴 卡片"])

    with tab1:
        st.markdown("### 🔬 内容提炼 (The Analyst)")
        if 'analysis' in st.session_state:
            analysis = st.session_state.analysis

            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("成就数量", len(analysis.get("achievements", [])))
                st.metric("证据质量", analysis.get("evidence_quality", "未知"))

            with col2:
                for i, ach in enumerate(analysis.get("achievements", []), 1):
                    with st.expander(f"成就 {i}: {ach.get('name', '未命名')}"):
                        st.markdown(f"**挑战**: {ach.get('challenge', 'N/A')}")
                        st.markdown(f"**方案**: {ach.get('solution', 'N/A')}")
                        st.markdown(f"**结果**: {ach.get('result', 'N/A')}")

            st.markdown("**JSON 输出:**")
            st.json(analysis)

    with tab2:
        st.markdown("### 🎬 大纲构建 (The Director)")
        if 'outline' in st.session_state:
            outline = st.session_state.outline

            st.markdown(f"**标题**: {outline.get('presentation_title', 'N/A')}")
            st.markdown(f"**副标题**: {outline.get('subtitle', 'N/A')}")

            st.markdown("**幻灯片结构:**")
            for slide in outline.get("slides", []):
                st.markdown(f"- 第{slide.get('slide_number', '?')}页: [{slide.get('slide_type', 'N/A')}] {slide.get('title', '')}")
                st.markdown(f"  - 目的: {slide.get('core_purpose', '')}")

            st.markdown("**JSON 输出:**")
            st.json(outline)

    with tab3:
        st.markdown("### 🎴 幻灯片卡片 (The Designer)")

        slides = st.session_state.slides
        renderer = CardRenderer()

        for slide in slides:
            slide_num = slide.get("slide_number", "?")
            title = slide.get("title", "无标题")
            card_type = slide.get("slide_type", "content")

            with st.expander(f"📄 第 {slide_num} 页: {title}"):
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.markdown(f"**标题**: {title}")
                    st.markdown(f"**类型**: {card_type}")

                    bullet_points = slide.get("bullet_points", [])
                    if bullet_points:
                        st.markdown("**要点:**")
                        for point in bullet_points:
                            st.markdown(f"- {point}")

                with col2:
                    st.markdown("**视觉建议:**")
                    st.info(slide.get("visual_suggestion", "无"))

                    st.markdown("**演讲逐字稿:**")
                    st.success(slide.get("speaker_notes", "无"))

# 卡片 Schema 显示
with st.expander("📐 卡片 JSON Schema 定义"):
    st.markdown("""
    ### 支持的卡片类型

    | 类型 | 用途 | 核心字段 |
    |------|------|----------|
    | `cover` | 封面 | title, subtitle, author, date |
    | `toc` | 目录 | items[] |
    | `bullet_list` | 要点列表 | title, bullets[] |
    | `data_point` | 数据点 | metric_label, metric_value, unit, change |
    | `before_after` | 对比 | before_content, after_content |
    | `timeline` | 时间线 | events[{time, event}] |
    | `process_flow` | 流程 | steps[{step, title, description}] |
    | `quote` | 引言 | quote_text, author |
    | `stats_card` | 统计组 | stats[{value, label, unit}] |
    | `summary` | 总结 | key_points[], next_steps[] |
    | `thank_you` | 致谢 | title, contact |
    """)

    schema = CardSchema.get_schema()
    st.json(schema)


# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    PPT Agent - 卡片式框架 | 基于 Python + Streamlit | 三节点工作流
    </div>
    """,
    unsafe_allow_html=True
)
