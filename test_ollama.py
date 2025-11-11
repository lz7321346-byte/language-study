#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Ollama本地AI模型是否正常工作
"""

import requests
import json
import sys

def test_ollama_connection():
    """测试Ollama服务连接"""
    print("🔍 测试Ollama服务连接...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print("✅ Ollama服务运行正常")
            print(f"📦 已安装的模型数量: {len(models)}")

            if models:
                print("📋 已安装的模型:")
                for model in models:
                    size_gb = model.get("size", 0) / (1024**3)
                    print(".1f"            else:
                print("⚠️  未安装任何模型")
                print("💡 请运行以下命令安装模型:")
                print("   ollama pull llama3.2")
            return True
        else:
            print(f"❌ Ollama服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Ollama服务")
        print("💡 请确保Ollama正在运行:")
        print("   1. 启动Ollama应用")
        print("   2. 或在命令行运行: ollama serve")
        return False
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

def test_model_generation():
    """测试模型生成能力"""
    print("\n🔍 测试AI模型生成能力...")

    # 检查是否有可用的模型
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        models = response.json().get("models", [])

        if not models:
            print("❌ 未找到已安装的模型，请先安装模型")
            return False

        # 使用第一个可用的模型
        model_name = models[0]["name"]
        print(f"🤖 使用模型: {model_name}")

        # 测试生成一个简单的故事
        prompt = """请写一个简短的英文故事，包含以下单词: happy, run, beautiful。故事要积极向上。"""

        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 200
            }
        }

        print("📝 正在生成测试故事...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            story = result.get("response", "").strip()

            if story:
                print("✅ 模型生成成功！")
                print("📖 生成的故事:")
                print("-" * 40)
                # 只显示前200个字符
                preview = story[:200] + "..." if len(story) > 200 else story
                print(preview)
                print("-" * 40)
                return True
            else:
                print("❌ 模型返回空内容")
                return False
        else:
            print(f"❌ 生成请求失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ 生成请求超时（模型可能需要更长时间）")
        print("💡 提示: 较大的模型可能需要更长时间来响应")
        return False
    except Exception as e:
        print(f"❌ 生成测试失败: {e}")
        return False

def test_story_generation():
    """测试完整的故事生成功能"""
    print("\n🔍 测试完整故事生成功能...")

    try:
        # 导入故事生成器
        sys.path.append('backend')
        from story_generator import StoryGenerator

        # 创建生成器实例
        generator = StoryGenerator()

        # 测试生成一个简单故事
        from pydantic import BaseModel
        from typing import List

        class TestRequest(BaseModel):
            words: List[str] = ["hello", "world", "happy"]
            user_level: str = "beginner"
            story_type: str = "daily"
            story_length: str = "short"
            custom_requirements: str = "请用简单的英语写一个积极的故事"

        import asyncio

        async def test_async():
            request = TestRequest()
            result = await generator.generate_story(request)
            return result

        # 运行异步测试
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(test_async())
        loop.close()

        if result and result.content:
            print("✅ 完整故事生成功能测试通过！")
            print("📖 生成的故事预览:")
            print("-" * 40)
            preview = result.content[:150] + "..." if len(result.content) > 150 else result.content
            print(preview)
            print("-" * 40)
            return True
        else:
            print("❌ 故事生成返回空结果")
            return False

    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 请确保已安装后端依赖: cd backend && pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ 故事生成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("🧪 Ollama本地AI模型测试工具")
    print("=" * 50)

    print("这个工具将测试您的Ollama安装和AI模型是否正常工作")
    print()

    # 测试项目
    tests = [
        ("Ollama服务连接测试", test_ollama_connection),
        ("AI模型生成能力测试", test_model_generation),
        ("完整故事生成功能测试", test_story_generation),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"⚠️  {test_name} 未完全通过")
        except Exception as e:
            print(f"❌ {test_name} 出现异常: {e}")

    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 项测试通过")

    if passed == total:
        print("🎉 所有测试通过！您的Ollama环境配置正确。")
        print("\n🚀 现在您可以运行单词学习应用了！")
        print("   Windows: 双击 start.bat")
        print("   Linux/Mac: ./start.sh")
    elif passed >= 1:
        print("⚠️  部分测试通过，基本功能可用但可能存在问题。")
        print("\n🔧 建议检查:")
        print("   1. Ollama服务是否正在运行")
        print("   2. 是否安装了合适的模型")
        print("   3. 网络连接是否正常")
    else:
        print("❌ 测试失败，请检查Ollama安装和配置。")
        print("\n🔧 故障排除步骤:")
        print("   1. 访问 https://ollama.ai/download 安装Ollama")
        print("   2. 运行: ollama pull llama3.2")
        print("   3. 确保Ollama服务正在运行")

    print("=" * 50)

if __name__ == "__main__":
    main()
