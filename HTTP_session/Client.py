from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
import sys
from pathlib import Path
import asyncio

SERVER={
    "FAST_MCP_SERVER":{
        "transport":"streamable_http",
        "url": 'http://127.0.0.1:8000/mcp'
    }
}


async def main():
    client=MultiServerMCPClient(SERVER)
    Tool_list=await client.get_tools()

    print("Tool List ", Tool_list)

    LLM=ChatOllama(model="mistral:latest").bind_tools(Tool_list) # Binding tools to the llm

    messages=[HumanMessage(content="Greet me with my name in unique way in default times")]

    response=await LLM.ainvoke(messages)

    print("response" , response.content)

    messages.append(AIMessage(content=response.content,tool_calls=response.tool_calls))


    tools_by_name = {tool.name: tool for tool in Tool_list}

    for tool_call in response.tool_calls:
      tool = tools_by_name[tool_call["name"]]
      result = await tool.ainvoke(tool_call['args'])   # to call the tool
      tool_output = result[0]['text']
      print(tool_output)
      messages.append(ToolMessage(content=tool_output,tool_call_id=tool_call['id']))

    final_response = await LLM.ainvoke(messages)

    print(final_response.content)

if __name__=="__main__":
   asyncio.run(main())
