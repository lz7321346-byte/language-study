#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
无虚拟环境启动脚本 - 直接使用系统Python，完全跳过虚拟环境
"""

import os
import subprocess
import time
import webbrowser
import sys

def main():
    print("=" * 50)
    print("🚀 单词学习应用启动器（无虚拟环境版）")
    print("=" * 50)
    print()

    # 检查目录
    if not os.path.exists('frontend/package.json'):
        print("❌ 请在vocabulary_story_app目录下运行此脚本")
        input("按回车退出...")
        exit(1)

    # 安装后端依赖到系统Python（使用--user避免权限问题）
    print("📦 [1/4] 安装后端依赖...")
    
    # 核心依赖列表（必须安装）
    core_deps = [
        'Flask==2.3.3',
        'Flask-CORS==4.0.0',
        'pydantic==2.5.0',
        'python-dotenv==1.0.0',
        'requests==2.31.0'
    ]
    
    # 可选依赖列表
    optional_deps = [
        'openai==1.12.0',
        'anthropic==0.7.8',
        'google-generativeai==0.3.2'
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
    
    # 尝试安装可选依赖
    print("安装可选依赖...")
    for dep in optional_deps:
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '--user', dep],
                capture_output=True,
                text=True,
                timeout=60
            )
        except:
            pass  # 可选依赖失败不影响
    
    print("✅ 后端依赖安装完成")

    # 安装前端依赖
    print("\n📦 [2/4] 安装前端依赖...")
    try:
        os.chdir('frontend')
        if not os.path.exists('node_modules'):
            result = subprocess.run(
                ['npm', 'install', '--no-optional'],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                print("✅ 前端依赖安装完成")
            else:
                print("⚠️ 前端依赖安装有警告，但继续...")
        else:
            print("✅ 前端依赖已存在")
        os.chdir('..')
    except subprocess.TimeoutExpired:
        print("⚠️ 安装超时，但继续启动...")
        if not os.path.exists('frontend'):
            os.chdir('..')
    except Exception as e:
        print(f"⚠️ 前端安装有问题: {e}，但继续启动...")
        if not os.path.exists('frontend'):
            os.chdir('..')

    # 启动后端
    print("\n🚀 [3/4] 启动后端服务...")
    try:
        backend_process = subprocess.Popen(
            [sys.executable, 'backend/app.py'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✅ 后端服务已启动（端口5000）")
    except Exception as e:
        print(f"❌ 后端启动失败: {e}")
        print("请检查Flask是否已安装: pip install --user Flask Flask-CORS")
        input("按回车退出...")
        exit(1)

    # 等待后端启动
    time.sleep(3)

    # 启动前端
    print("\n🚀 [4/4] 启动前端服务...")
    
    # 检查Node.js是否安装
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Node.js已安装: {result.stdout.strip()}")
        else:
            print("❌ Node.js未正确安装")
            print("请访问 https://nodejs.org/ 下载并安装Node.js")
            print("后端服务已启动，您可以手动启动前端：")
            print("  1. 打开新的命令提示符")
            print("  2. cd vocabulary_story_app\\frontend")
            print("  3. npm start")
            os.chdir('..')
            return
    except FileNotFoundError:
        print("❌ Node.js未安装")
        print("请访问 https://nodejs.org/ 下载并安装Node.js")
        print("后端服务已启动，您可以手动启动前端：")
        print("  1. 打开新的命令提示符")
        print("  2. cd vocabulary_story_app\\frontend")
        print("  3. npm start")
        os.chdir('..')
        return
    except Exception as e:
        print(f"⚠️ 检查Node.js时出错: {e}")
        print("尝试继续启动前端...")
    
    # 检查npm是否可用
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ npm已安装: {result.stdout.strip()}")
        else:
            print("❌ npm不可用")
            os.chdir('..')
            return
    except FileNotFoundError:
        print("❌ npm未找到")
        print("请确保Node.js已正确安装")
        os.chdir('..')
        return
    except Exception as e:
        print(f"⚠️ 检查npm时出错: {e}")
    
    # 启动前端服务
    try:
        os.chdir('frontend')
        frontend_process = subprocess.Popen(
            ['npm', 'start'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True  # 使用shell=True来确保能找到npm
        )
        os.chdir('..')
        print("✅ 前端服务已启动（端口3001）")
    except Exception as e:
        print(f"❌ 前端启动失败: {e}")
        print("\n💡 手动启动前端的方法：")
        print("  1. 打开新的命令提示符窗口")
        print("  2. 运行以下命令：")
        print("     cd vocabulary_story_app\\frontend")
        print("     npm start")
        print("\n后端服务已启动，您可以先访问后端API: http://localhost:5000")

    # 等待前端启动
    time.sleep(8)

    # 打开浏览器
    print("\n🌐 打开浏览器...")
    try:
        webbrowser.open('http://localhost:3001')
        print("✅ 浏览器已打开")
    except:
        print("⚠️ 浏览器打开失败，请手动访问: http://localhost:3001")

    print("\n" + "=" * 50)
    print("🎉 应用启动完成！")
    print("=" * 50)
    print()
    print("📱 前端界面: http://localhost:3001")
    print("🔧 后端API:   http://localhost:5000")
    print()
    print("💡 提示:")
    print("   - 如果页面空白，请等待10-15秒后刷新")
    print("   - 如果连接失败，请检查服务是否正常运行")
    print("   - 按 Ctrl+C 停止服务")
    print()

    # 保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 正在停止服务...")
        backend_process.terminate()
        if 'frontend_process' in locals():
            frontend_process.terminate()

if __name__ == "__main__":
    main()
