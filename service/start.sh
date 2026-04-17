#!/bin/bash
# PPT Agent API 服务启动脚本

cd /root/openclaw-agent

# 激活虚拟环境（如果有）
# source venv/bin/activate

# 启动服务
echo "🚀 启动 PPT Agent API..."
echo "📍 服务地址: http://0.0.0.0:8000"
echo "📚 API 文档: http://0.0.0.0:8000/docs"
echo ""

python3 service/api.py
