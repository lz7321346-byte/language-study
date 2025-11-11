@echo off
title 修复并启动单词学习应用

echo ========================================
echo   修复并启动单词学习应用
echo ========================================
echo.

echo [1/6] 检查当前目录...
cd
echo.

echo [2/6] 定位项目目录...
if exist "vocabulary_story_app" (
    echo ✅ 找到vocabulary_story_app目录
    cd vocabulary_story_app
) else (
    echo ❌ 未找到vocabulary_story_app目录
    echo 请确保vocabulary_story_app文件夹在当前目录
    pause
    exit /b 1
)

echo 当前目录: %CD%
echo.

echo [3/6] 检查项目结构...
if exist "frontend\package.json" (
    echo ✅ 前端配置文件存在
) else (
    echo ❌ 前端配置文件缺失
    pause
    exit /b 1
)

if exist "backend\app.py" (
    echo ✅ 后端主文件存在
) else (
    echo ❌ 后端主文件缺失
    pause
    exit /b 1
)

echo.
echo [4/6] 安装前端依赖...
cd frontend
if exist "node_modules" (
    echo ✅ 前端依赖已安装，跳过
) else (
    echo 📦 正在安装前端依赖...
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ 前端依赖安装失败
        echo 尝试使用国内镜像...
        call npm config set registry https://registry.npmmirror.com
        call npm install
        if %errorlevel% neq 0 (
            echo ❌ 安装仍然失败，请手动解决
            pause
            exit /b 1
        )
    )
    echo ✅ 前端依赖安装完成
)

cd ..
echo.

echo [5/6] 启动后端服务...
echo 命令: cd backend && python app.py
start "单词学习应用 - 后端" cmd /k "cd backend && echo 正在启动后端服务... && python app.py"

echo 等待5秒...
timeout /t 5 /nobreak >nul

echo.
echo [6/6] 启动前端服务...
echo 命令: cd frontend && npm start
start "单词学习应用 - 前端" cmd /k "cd frontend && echo 正在启动前端服务... && npm start"

echo.
echo ========================================
echo         ✅ 启动完成！
echo ========================================
echo.
echo 📱 应用访问地址:
echo    前端界面: http://localhost:3001
echo    后端API:   http://localhost:5000
echo.
echo 💡 注意事项:
echo   - 前端启动需要1-2分钟
echo   - 如果无法访问，请等待更长时间
echo   - 如有问题，请查看各个命令窗口的错误信息
echo.
echo 🔍 故障排除:
echo   - 运行: python check_status.py
echo.
pause
