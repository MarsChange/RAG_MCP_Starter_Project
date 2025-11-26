# 🚀 RAG_MCP_Starter_Project

一个基于 Python 的 RAG（检索增强生成）项目，集成了 MCP（模型上下文协议）服务器，使 AI 代理能够与外部工具和文件系统交互。<br>
这个项目是[https://github.com/KelvinQiu802/llm-mcp-rag/](https://github.com/KelvinQiu802/llm-mcp-rag/)的Python复现，[knowledge](./knowledge/)目录下的文件也来源于此仓库

## ✨ 功能特性

- 🔍 **RAG 集成**：使用嵌入向量从知识库中检索相关上下文
- 🔌 **MCP 支持**：连接到 MCP 服务器以执行工具
- ⚡ **异步架构**：使用 async/await 构建，实现高效的 I/O 操作
- 💬 **流式响应**：从大语言模型获取实时流式输出
- 🛠️ **工具调用**：基于 LLM 决策自动调用工具

## 📋 前置要求

- 📦 Node.js（用于 `npx`）
- 🎯 uv 包管理器（用于 `uvx`）

## 🔧 安装指南

### 1️⃣ 安装 npx（通过 Node.js）

#### 🍎 macOS
```bash
# 使用 Homebrew
brew install node

# 验证安装
npx --version
```

#### 🐧 Linux
```bash
# 使用 NodeSource 仓库（Ubuntu/Debian）
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 使用包管理器（Fedora/RHEL）
sudo dnf install nodejs

# 验证安装
npx --version
```

### 2️⃣ 安装 uvx（通过 uv）

#### 🍎 macOS
```bash
# 使用 Homebrew
brew install uv

# 验证安装
uvx --version
```

#### 🐧 Linux
```bash
# 使用 pip
pip install uv

# 或使用 curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# 验证安装
uvx --version
```

### 3️⃣ 安装 Python 依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows 系统使用: venv\Scripts\activate

# 安装依赖
pip install openai python-dotenv mcp

# RAG 功能所需
pip install numpy  # 或其他嵌入库
```

### 4️⃣ 配置环境变量

1. 复制模板文件：
```bash
cp .env.template .env
```

2. 编辑 `.env` 文件并填入您的配置：
```bash
API_KEY="your-api-key-here"
BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
BASE_MODEL_NAME="qwen-max"
EMBEDDING_MODEL_NAME="text-embedding-v3"
```

**📝 配置说明：**
- `API_KEY`：您的 LLM 提供商 API 密钥（例如 OpenAI、通义千问等）
- `BASE_URL`：API 端点 URL
- `BASE_MODEL_NAME`：要使用的主要 LLM 模型
- `EMBEDDING_MODEL_NAME`：用于生成文本嵌入的模型

## 📁 项目结构

```
RAG_MCP_Starter_Project/
├── main.py                 # 🎯 程序入口
├── .env.template           # ⚙️ 环境变量模板
├── knowledge/              # 📚 知识库目录
├── output/                 # 📤 生成文件的输出目录
└── utils/
    ├── agent.py            # 🤖 Agent 编排逻辑
    ├── chat.py             # 💬 LLM 聊天接口
    ├── mcp_client.py       # 🔌 MCP 客户端实现
    ├── embedding.py        # 🧠 嵌入和检索
    ├── vector_utils.py     # 📊 向量存储工具
    └── log_func.py         # 📝 日志工具
```

## 📂 Utils 目录文件说明

### 🤖 `agent.py`
Agent 编排工作流：
- 管理 MCP 客户端连接
- 处理工具调用循环
- 协调 LLM 和 MCP 工具之间的交互

### 💬 `chat.py`
LLM 聊天接口：
- 管理与 OpenAI 兼容 API 的对话
- 处理流式响应
- 处理 LLM 响应中的工具调用

### 🔌 `mcp_client.py`
MCP（模型上下文协议）客户端：
- 通过 stdio 连接到 MCP 服务器
- 管理异步上下文生命周期
- 提供工具发现和调用功能

### 🧠 `embedding.py`
RAG 嵌入和检索：
- 为文档生成嵌入向量
- 使用向量相似度检索相关上下文
- 管理知识库的向量存储

### 📊 `vector_utils.py`
向量操作：
- `vector_item`：存储嵌入向量和文本对
- `vector_store`：内存中的向量数据库
- `cosine_similarity`：计算向量之间的相似度

### 📝 `log_func.py`
日志工具：
- 格式化并显示分段标题
- 提高控制台输出的可读性

## 🎮 使用方法

### 🚀 基本用法

```bash
python main.py
```

### 📖 工作流程

1. 🔄 **初始化**：加载知识库并创建嵌入向量
2. 🔍 **上下文检索**：使用 RAG 检索相关文档
3. ⚙️ **Agent 设置**：初始化 MCP 客户端（fetch、filesystem）
4. 🎯 **任务执行**：LLM 使用工具处理任务
5. 🛠️ **工具调用**：Agent 根据需要自动调用工具
6. 📤 **输出**：在 `output/` 目录生成结果

### ✏️ 自定义任务

编辑 `main.py` 中的 `TASK_PROMPT`：

```python
TASK_PROMPT = "在这里输入您的自定义任务..."
```

### 📚 添加知识

将文本文件放入 `knowledge/` 目录。系统将自动：
1. 📖 读取文件
2. 🧠 生成嵌入向量
3. 🔗 将它们用作 RAG 的上下文

## 🔌 使用的 MCP 服务器

本项目连接到两个 MCP 服务器：

1. 🌐 **fetch**：网页抓取功能（通过 `uvx mcp-server-fetch`）
2. 📁 **filesystem**：文件操作（通过 `npx @modelcontextprotocol/server-filesystem`）

## 🐛 故障排除

### ❌ "No module named 'mcp'" 错误
```bash
pip install mcp
```

### ❌ "uvx: command not found" 错误
按照上面的安装步骤安装 uv。

### ❌ "npx: command not found" 错误
按照上面的安装步骤安装 Node.js。

### 💭 LLM 返回空响应
- 🔑 检查 `.env` 中的 API 密钥
- 🔗 验证 `BASE_URL` 和模型名称是否正确
- 🛠️ 确保模型支持工具调用功能

## 👨‍💻 开发指南

### ➕ 添加新的 MCP 工具

1. 在 `main.py` 中创建新的 `MCPClient` 实例：
```python
newMCP = MCPClient(args=["服务器参数"], command="npx")
```

2. 添加到 agent 初始化：
```python
agent = Agent(mcp_clients=[fetchMCP, fileMCP, newMCP], ...)
```

### 🔄 添加新的嵌入模型

修改 `.env` 以使用不同的embedding模型或提供商。

## 🛠️ 技术栈

- 🐍 **Python 3.12+**：主要编程语言
- 🤖 **OpenAI SDK**：LLM API 调用
- 🔌 **MCP (Model Context Protocol)**：工具集成
- ⚡ **asyncio**：异步编程
- 📊 **numpy**：向量计算