@echo off
chcp 65001 >nul
title 快速启动 - 跳过模型检查

echo ========================================
echo       快速启动模式
echo ========================================
echo.
echo ⚠️  注意: 此模式跳过AI模型检查
echo    适用于已经安装Ollama和llama3.2的用户
echo.
echo 如果您还没有安装AI模型，请运行:
echo install_ollama.bat
echo.

pause

echo.
echo [1/2] 检查基础环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装
    pause
    exit /b 1
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js未安装
    pause
    exit /b 1
)
echo ✅ 环境检查通过
echo.

echo [2/2] 启动服务...
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
echo.
echo 💡 提示:
echo   - 如果AI功能不工作，请先运行 install_ollama.bat
echo   - 首次启动可能需要1-2分钟
echo.
echo 按任意键关闭此窗口...
pause >nul
