@echo off
chcp 65001 >nul
title 手动启动服务

echo ========================================
echo       手动启动单词学习应用
echo ========================================
echo.

echo [1/4] 手动检查服务状态...
echo.

echo 检查端口 5000 (后端)...
netstat -ano | findstr :5000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ 端口5000被占用，请先停止占用进程
    echo    运行: taskkill /PID ^<PID^> /F
    echo.
    echo 或者按任意键继续启动（可能会有端口冲突）
    pause
) else (
    echo ✅ 端口5000可用
)

echo.
echo 检查端口 3001 (前端)...
netstat -ano | findstr :3001 >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ 端口3001被占用，请先停止占用进程
    echo    运行: taskkill /PID ^<PID^> /F
    echo.
    echo 或者按任意键继续启动（可能会有端口冲突）
    pause
) else (
    echo ✅ 端口3001可用
)

echo.
echo [2/4] 检查Ollama状态...
ollama list 2>nul | findstr llama3.2 >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  警告: 未检测到llama3.2模型
    echo     AI故事生成功能将不可用
    echo.
    echo     如需AI功能，请先运行:
    echo     ollama pull llama3.2
    echo.
) else (
    echo ✅ 检测到llama3.2模型
)

echo.
echo [3/4] 启动Ollama服务...
echo (如果已启动会显示错误，忽略即可)
ollama serve >nul 2>&1
timeout /t 2 /nobreak >nul
echo ✅ Ollama服务检查完成

echo.
echo [4/4] 启动应用服务...
echo.

echo 启动后端服务...
echo 命令: cd backend && python app.py
echo.
start "单词学习应用 - 后端" cmd /k "cd backend && echo 正在启动后端服务... && python app.py"

echo 等待5秒让后端启动...
timeout /t 5 /nobreak >nul

echo.
echo 启动前端服务...
echo 命令: cd frontend && npm start
echo.
start "单词学习应用 - 前端" cmd /k "cd frontend && echo 正在启动前端服务... && npm start"

echo.
echo ========================================
echo         🚀 启动完成！
echo ========================================
echo.
echo 📱 应用访问地址:
echo    前端界面: http://localhost:3001
echo    后端API:   http://localhost:5000
echo.
echo 💡 注意事项:
echo   - 前端启动需要1-2分钟
echo   - 如果浏览器显示"拒绝连接"，请等待更长时间
echo   - 如果仍有问题，请查看各个命令窗口的错误信息
echo.
echo 🔍 故障排除:
echo   - 运行: troubleshoot.bat
echo   - 运行: python test_ports.py
echo.
echo 按任意键关闭此窗口...
pause >nul
