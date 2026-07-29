"""
SOLUTION - Exercise 3: MCP client that consumes the campaign server.

Run in a SECOND terminal while ex3_mcp_server.py is running:
    python solutions/ex3_mcp_client.py
"""
import asyncio
from fastmcp import Client


async def main():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        # 1. discovery: which tools does the server expose?
        tools = await client.list_tools()
        print("Exposed tools:", [t.name for t in tools])

        # 2. call a tool
        res = await client.call_tool("top_campaigns_by_roi", {"n": 3})
        print("Top 3 by ROI:", getattr(res, "data", None) or res.content)

        # 3. read a resource
        resources = await client.read_resource("campaigns://all")
        print("Campaigns in the resource:", len(resources))

        # 4. list and render a prompt
        prompts = await client.list_prompts()
        print("Available prompts:", [p.name for p in prompts])
        rendered = await client.get_prompt("evaluate_campaign", {"campaign_id": "CMP-005"})
        print("Rendered prompt:", rendered)


if __name__ == "__main__":
    asyncio.run(main())
