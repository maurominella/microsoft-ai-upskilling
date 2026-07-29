"""
SOLUTION (bonus B1) - Exercise 4: second remote A2A agent, Media Planning.

Run:  python solutions/ex4_media_server.py     (listens on port 10000)
Then set QUERY_MEDIA = True in ex4_sales_client.py to orchestrate both agents.
"""
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from a2a.types import AgentCard, AgentSkill, AgentCapabilities


def availability(brief: str) -> str:
    parts = dict(p.split("=") for p in brief.replace(" ", "").split(";") if "=" in p)
    sector = parts.get("sector", "n/a")
    return (f"Media planning - sector {sector}: 3 prime-time TV slots and "
            f"5 digital packages available in March.")


class MediaAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        request = context.get_user_input()
        event_queue.enqueue_event(new_agent_text_message(availability(request)))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")


skill = AgentSkill(
    id="slot_availability",
    name="Slot availability",
    description="Returns available advertising slots from a brief (sector).",
    tags=["media planning", "advertising"],
    examples=["sector=Travel"],
)
agent_card = AgentCard(
    name="RAI Media Planning Agent",
    description="Media planning / slot availability agent for RAI Pubblicita.",
    url="http://localhost:10000/",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(),
    skills=[skill],
)


if __name__ == "__main__":
    handler = DefaultRequestHandler(
        agent_executor=MediaAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )
    app = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(app.build(), host="0.0.0.0", port=10000)
