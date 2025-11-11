#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查应用状态并打开网页
"""

import webbrowser
import time
import subprocess
import sys

def check_backend():
    """检查后端是否运行"""
    try:
        import requests
        response = requests.get('http://localhost:5000/api/vocabulary/daily', timeout=2)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def check_frontend():
    """检查前端是否运行"""
    try:
        import requests
        response = requests.get('http://localhost:3001', timeout=2)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def main():
    print("=" * 50)
    print("🔍 检查应用状态...")
    print("=" * 50)
    print()

    # 检查后端
    print("检查后端服务（端口5000）...")
    if check_backend():
        print("✅ 后端服务运行中")
    else:
        print("❌ 后端服务未运行")
        print("   请先运行: python no_venv_start.py")
        print()

    # 检查前端
    print("检查前端服务（端口3001）...")
    if check_frontend():
        print("✅ 前端服务运行中")
    else:
        print("❌ 前端服务未运行")
        print("   请先运行: python no_venv_start.py")
        print()

    # 打开浏览器
    print("🌐 打开浏览器...")
    try:
        webbrowser.open('http://localhost:3001')
        print("✅ 浏览器已打开")
        print()
        print("如果页面空白或无法访问，请：")
        print("1. 等待10-15秒后刷新页面")
        print("2. 检查服务是否正在启动")
        print("3. 运行: python no_venv_start.py")
    except:
        print("⚠️ 浏览器打开失败")
        print("请手动访问: http://localhost:3001")

    print()
    print("=" * 50)
    print("📱 前端界面: http://localhost:3001")
    print("🔧 后端API:   http://localhost:5000")
    print("=" * 50)

if __name__ == "__main__":
    main()
