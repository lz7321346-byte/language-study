#!/bin/bash

echo "========================================"
echo "   情景背单词小程序启动脚本"
echo "========================================"
echo

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[1/4] 检查Python环境..."
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python，请先安装Python 3.9+"
    exit 1
fi

# 使用python3或python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "[2/4] 安装后端依赖..."
cd backend
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "错误: 后端依赖安装失败"
    exit 1
fi

echo "[3/4] 安装前端依赖..."
cd ../frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
if [ $? -ne 0 ]; then
    echo "错误: 前端依赖安装失败"
    exit 1
fi

echo "[4/4] 检查AI模型配置..."
cd ..
if [ ! -f "config/metagpt_config.yaml" ]; then
    echo "错误: 未找到MetaGPT配置文件"
    exit 1
fi

echo "检查Ollama服务..."
if ! command -v ollama &> /dev/null; then
    echo "警告: 未检测到Ollama安装"
    echo "请访问 https://ollama.ai/download 下载并安装Ollama"
    echo "然后运行: ollama pull llama3.2"
    echo
else
    echo "✓ 发现Ollama安装"
    if ollama list | grep -q "llama3.2"; then
        echo "✓ 发现llama3.2模型"
    else
        echo "警告: 未检测到llama3.2模型"
        echo "请运行: ollama pull llama3.2"
        echo
    fi
fi

echo
echo "========================================"
echo "        启动完成！"
echo "========================================"
echo
echo "启动后端服务:"
echo "  cd backend && source venv/bin/activate && python app.py"
echo
echo "启动前端服务:"
echo "  cd frontend && npm start"
echo
echo "后端将在 http://localhost:5000 运行"
echo "前端将在 http://localhost:3001 运行"
echo
