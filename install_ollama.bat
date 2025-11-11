@echo off
chcp 65001 >nul
title Ollama模型安装器

echo ========================================
echo       Ollama AI模型安装器
echo ========================================
echo.

echo [1/3] 检查Ollama安装...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Ollama
    echo.
    echo 请先安装Ollama：
    echo 1. 访问: https://ollama.ai/download
    echo 2. 下载Windows版本
    echo 3. 安装并重启此脚本
    echo.
    pause
    exit /b 1
)
echo ✅ Ollama已安装
echo.

echo [2/3] 启动Ollama服务...
echo (如果服务已在运行，此步骤会失败但不影响使用)
ollama serve >nul 2>&1
timeout /t 2 /nobreak >nul
echo ✅ Ollama服务检查完成
echo.

echo [3/3] 下载AI模型...
echo 正在下载 llama3.2 (约2GB，需要一些时间)...
echo.

ollama pull llama3.2

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo         🎉 安装成功！
    echo ========================================
    echo.
    echo AI模型已准备就绪，现在可以启动单词学习应用了！
    echo.
    echo 运行 start_services.bat 启动应用
    echo.
) else (
    echo.
    echo ========================================
    echo         ❌ 安装失败
    echo ========================================
    echo.
    echo 请检查网络连接后重试，或手动运行：
    echo ollama pull llama3.2
    echo.
)

echo 按任意键退出...
pause >nul
