@echo off
chcp 65001 >nul
title 清理进程

echo ========================================
echo        清理单词学习应用进程
echo ========================================
echo.

echo [1/4] 停止Python进程...
tasklist /FI "IMAGENAME eq python.exe" /NH 2>nul | findstr python.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo 发现Python进程，正在停止...
    taskkill /F /IMAGENAME python.exe /T >nul 2>&1
    echo ✅ Python进程已停止
) else (
    echo ℹ️  未发现Python进程
)

echo.
echo [2/4] 停止Node.js进程...
tasklist /FI "IMAGENAME eq node.exe" /NH 2>nul | findstr node.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo 发现Node.js进程，正在停止...
    taskkill /F /IMAGENAME node.exe /T >nul 2>&1
    echo ✅ Node.js进程已停止
) else (
    echo ℹ️  未发现Node.js进程
)

echo.
echo [3/4] 清理端口占用...
echo 检查端口 5000...
netstat -ano | findstr :5000 >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
        echo 发现端口5000占用，PID: %%a
        taskkill /PID %%a /F >nul 2>&1
        echo ✅ 端口5000已清理
    )
) else (
    echo ℹ️  端口5000未被占用
)

echo 检查端口 3001...
netstat -ano | findstr :3001 >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3001') do (
        echo 发现端口3001占用，PID: %%a
        taskkill /PID %%a /F >nul 2>&1
        echo ✅ 端口3001已清理
    )
) else (
    echo ℹ️  端口3001未被占用
)

echo.
echo [4/4] 清理完成检查...
echo.
timeout /t 2 /nobreak >nul

netstat -ano | findstr "5000\|3001" >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  仍有端口被占用，请手动检查
) else (
    echo ✅ 端口清理完成
)

echo.
echo ========================================
echo         🧹 清理完成！
echo ========================================
echo.
echo 现在可以重新启动应用了！
echo 运行: start_services.bat
echo.
pause
