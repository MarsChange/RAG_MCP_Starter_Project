import dotenv
import os
import asyncio
from utils.log_func import logTitle
from utils.mcp_client import MCPClient
from utils.agent import Agent
from utils.embedding import embedding_retriever

current_dir = os.getcwd()
# Load environment variables from .env file
dotenv.load_dotenv()

# Load API key
API_KEY = os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")
BASE_MODEL_NAME = os.getenv("BASE_MODEL_NAME")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")

# MCP
fetchMCP = MCPClient(args=["mcp-server-fetch"], command="uvx")
fileMCP = MCPClient(args=['-y', '@modelcontextprotocol/server-filesystem', os.path.join(current_dir, "output")], command="npx") 

# Task prompt
TASK_PROMPT = f"告诉我 Chelsey Dietrich 的信息,先从我给你的文件中中找到相关信息,信息在"+ current_dir + "/knowledge 目录下,总结后创作一个关于她的故事把故事和她的基本信息保存到"+ current_dir + "/output/antonette.md,输出一个漂亮md文件"

# RAG
async def retrieve_context():
    embeddingRetriever = embedding_retriever()
    knowledge_dir = os.path.join(current_dir, "knowledge")
    for file in os.listdir(knowledge_dir):
        with open(os.path.join(knowledge_dir, file), "r", encoding="utf-8") as f:
            content = f.read()
            await embeddingRetriever.embed_document(content)
    
    context = await embeddingRetriever.retrieve(query=TASK_PROMPT, top_k=5)
    return context

async def main():
    context = await retrieve_context()
    logTitle("Init Agent")
    
    # Use async context managers to properly manage MCP client lifecycle
    async with fetchMCP as fetch_client, fileMCP as file_client:
        agent = Agent(mcp_clients=[fetch_client, file_client], system_prompt=TASK_PROMPT, context=context)
        await agent.init()
        logTitle("Agent Invoke")
        response = await agent.invoke(TASK_PROMPT)
        logTitle("Agent Response")
        # print(response)
        return response

if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)