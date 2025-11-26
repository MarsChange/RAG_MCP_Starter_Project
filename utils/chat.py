import dotenv
import os
from openai import OpenAI

dotenv.load_dotenv()

class chat_openai:
    def __init__(self, tools = [], system_prompt: str = "", context: str = ""):
        self.api_key = os.getenv("API_KEY")
        self.model_name = os.getenv("BASE_MODEL_NAME")
        self.url = os.getenv("BASE_URL")
        self.tools = tools
        self.system_prompt = system_prompt
        self.context = context
        self.messages = []
        self.client = OpenAI(api_key=self.api_key, base_url=self.url)
        
        # Initialize messages with system prompt and context
        if self.system_prompt or self.context:
            system_content = ""
            if self.context:
                system_content += f"Context:\n{self.context}\n\n"
            if self.system_prompt:
                system_content += self.system_prompt
            self.messages.append({"role": "system", "content": system_content})

    async def chat(self, prompt: str = None):
        if prompt:
            self.messages.append({"role": "user", "content": prompt})
        stream = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.messages,
            tools=self.get_tools_defination(),
            stream=True
        )

        content = ''
        toolCalls = []

        for chunk in stream:
            if not chunk.choices or len(chunk.choices) == 0:
                continue
            
            delta = chunk.choices[0].delta
            if delta.content:
                content += delta.content
            if delta.tool_calls:
                for tool_call in delta.tool_calls:
                    if len(toolCalls) <= tool_call.index:
                        toolCalls.append({
                            "id": "",
                            "function": {
                                "name": "",
                                "arguments": ""
                            }
                        })
                    current_call = toolCalls[tool_call.index]
                    if tool_call.id:
                        current_call["id"] = tool_call.id
                    if tool_call.function:
                        if tool_call.function.name:
                            current_call["function"]["name"] = tool_call.function.name
                        if tool_call.function.arguments:
                            current_call["function"]["arguments"] += tool_call.function.arguments
        
        self.messages.append({
            "role": "assistant", 
            "content": content,
            "tool_calls": [{"id": call["id"], "function": call["function"]} for call in toolCalls] if toolCalls else None
        })
        return {
            "content": content,
            "tool_calls": toolCalls
        }

    def append_tool_result(self, toolCallID: str, result: str):
        self.messages.append({
            "role": "tool",
            "content": result,
            "tool_call_id": toolCallID,
        })

    def get_tools_defination(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["inputSchema"]
                }
            }
            for tool in self.tools
        ]

async def main():
    chat = chat_openai()
    prompt = "Hello"
    response = await chat.chat(prompt)
    print(response)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())