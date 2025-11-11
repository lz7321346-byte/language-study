#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
只安装核心依赖，确保应用能启动
"""

import subprocess
import sys

print("安装核心依赖（Flask等）...")
print("=" * 30)

core_deps = [
    'Flask==2.3.3',
    'Flask-CORS==4.0.0',
    'pydantic==2.5.0',
    'python-dotenv==1.0.0',
    'requests==2.31.0'
]

for dep in core_deps:
    print(f"安装 {dep}...")
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--user', dep],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"  ✅ {dep.split('==')[0]} 安装成功")
        else:
            print(f"  ❌ {dep.split('==')[0]} 安装失败")
            print(f"  错误: {result.stderr[-100:]}")
    except Exception as e:
        print(f"  ❌ {dep.split('==')[0]} 安装异常: {e}")

print("\n" + "=" * 30)
print("安装完成！")
print("现在可以运行: python no_venv_start.py")
