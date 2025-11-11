@echo off
chcp 65001 >nul
title 前端环境设置

echo ========================================
echo       前端环境设置和启动
echo ========================================
echo.

echo [1/3] 检查Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Node.js
    echo.
    echo 请安装Node.js 16+:
    echo https://nodejs.org/
    echo.
    pause
    exit /b 1
)
echo ✅ Node.js已安装

npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到npm
    echo.
    echo npm应该随Node.js一起安装
    echo 请重新安装Node.js
    echo.
    pause
    exit /b 1
)
echo ✅ npm已安装

echo.
echo [2/3] 安装前端依赖...
if not exist "node_modules" (
    echo 📦 正在安装依赖包 (需要一些时间)...
    echo.
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        echo.
        echo 请检查网络连接后重试
        echo 或者手动运行: npm install
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
) else (
    echo ✅ 依赖已存在
)

echo.
echo [3/3] 启动前端服务...
echo 端口: 3001
echo 命令: npm start
echo.

start "前端服务" cmd /k "echo 正在启动前端服务... && npm start"

echo.
echo ========================================
echo         🚀 前端启动完成！
echo ========================================
echo.
echo 📱 前端界面: http://localhost:3001
echo.
echo 💡 等待1-2分钟让服务完全启动
echo.
echo 如果仍然无法访问，请检查:
echo 1. 端口3001是否被占用
echo 2. 防火墙设置
echo 3. 尝试不同浏览器
echo.
pause
