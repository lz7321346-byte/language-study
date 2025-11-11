@echo off
chcp 65001 >nul
title 加速安装前端依赖

echo ========================================
echo       加速安装前端依赖
echo ========================================
echo.

cd frontend

echo [1/3] 设置国内镜像源...
call npm config set registry https://registry.npmmirror.com
echo ✅ 已设置国内镜像源
echo.

echo [2/3] 清理npm缓存...
call npm cache clean --force >nul 2>&1
echo ✅ 已清理缓存
echo.

echo [3/3] 使用cnpm安装依赖...
echo 正在快速安装前端依赖...
echo.

call npm install --prefer-offline --no-audit

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo         🎉 安装完成！
    echo ========================================
    echo.
    echo 现在可以运行一键启动脚本了！
    echo.
) else (
    echo.
    echo ❌ 安装失败，尝试备用方法...
    echo.

    REM 如果cnpm失败，尝试yarn
    where yarn >nul 2>&1
    if %errorlevel% equ 0 (
        echo 尝试使用yarn安装...
        call yarn install
    ) else (
        echo 尝试使用npm强制安装...
        call npm install --force
    )
)

echo.
pause
