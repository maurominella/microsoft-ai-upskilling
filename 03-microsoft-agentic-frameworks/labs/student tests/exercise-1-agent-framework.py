import asyncio
import os
from dotenv import load_dotenv
from azure.identity import AzureCliCredential

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from typing import Annotated
from pydantic import Field
from requests import session
from rai_campaigns import get_campaign
from rai_campaigns import list_campaigns

def all_campaigns() -> list:
    """List (id, client, sector) of every campaign in the portfolio."""
    return list_campaigns()

def campaign_metrics(
    campaign_id: Annotated[str, Field(description="Campaign code, e.g. 'CMP-004'")]
) -> str:
    """Return budget, impressions, conversions and revenue for a RAI Pubblicita campaign."""
    c = get_campaign(campaign_id)
    if not c:
        return f"No campaign found with id {campaign_id}."
    return (
        f"{c['client']} ({c['id']}, sector {c['sector']}): "
        f"budget {c['budget_eur']} EUR, impressions {c['impressions']}, "
        f"conversions {c['conversions']}, revenue {c['revenue_eur']} EUR."
    )

load_dotenv()

def compute_roi(
    revenue_eur: Annotated[float, Field(description="Revenue in euro")],
    budget_eur: Annotated[float, Field(description="Budget spent in euro")],
) -> str:
    """Compute ROI percentage: (revenue - budget) / budget * 100."""
    value = (revenue_eur - budget_eur) / budget_eur * 100
    return f"ROI = {value:.1f}%"

async def main():
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
        tools=[campaign_metrics, compute_roi, all_campaigns],
    )
    """
    answer = await agent.run("Introduce yourself in one sentence and tell me how you can help.")
    answer = await agent.run("Give me the key metrics of campaign CMP-004.")
    answer = await agent.run(
        "Between campaigns CMP-004 and CMP-005, which has the better ROI and by how much? Show the values."
    )
    print(answer.text)

    session = agent.create_session()
    print((await agent.run("What is the ROI of CMP-001?", session=session)).text)
    print((await agent.run("And compared to CMP-003, which is better?", session=session)).text)
    print((await agent.run("Which campaign has the highest ROI in the portfolio?", session=session)).text)
    """
    resp = await agent.run("What is the ROI of CMP-002?")
    for m in resp.messages:
        print(m)   # look for function_call / function_result / m.role, m.author_name, m.contents[0].arguments,m.contents[0].call_id, m.text

if __name__ == "__main__":
    asyncio.run(main())