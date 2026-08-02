import asyncio
from agent_framework.a2a import A2AAgent
from agent_framework.orchestrations import SequentialBuilder

CAMPAIGN_BRIEF = "sector=Travel; impressions=9200000"

async def main():
    pricing_agent = A2AAgent(
        name="PricingAgent",
        description="Computes an advertising campaign quote.",
        url="http://localhost:9999",
    )
    media_agent = A2AAgent(
        name="MediaAgent",
        description="Finds available media inventory for a campaign.",
        url="http://localhost:10000",
    )

    workflow = SequentialBuilder(
        participants=[pricing_agent, media_agent],
        intermediate_output_from=[pricing_agent], # makes pricing_agent answer  visibile as intermediate output within the workflow
    ).build()

    async with pricing_agent, media_agent:
        result = await workflow.run(CAMPAIGN_BRIEF)

    for response in result.get_intermediate_outputs():
        print(f"Pricing: {response.text}")
    for response in result.get_outputs():
        print(f"Media planning: {response.text}")


asyncio.run(main())