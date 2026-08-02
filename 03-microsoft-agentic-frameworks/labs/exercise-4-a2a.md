# Exercise 4 - Agents that collaborate: pricing & media planning
### Topic: Agent-to-Agent (A2A) - Core duration: ~55 min

> **Goal:** build a **remote A2A agent** (a "Pricing Agent" that quotes campaigns) and a
> **client agent** ("Sales Assistant") that **discovers** it through its *Agent Card* and
> **delegates a task** over the A2A protocol. You'll see *horizontal* collaboration between
> agents, complementary to MCP.

**Concepts you'll cement (Day 1 slides):** the Agent Card (who it is / what it can do / where
it answers), delegating a task between agents, the client <-> remote-agent loop, MCP
(agent<->tools) vs A2A (agent<->agent).

**Docs:** A2A <https://a2a-protocol.org/> - Python SDK `a2a-sdk`
<https://github.com/a2aproject/a2a-python>

> Note: `a2a-sdk` moves fast: if a class/field name differs from your version, adapt using the
> linked docs. The goal is to see **Agent Card + task delegation** in action. This exercise is
> **local** and the pricing logic is deterministic (no cloud credentials required).

---

## Prerequisites
- Packages from `requirements.txt` (`a2a-sdk`, `uvicorn`, `httpx`).
- Two terminals (server + client).

---

## Part A - The remote agent: Pricing Agent (~25 min)

In this first step, you will expose a small deterministic Python function as a remote A2A agent.
This keeps the business logic intentionally simple, so you can focus on the A2A building blocks
introduced in the slides: the agent's identity and capabilities, its protocol endpoint, and the
executor that handles incoming requests.

The agent publishes an **Agent Card** (a machine-readable business card) and implements an
**AgentExecutor** containing its logic. The SDK routes the incoming A2A message to the executor
and returns its response through the event queue. Create `pricing_server.py`:

```python
import uvicorn
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
```

Start the server (**first terminal**):

```bash
python exercise-4-a2a_pricing_server.py
```

**What you should see:** Uvicorn listening on `http://0.0.0.0:9999`. The Agent Card is
published automatically at [`http://localhost:9999/.well-known/agent-card.json`](http://localhost:9999/.well-known/agent-card.json). Open it in a browser to see the "business card".

---

## Part B - The client: Sales Assistant that delegates (~20 min)

Now you will build the other side of the interaction. The Sales Assistant does not import or
reimplement the pricing logic: it only knows the remote agent's base URL. The A2A client uses the
Agent Card to discover how to communicate with the agent, sends a structured message, and receives
the remote response.

This is the key distinction from a normal local function call: the client **discovers** an
independently running agent and **delegates** the task through the A2A protocol.
Create `exercise-4-a2a_sales_client.py`:

```python
import asyncio

from a2a.client import create_client
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest
from google.protobuf.json_format import MessageToDict


async def main():
    client = await create_client("http://localhost:9999")

    async with client:
        request = SendMessageRequest(
            message=new_text_message(
                "sector=Travel; impressions=9200000",
                role=Role.ROLE_USER,
            )
        )

        async for response in client.send_message(request):
            print(MessageToDict(response))


asyncio.run(main())
```

Run (**second terminal**):

```bash
python sales_client.py
```

**What you should see:** a JSON response with the quote text, e.g.
*"sector Travel: 9,200,000 impressions x CPM 16.0 EUR = 147,200 EUR"*. The client contains
**no** pricing logic: it **delegated** it to the remote agent - that's A2A in action.

---

## Part C - Observe the Agent Card and the task loop (~10 min)

1. Open the Agent Card in a browser and locate the three key elements: **who it is** (`name`,
   `description`), **what it can do** (`skills`), **where it answers** (`url`).
2. In the client's JSON response, locate the message produced by the agent (`role: "agent"`)
   and its `text`.

> Checkpoint: you have a remote agent with its Agent Card and a client agent that discovers it
> and delegates a task. This is the "call a colleague in another department" from the
> MCP-vs-A2A slide.

---

## Optional (bonus, ~25 min)

**B1 - A second remote agent: Media Planning.** Copy `pricing_server.py` into
`media_server.py`: change the port (`10000`), the Agent Card (`name="RAI Media Planning Agent"`,
`url="http://localhost:10000/"`) and the executor logic, which given a brief returns slot
availability, e.g.:

```python
def availability(brief: str) -> str:
    parts = dict(p.split("=") for p in brief.replace(" ", "").split(";") if "=" in p)
    sector = parts.get("sector", "n/a")
    return f"Media planning - sector {sector}: 3 prime-time TV slots and 5 digital packages available in March."
```

Here is the modified client to invoke both the quote and media servers:
```python
import asyncio

from a2a.client import create_client
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest
from google.protobuf.json_format import MessageToDict


async def main():

    for url in ["http://localhost:9999", "http://localhost:10000"]:
        try:
            client = await create_client(url)
            async with client:
                request = SendMessageRequest(
                    message=new_text_message(
                        "sector=Travel; impressions=9200000",
                        role=Role.ROLE_USER,
                    )
                )

                async for response in client.send_message(request):
                    print(MessageToDict(response))
            
        except Exception as e:
            print(f"Failed to connect to {url}: {e}")


asyncio.run(main())
```

**B2 - Invoke the agents via A2A Client SDK.** In `exercise-4-a2a_sales_client_a2a.py`, the clients query both the Pricing Agent (9999) and the Media Planning Agent (10000):
```python
import asyncio
from a2a.client import create_client
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest

async def main():

    for url in ["http://localhost:9999", "http://localhost:10000"]:
        try:
            client = await create_client(url)
            async with client:
                request = SendMessageRequest(
                    message=new_text_message(
                        "sector=Travel; impressions=9200000",
                        role=Role.ROLE_USER,
                    )
                )

                async for response in client.send_message(request):
                    print(response.message.parts)
            
        except Exception as e:
            print(f"Failed to connect to {url}: {e}")


asyncio.run(main())
```

**B3 - Invoke the agents via Microsoft Agent Framework.** In `exercise-4-a2a_sales_client_maf.py`, the remote agents are represented as *two local MAF agents* using the A2A integration. The client then adds them to a **MAF sequential workflow**, so that a single workflow call invokes both the Pricing Agent (9999) and the Media Planning Agent (10000):
```python
import asyncio
from agent_framework.a2a import A2AAgent
from agent_framework.orchestrations import SequentialBuilder

CAMPAIGN_BRIEF = "sector=Travel; impressions=9200000"

async def main():
    pricing_agent = A2AAgent(
        name="PricingAgent",
        description="Computes an advertising campaign quote.",
        url="http://localhost:9999",
    )
    media_agent = A2AAgent(
        name="MediaAgent",
        description="Finds available media inventory for a campaign.",
        url="http://localhost:10000",
    )

    workflow = SequentialBuilder(
        participants=[pricing_agent, media_agent],
        intermediate_output_from=[pricing_agent], # makes pricing_agent answer  visibile as intermediate output within the workflow
    ).build()

    async with pricing_agent, media_agent:
        result = await workflow.run(CAMPAIGN_BRIEF)

    for response in result.get_intermediate_outputs():
        print(f"Pricing: {response.text}")
    for response in result.get_outputs():
        print(f"Media planning: {response.text}")


asyncio.run(main())
```
---

## Instructor demo script (solution walkthrough)

> Full runnable solution: [`solutions/exercise-4-a2a_pricing_server`](./solutions/exercise-4-a2a_pricing_server)
> [`solutions/exercise-4-a2a_media_server.py`](./solutions/exercise-4-a2a_media_server.py).
> [`solutions/exercise-4-a2a_sales_client_a2a.py`](./solutions/exercise-4-a2a_sales_client_a2a.py) and (bonus)
> [`solutions/exercise-4-a2a_sales_client_maf.py`](./solutions/exercise-4-a2a_sales_client_maf.py) and (bonus)
> Terminal 1: `python solutions/ex4_pricing_server.py` - Terminal 2: `python solutions/ex4_sales_client.py`.

1. **Set the scene.** "So far our agents used *tools*. Now an agent will call *another agent*.
   The Pricing Agent is owned by a different team; we don't import its code, we delegate to it."
2. **Terminal 1 - start the Pricing Agent.** Run it. Open
   `http://localhost:9999/.well-known/agent-card.json` in the browser: "This is the Agent Card -
   the machine-readable business card. Name, skills, endpoint. This is how another agent finds it."
3. **Terminal 2 - the Sales Assistant.** Run the client. "Step 1 it discovers the agent from that
   card. Step 2 it sends a brief - `sector=Travel; impressions=9200000`."
4. **Read the result.** Point at the quote in the JSON: **~147,200 EUR**. "Notice the client has
   zero pricing logic. It delegated the whole task. That's horizontal, agent-to-agent collaboration."
5. **Tie back to the slide.** "MCP was reaching *down* to a tool; A2A is reaching *sideways* to a
   peer. In a real RAI setup, pricing, media planning and legal could each be their own agent."
6. **(Optional) two agents.** Start `ex4_media_server.py` on 10000 and show the client composing a
   pricing quote **and** availability into one proposal - the sales-assistant-of-agents pattern.
7. **Close.** "Same protocol, swappable brains: tomorrow the Pricing Agent could be LLM-powered and
   nothing on the client side changes."

**Expected output (client, abridged):**
```json
{"jsonrpc": "2.0", "id": "...", "result": {"role": "agent",
 "parts": [{"type": "text",
   "text": "Quote - sector Travel: 9,200,000 impressions x CPM 16.0 EUR = 147,200 EUR."}],
 "messageId": "..."}}
```
> Note: the exact JSON envelope (field names, message vs task wrapper) depends on the `a2a-sdk`
> version; the delegated quote text is what matters.

---

## Final check / reflection questions
1. What is the **Agent Card** for, and why is it "machine-readable"?
2. What is the difference between using an **MCP tool** and **delegating to an A2A agent**? (vertical vs horizontal)
3. In the RAI case, which capabilities would you keep as **separate agents** (A2A) instead of internal functions? Why?
