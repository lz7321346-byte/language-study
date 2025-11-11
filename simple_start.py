#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的单词学习应用启动器
"""

import os
import subprocess
import time
import webbrowser

def main():
    print("单词学习应用 - 简单启动器")
    print("=" * 40)

    # 检查目录
    if not os.path.exists('frontend/package.json'):
        print("错误: 请在vocabulary_story_app目录下运行此脚本")
        input("按回车键退出...")
        return

    print("1. 安装前端依赖...")
    try:
        os.chdir('frontend')
        subprocess.run(['npm', 'install'], check=True)
        print("✅ 前端依赖安装完成")
        os.chdir('..')
    except:
        print("⚠️ 前端依赖安装可能有问题，继续启动...")

    print("2. 安装后端依赖...")
    try:
        os.chdir('backend')
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ 后端依赖安装完成")
        os.chdir('..')
    except:
        print("⚠️ 后端依赖安装可能有问题，继续启动...")

    print("3. 启动后端服务...")
    try:
        subprocess.Popen(['python', 'backend/app.py'])
        print("✅ 后端启动")
    except Exception as e:
        print(f"❌ 后端启动失败: {e}")

    time.sleep(5)

    print("4. 启动前端服务...")
    try:
        os.chdir('frontend')
        subprocess.Popen(['npm', 'start'])
        print("✅ 前端启动")
        os.chdir('..')
    except Exception as e:
        print(f"❌ 前端启动失败: {e}")

    time.sleep(8)

    print("5. 打开浏览器...")
    webbrowser.open('http://localhost:3001')

    print("\n🎉 启动完成！")
    print("请访问: http://localhost:3001")

if __name__ == "__main__":
    main()
