# MCP 基础示例代码

本目录包含 MCP 学习的基础示例代码。

## 📁 目录结构

```
examples/
├── typescript-hello-world/   # TypeScript 版本的 Hello World
│   ├── src/
│   │   └── index.ts         # 服务器主文件
│   ├── package.json         # 依赖配置
│   └── tsconfig.json        # TypeScript 配置
│
└── python-hello-world/       # Python 版本的 Hello World
    ├── server.py            # 服务器主文件
    └── requirements.txt     # 依赖配置
```

## 🚀 快速开始

### TypeScript 版本

```bash
cd typescript-hello-world

# 安装依赖
npm install

# 构建
npm run build

# 运行
npm start
```

### Python 版本

```bash
cd python-hello-world

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行
python server.py
```

## 🧪 测试服务器

### 使用 MCP Inspector

```bash
# 安装 Inspector
npm install -g @modelcontextprotocol/inspector

# 启动 Inspector
npx @modelcontextprotocol/inspector

# 在浏览器中打开 http://localhost:5173
# 然后添加服务器配置（见下文）
```

**TypeScript 服务器配置**：
```json
{
  "command": "node",
  "args": ["/绝对路径/to/typescript-hello-world/build/index.js"]
}
```

**Python 服务器配置**：
```json
{
  "command": "python",
  "args": ["/绝对路径/to/python-hello-world/server.py"]
}
```

### 集成到 Claude Desktop

编辑 Claude Desktop 配置文件：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

添加服务器配置：

```json
{
  "mcpServers": {
    "hello-world-ts": {
      "command": "node",
      "args": ["/绝对路径/to/typescript-hello-world/build/index.js"]
    },
    "hello-world-py": {
      "command": "python",
      "args": ["/绝对路径/to/python-hello-world/server.py"]
    }
  }
}
```

## 📚 学习重点

### TypeScript 版本展示

- ✅ 使用 `@modelcontextprotocol/sdk` 创建服务器
- ✅ 定义和注册工具
- ✅ 处理请求和响应
- ✅ 错误处理和日志

### Python 版本展示

- ✅ 使用 `FastMCP` 快速创建服务器
- ✅ 使用装饰器定义工具和资源
- ✅ 类型注解和文档字符串
- ✅ Stdio 传输配置

## 🔍 代码解析

### 关键概念

**1. 服务器初始化**

TypeScript:
```typescript
const server = new Server(
  { name: "hello-world-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);
```

Python:
```python
mcp = FastMCP("hello-world-server")
```

**2. 定义工具**

TypeScript:
```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  // 处理工具调用
});
```

Python:
```python
@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

**3. 启动服务器**

TypeScript:
```typescript
const transport = new StdioServerTransport();
await server.connect(transport);
```

Python:
```python
async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
    await mcp.run(read_stream, write_stream, mcp.create_initialization_options())
```

## 🐛 常见问题

### TypeScript

**问题**: `Cannot find module '@modelcontextprotocol/sdk'`  
**解决**: 运行 `npm install`

**问题**: 编译错误  
**解决**: 检查 TypeScript 版本 >= 5.0

### Python

**问题**: `ModuleNotFoundError: No module named 'mcp'`  
**解决**: 激活虚拟环境并运行 `pip install -r requirements.txt`

**问题**: 服务器无响应  
**解决**: 检查是否正确使用 stdio 传输

## 📖 下一步

完成这些示例后，你可以：

1. 修改代码添加更多工具
2. 尝试添加资源（Resources）
3. 探索提示词（Prompts）
4. 学习进阶篇内容

## 💡 提示

- 使用 `console.error()` (TS) 或 `print(..., file=sys.stderr)` (Python) 输出日志
- stdin/stdout 用于 MCP 协议通信，不要用于普通输出
- 始终使用绝对路径配置服务器

---

**Happy Coding! 🎉**