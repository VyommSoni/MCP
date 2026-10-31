from fastmcp import FastMCP,Context
import asyncio

fastmcp=FastMCP("Notification server (HTTP)")

@fastmcp.tool()
async def do_work(ctx:Context):
    """Do a Slow job and  report progress along the way"""
    for steps in range(1,4):

        asyncio.sleep(1)
        await ctx.info(f"Steps done {steps}")

        #progress update
        await ctx.report_progress(progress=steps,total=3,message=f"finished steps:{steps}")
    return "Job_Done"



if __name__=="__main__":
    fastmcp.run(transport="http",host='127.0.0.1',port=8001)


