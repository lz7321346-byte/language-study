@echo off
chcp 65001 >nul
title 单词学习应用启动器

echo ========================================
echo     情景背单词小程序 - 服务启动器
echo ========================================
echo.

echo [1/4] 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请安装Python 3.9+
    echo    下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python环境正常
echo.

echo [2/4] 检查Node.js环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Node.js，请安装Node.js 16+
    echo    下载地址: https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js环境正常
echo.

echo [3/4] 检查Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未安装Ollama
    echo.
    echo 请先安装Ollama：
    echo 1. 访问: https://ollama.ai/download
    echo 2. 下载Windows版本并安装
    echo 3. 运行 install_ollama.bat 安装AI模型
    echo.
    pause
    exit /b 1
)

echo 检查Ollama服务...
ollama list 2>nul | findstr llama3.2 >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  未找到llama3.2模型
    echo.
    echo 正在自动下载AI模型 (约2GB，请耐心等待)...
    echo.
    ollama pull llama3.2
    if %errorlevel% neq 0 (
        echo ❌ 模型下载失败
        echo    请检查网络连接后重试，或运行 install_ollama.bat
        pause
        exit /b 1
    )
)
echo ✅ Ollama环境正常
echo.

echo [4/4] 启动服务...
echo.

echo 启动后端服务...
start "后端服务" cmd /k "cd backend && python app.py"

echo 等待3秒...
timeout /t 3 /nobreak >nul

echo 启动前端服务...
start "前端服务" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo         🎉 服务启动完成！
echo ========================================
echo.
echo 📱 前端界面: http://localhost:3001
echo 🔧 后端API:   http://localhost:5000
echo 🤖 AI服务:    http://localhost:11434
echo.
echo 💡 提示:
echo   - 如果浏览器无法访问，请等待1-2分钟让服务完全启动
echo   - 首次启动可能需要更长时间
echo   - 按 Ctrl+C 可以停止服务
echo.
echo 按任意键关闭此窗口...
pause >nul
