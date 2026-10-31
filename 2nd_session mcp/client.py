import sys
from langchain_ollama import ChatOllama
from pathlib import Path
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio


Client = MultiServerMCPClient(
    {
        "MCP": {
            "command": sys.executable,
            "transport": "stdio",
            "args": [str(Path(__file__).parent / "server_with_context.py")]
        }
    }
)

async def main():
    async with Client.session("MCP") as session:
        tools = await load_mcp_tools(session)
        
        tools_by_name = {tool.name: tool for tool in tools}
        print("Loaded tools:", list(tools_by_name.keys()))

       
        result = await tools_by_name["add_to_cart"].ainvoke({"item": "apple"})
        print(result[0]["text"])
        
        result = await tools_by_name["add_to_cart"].ainvoke({"item": "banana"})
        print(result[0]["text"])
        
        result = await tools_by_name["add_to_cart"].ainvoke({"item": "grapes"})
        print(result[0]["text"])
        
        result = await tools_by_name["show_cart"].ainvoke({})
        print(result[0]["text"])
        
        result = await tools_by_name["show_session_id"].ainvoke({})
        print(result[0]["text"])

if __name__ == "__main__":
    asyncio.run(main())