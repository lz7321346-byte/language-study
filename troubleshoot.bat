@echo off
chcp 65001 >nul
title 故障排除工具

echo ========================================
echo     单词学习应用 - 故障排除工具
echo ========================================
echo.

echo [1/6] 检查端口占用情况...
echo.

echo 检查端口 3001 (前端)...
netstat -ano | findstr :3001 >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ 端口3001被占用
    echo    运行命令查看: netstat -ano | findstr :3001
    echo    杀死进程: taskkill /PID ^<PID^> /F
) else (
    echo ✅ 端口3001可用
)

echo.
echo 检查端口 5000 (后端)...
netstat -ano | findstr :5000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ 端口5000被占用
    echo    运行命令查看: netstat -ano | findstr :5000
    echo    杀死进程: taskkill /PID ^<PID^> /F
) else (
    echo ✅ 端口5000可用
)

echo.
echo [2/6] 检查Python进程...
tasklist /FI "IMAGENAME eq python.exe" /NH | findstr python.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 发现Python进程运行中
    tasklist /FI "IMAGENAME eq python.exe"
) else (
    echo ❌ 未发现Python进程
    echo    需要启动后端服务
)

echo.
echo [3/6] 检查Node.js进程...
tasklist /FI "IMAGENAME eq node.exe" /NH | findstr node.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 发现Node.js进程运行中
    tasklist /FI "IMAGENAME eq node.exe"
) else (
    echo ❌ 未发现Node.js进程
    echo    需要启动前端服务
)

echo.
echo [4/6] 测试网络连接...
echo.

echo 测试后端连接...
curl -s http://localhost:5000/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 后端API响应正常
) else (
    echo ❌ 后端API无响应
)

echo 测试前端连接...
curl -s http://localhost:3001 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 前端服务响应正常
) else (
    echo ❌ 前端服务无响应
)

echo 测试Ollama连接...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama服务正常
) else (
    echo ❌ Ollama服务无响应
    echo    请运行: ollama serve
)

echo.
echo [5/6] 检查防火墙设置...
echo 提示: 如果连接被拒绝，可能需要配置防火墙
echo       Windows Defender防火墙 -> 高级设置 -> 入站规则
echo       添加端口规则允许 3001 和 5000

echo.
echo [6/6] 生成解决方案...
echo.
echo ========================================
echo            🔧 解决方案
echo ========================================
echo.

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

echo.
echo 📋 如果仍然无法访问，请按以下步骤操作:
echo.

echo 1. 杀死所有相关进程:
echo    taskkill /F /IM python.exe /T 2>nul
echo    taskkill /F /IM node.exe /T 2>nul
echo.

echo 2. 重新安装依赖:
echo    cd backend && pip install -r requirements.txt
echo    cd frontend && npm install
echo.

echo 3. 重新启动服务:
echo    运行 start_services.bat
echo.

echo 4. 如果仍有问题，尝试更换端口:
echo    编辑 frontend\package.json 中的 PORT 设置
echo.

echo ========================================
echo 按任意键退出...
pause >nul
