from fastmcp import FastMCP,Client
from fastmcp.client.transports import PythonStdioTransport
import sys
from pathlib import Path


fastmcp=FastMCP("HTTP Server")

@fastmcp.tool()
def square(num:int)->int:
    """Return the square of a number."""
    return num * num

@fastmcp.tool()
async def double_then_square(num:int)->int:
    """Double a number, then return its square using the double tool of the stdio server."""
    stdio_server= PythonStdioTransport(Path(__file__).parent / "stdio_server.py", python_cmd=sys.executable)
    async with Client(stdio_server) as client:
        doubled=await client.call_tool("double",{"n":num})
    return square(doubled.data)

if __name__=="__main__":
    fastmcp.run(transport="http",host="127.0.0.1",port=8002)

