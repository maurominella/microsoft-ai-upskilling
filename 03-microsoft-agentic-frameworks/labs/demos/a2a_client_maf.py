import asyncio
from agent_framework.a2a import A2AAgent

CAMPAIGN_BRIEF = "sector=Travel; impressions=9200000"

async def main():
    pricing_agent = A2AAgent(
        name="PricingAgent",
        description="Computes an advertising campaign quote.",
        url="http://localhost:9999",
    )

    async with pricing_agent:
        result = await pricing_agent.run(CAMPAIGN_BRIEF)

    print(f"Pricing: {result.text}")


asyncio.run(main())