#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情景背单词小程序测试脚本
"""

import requests
import json
import time
import sys
import os

# 添加后端路径
sys.path.append('backend')

def test_backend_health():
    """测试后端健康检查"""
    print("🔍 测试后端健康检查...")
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 后端运行正常 - 状态: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ 后端响应异常 - 状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到后端: {e}")
        print("💡 请确保后端服务正在运行: cd backend && python app.py")
        return False

def test_vocabulary_api():
    """测试单词API"""
    print("\n🔍 测试单词API...")
    try:
        response = requests.get('http://localhost:5000/api/vocabulary/daily?count=5', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data'):
                words = data['data']
                print(f"✅ 成功获取 {len(words)} 个单词")
                for i, word in enumerate(words[:3], 1):
                    print(f"   {i}. {word['word']} - {word['meaning']}")
                return True
            else:
                print("❌ API返回数据格式错误")
                return False
        else:
            print(f"❌ 单词API响应异常 - 状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法访问单词API: {e}")
        return False

def test_user_preferences_api():
    """测试用户偏好API"""
    print("\n🔍 测试用户偏好API...")
    try:
        # 获取偏好
        response = requests.get('http://localhost:5000/api/user/preferences', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ 成功获取用户偏好设置")
                prefs = data.get('data', {})
                print(f"   故事类型: {prefs.get('story_type', 'unknown')}")
                print(f"   每日单词: {prefs.get('daily_words', 'unknown')}")
                return True
            else:
                print("❌ 获取偏好失败")
                return False
        else:
            print(f"❌ 偏好API响应异常 - 状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法访问偏好API: {e}")
        return False

def test_story_generation_api():
    """测试故事生成API（注意：需要有效的MetaGPT配置）"""
    print("\n🔍 测试故事生成API...")

    # 检查MetaGPT配置
    config_file = 'config/metagpt_config.yaml'
    if not os.path.exists(config_file):
        print("⚠️  未找到MetaGPT配置文件，跳过故事生成测试")
        print("💡 请配置 config/metagpt_config.yaml 文件")
        return False

    try:
        test_words = ["hello", "world", "beautiful"]
        payload = {
            "words": test_words,
            "user_level": "beginner",
            "story_type": "daily",
            "story_length": "short",
            "custom_requirements": "这是一个测试故事，请生成简单的句子。"
        }

        print(f"📝 尝试生成包含单词 {test_words} 的故事...")
        response = requests.post('http://localhost:5000/api/story/generate',
                               json=payload, timeout=60)

        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data'):
                story_data = data['data']
                print("✅ 故事生成成功！")
                print(f"   标题: {story_data.get('title', '无标题')}")
                print(f"   难度: {story_data.get('difficulty_level', 'unknown')}")
                print(f"   预计阅读时间: {story_data.get('estimated_reading_time', 0)} 分钟")
                words_used = story_data.get('words_used', [])
                print(f"   单词使用情况: {len([w for w in words_used if w.get('found', False)])}/{len(words_used)} 个单词被使用")
                return True
            else:
                print(f"❌ 故事生成失败: {data.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ 故事API响应异常 - 状态码: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   错误信息: {error_data.get('error', '无详细信息')}")
            except:
                print(f"   响应内容: {response.text[:200]}...")
            return False
    except requests.exceptions.Timeout:
        print("❌ 故事生成超时（可能需要更长的等待时间）")
        print("💡 MetaGPT可能需要更多时间来生成故事")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法访问故事生成API: {e}")
        return False

def test_learning_stats_api():
    """测试学习统计API"""
    print("\n🔍 测试学习统计API...")
    try:
        response = requests.get('http://localhost:5000/api/learning/stats', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data'):
                stats = data['data']
                print("✅ 成功获取学习统计")
                print(f"   已读故事数: {stats.get('total_stories', 0)}")
                print(f"   已学单词数: {stats.get('total_words_learned', 0)}")
                print(f"   连续学习天数: {stats.get('streak_days', 0)}")
                return True
            else:
                print("❌ 统计数据格式错误")
                return False
        else:
            print(f"❌ 统计API响应异常 - 状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法访问统计API: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("🎓 情景背单词小程序 - 功能测试")
    print("=" * 50)

    # 检查后端是否运行
    if not test_backend_health():
        print("\n❌ 后端服务未运行，请先启动后端服务：")
        print("   cd backend && python app.py")
        sys.exit(1)

    # 运行各项测试
    tests = [
        ("单词API测试", test_vocabulary_api),
        ("用户偏好API测试", test_user_preferences_api),
        ("学习统计API测试", test_learning_stats_api),
        ("故事生成API测试", test_story_generation_api),
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
        print("🎉 所有测试通过！应用运行正常。")
        print("\n🚀 现在您可以：")
        print("   1. 打开浏览器访问 http://localhost:3000")
        print("   2. 开始您的单词学习之旅！")
    else:
        print("⚠️  部分测试未通过，请检查配置和网络连接。")
        print("\n🔧 故障排除：")
        print("   1. 确保MetaGPT配置正确")
        print("   2. 检查网络连接")
        print("   3. 查看后端控制台错误信息")

    print("=" * 50)

if __name__ == "__main__":
    main()
