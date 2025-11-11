#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试单词学习应用
"""

import requests
import json
import time
import sys

def test_api():
    """测试API连接"""
    print("🔍 测试API连接...")

    try:
        # 测试健康检查
        response = requests.get('http://localhost:5000/api/health', timeout=10)
        if response.status_code == 200:
            print("✅ 后端服务正常运行")
            data = response.json()
            print(f"   状态: {data.get('status')}")
            print(f"   时间戳: {data.get('timestamp')}")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False

        # 测试单词API
        response = requests.get('http://localhost:5000/api/vocabulary/daily?count=3', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data'):
                words = data['data']
                print(f"✅ 单词API正常，获取到 {len(words)} 个单词")
                for word in words[:2]:
                    print(f"   - {word['word']}: {word['meaning']}")
            else:
                print("❌ 单词API返回数据错误")
                return False
        else:
            print(f"❌ 单词API失败: {response.status_code}")
            return False

        # 测试用户偏好
        response = requests.get('http://localhost:5000/api/user/preferences', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ 用户偏好API正常")
                prefs = data.get('data', {})
                print(f"   默认故事类型: {prefs.get('story_type')}")
                print(f"   每日单词数: {prefs.get('daily_words')}")
            else:
                print("❌ 用户偏好API返回数据错误")
        else:
            print(f"❌ 用户偏好API失败: {response.status_code}")

        # 测试学习统计
        response = requests.get('http://localhost:5000/api/learning/stats', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                stats = data.get('data', {})
                print("✅ 学习统计API正常")
                print(f"   已读故事数: {stats.get('total_stories')}")
                print(f"   已学单词数: {stats.get('total_words_learned')}")
                print(f"   连续学习天数: {stats.get('streak_days')}")
                print(f"   FSRS算法: {'启用' if stats.get('fsrs_enabled') else '未安装'}")
            else:
                print("❌ 学习统计API返回数据错误")
        else:
            print(f"❌ 学习统计API失败: {response.status_code}")

        return True

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务 (http://localhost:5000)")
        print("💡 请确保后端服务正在运行: cd backend && python app.py")
        return False
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")
        return False

def test_frontend():
    """测试前端服务"""
    print("\n🔍 检查前端服务...")
    try:
        # 简单检查前端端口是否开放
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 3001))
        sock.close()

        if result == 0:
            print("✅ 前端服务可能正在运行 (端口3001开放)")
            print("🌐 请在浏览器中访问: http://localhost:3001")
        else:
            print("⚠️ 前端服务可能未启动 (端口3001未开放)")
            print("💡 请运行: cd frontend && npm start")

    except Exception as e:
        print(f"⚠️ 前端服务检查失败: {e}")

def test_ollama():
    """测试Ollama服务"""
    print("\n🔍 检查Ollama服务...")
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("✅ Ollama服务正常运行")
            print(f"📦 已安装模型数量: {len(models)}")

            if models:
                llama_models = [m for m in models if 'llama' in m['name'].lower()]
                if llama_models:
                    print("🤖 发现Llama模型:")
                    for model in llama_models[:3]:
                        size_gb = model.get('size', 0) / (1024**3)
                        print(".1f"                else:
                    print("⚠️ 未发现Llama模型")
                    print("💡 建议安装: ollama pull llama3.2")
            else:
                print("⚠️ 未安装任何模型")
                print("💡 请运行: ollama pull llama3.2")
        else:
            print("❌ Ollama服务响应异常")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Ollama服务")
        print("💡 请确保Ollama正在运行")
        return False
    except Exception as e:
        print(f"❌ Ollama检查失败: {e}")
        return False

    return True

def main():
    """主测试函数"""
    print("=" * 60)
    print("🎓 情景背单词小程序 - 功能测试")
    print("=" * 60)

    print("这个脚本将测试应用的所有核心功能")
    print()

    # 测试各项功能
    api_ok = test_api()
    test_frontend()
    ollama_ok = test_ollama()

    print("\n" + "=" * 60)

    if api_ok and ollama_ok:
        print("🎉 恭喜！应用运行正常！")
        print("\n📋 可以使用以下功能:")
        print("   1. 🏠 首页概览 - 查看学习统计")
        print("   2. 📚 单词学习 - 学习新单词")
        print("   3. 🧠 单词复习 - 智能FSRS复习")
        print("   4. 📖 故事阅读器 - AI生成情景故事")
        print("   5. 📊 学习统计 - 查看详细数据")
        print("   6. ⚙️ 设置 - 个性化配置")
        print("\n🌐 打开浏览器访问: http://localhost:3001")
    else:
        print("⚠️ 部分功能可能存在问题")
        if not api_ok:
            print("   - 后端服务未启动或有问题")
        if not ollama_ok:
            print("   - Ollama未安装或未运行")
        print("\n🔧 请检查上述问题并重新运行测试")

    print("=" * 60)

if __name__ == "__main__":
    main()
