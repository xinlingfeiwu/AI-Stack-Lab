# MCP 环境搭建：从零开始建立开发环境

> **学习目标**：完成 MCP 开发环境的完整搭建，并运行第一个 MCP 服务器

## 📌 本章内容

- 开发环境准备
- 安装 MCP SDK
- 创建第一个 MCP 服务器
- 使用 MCP Inspector 测试
- 集成到 Claude Desktop
- 常见问题排查

---

## 1. 开发环境准备

### 1.1 硬件要求

**最低要求**：
- CPU: 双核处理器
- 内存: 4GB RAM
- 磁盘: 2GB 可用空间

**推荐配置**：
- CPU: 四核或更好
- 内存: 8GB+ RAM
- 磁盘: 10GB+ 可用空间

### 1.2 必需软件

根据你选择的开发语言，需要安装相应的运行时：

#### TypeScript/JavaScript 路径

```bash
# 检查 Node.js 版本（需要 >= 18）
node --version  # 应显示 v18.0.0 或更高

# 检查 npm 版本
npm --version   # 应显示 9.0.0 或更高
```

**如果没有安装 Node.js**：

```bash
# macOS (使用 Homebrew)
brew install node

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Windows (使用 Chocolatey)
choco install nodejs

# 或下载安装包
# https://nodejs.org/
```

#### Python 路径

```bash
# 检查 Python 版本（需要 >= 3.10）
python3 --version  # 应显示 3.10.0 或更高
# 或
python --version
```

**如果没有安装 Python**：

```bash
# macOS (使用 Homebrew)
brew install python@3.11

# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3-pip

# Windows (使用 Chocolatey)
choco install python

# 或下载安装包
# https://www.python.org/downloads/
```

### 1.3 推荐工具

**代码编辑器**：
- **VS Code** (强烈推荐)
  ```bash
  # macOS
  brew install --cask visual-studio-code
  
  # Ubuntu
  snap install code --classic
  ```

**版本控制**：
```bash
# 检查 Git
git --version

# 如果没有，安装 Git
# macOS
brew install git

# Ubuntu
sudo apt install git
```

**Python 虚拟环境管理** (Python 用户)：
```bash
# 安装 uv (推荐的 Python 包管理器)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 pip
pip install uv
```

---

## 2. 创建项目

### 2.1 项目结构

创建一个工作目录：

```bash
mkdir mcp-getting-started
cd mcp-getting-started
```

最终的项目结构：

```
mcp-getting-started/
├── servers/              # MCP 服务器代码
│   ├── hello-world/      # 第一个服务器
│   ├── weather/          # 天气服务器示例
│   └── calculator/       # 计算器服务器示例
├── clients/              # MCP 客户端代码（可选）
└── README.md
```

创建目录：

```bash
mkdir -p servers/hello-world
mkdir -p servers/weather
mkdir -p servers/calculator
```

---

## 3. 安装 MCP SDK

### 选项 A: TypeScript/JavaScript

#### 3.1 初始化项目

```bash
cd servers/hello-world
npm init -y
```

#### 3.2 安装 MCP SDK

```bash
# 安装 MCP SDK (v1.x 稳定版)
npm install @modelcontextprotocol/sdk

# 安装 TypeScript 和类型定义
npm install -D typescript @types/node

# 初始化 TypeScript 配置
npx tsc --init
```

#### 3.3 配置 package.json

编辑 `package.json`：

```json
{
  "name": "hello-world-mcp-server",
  "version": "1.0.0",
  "description": "My first MCP server",
  "type": "module",
  "main": "build/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node build/index.js",
    "dev": "tsc && node build/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  }
}
```

#### 3.4 配置 tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

### 选项 B: Python

#### 3.1 创建虚拟环境

```bash
cd servers/hello-world

# 使用 uv (推荐)
uv venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate  # Windows

# 或使用 venv
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

#### 3.2 安装 MCP SDK

```bash
# 使用 uv
uv pip install mcp

# 或使用 pip
pip install mcp

# 可选：安装 CLI 工具用于测试
uv pip install "mcp[cli]"
```

#### 3.3 创建 requirements.txt

```bash
echo "mcp>=1.25,<2.0" > requirements.txt
```

---

## 4. 创建第一个 MCP 服务器

### TypeScript 版本

创建 `src/index.ts`：

```typescript
#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// 创建服务器实例
const server = new Server(
  {
    name: "hello-world-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 注册工具列表处理器
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "greet",
        description: "向用户打招呼",
        inputSchema: {
          type: "object",
          properties: {
            name: {
              type: "string",
              description: "要打招呼的人的名字",
            },
          },
          required: ["name"],
        },
      },
      {
        name: "add",
        description: "两个数字相加",
        inputSchema: {
          type: "object",
          properties: {
            a: {
              type: "number",
              description: "第一个数字",
            },
            b: {
              type: "number",
              description: "第二个数字",
            },
          },
          required: ["a", "b"],
        },
      },
    ],
  };
});

// 注册工具调用处理器
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "greet") {
    const userName = args.name as string;
    return {
      content: [
        {
          type: "text",
          text: `你好，${userName}！欢迎使用 MCP！🎉`,
        },
      ],
    };
  }

  if (name === "add") {
    const a = args.a as number;
    const b = args.b as number;
    const result = a + b;
    return {
      content: [
        {
          type: "text",
          text: `${a} + ${b} = ${result}`,
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Hello World MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
```

### Python 版本

创建 `server.py`：

```python
#!/usr/bin/env python3
"""
一个简单的 Hello World MCP 服务器
"""

import asyncio
from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务器实例
mcp = FastMCP("hello-world-server")

@mcp.tool()
def greet(name: str) -> str:
    """
    向用户打招呼
    
    Args:
        name: 要打招呼的人的名字
    
    Returns:
        问候消息
    """
    return f"你好，{name}！欢迎使用 MCP！🎉"

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    两个数字相加
    
    Args:
        a: 第一个数字
        b: 第二个数字
    
    Returns:
        两数之和
    """
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """
    获取个性化问候语
    
    Args:
        name: 用户名称
    
    Returns:
        个性化问候
    """
    return f"Hello, {name}! This is a resource."

# 启动服务器
if __name__ == "__main__":
    import mcp.server.stdio
    
    async def main():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await mcp.run(
                read_stream,
                write_stream,
                mcp.create_initialization_options()
            )
    
    asyncio.run(main())
```

---

## 5. 构建和运行

### TypeScript

```bash
# 构建
npm run build

# 运行
npm start
```

### Python

```bash
# 直接运行
python server.py

# 或使用 uv
uv run server.py
```

**运行成功的标志**：

服务器会输出类似信息：
```
Hello World MCP Server running on stdio
```

然后等待输入。这是正常的！MCP 服务器通过 stdin/stdout 通信。

按 `Ctrl+C` 停止服务器。

---

## 6. 使用 MCP Inspector 测试

MCP Inspector 是一个图形化测试工具，让你无需集成到 AI 应用就能测试服务器。

### 6.1 安装 MCP Inspector

```bash
# 全局安装（任意位置）
npm install -g @modelcontextprotocol/inspector

# 或使用 npx（无需安装）
npx @modelcontextprotocol/inspector
```

### 6.2 启动 Inspector

```bash
# 在项目根目录
npx @modelcontextprotocol/inspector
```

浏览器会自动打开 `http://localhost:5173`

### 6.3 连接到你的服务器

**对于 TypeScript 服务器**：

在 Inspector 界面中：
1. 点击 "Add Server"
2. 填写配置：
   ```json
   {
     "command": "node",
     "args": ["/path/to/your/project/build/index.js"]
   }
   ```
3. 点击 "Connect"

**对于 Python 服务器**：

```json
{
  "command": "python",
  "args": ["/path/to/your/project/server.py"]
}
```

**或者使用 uv**：

```json
{
  "command": "uv",
  "args": ["run", "/path/to/your/project/server.py"]
}
```

### 6.4 测试工具

连接成功后：

1. **列出工具**：
   - 点击 "List Tools"
   - 应该看到 `greet` 和 `add` 工具

2. **测试 greet 工具**：
   - 选择 "greet"
   - 输入参数: `{"name": "Alice"}`
   - 点击 "Call Tool"
   - 应该看到: "你好，Alice！欢迎使用 MCP！🎉"

3. **测试 add 工具**：
   - 选择 "add"
   - 输入参数: `{"a": 5, "b": 3}`
   - 点击 "Call Tool"
   - 应该看到: "5 + 3 = 8"

---

## 7. 集成到 Claude Desktop

现在让我们将服务器集成到 Claude Desktop，这样你就可以通过对话使用它。

### 7.1 安装 Claude Desktop

如果还没有安装：

- **macOS**: 从 [Claude.ai](https://claude.ai/download) 下载
- **Windows**: 从同一页面下载

### 7.2 配置 Claude Desktop

找到配置文件：

**macOS**:
```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows**:
```bash
code %APPDATA%\Claude\claude_desktop_config.json
```

编辑配置文件：

```json
{
  "mcpServers": {
    "hello-world": {
      "command": "node",
      "args": ["/绝对路径/to/your/project/build/index.js"]
    }
  }
}
```

**对于 Python**:
```json
{
  "mcpServers": {
    "hello-world": {
      "command": "python",
      "args": ["/绝对路径/to/your/project/server.py"]
    }
  }
}
```

**重要提示**：
- 使用**绝对路径**，不要使用 `~` 或相对路径
- Windows 用户使用反斜杠 `\\` 或正斜杠 `/`

### 7.3 重启 Claude Desktop

完全退出并重新启动 Claude Desktop。

### 7.4 测试集成

在 Claude Desktop 中尝试：

**对话示例**：
```
你：使用 greet 工具向 Bob 打个招呼

Claude：[调用 greet 工具]
你好，Bob！欢迎使用 MCP！🎉

你：帮我算一下 42 加 58 等于多少

Claude：[调用 add 工具]
42 + 58 = 100
```

---

## 8. 添加更多功能

让我们扩展服务器，添加一个资源示例。

### TypeScript: 添加资源

在 `src/index.ts` 中添加：

```typescript
import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// 在创建服务器时更新 capabilities
const server = new Server(
  {
    name: "hello-world-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},  // 添加这一行
    },
  }
);

// 添加资源列表处理器
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "memo://daily",
        name: "每日备忘录",
        description: "查看今天的待办事项",
        mimeType: "text/plain",
      },
    ],
  };
});

// 添加资源读取处理器
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === "memo://daily") {
    const today = new Date().toLocaleDateString("zh-CN");
    return {
      contents: [
        {
          uri,
          mimeType: "text/plain",
          text: `📅 ${today} 的待办事项：

1. 学习 MCP 基础知识 ✅
2. 创建第一个 MCP 服务器 ✅
3. 测试工具和资源
4. 探索更多可能性`,
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});
```

重新构建并测试：

```bash
npm run build
# 在 Inspector 或 Claude Desktop 中测试
```

---

## 9. 常见问题排查

### 问题 1: "找不到命令"

**症状**：
```
Error: spawn node ENOENT
```

**解决方案**：
- 确保 Node.js/Python 已添加到 PATH
- 使用绝对路径指定命令：
  ```json
  {
    "command": "/usr/local/bin/node",
    "args": ["/path/to/index.js"]
  }
  ```

### 问题 2: 服务器无响应

**症状**：Claude Desktop 或 Inspector 无法连接

**解决方案**：
1. 检查服务器是否正确启动
2. 查看 Claude Desktop 的日志：
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`
3. 确保路径正确且文件存在

### 问题 3: TypeScript 编译错误

**症状**：
```
error TS2307: Cannot find module '@modelcontextprotocol/sdk'
```

**解决方案**：
```bash
# 删除 node_modules 和 package-lock.json
rm -rf node_modules package-lock.json

# 重新安装
npm install
```

### 问题 4: Python 模块找不到

**症状**：
```
ModuleNotFoundError: No module named 'mcp'
```

**解决方案**：
```bash
# 确保在虚拟环境中
source .venv/bin/activate

# 重新安装
pip install mcp
```

### 问题 5: 权限错误

**症状**：
```
Error: EACCES: permission denied
```

**解决方案**：
```bash
# 给脚本执行权限
chmod +x server.py
# 或
chmod +x build/index.js
```

---

## 10. 调试技巧

### 10.1 添加日志

**TypeScript**:
```typescript
// 使用 console.error (不要用 console.log)
console.error("Tool called:", name, args);
```

**Python**:
```python
import sys
# 输出到 stderr
print(f"Tool called: {name}", file=sys.stderr)
```

### 10.2 查看通信

使用环境变量启用详细日志：

```bash
# TypeScript
DEBUG=mcp:* node build/index.js

# Python
MCP_DEBUG=1 python server.py
```

### 10.3 测试工具单独运行

```bash
# 在 Python 中测试函数
python -c "from server import greet; print(greet('Test'))"
```

---

## 11. 下一步学习

恭喜！你已经成功：

✅ 搭建了 MCP 开发环境  
✅ 创建了第一个 MCP 服务器  
✅ 使用 Inspector 测试了工具  
✅ 集成到了 Claude Desktop  
✅ 添加了资源功能  

**接下来你可以**：

1. **探索示例**：查看 `servers/` 下的其他示例
2. **学习进阶**：进入 [02-Intermediate](../02-Intermediate/) 模块
3. **阅读文档**：深入研究 [MCP 规范](https://modelcontextprotocol.io/)
4. **社区交流**：加入 [MCP Discord](https://discord.gg/anthropic)

---

## 📖 补充资源

**官方资源**：
- [MCP 快速开始](https://modelcontextprotocol.io/quickstart)
- [TypeScript SDK 文档](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK 文档](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)

**社区资源**：
- [MCP 服务器示例](https://github.com/modelcontextprotocol/servers)
- [Claude Desktop 配置指南](https://docs.anthropic.com/claude/docs/mcp)

---

## 🎉 恭喜！

你现在已经拥有了一个完整的 MCP 开发环境，并成功运行了第一个服务器。

在下一章中，我们将深入学习如何构建更复杂的 MCP 服务器！

---

*最后更新：2025-01-29*