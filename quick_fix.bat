@echo off
echo ========================================
echo 快速修复 - 单词学习应用
echo ========================================
echo.
echo 当前目录: %CD%
echo.

REM 检查是否在正确的目录
if exist "vocabulary_story_app" (
    echo ✅ 找到vocabulary_story_app目录
    cd vocabulary_story_app
    goto :install_deps
) else (
    REM 检查是否已经在vocabulary_story_app目录
    if exist "frontend\package.json" (
        echo ✅ 已经在vocabulary_story_app目录
        goto :install_deps
    ) else (
        echo ❌ 未找到vocabulary_story_app目录
        echo.
        echo 请将此脚本放在vocabulary_story_app文件夹同级目录
        echo 或者直接在vocabulary_story_app文件夹中运行此脚本
        echo.
        pause
        exit /b 1
    )
)

:install_deps
echo.
echo [1/3] 检查前端依赖...
cd frontend
if exist "node_modules" (
    echo ✅ 前端依赖已安装
) else (
    echo 📦 安装前端依赖...
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ 安装失败，尝试国内镜像...
        call npm config set registry https://registry.npmmirror.com
        call npm install
    )
)
cd ..
echo.

echo [2/3] 启动后端服务...
start "后端服务" cmd /k "cd backend && python app.py"

echo [3/3] 启动前端服务...
start "前端服务" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo ✅ 启动完成！请等待1-2分钟
echo ========================================
echo.
echo 访问地址: http://localhost:3001
echo.
pause
