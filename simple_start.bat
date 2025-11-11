@echo off
chcp 65001 >nul
title 简化启动

echo ========================================
echo      简化启动单词学习应用
echo ========================================
echo.

echo 此脚本将直接启动服务，不进行任何检查
echo.

pause

echo.
echo 正在启动后端服务...
cd backend
start "后端服务" python app.py

echo 等待5秒...
timeout /t 5 /nobreak >nul

echo.
echo 正在启动前端服务...
cd ..\frontend
start "前端服务" npx react-scripts start

echo.
echo ========================================
echo         ✅ 启动命令已发送
echo ========================================
echo.
echo 📱 请等待1-2分钟，然后访问:
echo    http://localhost:3001
echo.
echo 💡 如果仍然无法访问:
echo   1. 检查命令窗口是否有错误信息
echo   2. 等待更长时间
echo   3. 运行 full_diagnostic.bat 检查问题
echo.
pause
