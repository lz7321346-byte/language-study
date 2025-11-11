#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接启动脚本 - 假设依赖已安装，跳过所有检查
"""

import os
import subprocess
import time
import webbrowser
import sys

def main():
    print("🚀 直接启动单词学习应用")
    print("=" * 30)
    print("假设所有依赖已安装，跳过检查")

    # 强制启动后端
    print("启动后端服务...")
    try:
        subprocess.Popen([sys.executable, 'backend/app.py'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        print("✅ 后端已启动")
    except Exception as e:
        print(f"⚠️ 后端启动可能有问题: {e}")

    time.sleep(2)

    # 启动前端
    print("启动前端服务...")
    try:
        os.chdir('frontend')
        subprocess.Popen(['npm', 'start'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        os.chdir('..')
        print("✅ 前端已启动")
    except Exception as e:
        print(f"⚠️ 前端启动可能有问题: {e}")

    time.sleep(3)

    # 打开浏览器
    print("🌐 打开浏览器...")
    try:
        webbrowser.open('http://localhost:3001')
        print("✅ 浏览器已打开")
    except:
        print("⚠️ 浏览器打开失败，请手动访问 http://localhost:3001")

    print("\n" + "=" * 50)
    print("🎉 应用启动完成！")
    print("=" * 50)
    print("📱 前端: http://localhost:3001")
    print("🔧 后端: http://localhost:5000")
    print("\n💡 如果页面空白，请刷新浏览器")
    print("🔄 如果连接失败，请等待10-15秒后刷新")

if __name__ == "__main__":
    main()
