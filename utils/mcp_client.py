import mcp
from typing import Optional
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession
from contextlib import AsyncExitStack

class MCPClient:
    def __init__(self, args: list[str], command: str):
        self.args = args
        self.command = command
        self.session: Optional[ClientSession] = None
        self.stdio: Optional[mcp.StdioTransport] = None
        self.write: Optional[mcp.StdioTransport] = None
        self.exit_stack = AsyncExitStack()
        self.tools = []
        
    async def __aenter__(self):
        # Async context manager entry - initializes the MCP client
        await self._connect_to_server()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Async context manager exit - cleans up resources
        try:
            self.session = None
            await self.exit_stack.aclose()
        except Exception as e:
            print(f"Error closing MCP client: {e}")
        return False  # Don't suppress exceptions

    async def list_tools(self):
        if not self.session:
            raise Exception("MCP client not initialized")
        tools = await self.session.list_tools()
        return tools
    
    async def _connect_to_server(self):
        # Connect to MCP server
        server_params = mcp.StdioServerParameters(
            args=self.args,
            command=self.command,
        )
        # Start stdio client
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        # Initialize session
        await self.session.initialize()
        # List tools
        valid_tools = await self.list_tools()
        self.tools = []
        # Add tools to list
        for tool in valid_tools.tools:
            tool_dict = {
                "name": tool.name if hasattr(tool, "name") else str(tool),
                "description": tool.description if hasattr(tool, "description") else "",
                "inputSchema": tool.inputSchema if hasattr(tool, 'inputSchema') else 
                            (tool.inputSchema if hasattr(tool, 'inputSchema') else {}),
            }
            self.tools.append(tool_dict)

        print("\nConnected to MCP server with tools: ", [tool.name for tool in valid_tools.tools])
    
    async def call_tool(self, tool_name: str, args: dict):
        if not self.session:
            raise Exception("MCP session not initialized")
        return await self.session.call_tool(name=tool_name, arguments=args)
    
    def get_tools(self):
        if self.tools:
            return self.tools
        else:
            raise Exception("MCP tools are empty")