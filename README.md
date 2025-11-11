# 情景背单词小程序

🎉 **完全免费的AI英语学习应用！** 集成本地开源AI模型，通过个性化故事生成帮助用户在语境中记忆单词，无需任何API费用！

🚀 **核心优势**：
- 🤖 **免费本地AI**：使用Ollama运行开源模型，完全离线无成本
- 📖 **智能故事生成**：AI根据单词自动生成情景故事
- 🎯 **个性化学习**：根据水平和偏好定制学习内容
- 📊 **学习跟踪**：详细的进度统计和效果分析

## 项目结构

```
vocabulary_story_app/
├── backend/          # Python后端服务
│   ├── app.py       # Flask主应用
│   ├── story_generator.py  # 规则引擎故事生成器（离线可用）
│   ├── vocabulary_manager.py  # 单词管理器
│   ├── user_data.py  # 偏好与学习统计存储
│   └── requirements.txt
├── frontend/         # React前端应用
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.js
│   └── package.json
├── config/           # 配置文件
│   ├── metagpt_config.yaml
│   └── story_templates.json
└── data/            # 数据文件
    ├── vocabulary.json
    └── user_data.json
```

## 功能特性

- 🤖 **免费本地AI**：集成Ollama本地模型，完全免费无API费用
- 📚 **每日单词学习**：智能推荐单词学习计划
- 🧠 **FSRS智能复习**：先进的间隔重复算法，最优复习时间安排
- 🎤 **语音识别练习**：实时发音评估，听说结合学习
- 📖 **情景故事生成**：AI自动生成包含指定单词的个性化故事
- 🎯 **水平自适应**：根据用户水平调整故事难度
- 📊 **学习统计**：跟踪学习进度和效果分析
- ⚙️ **个性化设置**：自定义学习偏好和故事类型
- 🔊 **语音功能**：单词发音和故事朗读

## 🧠 后端能力亮点（全新升级）

- 🔁 **离线故事生成引擎**：内置基于提示词模板的规则引擎，即使没有MetaGPT或外部LLM也能生成语境故事。
- 📚 **可配置词库系统**：`data/vocabulary.json` 支持多语言、多难度标签，后端会根据日期稳定推送每日单词。
- 🧑‍💻 **偏好与进度存储**：`user_data.py` 使用线程安全的JSON存储，支持更新偏好与学习统计。
- 🌍 **多语言模板**：`config/story_templates.json` 让你能快速新增不同语言的故事开头/结尾模板。
- 🧪 **RESTful API**：统一返回 `{success, data}` 结构，方便前端与测试脚本快速集成。

## 🚀 快速开始

### 🚀 一键启动（超级简单）
```bash
# ⭐⭐⭐⭐⭐ 推荐：无虚拟环境启动（解决所有路径问题）
# 如果首次运行失败，先运行: python install_core.py
python no_venv_start.py

# ⭐⭐⭐ 超级简单：假设依赖已安装，直接启动
python just_start.py

# ⭐⭐ 简单启动：自动安装依赖
python easy_start.py

# ⭐ 最快启动：直接安装依赖，无虚拟环境
python quick_start.py

# 🚀 主启动脚本：已修复，无虚拟环境
python start.py

# 📱 简单版本：基础功能
python simple_start.py

# 🔧 测试后端：诊断启动问题
python test_backend.py

# 📋 备选方案：批处理文件
# 如果Python脚本都不工作，尝试这些：
# 启动应用.bat      # 调用Python脚本
# 一键启动.bat      # 完整版（可能有编码问题）
# 加速安装.bat      # 加速版
```

### 其他启动方式
```bash
# 方法1: 完整启动（包含AI模型检查和自动下载）
start_services.bat

# 方法2: 快速启动（跳过AI模型检查）
quick_start.bat

# 方法3: 直接启动（无检查，最快）
direct_start.bat

# 方法4: 手动启动（逐步检查）
manual_start.bat

# 方法5: 仅安装AI模型
install_ollama.bat

# 方法6: 清理所有进程（重启前运行）
cleanup.bat
```

### 手动启动
```bash
# 1. 启动后端
cd backend && python app.py

# 2. 启动前端（新终端窗口）
cd frontend && npm start
```

### 故障排除
```bash
# 运行故障排除工具
troubleshoot.bat
```

## 🌐 访问应用

- **前端界面**: http://localhost:3001
- **后端API**: http://localhost:5000

## 💡 重要说明

### 🎉 完全免费的AI功能！

本应用使用**本地开源AI模型**，无需任何API费用：

1. **安装Ollama**：[ollama.ai/download](https://ollama.ai/download)
2. **下载免费模型**：`ollama pull llama3.2`
3. **开始使用**：享受无限的AI故事生成！

### 🚀 三种AI使用方案

- **推荐**：本地Ollama（完全免费）
- **备选**：Groq免费额度
- **高级**：OpenAI/Claude等付费服务

### 🔧 常见问题解决

如果遇到"拒绝连接"错误：

1. **检查端口占用**：
   ```bash
   netstat -ano | findstr "3001\|5000"
   ```

2. **杀死占用进程**：
   ```bash
   taskkill /PID <进程ID> /F
   ```

3. **重新启动服务**：
   ```bash
   start_services.bat
   ```

4. **检查防火墙**：确保端口3001和5000未被阻止

## 技术栈

- **后端**：Python Flask + MetaGPT
- **前端**：React + TypeScript + Material-UI
- **数据存储**：SQLite + JSON
- **AI引擎**：MetaGPT (支持多种LLM)
