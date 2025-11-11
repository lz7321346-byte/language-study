@echo off
chcp 65001 >nul
title 单词学习应用启动器

echo ========================================
echo      单词学习应用启动器
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未安装Python
    echo 请访问 https://www.python.org/downloads/ 下载Python 3.9+
    pause
    exit /b 1
)

echo 正在启动应用...
echo.

REM 运行无虚拟环境启动脚本
python no_venv_start.py

pause
