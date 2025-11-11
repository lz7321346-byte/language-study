@echo off
chcp 65001 >nul 2>&1
title 一键启动单词学习应用

echo.
echo ========================================
echo     🚀 一键启动单词学习应用
echo ========================================
echo.
echo 这个脚本会自动完成以下操作：
echo 1. 检测项目位置
echo 2. 安装前端依赖
echo 3. 启动后端服务
echo 4. 启动前端服务
echo 5. 打开浏览器
echo.
echo 请耐心等待...
echo.

REM 保存当前目录
set "ORIGINAL_DIR=%CD%"

REM 查找项目目录
if exist "vocabulary_story_app" (
    echo ✅ 找到vocabulary_story_app目录
    cd vocabulary_story_app
    goto :found_project
)

REM 检查是否已经在项目目录
if exist "frontend\package.json" (
    echo ✅ 已经在vocabulary_story_app目录
    goto :found_project
)

REM 在上级目录查找
cd ..
if exist "vocabulary_story_app" (
    echo ✅ 在上级目录找到vocabulary_story_app
    cd vocabulary_story_app
    goto :found_project
)

echo ❌ 未找到vocabulary_story_app目录
echo 请确保脚本在正确的位置运行
pause
exit /b 1

:found_project
echo 项目目录: %CD%
echo.

REM 检查Python
echo 🔍 检查Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装
    echo 请安装Python 3.9+: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python正常

REM 检查Node.js
echo.
echo 🔍 检查Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js未安装
    echo 请安装Node.js 16+: https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js正常

REM 检查项目文件
echo.
echo 🔍 检查项目文件...
if not exist "backend\app.py" (
    echo ❌ 后端文件缺失
    pause
    exit /b 1
)
if not exist "frontend\package.json" (
    echo ❌ 前端文件缺失
    pause
    exit /b 1
)
echo ✅ 项目文件完整

REM 安装前端依赖
echo.
echo 📦 安装前端依赖...
cd frontend
if exist "node_modules" (
    echo ✅ 前端依赖已安装
) else (
    echo 正在快速安装前端依赖...
    echo (使用国内镜像源加速下载)
    call npm config set registry https://registry.npmmirror.com >nul 2>&1
    call npm install --prefer-offline --no-audit
    if %errorlevel% neq 0 (
        echo 尝试强制安装...
        call npm install --force
        if %errorlevel% neq 0 (
            echo ❌ 前端依赖安装失败
            echo 请运行: 加速安装.bat
            pause
            exit /b 1
        )
    )
    echo ✅ 前端依赖安装完成
)
cd ..

REM 清理可能存在的进程
echo.
echo 🧹 清理旧进程...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1

REM 启动后端服务
echo.
echo 🚀 启动后端服务...
start "单词学习应用 - 后端" cmd /k "cd backend && python app.py"

REM 等待后端启动
echo 等待后端启动...
timeout /t 3 /nobreak >nul

REM 启动前端服务
echo.
echo 🚀 启动前端服务...
start "单词学习应用 - 前端" cmd /k "cd frontend && npm start"

REM 等待前端启动
echo 等待前端编译...
timeout /t 8 /nobreak >nul

REM 打开浏览器
echo.
echo 🌐 打开浏览器...
start http://localhost:3001

echo.
echo ========================================
echo         🎉 启动完成！
echo ========================================
echo.
echo 📱 应用现在应该在浏览器中打开
echo.
echo 如果浏览器没有自动打开，请手动访问:
echo http://localhost:3001
echo.
echo 💡 提示:
echo - 首次启动需要1-2分钟编译
echo - 如果页面空白，请刷新浏览器
echo - 后端运行在 http://localhost:5000
echo.
echo 🔍 如有问题，请查看后端和前端的命令窗口
echo.
pause
