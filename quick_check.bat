@echo off
title 快速检查

echo ========================================
echo      单词学习应用 - 快速检查
echo ========================================
echo.

echo [1/5] 检查Python...
python --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python未安装
) else (
    echo ✅ Python正常
)

echo.
echo [2/5] 检查Node.js...
node --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js未安装
) else (
    echo ✅ Node.js正常
)

echo.
echo [3/5] 检查项目文件...
if exist "backend\app.py" (
    echo ✅ 后端文件存在
) else (
    echo ❌ 后端文件缺失
)

if exist "frontend\package.json" (
    echo ✅ 前端文件存在
) else (
    echo ❌ 前端文件缺失
)

if exist "frontend\node_modules" (
    echo ✅ 前端依赖已安装
) else (
    echo ⚠️  前端依赖未安装
)

echo.
echo [4/5] 检查端口占用...
netstat -ano 2>nul | findstr :3001 >nul
if %errorlevel% equ 0 (
    echo ❌ 端口3001被占用
) else (
    echo ✅ 端口3001可用
)

netstat -ano 2>nul | findstr :5000 >nul
if %errorlevel% equ 0 (
    echo ❌ 端口5000被占用
) else (
    echo ✅ 端口5000可用
)

echo.
echo [5/5] 检查运行进程...
tasklist 2>nul | findstr python.exe >nul
if %errorlevel% equ 0 (
    echo ✅ 发现Python进程
) else (
    echo ℹ️  未发现Python进程
)

tasklist 2>nul | findstr node.exe >nul
if %errorlevel% equ 0 (
    echo ✅ 发现Node.js进程
) else (
    echo ℹ️  未发现Node.js进程
)

echo.
echo ========================================
echo          📊 检查完成
echo ========================================
echo.
echo 💡 建议步骤:
echo 1. 如果前端依赖未安装: 运行 setup_frontend.bat
echo 2. 如果端口被占用: 运行 cleanup.bat
echo 3. 启动服务: 运行 simple_start.bat
echo.
pause
