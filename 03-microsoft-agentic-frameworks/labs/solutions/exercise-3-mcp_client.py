import asyncio
from fastmcp import Client

async def client_side_llm(query: str | list[str]): 
    import os
    from azure.identity import AzureCliCredential
    from agent_framework import Agent, MCPStreamableHTTPTool
    from agent_framework.openai import OpenAIChatClient
    from dotenv import load_dotenv

    load_dotenv()

    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        credential=AzureCliCredential(),
    )
    
    mcp_tool = MCPStreamableHTTPTool(
        name="rai_campaigns",
        url="http://127.0.0.1:8000/mcp",
        approval_mode="never_require",
        load_prompts=False,
    )

    agent = Agent(
        client=client,
        name="CampaignAnalyst",
        instructions="Always answer in English, concisely and professionally.",
        tools=[mcp_tool],
    )

    async with agent:
        answer = await agent.run(query)
    return answer.text


async def foundry_side_llm(query: str | list[str]):
    import os
    from azure.identity import AzureCliCredential
    from agent_framework import Agent
    from agent_framework.openai import OpenAIChatClient
    from dotenv import load_dotenv

    load_dotenv()

    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        credential=AzureCliCredential(),
    )

    agent = Agent(
        client=client,
        name="CampaignAnalyst",
        instructions=(
            "You are an analyst at RAI Pubblicita. Always answer in English, "
            "concisely and professionally."
        ),
        tools=[{
            "type": "mcp",
            "server_label": "rai_campaigns",
            "server_url": "https://5ndxcpg3-8000.eun1.devtunnels.ms/mcp",
            "require_approval": "never",
        }],
    )

    async with agent:
        answer = await agent.run(query)
    return answer.text



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

        # 4. get a prompt and render it
        prompts = await client.list_prompts()
        print("Available prompts:", [p.name for p in prompts])
        rendered = await client.get_prompt("evaluate_campaign", {"campaign_id": "CMP-005"})
        print(rendered.messages[0].content.text)

        # 5. call the compare_campaigns tool
        comparison = await client.call_tool("compare_campaigns", {"id_a": "CMP-005", "id_b": "CMP-004"})
        print("Comparison of CMP-005 and CMP-004:", getattr(comparison, "data", None) or comparison.content)

    # 6. run the Local agent with the MCP tool
    llm_answer = await client_side_llm(
        ["Which campaign is better and why, CMP-004 or CMP-005?",
        "Which campaign has the highest ROI and what would you recommend for the worst one?"]
    )
    print(f"llm_answer: {llm_answer}")
    print("main ends here")

    # 7. run the Foundry agent with the MCP tool
    llm_answer = await foundry_side_llm(
        ["Which campaign is better and why, CMP-004 or CMP-005?",
        "Which campaign has the highest ROI and what would you recommend for the worst one?"]
    )
    print(f"llm_answer: {llm_answer}")
    print("main ends here")

    

asyncio.run(main())