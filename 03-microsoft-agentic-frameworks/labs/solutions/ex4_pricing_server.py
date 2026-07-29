"""
SOLUTION - Exercise 4: remote A2A Pricing Agent.

Run:  python solutions/ex4_pricing_server.py     (leave running; then run the client)
Fully local - no cloud credentials required. Deterministic pricing logic.

Note: a2a-sdk evolves quickly. If a class/field name differs from your installed version,
adapt using https://github.com/a2aproject/a2a-python . The concept (Agent Card + task
delegation) is what matters.
"""
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from a2a.types import AgentCard, AgentSkill, AgentCapabilities

# --- Deterministic pricing logic: base CPM per sector ---
CPM_BASE = {"Automotive": 18.0, "Finance": 22.0, "FMCG": 12.0,
            "Travel": 16.0, "Telco": 14.0, "default": 15.0}


def quote(brief: str) -> str:
    # expected brief, e.g.: "sector=Travel; impressions=9200000"
    parts = dict(p.split("=") for p in brief.replace(" ", "").split(";") if "=" in p)
    sector = parts.get("sector", "default")
    impressions = float(parts.get("impressions", 5_000_000))
    cpm = CPM_BASE.get(sector, CPM_BASE["default"])
    price = impressions / 1000 * cpm
    return (f"Quote - sector {sector}: {impressions:,.0f} impressions "
            f"x CPM {cpm} EUR = {price:,.0f} EUR.")


class PricingAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        request = context.get_user_input()          # text sent by the client
        event_queue.enqueue_event(new_agent_text_message(quote(request)))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")


skill = AgentSkill(
    id="campaign_quote",
    name="Campaign quote",
    description="Computes an advertising quote from a brief (sector, impressions).",
    tags=["pricing", "advertising"],
    examples=["sector=Travel; impressions=9200000"],
)
agent_card = AgentCard(
    name="RAI Pricing Agent",
    description="Campaign pricing agent for RAI Pubblicita.",
    url="http://localhost:9999/",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(),
    skills=[skill],
)


if __name__ == "__main__":
    handler = DefaultRequestHandler(
        agent_executor=PricingAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )
    app = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(app.build(), host="0.0.0.0", port=9999)
