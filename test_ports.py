#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端口连接测试脚本
"""

import socket
import requests
import time
import sys

def test_port(host, port, name):
    """测试端口连接"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            print(f"✅ {name} (端口 {port}) - 连接成功")
            return True
        else:
            print(f"❌ {name} (端口 {port}) - 连接失败")
            return False
    except Exception as e:
        print(f"⚠️  {name} (端口 {port}) - 错误: {e}")
        return False

def test_http(url, name):
    """测试HTTP连接"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {name} - HTTP响应正常")
            return True
        else:
            print(f"⚠️  {name} - HTTP状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name} - 连接被拒绝")
        return False
    except Exception as e:
        print(f"⚠️  {name} - 错误: {e}")
        return False

def main():
    print("=" * 50)
    print("🔍 单词学习应用 - 端口连接测试")
    print("=" * 50)
    print()

    print("测试服务端口连接...")
    print("-" * 30)

    # 测试端口
    frontend_ok = test_port('localhost', 3001, '前端服务')
    backend_ok = test_port('localhost', 5000, '后端服务')
    ollama_ok = test_port('localhost', 11434, 'Ollama服务')

    print()
    print("测试HTTP连接...")
    print("-" * 30)

    # 测试HTTP
    frontend_http = test_http('http://localhost:3001', '前端页面')
    backend_http = test_http('http://localhost:5000/api/health', '后端API')

    print()
    print("=" * 50)
    print("📊 测试结果总结")
    print("=" * 50)

    all_ok = frontend_ok and backend_ok and frontend_http and backend_http

    if all_ok:
        print("🎉 所有服务连接正常！")
        print("🌐 立即访问: http://localhost:3001")
    else:
        print("⚠️  发现连接问题：")
        print()

        if not frontend_ok:
            print("🔴 前端端口(3001)无法连接")
            print("   💡 解决方案:")
            print("      1. 检查前端服务是否启动: cd frontend && npm start")
            print("      2. 检查端口是否被占用: netstat -ano | findstr :3001")
            print()

        if not backend_ok:
            print("🔴 后端端口(5000)无法连接")
            print("   💡 解决方案:")
            print("      1. 检查后端服务是否启动: cd backend && python app.py")
            print("      2. 检查端口是否被占用: netstat -ano | findstr :5000")
            print()

        if not frontend_http and frontend_ok:
            print("🟡 前端HTTP响应异常")
            print("   💡 可能需要等待服务完全启动（1-2分钟）")
            print()

        if not backend_http and backend_ok:
            print("🟡 后端API响应异常")
            print("   💡 检查后端控制台是否有错误信息")
            print()

        if not ollama_ok:
            print("🟠 Ollama服务未运行")
            print("   💡 启动Ollama: ollama serve")
            print("   💡 下载模型: ollama pull llama3.2")
            print()

        print("🔧 快速修复:")
        print("   1. 运行: troubleshoot.bat")
        print("   2. 或重新运行: start_services.bat")

    print("=" * 50)

if __name__ == "__main__":
    main()
