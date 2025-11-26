import json
from utils.chat import chat_openai
from utils.mcp_client import MCPClient
from utils.log_func import logTitle

class Agent:
    def __init__(self, mcp_clients: list[MCPClient], system_prompt: str = "", context: str = ""):
        self.chat = chat_openai()
        self.mcp_clients = mcp_clients
        self.system_prompt = system_prompt
        self.context = context
        self.agent = None
    
    async def init(self):
        logTitle("MCP Tools Init")
        all_tools = []
        for mcp_client in self.mcp_clients:
            all_tools.extend(mcp_client.get_tools())
        
        self.agent = chat_openai(tools=all_tools, system_prompt=self.system_prompt, context=self.context)

    async def close(self):
        for mcp_client in self.mcp_clients:
            try:
                await mcp_client.close()
            except Exception as e:
                print(f"Error closing MCP client: {e}")
    
    async def invoke(self, prompt: str):
        if self.agent is None:
            raise Exception("Agent not initialized")
        
        response = await self.agent.chat(prompt)
        
        print(f"Response content: {response['content'][:200] if response['content'] else 'None'}...")
        print(f"Tool calls count: {len(response['tool_calls'])}")
        
        while True:
            if len(response["tool_calls"]) > 0:
                for tool_call in response["tool_calls"]:
                    tool_name = tool_call['function']['name']
                    
                    # Find which MCP client has this tool
                    mcp = None
                    for mcp_client in self.mcp_clients:
                        if any(tool['name'] == tool_name for tool in mcp_client.tools):
                            mcp = mcp_client
                            break
                    
                    if mcp is None:
                        raise Exception(f"MCP client not found for tool: {tool_name}")
                    
                    logTitle("TOOL USE")
                    print(f"Calling tool: {tool_name}")
                    print(f"Arguments: {tool_call['function']['arguments']}")
                    
                    result = await mcp.call_tool(tool_name, json.loads(tool_call['function']['arguments']))
                    
                    result_str = ""
                    if hasattr(result, "content") and result.content:
                        result_dic = {
                            "content": result.content[0].text if result.content[0].text else "",
                            "is_error": getattr(result, "isError", False)
                        }
                        result_str = json.dumps(result_dic)
                    else:
                        result_str = str(result)
                    print(f"Result: {result_str}")
                    self.agent.append_tool_result(tool_call['id'], result_str)
                
                response = await self.agent.chat()
                continue

            # Cleanup is now handled by async context managers in main.py
            return response["content"]
            