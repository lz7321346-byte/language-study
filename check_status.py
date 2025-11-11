#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的状态检查脚本
"""

import os
import subprocess
import sys

def check_python():
    """检查Python"""
    try:
        result = subprocess.run([sys.executable, '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Python正常:", result.stdout.strip())
            return True
        else:
            print("❌ Python检查失败")
            return False
    except:
        print("❌ Python未找到")
        return False

def check_node():
    """检查Node.js"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Node.js正常:", result.stdout.strip())
            return True
        else:
            print("❌ Node.js检查失败")
            return False
    except:
        print("❌ Node.js未找到")
        return False

def check_files():
    """检查项目文件"""
    print("\n📁 检查项目文件:")

    files_to_check = [
        ('backend/app.py', '后端主文件'),
        ('frontend/package.json', '前端配置文件'),
        ('frontend/src/App.js', '前端主文件'),
        ('config/metagpt_config.yaml', 'AI配置文件')
    ]

    all_exist = True
    for file_path, desc in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {desc}存在")
        else:
            print(f"❌ {desc}缺失: {file_path}")
            all_exist = False

    # 检查前端依赖
    if os.path.exists('frontend/node_modules'):
        print("✅ 前端依赖已安装")
    else:
        print("⚠️  前端依赖未安装 (需要运行 npm install)")

    return all_exist

def check_ports():
    """检查端口占用"""
    print("\n🔌 检查端口占用:")

    import socket
    ports_to_check = [3001, 5000]

    for port in ports_to_check:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()

            service = "前端服务" if port == 3001 else "后端API"
            if result == 0:
                print(f"❌ 端口 {port} ({service}) 被占用")
            else:
                print(f"✅ 端口 {port} ({service}) 可用")
        except:
            print(f"⚠️  端口 {port} 检查失败")

def check_processes():
    """检查进程"""
    print("\n⚙️  检查运行进程:")

    try:
        # 检查Python进程
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], capture_output=True, text=True)
        python_count = result.stdout.count('python.exe')
        if python_count > 0:
            print(f"✅ 发现 {python_count} 个Python进程运行中")
        else:
            print("ℹ️  未发现Python进程")

        # 检查Node.js进程
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq node.exe'], capture_output=True, text=True)
        node_count = result.stdout.count('node.exe')
        if node_count > 0:
            print(f"✅ 发现 {node_count} 个Node.js进程运行中")
        else:
            print("ℹ️  未发现Node.js进程")

    except:
        print("⚠️  进程检查失败")

def main():
    """主函数"""
    print("=" * 50)
    print("🔍 单词学习应用 - 状态检查")
    print("=" * 50)

    # 检查环境
    python_ok = check_python()
    node_ok = check_node()

    # 检查文件
    files_ok = check_files()

    # 检查端口
    check_ports()

    # 检查进程
    check_processes()

    print("\n" + "=" * 50)
    print("📋 诊断结果和建议:")
    print("=" * 50)

    issues = []

    if not python_ok:
        issues.append("安装Python 3.9+")
        print("🔧 需要安装Python: https://www.python.org/downloads/")

    if not node_ok:
        issues.append("安装Node.js 16+")
        print("🔧 需要安装Node.js: https://nodejs.org/")

    if not os.path.exists('frontend/node_modules'):
        issues.append("安装前端依赖")
        print("🔧 需要安装前端依赖: cd frontend && npm install")

    if issues:
        print(f"\n⚠️  发现 {len(issues)} 个问题需要解决:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print("\n🚀 解决后，运行以下命令启动:")
        print("   后端: cd backend && python app.py")
        print("   前端: cd frontend && npm start")
        print("   访问: http://localhost:3001")
    else:
        print("✅ 环境检查通过！")
        print("\n🚀 启动命令:")
        print("   1. 启动后端: cd backend && python app.py")
        print("   2. 启动前端: cd frontend && npm start")
        print("   3. 访问应用: http://localhost:3001")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()