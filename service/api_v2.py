"""
PPT Agent API 服务 v2 - 集成知识库
支持文件上传 → 知识库存储 → 增量检索 → PPT 生成
"""
import os
import sys
import json
import tempfile
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.parsers import MultimodalParser, DocumentProcessor
from agents.knowledge_base import KnowledgeBase, get_knowledge_base
from agents.ppt_agent_v2 import AnalystNode, DirectorNode, DesignerNode
from core.engine import AgentEngine


# ============== 配置 ==============

app = FastAPI(
    title="PPT Agent API v2",
    description="集成知识库的 PPT 生成服务",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化组件
engine = AgentEngine()
parser = MultimodalParser()
processor = DocumentProcessor(parser)
kb = get_knowledge_base()


# ============== 工具函数 ==============

def save_upload_file(upload_file: UploadFile) -> Path:
    """保存上传文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{upload_file.filename}"
    file_path = Path("/tmp/ppt_agent_uploads") / filename
    file_path.parent.mkdir(exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())

    return file_path


# ============== API 端点 ==============

@app.get("/")
async def root():
    """服务信息"""
    return {
        "service": "PPT Agent API v2",
        "version": "2.0.0",
        "features": ["知识库", "文件上传", "PPT生成"],
        "endpoints": {
            "知识库": "/kb/*",
            "PPT生成": "/workflow",
            "工作流": "/workflow_full"
        }
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy", "service": "PPT Agent API v2"}


# ============== 知识库接口 ==============

@app.post("/kb/add")
async def kb_add_file(
    files: List[UploadFile] = File(...),
    tags: str = Form(""),
    parse_content: bool = Form(True)
):
    """
    添加文件到知识库
    - 自动解析文本内容
    - 存入向量数据库
    - 支持增量添加
    """
    added = []
    errors = []

    for f in files:
        try:
            # 保存文件
            file_path = save_upload_file(f)

            # 解析内容
            if parse_content:
                docs = parser.parse(str(file_path))
                content = processor.documents_to_string([docs])
            else:
                content = f.file.read().decode("utf-8", errors="ignore")

            # 添加到知识库
            tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
            doc = kb.add_document(
                filename=f.filename,
                content=content,
                file_type=Path(f.filename).suffix,
                tags=tag_list
            )

            added.append({
                "filename": f.filename,
                "doc_id": doc.doc_id,
                "char_count": doc.char_count
            })

            # 清理临时文件
            file_path.unlink()

        except Exception as e:
            errors.append({"filename": f.filename, "error": str(e)})

    return {
        "status": "success",
        "added": added,
        "errors": errors,
        "total_documents": kb.get_stats()["total_documents"]
    }


@app.post("/kb/add_text")
async def kb_add_text(
    content: str = Form(...),
    filename: str = Form("text"),
    tags: str = Form("")
):
    """
    直接添加文本到知识库
    """
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    doc = kb.add_document(
        filename=filename,
        content=content,
        file_type="txt",
        tags=tag_list
    )

    return {
        "status": "success",
        "doc_id": doc.doc_id,
        "char_count": doc.char_count
    }


@app.get("/kb/search")
async def kb_search(query: str, top_k: int = 5):
    """
    检索知识库
    返回与查询相关的文档
    """
    results = kb.search(query, top_k=top_k)

    return {
        "query": query,
        "results": results,
        "total_results": len(results)
    }


@app.get("/kb/context")
async def kb_get_context(query: str, max_chars: int = 100000):
    """
    获取检索到的上下文
    合并为可发送给 LLM 的字符串
    """
    context = kb.get_context(query, max_chars=max_chars)

    return {
        "query": query,
        "context": context,
        "char_count": len(context)
    }


@app.get("/kb/list")
async def kb_list():
    """列出知识库所有文档"""
    docs = kb.list_documents()
    stats = kb.get_stats()

    return {
        "documents": docs,
        "stats": stats
    }


@app.delete("/kb/delete/{doc_id}")
async def kb_delete(doc_id: str):
    """删除知识库文档"""
    success = kb.delete_document(doc_id)

    return {
        "status": "success" if success else "failed",
        "doc_id": doc_id
    }


@app.get("/kb/stats")
async def kb_stats():
    """获取知识库统计"""
    return kb.get_stats()


# ============== PPT 生成接口 ==============

@app.post("/workflow")
async def generate_ppt_workflow(
    topic: str = Form(...),
    query: str = Form(""),  # 可选：从知识库检索
    source_material: str = Form(""),  # 可选：直接提供材料
    num_achievements: int = Form(3),
    use_knowledge_base: bool = Form(True)
):
    """
    PPT 生成工作流
    1. 从知识库检索相关内容（如果 query 提供了）
    2. 或者使用直接提供的 source_material
    3. 执行完整工作流
    """
    result = {
        "topic": topic,
        "stages": {}
    }

    # Step 1: 获取材料
    if use_knowledge_base and query:
        # 从知识库检索
        context = kb.get_context(query)
        material = context
        result["stages"]["knowledge_base"] = {
            "status": "retrieved",
            "query": query,
            "char_count": len(context)
        }
    elif source_material:
        material = source_material
        result["stages"]["source"] = {
            "status": "provided",
            "char_count": len(source_material)
        }
    else:
        raise HTTPException(status_code=400, detail="请提供 query 或 source_material")

    result["stages"]["material"] = {
        "source": "knowledge_base" if (use_knowledge_base and query) else "provided",
        "char_count": len(material)
    }

    # Step 2: 提炼成就 (The Analyst)
    analyst = AnalystNode(engine)
    analysis = analyst.extract(
        source_material=material,
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
    result["stages"]["slides"] = slides
    result["final_slides"] = slides

    return {
        "status": "success",
        "result": result
    }


@app.post("/workflow_simple")
async def simple_workflow(
    topic: str = Form(...),
    source_material: str = Form(""),
    num_achievements: int = Form(3)
):
    """
    简化工作流（不使用知识库）
    """
    analyst = AnalystNode(engine)
    director = DirectorNode(engine)
    designer = DesignerNode(engine)

    analysis = analyst.extract(
        source_material=source_material,
        topic=topic,
        num_achievements=num_achievements
    )

    outline = director.build_outline(analysis=analysis, topic=topic)

    slides = designer.generate_slides(
        outline=outline,
        analysis=analysis,
        topic=topic
    )

    return {
        "status": "success",
        "data": {
            "topic": topic,
            "analysis": analysis,
            "outline": outline,
            "slides": slides
        }
    }


# ============== 启动 ==============

def start_server(host: str = "0.0.0.0", port: int = 8000):
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    print("🚀 启动 PPT Agent API v2 (知识库版)...")
    print("📍 地址: http://0.0.0.0:8000")
    start_server()
