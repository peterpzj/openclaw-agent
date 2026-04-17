"""
PPT Agent API 服务
基于 FastAPI 的 REST API 服务
Cherry Studio 通过此 API 调用 PPT Agent 能力
"""
import os
import sys
import json
import base64
import tempfile
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.parsers import MultimodalParser, DocumentProcessor
from agents.presentation_schema import PresentationSchema, PresentationRenderer
from agents.ppt_agent_v2 import AnalystNode, DirectorNode, DesignerNode
from core.engine import AgentEngine


# ============== 配置 ==============

app = FastAPI(
    title="PPT Agent API",
    description="本地化 PPT 生成 Agent 服务",
    version="1.0.0"
)

# CORS 配置，允许跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录
UPLOAD_DIR = Path("/tmp/ppt_agent_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

OUTPUT_DIR = Path("/tmp/ppt_agent_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# 初始化组件
engine = AgentEngine()
parser = MultimodalParser()
processor = DocumentProcessor(parser)
schema = PresentationSchema()
renderer = PresentationRenderer()


# ============== 工具函数 ==============

def save_upload_file(upload_file: UploadFile) -> Path:
    """保存上传文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{upload_file.filename}"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as f:
        content = upload_file.file.read()
        f.write(content)

    return file_path


def process_files_to_context(file_paths: List[Path]) -> str:
    """处理文件列表，转换为标准上下文字符串"""
    documents = parser.parse_multiple([str(p) for p in file_paths])
    return processor.documents_to_string(documents)


# ============== API 端点 ==============

@app.get("/")
async def root():
    """服务健康检查"""
    return {
        "status": "ok",
        "service": "PPT Agent API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "parse_document": "POST /parse",
            "extract_achievements": "POST /extract",
            "generate_outline": "POST /outline",
            "generate_cards": "POST /cards",
            "generate_ppt": "POST /generate",
            "full_workflow": "POST /workflow"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.post("/parse")
async def parse_document(files: List[UploadFile] = File(...)):
    """
    解析文档
    支持 PDF、Word、图片等多种格式
    返回解析后的文本内容
    """
    try:
        # 保存上传文件
        file_paths = []
        for f in files:
            path = save_upload_file(f)
            file_paths.append(path)

        # 解析内容
        context = process_files_to_context(file_paths)

        # 统计信息
        total_chars = len(context)
        file_info = [{"name": p.name, "size": p.stat().st_size} for p in file_paths]

        return {
            "status": "success",
            "content": context,
            "statistics": {
                "total_characters": total_chars,
                "file_count": len(file_paths),
                "files": file_info
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract")
async def extract_achievements(
    topic: str = Form(...),
    num_achievements: int = Form(3),
    source_material: str = Form("")
):
    """
    提炼核心成就
    使用 The Analyst 节点
    """
    try:
        analyst = AnalystNode(engine)

        result = analyst.extract(
            source_material=source_material,
            topic=topic,
            num_achievements=num_achievements
        )

        return {
            "status": "success",
            "achievements": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/outline")
async def generate_outline(
    topic: str = Form(...),
    achievements: str = Form("")  # JSON 字符串
):
    """
    生成演示大纲
    使用 The Director 节点
    """
    try:
        director = DirectorNode(engine)

        # 解析成就数据
        try:
            achievements_data = json.loads(achievements)
        except:
            achievements_data = {"achievements": []}

        result = director.build_outline(
            analysis=achievements_data,
            topic=topic
        )

        return {
            "status": "success",
            "outline": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cards")
async def generate_cards(
    topic: str = Form(...),
    outline: str = Form(""),  # JSON 字符串
    analysis: str = Form("")   # JSON 字符串
):
    """
    生成幻灯片卡片
    使用 The Designer 节点
    """
    try:
        designer = DesignerNode(engine)

        # 解析输入
        try:
            outline_data = json.loads(outline) if outline else {}
            analysis_data = json.loads(analysis) if analysis else {}
        except:
            outline_data = {}
            analysis_data = {}

        slides = designer.generate_slides(
            outline=outline_data,
            analysis=analysis_data,
            topic=topic
        )

        return {
            "status": "success",
            "slides": slides
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate")
async def generate_ppt(
    topic: str = Form(...),
    slides_data: str = Form(""),  # JSON 字符串，卡片数据
    output_format: str = Form("json")  # json 或 pptx
):
    """
    生成最终 PPT
    返回卡片 JSON 或生成 PPTX 文件
    """
    try:
        # 解析卡片数据
        try:
            cards = json.loads(slides_data) if slides_data else []
        except:
            cards = []

        if output_format == "json":
            # 只返回 JSON 数据
            return {
                "status": "success",
                "format": "json",
                "slides": cards,
                "total_slides": len(cards)
            }

        else:
            # TODO: 生成 PPTX 文件
            # 需要集成 PptxGenJS
            return {
                "status": "pending",
                "message": "PPTX generation not yet implemented",
                "slides": cards
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/workflow")
async def full_workflow(
    topic: str = Form(...),
    files: Optional[List[UploadFile]] = File(None),
    source_material: str = Form(""),
    num_achievements: int = Form(3)
):
    """
    完整工作流
    1. 解析上传的文件
    2. 提炼核心成就
    3. 生成大纲
    4. 生成卡片
    """
    try:
        result = {
            "topic": topic,
            "stages": {}
        }

        # Step 1: 解析文件
        if files:
            file_paths = []
            for f in files:
                path = save_upload_file(f)
                file_paths.append(path)

            context = process_files_to_context(file_paths)
            result["stages"]["parsed"] = {
                "status": "success",
                "char_count": len(context)
            }
        else:
            context = source_material
            result["stages"]["parsed"] = {
                "status": "skipped",
                "reason": "no files uploaded"
            }

        # Step 2: 提炼成就 (The Analyst)
        analyst = AnalystNode(engine)
        analysis = analyst.extract(
            source_material=context,
            topic=topic,
            num_achievements=num_achievements
        )
        result["stages"]["analysis"] = analysis

        # Step 3: 生成大纲 (The Director)
        director = DirectorNode(engine)
        outline = director.build_outline(
            analysis=analysis,
            topic=topic
        )
        result["stages"]["outline"] = outline

        # Step 4: 生成卡片 (The Designer)
        designer = DesignerNode(engine)
        slides = designer.generate_slides(
            outline=outline,
            analysis=analysis,
            topic=topic
        )
        result["stages"]["cards"] = slides
        result["final_slides"] = slides

        return {
            "status": "success",
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/workflow_simple")
async def simple_workflow(
    topic: str = Form(...),
    source_material: str = Form(""),
    num_achievements: int = Form(3)
):
    """
    简化工作流（不需要文件上传）
    直接传入文本内容
    """
    try:
        result = {
            "topic": topic,
            "stages": {}
        }

        # 提炼成就
        analyst = AnalystNode(engine)
        analysis = analyst.extract(
            source_material=source_material,
            topic=topic,
            num_achievements=num_achievements
        )
        result["analysis"] = analysis

        # 生成大纲
        director = DirectorNode(engine)
        outline = director.build_outline(
            analysis=analysis,
            topic=topic
        )
        result["outline"] = outline

        # 生成卡片
        designer = DesignerNode(engine)
        slides = designer.generate_slides(
            outline=outline,
            analysis=analysis,
            topic=topic
        )
        result["slides"] = slides

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============== 启动服务 ==============

def start_server(host: str = "0.0.0.0", port: int = 8000):
    """启动 API 服务"""
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    print("🚀 启动 PPT Agent API 服务...")
    print("📍 地址: http://0.0.0.0:8000")
    print("📚 文档: http://0.0.0.0:8000/docs")
    start_server()
