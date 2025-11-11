@echo off
chcp 65001 >nul
title 打开单词学习应用

echo ========================================
echo      打开单词学习应用网页
echo ========================================
echo.

echo 正在打开浏览器...
start http://localhost:3001

echo.
echo ✅ 浏览器已打开
echo.
echo 如果页面无法访问，请：
echo 1. 确保应用已启动（运行 启动.bat）
echo 2. 等待10-15秒后刷新页面
echo 3. 检查服务是否正在运行
echo.
echo 前端地址: http://localhost:3001
echo 后端地址: http://localhost:5000
echo.
pause
