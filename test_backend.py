#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后端测试脚本
"""

import os
import sys
import subprocess

def test_backend():
    print("测试后端启动...")
    print("=" * 30)

    # 检查Python版本
    print(f"Python版本: {sys.version}")

    # 检查依赖
    try:
        import flask
        print("✅ Flask 已安装")
    except ImportError:
        print("❌ Flask 未安装")

    try:
        import flask_cors
        print("✅ Flask-CORS 已安装")
    except ImportError:
        print("❌ Flask-CORS 未安装")

    try:
        from pydantic import BaseModel
        print("✅ Pydantic 已安装")
    except ImportError:
        print("❌ Pydantic 未安装")

    # 检查MetaGPT路径
    metagpt_path = os.path.join(os.getcwd(), 'MetaGPT-main')
    if os.path.exists(metagpt_path):
        print("✅ MetaGPT-main 目录存在")
        sys.path.append(metagpt_path)

        try:
            from metagpt.actions.action_node import ActionNode
            print("✅ MetaGPT ActionNode 可导入")
        except ImportError as e:
            print(f"❌ MetaGPT ActionNode 导入失败: {e}")

        try:
            from metagpt.llm import LLM
            print("✅ MetaGPT LLM 可导入")
        except ImportError as e:
            print(f"❌ MetaGPT LLM 导入失败: {e}")
    else:
        print("❌ MetaGPT-main 目录不存在")

    # 尝试启动后端
    print("\n尝试启动后端...")
    try:
        result = subprocess.run([sys.executable, 'backend/app.py'],
                              capture_output=True,
                              text=True,
                              timeout=10)
        print("后端启动结果:")
        print("STDOUT:", result.stdout[-500:])  # 最后500字符
        print("STDERR:", result.stderr[-500:])  # 最后500字符
        print(f"Return code: {result.returncode}")
    except subprocess.TimeoutExpired:
        print("✅ 后端启动成功（超时表示服务正在运行）")
    except Exception as e:
        print(f"❌ 后端启动失败: {e}")

if __name__ == "__main__":
    test_backend()
