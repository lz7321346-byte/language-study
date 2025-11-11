@echo off
title 完整诊断工具

echo ========================================
echo      单词学习应用 - 完整诊断
echo ========================================
echo.

echo [1/8] 系统信息检查...
echo.

echo 操作系统: Windows
ver

echo.
echo 用户名: %USERNAME%

echo.
echo 当前目录: %CD%

echo.
echo [2/8] Python环境检查...
python --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python未安装
    echo    请安装Python 3.9+: https://www.python.org/downloads/
) else (
    echo ✅ Python正常
)

echo.
echo [3/8] Node.js环境检查...
node --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js未安装
    echo    请安装Node.js 16+: https://nodejs.org/
) else (
    echo ✅ Node.js正常
)

npm --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ npm未安装
    echo    npm应该随Node.js一起安装
) else (
    echo ✅ npm正常
)

echo.
echo [4/8] Ollama检查...
ollama --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Ollama未安装
) else (
    echo ✅ Ollama已安装
    ollama list 2>nul | findstr llama3.2 >nul 2>&1
    if %errorlevel% neq 0 (
        echo ⚠️  未找到llama3.2模型
    ) else (
        echo ✅ llama3.2模型已安装
    )
)

echo.
echo [5/8] 项目文件检查...
if not exist "backend\app.py" (
    echo ❌ 后端文件缺失: backend\app.py
    echo    请检查项目文件是否完整
) else (
    echo ✅ 后端文件存在
)

if not exist "frontend\package.json" (
    echo ❌ 前端文件缺失: frontend\package.json
    echo    请检查项目文件是否完整
) else (
    echo ✅ 前端文件存在
)

if not exist "frontend\node_modules" (
    echo ⚠️  前端依赖未安装
    echo    建议运行: setup_frontend.bat
) else (
    echo ✅ 前端依赖已安装
)

if not exist "backend\venv" (
    echo ⚠️  Python虚拟环境未创建
    echo    建议运行: cd backend && python -m venv venv
) else (
    echo ✅ Python虚拟环境存在
)

echo.
echo [6/8] 端口检查...
echo.

echo 检查端口 5000 (后端)...
netstat -ano | findstr :5000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ 端口5000被占用
    netstat -ano | findstr :5000
) else (
    echo ✅ 端口5000可用
)

echo.
echo 检查端口 3001 (前端)...
netstat -ano | findstr :3001 >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ 端口3001被占用
    netstat -ano | findstr :3001
) else (
    echo ✅ 端口3001可用
)

echo.
echo [7/8] 进程检查...
echo.

echo Python进程:
tasklist /FI "IMAGENAME eq python.exe" /NH 2>nul

echo.
echo Node.js进程:
tasklist /FI "IMAGENAME eq node.exe" /NH 2>nul

echo.
echo [8/8] 网络连接测试...
echo.

echo 测试本地连接...
ping -n 1 127.0.0.1 >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 本地网络异常
) else (
    echo ✅ 本地网络正常
)

echo.
echo ========================================
echo          📊 诊断完成
echo ========================================
echo.
echo 🎯 主要问题和解决方案:
echo.

if not exist "frontend\node_modules" (
    echo 🔧 前端依赖缺失
    echo    解决: 运行 setup_frontend.bat
    echo.
)

netstat -ano | findstr :3001 >nul 2>&1
if %errorlevel% equ 0 (
    echo 🔧 端口3001被占用
    echo    解决: 运行 cleanup.bat 清理进程
    echo.
)

netstat -ano | findstr :5000 >nul 2>&1
if %errorlevel% equ 0 (
    echo 🔧 端口5000被占用
    echo    解决: 运行 cleanup.bat 清理进程
    echo.
)

echo 🚀 启动建议:
echo    1. 运行: cleanup.bat (清理环境)
echo    2. 运行: setup_frontend.bat (安装前端依赖)
echo    3. 运行: direct_start.bat (启动服务)
echo.

goto :end

:error
echo.
echo ❌ 发现严重问题，请先解决上述问题后再试
echo.

:end
echo 按任意键退出...
pause >nul
