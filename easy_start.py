#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超级简单启动脚本 - 跳过所有依赖安装，直接启动
"""

import os
import subprocess
import time
import webbrowser
import sys

def main():
    print("超级简单启动 - 跳过依赖安装")
    print("=" * 35)

    # 检查是否在正确的目录
    if not os.path.exists('frontend/package.json'):
        print("请在vocabulary_story_app目录下运行此脚本")
        input("按回车退出...")
        exit(1)

    # 检查依赖是否已安装
    print("检查依赖状态...")
    backend_deps_ok = False
    frontend_deps_ok = False

    try:
        import flask
        backend_deps_ok = True
        print("✅ 后端依赖已安装")
    except ImportError:
        print("⚠️ 后端依赖未安装，将尝试安装")

    if os.path.exists('frontend/node_modules'):
        frontend_deps_ok = True
        print("✅ 前端依赖已安装")
    else:
        print("⚠️ 前端依赖未安装，将尝试安装")

    # 安装后端依赖（如果需要）
    if not backend_deps_ok:
        print("\n安装后端依赖...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', '-r', 'backend/requirements.txt'],
                         check=True, timeout=120)
            print("✅ 后端依赖安装完成")
        except:
            print("❌ 后端依赖安装失败，尝试跳过...")

    # 安装前端依赖（如果需要）
    if not frontend_deps_ok:
        print("\n安装前端依赖...")
        try:
            os.chdir('frontend')
            subprocess.run(['npm', 'install', '--no-optional'], check=True, timeout=180)
            os.chdir('..')
            print("✅ 前端依赖安装完成")
        except:
            print("❌ 前端依赖安装失败，尝试跳过...")
            if not os.path.exists('frontend'):
                os.chdir('..')

    # 直接启动后端
    print("\n启动后端服务...")
    try:
        backend_process = subprocess.Popen([sys.executable, 'backend/app.py'],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        print("✅ 后端启动")
    except Exception as e:
        print(f"❌ 后端启动失败: {e}")
        input("按回车退出...")
        exit(1)

    time.sleep(3)

    # 启动前端
    print("启动前端服务...")
    try:
        os.chdir('frontend')
        frontend_process = subprocess.Popen(['npm', 'start'],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
        os.chdir('..')
        print("✅ 前端启动")
    except Exception as e:
        print(f"❌ 前端启动失败: {e}")

    time.sleep(8)

    # 打开浏览器
    print("打开浏览器...")
    try:
        webbrowser.open('http://localhost:3001')
        print("✅ 浏览器已打开")
    except:
        print("⚠️ 浏览器打开失败，请手动访问 http://localhost:3001")

    print("\n" + "=" * 50)
    print("🎉 应用已启动！")
    print("=" * 50)
    print("前端: http://localhost:3001")
    print("后端: http://localhost:5000")
    print("\n按 Ctrl+C 停止服务")

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
