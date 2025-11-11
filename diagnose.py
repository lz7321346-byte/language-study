#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用诊断脚本 - 检查各项服务状态
"""

import socket
import requests
import subprocess
import sys
import time
import os

def check_port(port, service_name):
    """检查端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        if result == 0:
            print(f"✅ {service_name} (端口 {port}) - 正在运行")
            return True
        else:
            print(f"❌ {service_name} (端口 {port}) - 未运行")
            return False
    except Exception as e:
        print(f"⚠️  {service_name} (端口 {port}) - 检查失败: {e}")
        return False

def test_api_endpoint(url, service_name):
    """测试API端点"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {service_name} - 正常响应")
            return True
        else:
            print(f"⚠️  {service_name} - 响应码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {service_name} - 连接失败")
        return False
    except Exception as e:
        print(f"⚠️  {service_name} - 错误: {e}")
        return False

def check_ollama():
    """检查Ollama服务"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=3)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama服务 - 正常运行 ({len(models)} 个模型)")
            if models:
                llama_models = [m for m in models if 'llama' in m['name'].lower()]
                if llama_models:
                    print(f"   🤖 发现Llama模型: {[m['name'] for m in llama_models[:2]]}")
                else:
                    print("   ⚠️  未发现Llama模型")
            return True
        else:
            print("⚠️  Ollama服务 - 响应异常")
            return False
    except Exception as e:
        print(f"❌ Ollama服务 - 未运行: {e}")
        return False

def check_processes():
    """检查相关进程"""
    print("\n🔍 检查运行进程...")
    try:
        # 检查Python进程
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], capture_output=True, text=True)
        python_processes = [line for line in result.stdout.split('\n') if 'python.exe' in line.lower()]
        if python_processes:
            print(f"✅ 发现 {len(python_processes)} 个Python进程")
        else:
            print("⚠️  未发现Python进程")

        # 检查node进程
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq node.exe'], capture_output=True, text=True)
        node_processes = [line for line in result.stdout.split('\n') if 'node.exe' in line.lower()]
        if node_processes:
            print(f"✅ 发现 {len(node_processes)} 个Node.js进程")
        else:
            print("⚠️  未发现Node.js进程")

    except Exception as e:
        print(f"⚠️  进程检查失败: {e}")

def main():
    """主诊断函数"""
    print("=" * 60)
    print("🔧 情景背单词小程序 - 系统诊断")
    print("=" * 60)

    print("检查各项服务状态...\n")

    # 检查端口
    backend_ok = check_port(5000, "后端服务")
    frontend_ok = check_port(3001, "前端服务")

    print()

    # 测试API
    if backend_ok:
        api_ok = test_api_endpoint('http://localhost:5000/api/health', '后端健康检查')
        vocab_ok = test_api_endpoint('http://localhost:5000/api/vocabulary/daily?count=1', '单词API')
    else:
        api_ok = vocab_ok = False

    print()

    # 检查Ollama
    ollama_ok = check_ollama()

    print()

    # 检查进程
    check_processes()

    print("\n" + "=" * 60)

    # 提供解决方案
    if not backend_ok:
        print("🔧 后端服务未运行:")
        print("   cd vocabulary_story_app/backend")
        print("   python app.py")
        print()

    if not frontend_ok:
        print("🔧 前端服务未运行:")
        print("   cd vocabulary_story_app/frontend")
        print("   npm start")
        print()

    if not ollama_ok:
        print("🔧 Ollama未运行:")
        print("   1. 安装Ollama: https://ollama.ai/download")
        print("   2. 启动服务: ollama serve")
        print("   3. 下载模型: ollama pull llama3.2")
        print()

    if backend_ok and frontend_ok and api_ok and ollama_ok:
        print("🎉 所有服务正常运行！")
        print("🌐 打开浏览器访问: http://localhost:3001")
    else:
        print("⚠️  发现问题，请按照上述建议修复")

    print("=" * 60)

if __name__ == "__main__":
    main()
