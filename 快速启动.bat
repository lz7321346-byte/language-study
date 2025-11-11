@echo off
chcp 65001 >nul
title 快速启动（跳过安装）

echo ========================================
echo     🚀 快速启动单词学习应用
echo ========================================
echo.
echo 此脚本跳过依赖安装，直接启动服务
echo 如果还没有安装依赖，请先运行: 加速安装.bat
echo.

pause

REM 查找项目目录
if exist "vocabulary_story_app" (
    cd vocabulary_story_app
    goto :start_services
)

if exist "frontend\package.json" (
    goto :start_services
)

cd ..
if exist "vocabulary_story_app" (
    cd vocabulary_story_app
    goto :start_services
)

echo ❌ 未找到vocabulary_story_app目录
pause
exit /b 1

:start_services
echo 项目目录: %CD%
echo.

REM 检查前端依赖
if not exist "frontend\node_modules" (
    echo ⚠️  警告: 前端依赖未安装
    echo 请先运行: 加速安装.bat
    echo.
    echo 继续启动可能失败，按任意键继续...
    pause
)

REM 清理进程
echo 🧹 清理旧进程...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1

REM 启动后端
echo 🚀 启动后端服务...
start "后端服务" cmd /k "cd backend && python app.py"

REM 等待
timeout /t 3 /nobreak >nul

REM 启动前端
echo 🚀 启动前端服务...
start "前端服务" cmd /k "cd frontend && npm start"

REM 等待
timeout /t 5 /nobreak >nul

REM 打开浏览器
echo 🌐 打开浏览器...
start http://localhost:3001

echo.
echo ========================================
echo         ✅ 启动完成！
echo ========================================
echo.
echo 访问地址: http://localhost:3001
echo.
pause
