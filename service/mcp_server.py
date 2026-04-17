"""
PPT Agent MCP 服务器
Cherry Studio MCP 工具服务
"""
import sys
import json
import asyncio
from typing import Any, Dict
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.background import BackgroundTask
import uvicorn

# 导入 PPT Agent 模块
sys.path.insert(0, '/root/openclaw-agent')
from agents.parsers import MultimodalParser, DocumentProcessor
from agents.ppt_agent_v2 import AnalystNode, DirectorNode, DesignerNode
from core.engine import AgentEngine


# 初始化组件
engine = AgentEngine()
parser = MultimodalParser()
processor = DocumentProcessor(parser)


# MCP 协议相关
MCP_capabilities = {
    "capabilities": {
        "tools": {},
        "resources": {},
        "prompts": {}
    }
}


# 工具定义
TOOLS = [
    {
        "name": "parse_document",
        "description": "解析文档，支持 PDF、Word、图片等多种格式",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "文档的文本内容"
                }
            },
            "required": ["content"]
        }
    },
    {
        "name": "extract_achievements",
        "description": "从材料中提炼核心成就",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "PPT 主题"},
                "source_material": {"type": "string", "description": "源材料内容"},
                "num_achievements": {"type": "integer", "description": "成就数量", "default": 3}
            },
            "required": ["topic", "source_material"]
        }
    },
    {
        "name": "generate_outline",
        "description": "生成演示大纲",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "achievements": {"type": "string", "description": "成就JSON字符串"}
            },
            "required": ["topic"]
        }
    },
    {
        "name": "generate_cards",
        "description": "生成幻灯片卡片",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "outline": {"type": "string", "description": "大纲JSON字符串"},
                "analysis": {"type": "string", "description": "分析JSON字符串"}
            },
            "required": ["topic"]
        }
    },
    {
        "name": "ppt_workflow",
        "description": "完整PPT生成工作流",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "source_material": {"type": "string"},
                "num_achievements": {"type": "integer", "default": 3}
            },
            "required": ["topic", "source_material"]
        }
    }
]


class MCPProtocol:
    """MCP 协议处理器"""

    @staticmethod
    def handle_initialize(params: Dict) -> Dict:
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": MCP_capabilities["capabilities"],
            "serverInfo": {"name": "ppt-agent", "version": "1.0.0"}
        }

    @staticmethod
    def handle_tools_list(params: Dict) -> Dict:
        return {"tools": TOOLS}

    @staticmethod
    async def handle_tools_call(params: Dict) -> Dict:
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        result = await execute_tool(tool_name, arguments)
        return {
            "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]
        }


async def execute_tool(name: str, args: Dict) -> Dict:
    """执行工具"""
    try:
        if name == "parse_document":
            content = args.get("content", "")
            return {"status": "success", "content": content, "char_count": len(content)}

        elif name == "extract_achievements":
            analyst = AnalystNode(engine)
            return analyst.extract(
                source_material=args.get("source_material", ""),
                topic=args.get("topic", ""),
                num_achievements=args.get("num_achievements", 3)
            )

        elif name == "generate_outline":
            director = DirectorNode(engine)
            try:
                achievements = json.loads(args.get("achievements", "{}"))
            except:
                achievements = {}
            return director.build_outline(analysis=achievements, topic=args.get("topic", ""))

        elif name == "generate_cards":
            designer = DesignerNode(engine)
            try:
                outline = json.loads(args.get("outline", "{}"))
            except:
                outline = {}
            try:
                analysis = json.loads(args.get("analysis", "{}"))
            except:
                analysis = {}
            slides = designer.generate_slides(outline=outline, analysis=analysis, topic=args.get("topic", ""))
            return {"slides": slides}

        elif name == "ppt_workflow":
            analyst = AnalystNode(engine)
            director = DirectorNode(engine)
            designer = DesignerNode(engine)
            topic = args.get("topic", "")
            source = args.get("source_material", "")
            num = args.get("num_achievements", 3)
            analysis = analyst.extract(source_material=source, topic=topic, num_achievements=num)
            outline = director.build_outline(analysis=analysis, topic=topic)
            slides = designer.generate_slides(outline=outline, analysis=analysis, topic=topic)
            return {"topic": topic, "analysis": analysis, "outline": outline, "slides": slides, "status": "success"}

        return {"error": f"Unknown tool: {name}"}
    except Exception as e:
        return {"error": str(e)}


# SSE 连接管理
class SSEManager:
    def __init__(self):
        self.connections: Dict[str, asyncio.Queue] = {}

    def add_connection(self, queue: asyncio.Queue) -> str:
        client_id = str(id(queue))
        self.connections[client_id] = queue
        return client_id

    def remove_connection(self, client_id: str):
        if client_id in self.connections:
            del self.connections[client_id]

    async def broadcast(self, message: dict):
        for client_id, queue in self.connections.items():
            await queue.put(message)


sse_manager = SSEManager()


# Starlette 路由
async def sse_endpoint(request):
    """SSE 连接端点"""
    queue = asyncio.Queue()
    client_id = sse_manager.add_connection(queue)

    async def event_generator():
        try:
            while True:
                try:
                    message = await asyncio.wait_for(queue.get(), timeout=30)
                    yield {"event": "message", "data": json.dumps(message)}
                except asyncio.TimeoutError:
                    yield {"event": "ping", "data": "{}"}
        finally:
            sse_manager.remove_connection(client_id)

    from starlette.responses import StreamingResponse
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


async def mcp_endpoint(request):
    """MCP 消息端点"""
    body = await request.json()
    method = body.get("method")
    params = body.get("params", {})
    msg_id = body.get("id")

    result = None
    error = None

    try:
        if method == "initialize":
            result = MCPProtocol.handle_initialize(params)
        elif method == "tools/list":
            result = MCPProtocol.handle_tools_list(params)
        elif method == "tools/call":
            result = await MCPProtocol.handle_tools_call(params)
        elif method == "ping":
            result = {"pong": True}
        else:
            error = {"code": -32601, "message": f"Method not found: {method}"}
    except Exception as e:
        error = {"code": -32603, "message": str(e)}

    if error:
        return JSONResponse({"jsonrpc": "2.0", "error": error, "id": msg_id})
    return JSONResponse({"jsonrpc": "2.0", "result": result, "id": msg_id})


async def health(request):
    """健康检查"""
    return JSONResponse({
        "status": "ok",
        "service": "PPT Agent MCP",
        "endpoints": {
            "sse": "/sse",
            "mcp": "/mcp"
        }
    })


# 创建应用
app = Starlette(
    routes=[
        Route("/sse", sse_endpoint),
        Route("/mcp", mcp_endpoint, methods=["POST"]),
        Route("/health", health),
    ]
)


if __name__ == "__main__":
    print("🚀 启动 PPT Agent MCP 服务器...")
    print("📍 SSE: http://0.0.0.0:8001/sse")
    print("📍 MCP: http://0.0.0.0:8001/mcp")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
