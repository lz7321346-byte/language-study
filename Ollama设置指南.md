# Ollama本地AI模型设置指南

## 📦 什么是Ollama？

Ollama是一个在本地运行开源大语言模型的工具，让您可以在自己的电脑上免费使用强大的AI模型，完全不需要API密钥或网络连接！

## 🚀 快速开始

### 1. 下载安装Ollama

访问 [ollama.ai/download](https://ollama.ai/download) 下载对应您系统的版本：

- **Windows**: 下载 `.exe` 安装包，双击安装
- **macOS**: 下载 `.dmg` 安装包，双击安装
- **Linux**: 运行安装脚本：
  ```bash
  curl -fsSL https://ollama.ai/install.sh | sh
  ```

### 2. 安装AI模型

打开命令行工具，运行以下命令下载模型：

#### 推荐模型（性能与资源平衡）：
```bash
# Llama 3.2 - Meta出品的优秀模型（2GB）
ollama pull llama3.2

# Qwen 2.5 - 腾讯出品，中英文都很好（4GB）
ollama pull qwen2.5:7b

# Mistral - 欧洲开源模型，性能均衡（4GB）
ollama pull mistral:7b
```

#### 轻量级模型（适合配置较低的电脑）：
```bash
# 更小的Llama模型（1.3GB）
ollama pull llama3.2:1b

# Phi-3 Mini（2.3GB）
ollama pull phi3:3.8b
```

#### 高性能模型（需要更好配置）：
```bash
# Llama 3 - 完整版（4.7GB）
ollama pull llama3

# Qwen 2.5 - 更大版本（8GB+）
ollama pull qwen2.5:14b
```

### 3. 测试安装

运行以下命令测试模型是否正常工作：

```bash
# 测试基本对话
ollama run llama3.2 "Hello, can you help me learn English?"

# 查看已安装的模型
ollama list

# 查看运行状态
ollama ps
```

### 4. 配置本项目

确保 `config/metagpt_config.yaml` 中的配置正确：

```yaml
llm:
  api_type: "ollama"
  model: "llama3.2"  # 或您安装的其他模型名
  base_url: "http://localhost:11434"
  api_key: ""  # 本地模型不需要API密钥
  timeout: 300
```

## 🎯 模型推荐

根据您的使用场景选择合适的模型：

### 英语学习场景
- **llama3.2** ⭐⭐⭐ - 通用优秀，英语表达流畅
- **qwen2.5:7b** ⭐⭐⭐ - 中英文切换自如，适合中文用户
- **mistral:7b** ⭐⭐ - 英语专业性强

### 电脑配置要求

| 模型大小 | 内存要求 | 适用场景 |
|---------|---------|---------|
| 1-2GB   | 4GB+    | 基础对话，简单任务 |
| 4GB     | 8GB+    | 故事生成，内容创作 |
| 8GB+    | 16GB+   | 复杂分析，高精度生成 |

## 🛠️ 高级配置

### 修改默认端口
```bash
# 设置环境变量
export OLLAMA_HOST=0.0.0.0:8080

# 然后重启Ollama服务
```

### 自定义模型参数
在配置文件中可以调整：
```yaml
llm:
  api_type: "ollama"
  model: "llama3.2"
  temperature: 0.7    # 创造性 (0.0-1.0)
  top_p: 0.9         # 多样性控制
  max_tokens: 1000   # 最大输出长度
```

### GPU加速（可选）
Ollama会自动检测并使用GPU，如果您有NVIDIA显卡，确保安装了CUDA。

## 🔧 故障排除

### 问题：模型下载慢或失败
```bash
# 使用国内镜像加速（可选）
export OLLAMA_REGISTRY=https://registry.ollama.ai
# 或使用代理
export HTTPS_PROXY=http://your-proxy:port
```

### 问题：内存不足
- 选择更小的模型
- 关闭其他程序
- 增加虚拟内存

### 问题：启动失败
```bash
# 检查服务状态
ollama serve

# 重新安装
ollama --version
```

### 问题：项目无法连接到Ollama
1. 确保Ollama正在运行：`ollama ps`
2. 检查端口是否被占用：`netstat -an | find "11434"`
3. 确认配置文件中的base_url正确

## 📊 性能对比

| 模型 | 英语质量 | 中文支持 | 推理速度 | 资源占用 |
|-----|---------|---------|---------|----------|
| llama3.2 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| qwen2.5:7b | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| mistral:7b | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| phi3:3.8b | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |

## 🎉 开始使用

安装完成后，运行我们的单词小程序：

```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

现在您就可以免费使用强大的AI来生成个性化的英语学习故事了！

## 📚 更多资源

- [Ollama官方文档](https://github.com/jmorganca/ollama)
- [Ollama模型库](https://ollama.ai/library)
- [开源模型介绍](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)
