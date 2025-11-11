#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动单词学习应用
"""

import os
import subprocess
import time
import webbrowser

print("快速启动单词学习应用")
print("=" * 30)

# 检查是否在正确的目录
if not os.path.exists('frontend/package.json'):
    print("请在vocabulary_story_app目录下运行此脚本")
    input("按回车退出...")
    exit(1)

print("启动后端...")
subprocess.Popen(['python', 'backend/app.py'])

time.sleep(3)

print("启动前端...")
os.chdir('frontend')
subprocess.Popen(['npm', 'start'])
os.chdir('..')

time.sleep(5)

print("打开浏览器...")
webbrowser.open('http://localhost:3001')

print("启动完成！访问 http://localhost:3001")
