# MCP 架构设计：深入理解协议的内部机制

> **学习目标**：掌握 MCP 的技术架构、组件交互和通信机制

## 📌 本章内容

- MCP 架构总览
- 四大核心组件详解
- 通信协议与传输层
- 生命周期管理
- 三大原语（Primitives）
- 数据流与消息格式

---

## 1. MCP 架构总览

MCP 采用**客户端-服务器架构**，这种设计使其具有模块化、可扩展和跨平台的特性。

### 1.1 架构图

```
┌──────────────────────────────────────────────────────────┐
│                       MCP Host                            │
│  (AI 应用：Claude Desktop, Cursor, IDE 等)                │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │          MCP Client (集成在 Host 中)             │    │
│  │  - 请求管理                                       │    │
│  │  - 会话管理                                       │    │
│  │  - 协议转换                                       │    │
│  └─────────────────┬────────────────────────────────┘    │
└────────────────────┼───────────────────────────────────────┘
                     │
                     │ MCP Protocol
                     │ (JSON-RPC 2.0)
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌────────┐  ┌────────┐  ┌────────┐
   │ MCP    │  │ MCP    │  │ MCP    │
   │ Server │  │ Server │  │ Server │
   │        │  │        │  │        │
   │ GitHub │  │ Slack  │  │Database│
   └────────┘  └────────┘  └────────┘
```

### 1.2 关键设计原则

**1:1 客户端-服务器关系**  
每个 MCP 客户端与一个 MCP 服务器建立专属连接，但一个 Host 可以包含多个客户端，从而连接多个服务器。

**状态化协议**  
MCP 是有状态的协议，需要明确的生命周期管理（初始化、能力协商、关闭）。

**双向通信**  
支持客户端到服务器和服务器到客户端的双向消息传递。

---

## 2. 四大核心组件

### 2.1 MCP Host（主机）

**定义**：使用 AI 代理的应用程序

**职责**：
- 协调整个系统
- 管理 LLM 交互
- 包含一个或多个 MCP 客户端

**示例**：
- Claude Desktop（消费级 AI 助手）
- Cursor、Zed（AI 驱动的 IDE）
- 自定义的企业 AI 应用

**代码示例**：
```typescript
// Host 初始化多个 MCP 客户端
class MCPHost {
  private clients: Map<string, MCPClient> = new Map();
  
  async addServer(name: string, serverConfig: ServerConfig) {
    const client = new MCPClient();
    await client.connect(serverConfig);
    this.clients.set(name, client);
  }
  
  async handleUserQuery(query: string) {
    // 1. 从所有客户端收集可用工具
    const allTools = [];
    for (const [name, client] of this.clients) {
      const tools = await client.listTools();
      allTools.push(...tools);
    }
    
    // 2. 让 LLM 决定使用哪些工具
    const response = await this.llm.generate(query, allTools);
    
    // 3. 执行工具调用
    for (const toolCall of response.toolCalls) {
      const client = this.findClientForTool(toolCall.name);
      await client.callTool(toolCall.name, toolCall.args);
    }
  }
}
```

### 2.2 MCP Client（客户端）

**定义**：集成在 Host 中的组件，负责与 MCP 服务器通信

**职责**：
- 会话管理（超时、重连、关闭）
- 协议消息转换（MCP ↔ JSON-RPC）
- 请求路由和响应处理

**1:1 关系**：
```
一个 Host 可以有多个 Client
但每个 Client 只连接一个 Server

Host
├── Client A → Server 1 (GitHub)
├── Client B → Server 2 (Slack)
└── Client C → Server 3 (Database)
```

**关键方法**：
```typescript
interface MCPClient {
  // 生命周期
  connect(config: ServerConfig): Promise<void>;
  disconnect(): Promise<void>;
  
  // 发现能力
  listTools(): Promise<Tool[]>;
  listResources(): Promise<Resource[]>;
  listPrompts(): Promise<Prompt[]>;
  
  // 使用能力
  callTool(name: string, args: any): Promise<any>;
  getResource(uri: string): Promise<ResourceContent>;
  getPrompt(name: string, args: any): Promise<PromptContent>;
}
```

### 2.3 MCP Server（服务器）

**定义**：暴露特定能力的轻量级程序

**职责**：
- 提供 Tools（工具）
- 提供 Resources（资源）
- 提供 Prompts（提示词）
- 处理客户端请求

**示例服务器**：
```typescript
// 简单的 GitHub MCP 服务器
class GitHubMCPServer {
  // 注册工具
  tools = [
    {
      name: 'create_issue',
      description: '在 GitHub 仓库中创建 Issue',
      parameters: {
        type: 'object',
        properties: {
          repo: { type: 'string', description: '仓库名称' },
          title: { type: 'string', description: 'Issue 标题' },
          body: { type: 'string', description: 'Issue 内容' }
        },
        required: ['repo', 'title']
      }
    }
  ];
  
  // 处理工具调用
  async handleToolCall(name: string, args: any) {
    if (name === 'create_issue') {
      const issue = await octokit.issues.create({
        owner: 'user',
        repo: args.repo,
        title: args.title,
        body: args.body
      });
      return { issueNumber: issue.data.number };
    }
  }
  
  // 注册资源
  resources = [
    {
      uri: 'github://repos/{owner}/{repo}/issues',
      name: '仓库的所有 Issues',
      mimeType: 'application/json'
    }
  ];
  
  // 处理资源请求
  async handleResourceRead(uri: string) {
    const match = uri.match(/github:\/\/repos\/(.+)\/(.+)\/issues/);
    if (match) {
      const [_, owner, repo] = match;
      const issues = await octokit.issues.listForRepo({ owner, repo });
      return { content: JSON.stringify(issues.data) };
    }
  }
}
```

### 2.4 Transport Layer（传输层）

**定义**：负责客户端和服务器之间的消息传递

**支持的传输方式**：

**1. Stdio（标准输入输出）**
- 用于本地进程
- 服务器作为子进程启动
- 通过 stdin/stdout 通信

```typescript
// Stdio 传输配置
{
  type: 'stdio',
  command: 'node',
  args: ['./github-server.js']
}
```

**2. HTTP + SSE（Server-Sent Events）**
- 用于远程服务器
- 客户端发送 HTTP POST 请求
- 服务器通过 SSE 推送消息

```typescript
// HTTP 传输配置
{
  type: 'sse',
  url: 'https://mcp-server.example.com/sse',
  headers: {
    'Authorization': 'Bearer <token>'
  }
}
```

**传输层抽象**：
```
MCP Protocol (应用层)
       ↓
JSON-RPC 2.0 (消息格式)
       ↓
Transport Layer (传输层)
    ↙      ↘
  Stdio    HTTP/SSE
```

---

## 3. 通信协议详解

### 3.1 JSON-RPC 2.0

MCP 使用 JSON-RPC 2.0 作为底层 RPC 协议。

**三种消息类型**：

**1. Request（请求）**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "create_issue",
    "arguments": {
      "repo": "my-repo",
      "title": "Bug Report"
    }
  }
}
```

**2. Response（响应）**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "issueNumber": 42
  }
}
```

**3. Notification（通知）**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "task-123",
    "progress": 50,
    "total": 100
  }
}
```

### 3.2 消息流示例

**工具调用流程**：

```
Client                          Server
  │                                │
  │  1. tools/list (Request)       │
  │─────────────────────────────→  │
  │                                │
  │  2. List of tools (Response)   │
  │←─────────────────────────────  │
  │                                │
  │  3. tools/call (Request)       │
  │─────────────────────────────→  │
  │                                │
  │  4. Execution result (Response)│
  │←─────────────────────────────  │
```

---

## 4. 生命周期管理

MCP 是有状态协议，需要明确的生命周期管理。

### 4.1 连接生命周期

```
   ┌─────────────┐
   │   未连接     │
   └─────┬───────┘
         │ connect()
         ▼
   ┌─────────────┐
   │  初始化中    │
   └─────┬───────┘
         │ initialize
         ▼
   ┌─────────────┐
   │  能力协商    │
   └─────┬───────┘
         │ initialized
         ▼
   ┌─────────────┐
   │   已连接     │ ◄──┐
   └─────┬───────┘    │
         │           正常操作
         │ disconnect()│
         ▼            │
   ┌─────────────┐   │
   │  关闭中      │───┘
   └─────┬───────┘
         │ closed
         ▼
   ┌─────────────┐
   │   已关闭     │
   └─────────────┘
```

### 4.2 初始化序列

**Step 1: 客户端发起初始化**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "roots": {
        "listChanged": true
      },
      "sampling": {}
    },
    "clientInfo": {
      "name": "ExampleClient",
      "version": "1.0.0"
    }
  }
}
```

**Step 2: 服务器响应能力**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {},
      "resources": {
        "subscribe": true
      },
      "prompts": {}
    },
    "serverInfo": {
      "name": "ExampleServer",
      "version": "1.0.0"
    }
  }
}
```

**Step 3: 客户端确认就绪**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

### 4.3 能力协商

在初始化过程中，客户端和服务器交换支持的能力：

**客户端能力**：
- `roots`: 提供根目录列表
- `sampling`: 支持 LLM 采样

**服务器能力**：
- `tools`: 提供工具
- `resources`: 提供资源（是否支持订阅）
- `prompts`: 提供提示词

---

## 5. 三大原语（Primitives）

### 5.1 Tools（工具）

**用途**：让 AI 执行具有副作用的操作

**特点**：
- 可以修改状态
- 可以调用外部 API
- 可以执行计算

**方法**：
- `tools/list`: 列出所有工具
- `tools/call`: 执行工具

**示例**：
```typescript
// 工具定义
{
  name: 'send_email',
  description: '发送电子邮件',
  inputSchema: {
    type: 'object',
    properties: {
      to: { type: 'string', format: 'email' },
      subject: { type: 'string' },
      body: { type: 'string' }
    },
    required: ['to', 'subject', 'body']
  }
}

// 工具调用
await client.callTool('send_email', {
  to: 'user@example.com',
  subject: 'Hello',
  body: 'This is a test email.'
});
```

### 5.2 Resources（资源）

**用途**：提供数据访问，不执行操作

**特点**：
- 只读或可读写
- 通过 URI 标识
- 支持订阅更新

**方法**：
- `resources/list`: 列出所有资源
- `resources/read`: 读取资源内容
- `resources/subscribe`: 订阅资源变化（可选）

**示例**：
```typescript
// 资源定义
{
  uri: 'file:///path/to/document.md',
  name: 'Project Documentation',
  description: '项目的主要文档',
  mimeType: 'text/markdown'
}

// 资源读取
const content = await client.getResource('file:///path/to/document.md');
console.log(content.text); // Markdown 内容
```

### 5.3 Prompts（提示词）

**用途**：可重用的提示词模板和工作流

**特点**：
- 参数化模板
- 标准化工作流
- 包含示例（few-shot）

**方法**：
- `prompts/list`: 列出所有提示词
- `prompts/get`: 获取提示词内容

**示例**：
```typescript
// 提示词定义
{
  name: 'code-review',
  description: '代码审查提示词',
  arguments: [
    { name: 'language', description: '编程语言', required: true },
    { name: 'code', description: '要审查的代码', required: true }
  ]
}

// 提示词使用
const prompt = await client.getPrompt('code-review', {
  language: 'javascript',
  code: 'function add(a, b) { return a + b; }'
});

console.log(prompt.messages);
// [
//   { role: 'user', content: '请审查以下 JavaScript 代码...' }
// ]
```

---

## 6. 数据流示例

### 完整的请求-响应流程

**场景**：用户要求创建一个 GitHub Issue

```
┌──────────┐
│   User   │ "Create an issue about bug in login"
└────┬─────┘
     │
     ▼
┌──────────────────────────────────────┐
│          MCP Host (Claude)            │
│                                       │
│  1. 理解用户意图                       │
│  2. 查询可用工具                       │
│     ↓                                 │
│  ┌──────────────────────┐            │
│  │    MCP Client         │            │
│  │  tools/list request  │────────┐   │
│  └──────────────────────┘        │   │
└─────────────────────────────────┼───┘
                                  │
                        ┌─────────▼────────┐
                        │   MCP Server     │
                        │    (GitHub)       │
                        │                   │
                        │  Response:        │
                        │  [create_issue,   │
                        │   list_issues,    │
                        │   ...]            │
                        └─────────┬─────────┘
                                  │
┌─────────────────────────────────┼───┐
│          MCP Host                │   │
│  3. LLM 决定使用 create_issue    │   │
│  4. 执行工具调用                  │   │
│     ↓                            │   │
│  ┌──────────────────────┐       │   │
│  │    MCP Client         │       │   │
│  │  tools/call request  │───────┘   │
│  │  {                    │           │
│  │    name: "create_i.." │           │
│  │    args: {repo, ...} │           │
│  │  }                    │           │
│  └──────────────────────┘           │
└──────────────────────────────────────┘
                                  │
                        ┌─────────▼─────────┐
                        │   MCP Server      │
                        │                    │
                        │  1. 验证参数       │
                        │  2. 调用 GitHub API│
                        │  3. 返回结果       │
                        │                    │
                        │  Response:         │
                        │  {issueNumber: 42} │
                        └─────────┬──────────┘
                                  │
┌─────────────────────────────────┼───┐
│          MCP Host                │   │
│  5. 接收结果                      │   │
│  6. 生成用户友好的回复             │   │
└─────────────────────────────────┼───┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │      User        │
                        │                  │
                        │ "Issue #42 has   │
                        │  been created!"  │
                        └──────────────────┘
```

---

## 7. 关键架构决策

### 7.1 为什么选择客户端-服务器？

**优势**：
- **清晰的职责分离**：Host 管理 AI，Server 管理数据
- **可扩展性**：轻松添加新服务器
- **安全性**：服务器控制访问权限
- **可测试性**：组件可独立测试

### 7.2 为什么选择 JSON-RPC？

**优势**：
- **成熟标准**：广泛使用和支持
- **语言无关**：任何语言都能实现
- **简单明了**：易于调试和理解
- **双向通信**：支持请求、响应和通知

### 7.3 为什么是有状态协议？

**优势**：
- **能力协商**：客户端和服务器知道彼此支持什么
- **会话管理**：跟踪连接状态
- **资源优化**：避免重复初始化

---

## 8. 架构最佳实践

### 8.1 服务器设计

```typescript
// ✅ 好的设计：模块化和可扩展
class MCPServer {
  private tools = new ToolRegistry();
  private resources = new ResourceRegistry();
  private prompts = new PromptRegistry();
  
  constructor(config: ServerConfig) {
    this.registerTools();
    this.registerResources();
    this.registerPrompts();
  }
  
  private registerTools() {
    this.tools.register('create_issue', new CreateIssueTool());
    this.tools.register('list_issues', new ListIssuesTool());
  }
}
```

```typescript
// ❌ 不好的设计：所有逻辑混在一起
class MCPServer {
  async handleRequest(method: string, params: any) {
    if (method === 'tools/call') {
      if (params.name === 'create_issue') {
        // 大量硬编码逻辑...
      } else if (params.name === 'list_issues') {
        // 更多硬编码...
      }
    }
  }
}
```

### 8.2 错误处理

```typescript
// MCP 错误响应
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Invalid request",
    "data": {
      "details": "Missing required parameter: repo"
    }
  }
}
```

### 8.3 性能考虑

**缓存策略**：
```typescript
class ResourceCache {
  private cache = new Map<string, CachedResource>();
  
  async get(uri: string): Promise<ResourceContent> {
    const cached = this.cache.get(uri);
    if (cached && !cached.isExpired()) {
      return cached.content;
    }
    
    const fresh = await this.fetchResource(uri);
    this.cache.set(uri, { content: fresh, timestamp: Date.now() });
    return fresh;
  }
}
```

---

## 9. 总结

**架构核心要点**：

✅ **客户端-服务器模型**：清晰的职责分离  
✅ **JSON-RPC 2.0**：标准化的消息格式  
✅ **生命周期管理**：初始化、能力协商、关闭  
✅ **三大原语**：Tools、Resources、Prompts  
✅ **双向传输**：Stdio（本地）和 HTTP/SSE（远程）  
✅ **动态发现**：运行时发现可用能力  

---

## 10. 下一步

现在你已经理解了 MCP 的架构设计，接下来我们将：

👉 **[下一章：环境搭建](./03-setup.md)**  
实际动手搭建 MCP 开发环境，运行第一个 MCP 服务器

---

## 📖 补充阅读

- [MCP 架构概览](https://modelcontextprotocol.io/docs/learn/architecture) - 官方文档
- [JSON-RPC 2.0 规范](https://www.jsonrpc.org/specification) - 协议详解
- [MCP 规范](https://spec.modelcontextprotocol.io/) - 完整技术规范

---

*最后更新：2025-01-29*