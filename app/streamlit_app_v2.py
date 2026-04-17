"""
PPT Agent - 飞书/本地 多文件上传版
支持：PDF / Word / TXT / 图片
"""
import streamlit as st
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.parsers import MultimodalParser, DocumentProcessor
from agents.multimodal import MultimodalFusion, SimpleContextBuilder
from agents.presentation_schema import PresentationSchema
from core.engine import AgentEngine


st.set_page_config(
    page_title="PPT Agent - 多文件上传版",
    page_icon="📊",
    layout="wide"
)


# 侧边栏
with st.sidebar:
    st.title("⚙️ 配置")

    st.markdown("### 📂 支持的文件类型")
    st.markdown("""
    - **文本**: TXT, PDF, Word (.docx)
    - **图片**: JPG, PNG, GIF, BMP, WEBP
    """)

    st.markdown("### 🔄 工作流程")
    st.markdown("""
    1. **上传文件** - 支持多文件同时上传
    2. **解析内容** - 自动提取文本和图片
    3. **提炼成果** - AI 分析核心成就
    4. **生成卡片** - 输出结构化卡片 JSON
    5. **导出 PPT** - 生成最终文件
    """)

    st.divider()

    num_achievements = st.number_input(
        "提炼成就数量",
        min_value=1,
        max_value=5,
        value=3,
        help="从材料中提炼的代表性成果数量"
    )

    topic = st.text_input(
        "PPT 主题",
        value="年度述职报告",
        help="本次汇报的主题"
    )


# 主界面
st.title("📊 PPT Agent - 多文件上传版")
st.markdown("上传你的源材料，AI 自动分析并生成结构化汇报卡片")

# 文件上传区域
st.markdown("## 📤 上传源材料")

uploaded_files = st.file_uploader(
    "支持多文件上传（PDF、Word、图片等）",
    type=["pdf", "docx", "doc", "txt", "jpg", "jpeg", "png", "gif", "bmp", "webp"],
    accept_multiple_files=True,
    help="可以同时上传多个文件，AI 会自动整合所有内容"
)

# 手动输入区域（备用）
with st.expander("✏️ 或者直接粘贴文本内容"):
    manual_text = st.text_area(
        "粘贴文本材料",
        placeholder="如果不想上传文件，可以直接粘贴文本内容...",
        height=150
    )

# 解析按钮
col1, col2 = st.columns([1, 3])

with col1:
    parse_button = st.button("🔍 解析文件", type="primary", use_container_width=True)

if parse_button:
    parser = MultimodalParser()
    processor = DocumentProcessor(parser)

    # 存储解析结果
    parsed_text = ""

    if uploaded_files:
        # 处理上传的文件
        files_data = [(f.getvalue(), f.name) for f in uploaded_files]
        parsed_text = processor.process_bytes(files_data)
        st.session_state.parsed_text = parsed_text
        st.session_state.file_count = len(uploaded_files)
        st.session_state.uploaded_filenames = [f.name for f in uploaded_files]

    elif manual_text:
        parsed_text = manual_text
        st.session_state.parsed_text = parsed_text
        st.session_state.file_count = 0
        st.session_state.uploaded_filenames = []

# 显示解析结果
if 'parsed_text' in st.session_state:
    st.markdown("---")
    st.markdown("## 📋 解析结果")

    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("文件数量", st.session_state.get('file_count', 0))
        if st.session_state.get('uploaded_filenames'):
            with st.expander("📁 文件列表"):
                for fn in st.session_state.uploaded_filenames:
                    st.text(f"• {fn}")

    with col2:
        with st.expander("📄 解析内容预览"):
            st.text(st.session_state.parsed_text[:2000] + "..." if len(st.session_state.parsed_text) > 2000 else st.session_state.parsed_text)

# 运行工作流
if 'parsed_text' in st.session_state:
    st.markdown("---")
    run_workflow = st.button("🚀 运行完整工作流（分析→提炼→生成卡片）", type="primary", use_container_width=True)

    if run_workflow:
        progress_bar = st.progress(0)
        status_text = st.empty()

        engine = AgentEngine()

        # Stage 1: 内容提炼
        status_text.text("🔬 Stage 1: 内容提炼中...")
        progress_bar.progress(20)

        from agents.ppt_agent_v2 import AnalystNode
        analyst = AnalystNode(engine)

        # 构建上下文
        context = SimpleContextBuilder.build(
            text_content=st.session_state.parsed_text,
            topic=topic,
            num_achievements=num_achievements
        )

        analysis = analyst.extract(
            source_material=context,
            topic=topic,
            num_achievements=num_achievements
        )

        st.session_state.analysis = analysis

        # Stage 2: 大纲构建
        status_text.text("🎬 Stage 2: 大纲构建中...")
        progress_bar.progress(50)

        from agents.ppt_agent_v2 import DirectorNode
        director = DirectorNode(engine)

        outline = director.build_outline(
            analysis=analysis,
            topic=topic
        )

        st.session_state.outline = outline

        # Stage 3: 卡片生成
        status_text.text("🎨 Stage 3: 生成卡片中...")
        progress_bar.progress(80)

        from agents.ppt_agent_v2 import DesignerNode
        designer = DesignerNode(engine)

        slides = designer.generate_slides(
            outline=outline,
            analysis=analysis,
            topic=topic
        )

        st.session_state.slides = slides
        progress_bar.progress(100)
        status_text.text("✅ 完成！")

# 显示结果
if 'slides' in st.session_state:
    st.markdown("---")
    st.markdown("## 📤 生成结果")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔬 提炼结果",
        "🎬 大纲",
        "🎴 卡片 JSON",
        "📊 三列卡片预览"
    ])

    with tab1:
        st.markdown("### 内容提炼")
        if 'analysis' in st.session_state:
            analysis = st.session_state.analysis
            for i, ach in enumerate(analysis.get("achievements", []), 1):
                with st.expander(f"成就 {i}: {ach.get('name', 'N/A')}"):
                    st.markdown(f"**挑战**: {ach.get('challenge', 'N/A')}")
                    st.markdown(f"**方案**: {ach.get('solution', 'N/A')}")
                    st.markdown(f"**成果**: {ach.get('result', 'N/A')}")

    with tab2:
        st.markdown("### 演示大纲")
        if 'outline' in st.session_state:
            outline = st.session_state.outline
            st.markdown(f"**标题**: {outline.get('presentation_title', '')}")
            for slide in outline.get("slides", []):
                st.markdown(f"- 第{slide.get('slide_number', '?')}页: {slide.get('title', '')}")

    with tab3:
        st.markdown("### 卡片 JSON")
        st.json(st.session_state.slides)

    with tab4:
        st.markdown("### 三列卡片预览")

        slides = st.session_state.slides
        for slide in slides:
            if isinstance(slide, dict):
                slide_num = slide.get("slide_number", "?")
                title = slide.get("title", "")
                cards = slide.get("bullet_points", [])

                st.markdown(f"#### 第 {slide_num} 页: {title}")

                # 三列展示
                cols = st.columns(3)

                # Context (痛点)
                with cols[0]:
                    st.markdown("**🟠 背景/痛点**")
                    st.info(cards[0] if len(cards) > 0 else "待填充")

                # Action (方案)
                with cols[1]:
                    st.markdown("**🔵 方案/创新**")
                    st.info(cards[1] if len(cards) > 1 else "待填充")

                # Impact (成果)
                with cols[2]:
                    st.markdown("**🟢 成果/影响**")
                    st.success(cards[2] if len(cards) > 2 else "待填充")

                st.markdown("---")


# 架构说明
with st.expander("📐 架构说明 - 多模态输入处理"):
    st.markdown("""
    ### 工作流程

    ```
    ┌─────────────────────────────────────────────────────────────┐
    │                      多模态输入处理                            │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │   📄 PDF ──┐                                                │
    │   📝 DOCX ─┤                                                │
    │   🖼️ IMG  ─┼──→ MultimodalParser ──→ DocumentProcessor     │
    │   📃 TXT  ─┘                              │                  │
    │                                           ▼                  │
    │                               ┌─────────────────┐            │
    │                               │  标准化字符串     │            │
    │                               │  (LLM 上下文)    │            │
    │                               └────────┬────────┘            │
    │                                        │                     │
    │           ┌────────────────────────────┼──────────────────┐  │
    │           │                            ▼                  │  │
    │           │    ┌─────────────────────────────────────┐    │  │
    │           │    │   三阶段工作流 (The Analyst→Director→Designer) │    │  │
    │           │    └─────────────────────────────────────┘    │  │
    │           │                            │                  │  │
    │           │                            ▼                  │  │
    │           │              ┌─────────────────────┐          │  │
    │           │              │   三列卡片 JSON      │          │  │
    │           │              └─────────────────────┘          │  │
    │           │                                               │  │
    │           └───────────────────────────────────────────────┘  │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
    ```

    ### 支持的文件类型

    | 类型 | 扩展名 | 处理方式 |
    |------|--------|----------|
    | PDF | .pdf | PyMuPDF 提取文本和图片 |
    | Word | .docx, .doc | python-docx 提取段落和表格 |
    | 文本 | .txt | 直接读取 |
    | 图片 | .jpg, .png 等 | Base64 编码，待多模态模型描述 |
    """)
