import uvicorn
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import InMemoryTaskStore
from a2a.helpers import new_text_message
from a2a.types import AgentCard, AgentInterface
from starlette.applications import Starlette

# --- Agent logic ---
def quote(brief: str) -> str:
    return f"You asked a quote for: {brief}"

# --- Minimal Agent Card ---
agent_card = AgentCard(
    name="Minimal A2A Agent with Agent Executor.",
    description="Ultra-minimal A2A demo.",
    version="1.0",
    supported_interfaces=[AgentInterface(url="http://localhost:9999/", 
                                         protocol_binding="JSONRPC")]
)

# --- Agent executor ---
class PricingAgent(AgentExecutor):
    async def execute(self, context: RequestContext, queue: EventQueue):
        await queue.enqueue_event(
            new_text_message(quote(context.get_user_input())))
    async def cancel(self, *_):
        pass




# --- Server ---
handler = DefaultRequestHandler(
    agent_executor=PricingAgent(),
    task_store=InMemoryTaskStore(),
    agent_card=agent_card,
)

app = Starlette(routes=[*create_agent_card_routes(agent_card),
                        *create_jsonrpc_routes(handler, rpc_url="/")])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)