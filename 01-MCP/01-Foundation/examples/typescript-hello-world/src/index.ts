#!/usr/bin/env node
/**
 * Hello World MCP Server (TypeScript)
 * 
 * 这是一个简单的 MCP 服务器示例，展示了：
 * - 如何创建基本的 MCP 服务器
 * - 如何注册和实现工具（Tools）
 * - 如何处理请求和返回响应
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
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

// 定义可用的工具
const TOOLS: Tool[] = [
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
];

// 注册工具列表处理器
server.setRequestHandler(ListToolsRequestSchema, async () => {
  console.error("[Server] Listing tools");
  return {
    tools: TOOLS,
  };
});

// 注册工具调用处理器
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  console.error(`[Server] Tool called: ${name}`, args);

  try {
    if (name === "greet") {
      const userName = args?.name as string;
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
      const a = args?.a as number;
      const b = args?.b as number;
      const result = a + b;
      return {
        content: [
          {
            type: "text",
            text: `计算结果：${a} + ${b} = ${result}`,
          },
        ],
      };
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (error) {
    console.error(`[Server] Error executing tool ${name}:`, error);
    throw error;
  }
});

// 启动服务器
async function main() {
  console.error("[Server] Starting Hello World MCP Server...");
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("[Server] Server running on stdio");
  console.error("[Server] Waiting for requests...");
}

// 错误处理
main().catch((error) => {
  console.error("[Server] Fatal error:", error);
  process.exit(1);
});
