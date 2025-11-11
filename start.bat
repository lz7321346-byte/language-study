@echo off
echo ========================================
echo   情景背单词小程序启动脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.9+
    pause
    exit /b 1
)

echo [2/4] 安装后端依赖...
cd backend
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 后端依赖安装失败
    pause
    exit /b 1
)

echo [3/4] 安装前端依赖...
cd ../frontend
if not exist node_modules (
    npm install
)
if errorlevel 1 (
    echo 错误: 前端依赖安装失败
    pause
    exit /b 1
)

echo [4/4] 检查AI模型配置...
cd ..
if not exist config\metagpt_config.yaml (
    echo 错误: 未找到MetaGPT配置文件
    pause
    exit /b 1
)

echo 检查Ollama服务...
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 未检测到Ollama安装
    echo 请访问 https://ollama.ai/download 下载并安装Ollama
    echo 然后运行: ollama pull llama3.2
    echo.
) else (
    echo ✓ 发现Ollama安装
    ollama list | findstr llama3.2 >nul 2>&1
    if %errorlevel% neq 0 (
        echo 警告: 未检测到llama3.2模型
        echo 请运行: ollama pull llama3.2
        echo.
    ) else (
        echo ✓ 发现llama3.2模型
    )
)

echo.
echo ========================================
echo        启动完成！
echo ========================================
echo.
echo 启动后端服务:
echo   cd backend && venv\Scripts\activate && python app.py
echo.
echo 启动前端服务:
echo   cd frontend && npm start
echo.
echo 后端将在 http://localhost:5000 运行
echo 前端将在 http://localhost:3001 运行
echo.
pause
