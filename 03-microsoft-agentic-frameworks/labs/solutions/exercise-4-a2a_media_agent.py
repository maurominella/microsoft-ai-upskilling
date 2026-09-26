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

port_number = 9998

def availability(brief: str) -> str:
    """Return a media availability summary for the sector specified in a campaign brief.

    The sector can be provided as ``sector=<value>`` or ``sector <value>``.
    If the brief does not contain a sector, ``n/a`` is used in the summary.

    Args:
        brief: Campaign brief containing the sector information.

    Returns:
        A summary of the media slots and digital packages available in March.

    Example:
        Input:
            ``sector=Travel``

        Output:
            ``Media planning - sector Travel: 3 prime-time TV slots and 5 digital
            packages available in March.``
    """
    match = re.search(r"sector(?:=|\s+)([^:;\s]+)", brief, re.IGNORECASE)
    sector = match.group(1) if match else "n/a"
    return f"Media planning - sector {sector}: 3 prime-time TV slots and 5 digital packages available in March."


class MediaExecutorAgent(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        request = context.get_user_input()  # text sent by the client
        await event_queue.enqueue_event(new_text_message(availability(request)))
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")

# --- Skill + Agent Card ---
skill = AgentSkill(
    id="campaign_media",
    name="Campaign media planning",
    description="Checks media availability for advertising campaigns.",
    tags=["media planning", "advertising"],
    examples=["sector=Travel"],
)

agent_card = AgentCard(
    name="ASB Media Agent",
    description="Campaign media planning agent for AdverSphere Broadcasting.",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(),
    skills=[skill],
    supported_interfaces=[
        AgentInterface(
            url=f"http://localhost:{port_number}/",
            protocol_binding="JSONRPC",
        )
    ],
)

if __name__ == "__main__":
    handler = DefaultRequestHandler(
        agent_executor=MediaExecutorAgent(),
        task_store=InMemoryTaskStore(),
        agent_card=agent_card,
    )

    agent_card_routes = create_agent_card_routes(agent_card)
    jsonrpc_routes = create_jsonrpc_routes(handler, rpc_url="/")

    print(f"\n\nThe agent card path is {agent_card_routes[0].path}\n\n")

    # Starlette creates the web ASGI application
    # and sets up the routes for the agent card and JSON-RPC handler
    # to expose the A2A agent.
    app = Starlette(
        routes=[
            *agent_card_routes,
            *jsonrpc_routes,
        ]
    )

    uvicorn.run(app, host="0.0.0.0", port=port_number)