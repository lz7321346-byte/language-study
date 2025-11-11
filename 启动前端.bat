@echo off
chcp 65001 >nul
title 启动前端服务

echo ========================================
echo      启动前端服务
echo ========================================
echo.

REM 检查Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js未安装
    echo.
    echo 请访问 https://nodejs.org/ 下载并安装Node.js
    echo 安装完成后重新运行此脚本
    pause
    exit /b 1
)

echo ✅ Node.js已安装
node --version

echo.
echo 进入前端目录...
cd frontend

if not exist "package.json" (
    echo ❌ 未找到package.json
    echo 请确保在vocabulary_story_app目录下运行此脚本
    pause
    exit /b 1
)

echo ✅ 找到package.json
echo.

REM 检查node_modules
if not exist "node_modules" (
    echo 📦 安装前端依赖...
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
    echo.
)

echo 🚀 启动前端服务...
echo 前端将在 http://localhost:3001 运行
echo.
echo 按 Ctrl+C 停止服务
echo.

call npm start
