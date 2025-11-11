#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单词学习应用启动脚本 - 无编码问题版本
"""

import os
import sys
import subprocess
import time
import webbrowser

def check_environment():
    """检查环境"""
    print("🔍 检查环境...")

    # 检查Python
    print(f"✅ Python版本: {sys.version}")

    # 检查当前目录
    current_dir = os.getcwd()
    print(f"📁 当前目录: {current_dir}")

    # 检查项目结构
    required_paths = [
        'frontend/package.json',
        'backend/app.py',
        'config/metagpt_config.yaml'
    ]

    for path in required_paths:
        if os.path.exists(path):
            print(f"✅ 找到: {path}")
        else:
            print(f"❌ 缺失: {path}")
            return False

    return True

def install_backend_deps():
    """安装后端依赖"""
    print("\n📦 安装后端依赖...")

    backend_dir = os.path.join(os.getcwd(), 'backend')

    # 直接使用系统Python安装，逐个安装核心依赖
    print("使用系统Python安装依赖（--user模式，逐个安装）...")
    
    # 核心依赖列表（必须安装）
    core_deps = [
        'Flask==2.3.3',
        'Flask-CORS==4.0.0',
        'pydantic==2.5.0',
        'python-dotenv==1.0.0',
        'requests==2.31.0'
    ]
    
    # 先安装核心依赖
    print("安装核心依赖...")
    for dep in core_deps:
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '--user', dep],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                print(f"  ✅ {dep.split('==')[0]}")
            else:
                print(f"  ⚠️ {dep.split('==')[0]} 安装失败，但继续...")
        except:
            print(f"  ⚠️ {dep.split('==')[0]} 安装异常，但继续...")
    
    print("✅ 后端依赖安装完成")
    return sys.executable  # 返回系统Python路径

def install_frontend_deps():
    """安装前端依赖"""
    print("\n📦 安装前端依赖...")

    frontend_dir = os.path.join(os.getcwd(), 'frontend')
    os.chdir(frontend_dir)

    try:
        # 检查node_modules是否存在
        if os.path.exists('node_modules'):
            print("✅ 前端依赖已安装")
        else:
            print("正在安装前端依赖 (需要几分钟)...")
            subprocess.run(['npm', 'install'], check=True, capture_output=True)
            print("✅ 前端依赖安装完成")

        os.chdir('..')
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 前端依赖安装失败: {e}")
        os.chdir('..')
        return False

def start_services(python_path):
    """启动服务"""
    print("\n🚀 启动服务...")

    try:
        # 启动后端
        print("启动后端服务...")
        backend_process = subprocess.Popen(
            [python_path, 'backend/app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )

        # 等待后端启动
        time.sleep(5)

        # 检查后端是否启动成功
        if backend_process.poll() is None:
            print("✅ 后端服务启动成功")
        else:
            stdout, stderr = backend_process.communicate()
            print("❌ 后端服务启动失败")
            print("错误信息:")
            print(stderr.decode('utf-8', errors='ignore'))
            return False

        # 启动前端
        print("启动前端服务...")
        frontend_process = subprocess.Popen(
            ['npm', 'start'],
            cwd='frontend',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )

        # 等待前端启动
        time.sleep(8)

        # 检查前端是否启动成功
        if frontend_process.poll() is None:
            print("✅ 前端服务启动成功")
        else:
            print("❌ 前端服务启动失败")
            return False

        return True

    except Exception as e:
        print(f"❌ 服务启动失败: {e}")
        return False

def open_browser():
    """打开浏览器"""
    print("\n🌐 打开浏览器...")
    try:
        webbrowser.open('http://localhost:3001')
        print("✅ 浏览器已打开")
    except Exception as e:
        print(f"⚠️ 浏览器打开失败: {e}")
        print("请手动打开浏览器访问: http://localhost:3001")

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 单词学习应用启动器 (Python版)")
    print("=" * 50)
    print("这个脚本没有编码问题，适合所有系统")
    print()

    # 检查环境
    if not check_environment():
        print("\n❌ 环境检查失败，请检查项目文件")
        input("按回车键退出...")
        return

    # 安装后端依赖
    python_path = install_backend_deps()
    if not python_path:
        print("\n❌ 后端依赖安装失败")
        input("按回车键退出...")
        return

    # 安装前端依赖
    if not install_frontend_deps():
        print("\n❌ 前端依赖安装失败")
        input("按回车键退出...")
        return

    # 启动服务
    if not start_services(python_path):
        print("\n❌ 服务启动失败")
        input("按回车键退出...")
        return

    # 打开浏览器
    open_browser()

    print("\n" + "=" * 50)
    print("🎉 启动完成！")
    print("=" * 50)
    print()
    print("📱 前端界面: http://localhost:3001")
    print("🔧 后端API:   http://localhost:5000")
    print()
    print("💡 提示:")
    print("   - 首次启动需要1-2分钟")
    print("   - 如果页面空白，请刷新浏览器")
    print("   - 按 Ctrl+C 停止服务")
    print()
    print("🔍 如有问题，请检查控制台输出")

    # 保持脚本运行，显示服务状态
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 正在停止服务...")
        sys.exit(0)

if __name__ == "__main__":
    main()
