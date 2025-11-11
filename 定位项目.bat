@echo off
echo ========================================
echo       项目定位工具
echo ========================================
echo.

echo 当前目录: %CD%
echo.

REM 检查当前目录
if exist "frontend\package.json" (
    echo ✅ 已在vocabulary_story_app目录
    echo 项目路径: %CD%
    goto :show_commands
)

REM 检查上级目录
cd ..
if exist "vocabulary_story_app" (
    echo ✅ 找到vocabulary_story_app目录
    cd vocabulary_story_app
    echo 项目路径: %CD%
    goto :show_commands
)

REM 检查其他可能位置
cd ..
if exist "vocabulary_story_app" (
    cd vocabulary_story_app
    echo ✅ 在上级目录找到项目
    echo 项目路径: %CD%
    goto :show_commands
)

REM 如果都找不到，显示搜索结果
echo ❌ 未找到vocabulary_story_app目录
echo.
echo 请手动定位项目文件夹，然后运行：
echo cd [项目路径]\vocabulary_story_app\frontend
echo npm install
echo.
echo 或者使用资源管理器查找vocabulary_story_app文件夹
echo.
pause
exit /b 1

:show_commands
echo.
echo ========================================
echo         🎯 执行命令
echo ========================================
echo.
echo 1. 安装前端依赖:
echo    cd frontend
echo    npm install
echo.
echo 2. 启动前端服务:
echo    npm start
echo.
echo 3. 或者使用一键启动:
echo    双击运行 一键启动.bat
echo.
echo 项目已准备就绪！
echo.
pause
