from fastmcp import FastMCP,Context
import sys

fast_mcp_server=FastMCP("Server")

DEFAULT_PRODUCT_QUANTITY = 100
@fast_mcp_server.tool()
async def add_to_cart(ctx:Context,item:str):
    """Add an item to shopping cart to the current session"""

    cart= await ctx.get_state("cart")

    product_quantity=await ctx.get_state("product_quantity")
    if product_quantity is None:
        product_quantity=DEFAULT_PRODUCT_QUANTITY

    await ctx.set_state("product_quantity",product_quantity-1)

    if cart is None:
       cart= []
    cart.append(item)

    await ctx.set_state("cart",cart)
    return f"Added {item}. Cart now has {len(cart)} item(s)."

@fast_mcp_server.tool()
async def show_cart(ctx:Context):
    """Show all the items in the shopping cart of the current session"""
    cart= await ctx.get_state("cart") or []
    add(3,6)
    return f"Cart : {cart}"

@fast_mcp_server.tool()
async def show_session_id(ctx:Context):
    """Return the session ID of the current mcp session"""
    return  ctx.session_id
@fast_mcp_server.tool()
def add(num1: int, num2: int) -> int:
 '''Use this tool to add two numbers'''
 return num1 + num2

if __name__=="__main__":
    fast_mcp_server.run(transport="stdio")





