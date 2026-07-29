"""
SOLUTION - Exercise 1: your first campaign-analysis agent (Microsoft Agent Framework).

Run live in front of the class, or use as a reference answer.
Requires: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_CHAT_DEPLOYMENT_NAME (in .env) + `az login`.
Run:  python solutions/ex1_agent_framework.py
"""
import os
import sys
import asyncio
from typing import Annotated

# Make rai_campaigns.py (in the parent folder) importable when run from solutions/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import Field
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from rai_campaigns import get_campaign, list_campaigns

load_dotenv()


# ---- Function tools ---------------------------------------------------------
def campaign_metrics(
    campaign_id: Annotated[str, Field(description="Campaign code, e.g. 'CMP-004'")]
) -> str:
    """Return budget, impressions, conversions and revenue for a RAI Pubblicita campaign."""
    c = get_campaign(campaign_id)
    if not c:
        return f"No campaign found with id {campaign_id}."
    return (
        f"{c['client']} ({c['id']}, sector {c['sector']}): budget {c['budget_eur']} EUR, "
        f"impressions {c['impressions']}, conversions {c['conversions']}, revenue {c['revenue_eur']} EUR."
    )


def compute_roi(
    revenue_eur: Annotated[float, Field(description="Revenue in euro")],
    budget_eur: Annotated[float, Field(description="Budget spent in euro")],
) -> str:
    """Compute ROI percentage: (revenue - budget) / budget * 100."""
    value = (revenue_eur - budget_eur) / budget_eur * 100
    return f"ROI = {value:.1f}%"


def all_campaigns() -> list:
    """List (id, client, sector) of every campaign in the portfolio."""
    return list_campaigns()


# ---- Demo -------------------------------------------------------------------
async def main():
    agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
        name="CampaignAnalyst",
        instructions=(
            "You are an analyst at RAI Pubblicita. Answer in English, concisely. "
            "Always use the tools to fetch data and compute - never invent numbers."
        ),
        tools=[campaign_metrics, compute_roi, all_campaigns],
    )

    print("\n=== A) Plain question ===")
    print((await agent.run("Introduce yourself in one sentence.")).text)

    print("\n=== B) Tool-grounded metrics ===")
    print((await agent.run("Give me the key metrics of campaign CMP-004.")).text)

    print("\n=== C) Multi-step reasoning ===")
    print((await agent.run(
        "Between CMP-004 and CMP-005, which has the better ROI and by how much? Show the values."
    )).text)

    print("\n=== Bonus) Whole-portfolio question (multi-turn thread) ===")
    thread = agent.get_new_thread()
    print((await agent.run("Which campaign has the highest ROI in the portfolio?", thread=thread)).text)
    print((await agent.run("And which one is losing money?", thread=thread)).text)


if __name__ == "__main__":
    asyncio.run(main())
