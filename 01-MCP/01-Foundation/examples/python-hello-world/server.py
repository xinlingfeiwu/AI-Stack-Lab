#!/usr/bin/env python3
"""
Hello World MCP Server (Python)

这是一个简单的 MCP 服务器示例，展示了：
- 如何使用 FastMCP 创建服务器
- 如何定义工具（Tools）
- 如何定义资源（Resources）
- 如何处理请求
"""

import asyncio
import sys
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务器实例
mcp = FastMCP("hello-world-server")

# 定义工具：问候功能
@mcp.tool()
def greet(name: str) -> str:
    """
    向用户打招呼
    
    Args:
        name: 要打招呼的人的名字
    
    Returns:
        问候消息
    """
    print(f"[Server] Greeting {name}", file=sys.stderr)
    return f"你好，{name}！欢迎使用 MCP！🎉"

# 定义工具：加法计算
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
    print(f"[Server] Adding {a} + {b}", file=sys.stderr)
    result = a + b
    return result

# 定义工具：乘法计算
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """
    两个数字相乘
    
    Args:
        a: 第一个数字
        b: 第二个数字
    
    Returns:
        两数之积
    """
    print(f"[Server] Multiplying {a} * {b}", file=sys.stderr)
    return a * b

# 定义资源：个性化问候
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """
    获取个性化问候语资源
    
    Args:
        name: 用户名称
    
    Returns:
        个性化问候
    """
    print(f"[Server] Getting greeting resource for {name}", file=sys.stderr)
    current_time = datetime.now().strftime("%H:%M")
    return f"Hello, {name}! Current time is {current_time}. Have a great day!"

# 定义资源：服务器信息
@mcp.resource("info://server")
def get_server_info() -> str:
    """
    获取服务器信息
    
    Returns:
        服务器信息字符串
    """
    print("[Server] Getting server info resource", file=sys.stderr)
    return """
MCP Hello World Server
======================

Version: 1.0.0
Language: Python
SDK: FastMCP

Available Tools:
- greet(name: str) - 向用户打招呼
- add(a: int, b: int) - 两个数字相加
- multiply(a: int, b: int) - 两个数字相乘

Available Resources:
- greeting://{name} - 个性化问候语
- info://server - 服务器信息
"""

# 启动服务器
if __name__ == "__main__":
    print("[Server] Starting Hello World MCP Server...", file=sys.stderr)
    print("[Server] Server running on stdio", file=sys.stderr)
    print("[Server] Waiting for requests...", file=sys.stderr)
    
    # 使用 stdio 传输运行服务器
    import mcp.server.stdio
    
    async def main():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await mcp.run(
                read_stream,
                write_stream,
                mcp.create_initialization_options()
            )
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Server] Server stopped by user", file=sys.stderr)
    except Exception as e:
        print(f"[Server] Fatal error: {e}", file=sys.stderr)
        sys.exit(1)