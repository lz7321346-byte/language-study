@echo off
chcp 65001 >nul
title 直接启动 - 无检查

echo ========================================
echo     直接启动单词学习应用
echo ========================================
echo.
echo ⚠️  此脚本跳过所有环境检查
echo    适用于已确认环境正常的用户
echo.

pause

echo.
echo [1/2] 启动后端服务...
start "后端服务" cmd /k "cd backend && python app.py"

echo 等待3秒...
timeout /t 3 /nobreak >nul

echo [2/2] 启动前端服务...
start "前端服务" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo         ✅ 启动命令已执行
echo ========================================
echo.
echo 📱 请在浏览器中访问:
echo    http://localhost:3001
echo.
echo 💡 如果无法访问，请等待1-2分钟让服务完全启动
echo.
echo 🔍 如需检查状态，请运行:
echo    python test_ports.py
echo.
pause
