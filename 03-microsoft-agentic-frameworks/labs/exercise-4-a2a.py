import uvicorn
from starlette.applications import Starlette
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.helpers import new_text_message
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    AgentCard,
    AgentSkill,
    AgentCapabilities,
    AgentInterface,
)

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
        request = context.get_user_input()  # text sent by the client
        event_queue.enqueue_event(new_text_message(quote(request)))
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")

# --- Skill + Agent Card ---
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
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(),
    skills=[skill],
    supported_interfaces=[
        AgentInterface(
            url="http://localhost:9999/",
            protocol_binding="JSONRPC",
        )
    ],
)

if __name__ == "__main__":
    handler = DefaultRequestHandler(
        agent_executor=PricingAgentExecutor(),
        task_store=InMemoryTaskStore(),
        agent_card=agent_card,
    )

    app = Starlette(
        routes=[
            *create_agent_card_routes(agent_card),
            *create_jsonrpc_routes(handler, rpc_url="/"),
        ]
    )

    uvicorn.run(app, host="0.0.0.0", port=9999)