from fastmcp import FastMCP,Client

fastmcp=FastMCP("Stdio Server")

@fastmcp.tool
def double(n: int) -> int:
 """Return n multiplied by 2."""
 return n * 2
@fastmcp.tool()
def add_then_double(a: int, b: int) -> int:
 """Add two numbers, then double the result."""
 return double(a + b)



@fastmcp.tool()
async def sum_of_squares(a:int,b:int)->int:
     """Return a*a + b*b, using the square tool of the HTTP server."""
     async with Client("http://127.0.0.1:8002/mcp") as client:
       square_a=await client.call_tool("square",{"num":a})
       square_b=await client.call_tool("square",{"num":b})

     return square_a.data + square_b.data

if __name__=="__main__":
  fastmcp.run(transport="stdio")


