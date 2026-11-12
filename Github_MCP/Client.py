from fastmcp import FastMCP
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import json
import os 

load_dotenv()

mcp=FastMCP("Github MCP Server")
BRANCH = 'live-mcp'
BASE_BRANCH = 'master'
FILE_PATH = 'live_mcp.txt'

async def call(tool, args):
    result = await tool.ainvoke(args)
    # MCP tools return a list of content blocks, the first one holds the text
    text = result[0]['text']
    try:
        text = json.loads(text)
    except json.JSONDecodeError:
        pass

    print(f"\n--- {tool.name} ---\n{text}")
    if isinstance(text, str) and text.startswith('failed'):
        raise RuntimeError(f"{tool.name}: {text}")  # stop at the first failed step
    return text

async def main():
  Client = MultiServerMCPClient({
        "Github": {
            "transport": "streamable_http",
            "url": "https://api.githubcopilot.com/mcp/",
            "headers": {
                "Authorization": f'Bearer {os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")}'
            }
        }
    })

  tools= await Client.get_tools()

  tools_by_name = {tool.name: tool for tool in tools}


  me=await call(tools_by_name['get_me'],{})

  owner=me['login']

  #create repo
  repo="Creating Repo Using MCP"

  target={"owner":owner,"repo":repo}

  await call(tools_by_name['create_repository'], {
      'name': repo,
      'description': 'Created through the GitHub MCP server',
      'private': True,
      'autoInit': True,
        })


  await call(tools_by_name['create_branch'], {
        **target, 'branch': BRANCH,
        'from_branch': BASE_BRANCH})

  created = await call(tools_by_name['create_or_update_file'], {
        **target,
        'branch': BRANCH,
        'path': FILE_PATH,
        'content': '# Live MCP\n\nThis file was created through the GitHub MCP server.\n',
        'message': 'Add live_mcp.txt',
    })


  


if __name__=="__main__":
 asyncio.run(main())


 