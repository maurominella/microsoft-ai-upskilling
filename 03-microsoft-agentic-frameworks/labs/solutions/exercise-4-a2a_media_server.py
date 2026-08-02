import uvicorn
import re
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
from starlette.applications import Starlette


def availability(brief: str) -> str:
    match = re.search(r"sector(?:=|\s+)([^:;\s]+)", brief, re.IGNORECASE)
    sector = match.group(1) if match else "n/a"
    return f"Media planning - sector {sector}: 3 prime-time TV slots and 5 digital packages available in March."


class MediaAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        request = context.get_user_input()  # text sent by the client
        await event_queue.enqueue_event(new_text_message(availability(request)))
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")

# --- Skill + Agent Card ---
skill = AgentSkill(
    id="campaign_media",
    name="RAI Media Agent",
    description="Campaign media planning agent for RAI Pubblicita.",
    tags=["media planning", "advertising"],
    examples=["sector=Travel; impressions=9200000"],
)
agent_card = AgentCard(
    name="RAI Media Agent",
    description="Campaign media planning agent for RAI Pubblicita.",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(),
    skills=[skill],
    supported_interfaces=[
        AgentInterface(
            url="http://localhost:10000/",
            protocol_binding="JSONRPC",
        )
    ],
)

if __name__ == "__main__":
    handler = DefaultRequestHandler(
        agent_executor=MediaAgentExecutor(),
        task_store=InMemoryTaskStore(),
        agent_card=agent_card,
    )

    app = Starlette(
        routes=[
            *create_agent_card_routes(agent_card),
            *create_jsonrpc_routes(handler, rpc_url="/"),
        ]
    )

    uvicorn.run(app, host="0.0.0.0", port=10000)