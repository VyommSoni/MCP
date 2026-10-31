from fastmcp import FastMCP
import sys


fast_mcp=FastMCP("First mcp httpserver")

@fast_mcp.tool()
def unique_way_print(name: str) -> str:
 '''Use this tool to print name in unique way'''
 return 'Haha' + name

@fast_mcp.tool()
def default_number_of_printing() -> int:
  '''Use this tool to get the default times of printing'''
  return 5


if __name__=="__main__":
  fast_mcp.run(transport="http",port=8000,host='127.0.0.1')