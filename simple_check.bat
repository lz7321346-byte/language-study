@echo off
echo ========================================
echo 单词学习应用 - 简单检查
echo ========================================
echo.

REM 检查Python
echo [1/3] 检查Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python 已安装
) else (
    echo ❌ Python 未安装
)

REM 检查Node.js
echo.
echo [2/3] 检查Node.js...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Node.js 已安装
) else (
    echo ❌ Node.js 未安装
)

REM 检查文件
echo.
echo [3/3] 检查文件...
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
    echo ❌ 前端依赖未安装
)

echo.
echo ========================================
echo 检查完成！
echo ========================================
echo.
echo 建议步骤：
echo 1. 如果缺少依赖：运行 setup_frontend.bat
echo 2. 启动后端：cd backend && python app.py
echo 3. 启动前端：cd frontend && npm start
echo 4. 访问：http://localhost:3001
echo.
pause
