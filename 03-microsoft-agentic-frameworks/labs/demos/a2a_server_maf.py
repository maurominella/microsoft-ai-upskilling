import os

import uvicorn

from agent_framework import Agent
from agent_framework.a2a import A2AExecutor
from agent_framework.openai import OpenAIChatClient
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentInterface
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from starlette.applications import Starlette

load_dotenv()

# --- Agent logic ---
def quote(brief: str) -> str:
    return f"Preventivo per: {brief}"

# --- Minimal Agent Card ---
agent_card = AgentCard(
    name="Minimal A2A Agent with Microsoft Agent Framework.",
    description="Ultra-minimal A2A demo.",
    version="1.0",
    supported_interfaces=[AgentInterface(url="http://localhost:9999/", 
                                         protocol_binding="JSONRPC")]
)

# --- Agent creation with Microsoft Agent Framework ---
agent = Agent(
    client=OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        credential=AzureCliCredential(),
    ),
    name="PricingAgent",
    instructions="Use the tool to calculate the quote (il tool quote).",
    tools=[quote],
)

# --- Server ---
handler = DefaultRequestHandler(
    agent_executor=A2AExecutor(agent),
    task_store=InMemoryTaskStore(),
    agent_card=agent_card,
)

app = Starlette(routes=[*create_agent_card_routes(agent_card),
                        *create_jsonrpc_routes(handler, rpc_url="/")])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)