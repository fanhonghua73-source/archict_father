#!/bin/bash

# 建筑学爸 AI 助手 - 启动脚本

echo "🏗️  建筑学爸 AI 助手"
echo "===================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    exit 1
fi

echo "✓ Python 版本: $(python3 --version)"

# 进入后端目录
cd "$(dirname "$0")/backend"

# 检查依赖
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 首次运行，正在安装依赖..."
    pip3 install -r requirements.txt
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  未找到 .env 文件，正在创建..."
    cp .env.example .env
    echo "✓ 已创建 .env 文件"
    echo "💡 提示: 如需使用 AI 功能，请编辑 backend/.env 文件配置 API Keys"
fi

echo ""
echo "🚀 启动后端服务..."
echo "📍 地址: http://localhost:5002"
echo "📖 API 文档: http://localhost:5002/api/health"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动服务
python3 app.py
