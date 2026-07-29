# Exercise 3 - Expose the campaigns as an MCP server
### Topic: Model Context Protocol (MCP) - Core duration: ~70 min

> **Goal:** build an **MCP server** that exposes RAI Pubblicita campaign data as **tools**,
> **resources** and **prompts**, then consume it with an **MCP client**. You'll see the
> "**build once, reuse everywhere**" principle in practice: the same server can later be used
> by any compliant agent (Agent Framework, Foundry, ...).

**Concepts you'll cement (Day 1 slides):** MCP's client-server architecture, the *primitives*
(tools / resources / prompts), the M x N -> M + N problem, tool reusability.

**Docs:** MCP <https://modelcontextprotocol.io/> - FastMCP <https://gofastmcp.com/>

> This exercise is **fully local**: no cloud credentials are needed for parts A-C.

---

## Prerequisites
- Packages from `requirements.txt` (`fastmcp`, `mcp`).
- The `rai_campaigns.py` file in the same folder.
- Two terminals (one for the server, one for the client).

---

## Part A - Build the MCP server (~30 min)

Create `mcp_server.py`. With **FastMCP** you define tools as plain functions: the *type hints*
and *docstrings* automatically generate the MCP schema.

```python
from fastmcp import FastMCP
from rai_campaigns import CAMPAIGNS, get_campaign, list_campaigns, roi

mcp = FastMCP("RAI Campaigns MCP")

# --- TOOLS: actions an agent can call ---
@mcp.tool
def get_campaign_details(campaign_id: str) -> dict:
    """Full details of a campaign by its id (e.g. 'CMP-004')."""
    c = get_campaign(campaign_id)
    return c or {"error": f"campaign {campaign_id} not found"}

@mcp.tool
def all_campaigns() -> list:
    """Short list (id, client, sector) of all campaigns."""
    return list_campaigns()

@mcp.tool
def top_campaigns_by_roi(n: int = 3) -> list:
    """Top n campaigns by descending ROI, with the ROI% value."""
    data = [{"id": c["id"], "client": c["client"], "roi_pct": roi(c["id"])}
            for c in CAMPAIGNS]
    data.sort(key=lambda x: x["roi_pct"], reverse=True)
    return data[:n]

# --- RESOURCE: readable data to ground the answers on ---
@mcp.resource("campaigns://all")
def campaigns_resource() -> list:
    """All campaigns as raw data (context for the agent)."""
    return CAMPAIGNS

# --- PROMPT: reusable template ---
@mcp.prompt
def evaluate_campaign(campaign_id: str) -> str:
    """Template to evaluate a campaign in a standard way."""
    return (
        f"Evaluate campaign {campaign_id}: fetch the data with the tools, "
        f"compute the ROI, compare it with the others and propose an action."
    )

if __name__ == "__main__":
    # HTTP transport: the server listens on http://127.0.0.1:8000/mcp
    mcp.run(transport="http", host="127.0.0.1", port=8000)
```

Start the server (**first terminal**):

```bash
python mcp_server.py
```

**What you should see:** a log saying the MCP server is listening on `127.0.0.1:8000`.
Leave it running.

---

## Part B - Consume the server with an MCP client (~25 min)

Create `mcp_client.py`. The client **discovers** the tools and then **calls** one - all over
the protocol, without knowing anything about the server's internal implementation.

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        # 1. discovery: which tools does the server expose?
        tools = await client.list_tools()
        print("Exposed tools:", [t.name for t in tools])

        # 2. call a tool
        res = await client.call_tool("top_campaigns_by_roi", {"n": 3})
        print("Top 3 by ROI:", getattr(res, "data", None) or res.content)

        # 3. read a resource
        resources = await client.read_resource("campaigns://all")
        print("Campaigns in the resource:", len(resources))

asyncio.run(main())
```

Run (**second terminal**):

```bash
python mcp_client.py
```

**What you should see:** the list of tools (`get_campaign_details`, `all_campaigns`,
`top_campaigns_by_roi`) and, at the top of the top-3 by ROI, **CMP-004 (VoloBlu, 134.0%)**.

> Note: depending on the FastMCP version, a `call_tool` result is read via `res.data`
> (structured output) or `res.content`. The snippet above tries both.

---

## Part C - Add a prompt and verify (~15 min)

You already defined the `evaluate_campaign` prompt. List it and fetch it from the client:

```python
async with Client("http://127.0.0.1:8000/mcp") as client:
    prompts = await client.list_prompts()
    print("Available prompts:", [p.name for p in prompts])
    rendered = await client.get_prompt("evaluate_campaign", {"campaign_id": "CMP-005"})
    print(rendered)
```

**What you should see:** the `evaluate_campaign` prompt and the text rendered for **CMP-005**.
Prompts capture "the right way to ask for something", reusable by anyone.

> Checkpoint: you have an MCP server exposing tools, resources and prompts over campaign data,
> and a client that consumes them. This is exactly what an agent would do on your behalf.

---

## Optional (bonus, ~15 min)

**B1 - A new comparison tool.** Add to the server:

```python
from rai_campaigns import roi
@mcp.tool
def compare_campaigns(id_a: str, id_b: str) -> dict:
    """Compare the ROI of two campaigns and say which performs better."""
    ra, rb = roi(id_a), roi(id_b)
    better = id_a if (ra or -1e9) >= (rb or -1e9) else id_b
    return {"roi": {id_a: ra, id_b: rb}, "better": better}
```
Restart the server and call the tool from the client with `CMP-004` and `CMP-005`.

**B2 - Proper logging for MCP.** In an MCP server do **not** `print` to stdout (it would break
the JSON-RPC messages in stdio mode): use the `logging` module, which writes to *stderr*.

```python
import logging
logger = logging.getLogger(__name__)
# inside a tool:  logger.info("Top ROI requested, n=%s", n)
```

**B3 - [Advanced] Let a model pick the tools.** Connect this server to an LLM so the model
decides which tool to use. Two paths:
- **Client-side (local, reaches 127.0.0.1):** use the Agent Framework's MCP integration to pass
  the server as a tool to an agent (see Agent Framework docs -> *MCP*).
- **Via Foundry:** use the Responses API `mcp` tool (Exercise 2 bonus), remembering the server
  must be publicly reachable.

Ask: *"Which campaign has the highest ROI and what would you recommend for the worst one?"*

---

## Instructor demo script (solution walkthrough)

> Full runnable solution: [`solutions/ex3_mcp_server.py`](./solutions/ex3_mcp_server.py) and
> [`solutions/ex3_mcp_client.py`](./solutions/ex3_mcp_client.py).
> Terminal 1: `python solutions/ex3_mcp_server.py` - Terminal 2: `python solutions/ex3_mcp_client.py`.

1. **Set the scene.** "Yesterday MCP was a box on a diagram. Now we build one. On the left a
   server that owns the campaign data; on the right a client that has never seen that code."
2. **Terminal 1 - start the server.** Run it. "It's listening on port 8000. Notice I wrote
   three tools as normal Python functions - FastMCP turned the type hints and docstrings into
   an MCP schema for me."
3. **Terminal 2 - discovery.** Run the client. Point at `Exposed tools: [...]`: "The client
   *asked* the server what it can do - it discovered the tools over the protocol."
4. **Call a tool.** Point at `Top 3 by ROI`: "It called `top_campaigns_by_roi` and got real
   results - **CMP-004 on top at 134%**. The client knows nothing about how that's computed."
5. **Resource + prompt.** "The resource is readable context; the prompt is a reusable template -
   `evaluate_campaign` is 'the right way to ask'."
6. **The punchline.** "I never wrote an integration. I spoke MCP once. This exact server can now
   be used by an Agent Framework agent or a Foundry agent - build once, reuse everywhere. That's
   M x N collapsing to M + N."
7. **(Optional) live edit.** Add `compare_campaigns`, restart, call it with CMP-004 vs CMP-005 to
   show how cheap it is to extend.

**Expected output (client, abridged):**
```
Exposed tools: ['get_campaign_details', 'all_campaigns', 'top_campaigns_by_roi']
Top 3 by ROI: [{'id': 'CMP-004', 'client': 'VoloBlu', 'roi_pct': 134.0}, {'id': 'CMP-001', 'client': 'AutoMilano', 'roi_pct': 75.0}, {'id': 'CMP-003', 'client': 'FreschErba', 'roi_pct': 60.0}]
Campaigns in the resource: 5
```
> Note: the exact ordering of ties and the result wrapper (`.data` vs `.content`) can vary by FastMCP version; CMP-004 is always first.

---

## Final check / reflection questions
1. What is the difference between a **tool**, a **resource** and a **prompt** in MCP?
2. Why can the same MCP server be used by different agents with no changes? (M x N -> M + N)
3. What risk does connecting an **external**, untrusted MCP server introduce? (prompt injection / XPIA)
