# Exercise 1 - Your first campaign-analysis agent
### Topic: Microsoft Agent Framework - Core duration: ~55 min

> **Goal:** build, with the **Microsoft Agent Framework**, an agent that *reasons about a
> goal* and *calls function tools* to answer real questions about RAI Pubblicita campaigns
> (metrics, ROI, comparisons). You'll see the **agentic loop** live (perceive -> reason ->
> act with a tool -> observe), just as we discussed yesterday.

**Concepts you'll cement (Day 1 slides):** anatomy of an agent (model + instructions +
tools), function tools, the agentic loop, observability of tool calls.

**Docs:**<br/>
- <https://learn.microsoft.com/agent-framework/>
- Function tools: <https://learn.microsoft.com/agent-framework/agents/tools/function-tools>

---

## Prerequisites
- Packages from `requirements.txt` installed (`agent-framework`, `azure-identity`).
- `az login` done.
- In `.env`: `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`.
- The `rai_campaigns.py` file (provided) in the same folder.

Create a file `es1_agent.py` and work there. At the top of the file load `.env`:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Part A - A minimal agent (~10 min)

The core of the Agent Framework: model + instructions. Still **without tools**.

```python
import asyncio
import os
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

load_dotenv()

async def main():
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        credential=AzureCliCredential(),
    )
    agent = Agent(
        client=client,
        name="CampaignAnalyst",
        instructions=(
            "You are an analyst at RAI Pubblicita. Always answer in English, "
            "concisely and professionally."
        )
    )
    answer = await agent.run("Introduce yourself in one sentence and tell me how you can help.")
    print(answer.text)

if __name__ == "__main__":
    asyncio.run(main())
```

**What you should see:** a short self-introduction. So far it's just a conversational
assistant: it understands and replies, but does not *do* anything.

---

## Part B - Add a function tool (~20 min)

Let's give the agent a **tool**: a plain Python function. The Agent Framework generates the tool schema from the *type hints* and *docstring*; with `Annotated` + `Field` we describe the parameters to the model.

```python
from typing import Annotated
from pydantic import Field
from rai_campaigns import get_campaign

def campaign_metrics(
    campaign_id: Annotated[str, Field(description="Campaign code, e.g. 'CMP-004'")]
) -> str:
    """Return budget, impressions, conversions and revenue for a RAI Pubblicita campaign."""
    c = get_campaign(campaign_id)
    if not c:
        return f"No campaign found with id {campaign_id}."
    return (
        f"{c['client']} ({c['id']}, sector {c['sector']}): "
        f"budget {c['budget_eur']} EUR, impressions {c['impressions']}, "
        f"conversions {c['conversions']}, revenue {c['revenue_eur']} EUR."
    )
```

Register the tool on the agent and ask a question that **forces** its use:

```python
async def main():
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        credential=AzureCliCredential(),
    )
    agent = Agent(
        client=client,
        name="CampaignAnalyst",
        instructions=(
            "You are an analyst at RAI Pubblicita. Always answer in English, "
            "concisely and professionally."
        ),
        tools=[campaign_metrics],
    )
    answer = await agent.run("Give me the key metrics of campaign CMP-004.")
    print(answer.text)
```

**What you should see:** the answer reports VoloBlu's **real** numbers taken from the tool
(revenue 351000 EUR, etc.), not invented values. This is *grounding* on your data.

---

## Part C - Two tools + multi-step reasoning (~15 min)

Add a second tool that computes ROI, so the agent **chains** several calls (first fetch the
data, then compute).

```python
def compute_roi(
    revenue_eur: Annotated[float, Field(description="Revenue in euro")],
    budget_eur: Annotated[float, Field(description="Budget spent in euro")],
) -> str:
    """Compute ROI percentage: (revenue - budget) / budget * 100."""
    value = (revenue_eur - budget_eur) / budget_eur * 100
    return f"ROI = {value:.1f}%"

async def main():
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        credential=AzureCliCredential(),
    )
    agent = Agent(
        client=client,
        name="CampaignAnalyst",
        instructions=(
            "You are an analyst at RAI Pubblicita. Always answer in English, "
            "concisely and professionally."
        ),
        tools=[campaign_metrics, compute_roi],
    )
    answer = await agent.run(
        "Between campaigns CMP-004 and CMP-005, which has the better ROI and by how much? Show the values."
    )
    print(answer.text)
```

**What you should see:** the agent concludes that **CMP-004 (VoloBlu, ROI 134.0%)** beats**CMP-005  (TeleCasa, ROI -10.0%)**. Note that to get there it called the tools multiple times: the **agentic loop** in action.

> Checkpoint: you have an agent that reasons and uses tools to answer a real business
> question. If you stop here, you're perfectly on track.

---

## Optional (bonus, ~10-15 min)

**B1 - Multi-turn conversation (session memory).** Use a *thread* to keep context across
follow-up questions:

```python
from requests import session

session = agent.create_session()
print((await agent.run("What is the ROI of CMP-001?", session=session)).text)
print((await agent.run("And compared to CMP-003, which is better?", session=session)).text)
```
Notice how in the second question the agent "remembers" CMP-001 without repeating it.

**B2 - A third tool for the whole portfolio.** Add:

```python
from rai_campaigns import list_campaigns
def all_campaigns() -> list:
    """List (id, client, sector) of every campaign in the portfolio."""
    return list_campaigns()
```
Then ask: *"Which campaign has the highest ROI in the portfolio?"* and watch the agent iterate (list -> fetch -> compute) until the answer (**CMP-004**).

**B3 - Inspect the tool calls (observability).** After a `run`, print the produced messages to see the *function calls* and their results:

```python
resp = await agent.run("What is the ROI of CMP-002?")
for m in resp.messages:
    print(m)   # look for function_call / function_result / m.role, m.author_name, m.contents[0].arguments,m.contents[0].call_id, m.text
```
This is the "in-code" equivalent of the *trace* panel from the slides.

---

## Instructor demo script (solution walkthrough)

> Full runnable solution: [`solutions/ex1_agent_framework.py`](./solutions/ex1_agent_framework.py).
> Run it live: `python solutions/ex1_agent_framework.py`. It prints four labelled sections.

1. **Set the scene.** "We're going to build the simplest possible agent and then teach it to
   use tools. Watch how it decides *on its own* to call a tool instead of guessing."
2. **Section A - plain question.** Run the script. Point at the first block: "This is just a
   conversational assistant - it introduces itself, but it can't touch our data yet."
3. **Section B - grounded metrics.** Point at the CMP-004 metrics: "These numbers -
   revenue 351000 - come from our `campaign_metrics` tool, not from the model's imagination.
   That's grounding." Optionally open `rai_campaigns.py` to show the numbers are real.
4. **Section C - multi-step reasoning.** "Now I ask it to *compare* two campaigns. It has to
   fetch metrics for both and then compute ROI - several tool calls chained together." Read
   the conclusion out loud: **CMP-004 at 134% vs CMP-005 at -10%**. "That chain is the
   agentic loop: reason, act, observe, repeat."
5. **Bonus - portfolio + memory.** Run the last block: "With a `thread`, it keeps context; and
   with a third tool it can scan the whole portfolio and still land on CMP-004."
6. **Close.** "Model + instructions + tools, running in a loop - the exact anatomy from the
   slides, now in ~40 lines of Python."

**Expected output (abridged):**
```
=== A) Plain question ===
I'm a RAI Pubblicita campaign analyst; I can pull campaign metrics and compute ROI for you.
=== B) Tool-grounded metrics ===
VoloBlu (CMP-004, sector Travel): budget 150000 EUR, impressions 9200000, conversions 2208, revenue 351000 EUR.
=== C) Multi-step reasoning ===
CMP-004 (VoloBlu) has ROI 134.0%, CMP-005 (TeleCasa) has ROI -10.0% -> CMP-004 is better by 144 points.
=== Bonus) Whole-portfolio question (multi-turn thread) ===
Highest ROI: CMP-004 (VoloBlu), 134.0%.
Losing money: CMP-005 (TeleCasa), -10.0%.
```
> Note: LLM wording will vary run to run; the numbers should not.

---

## Final check / reflection questions
1. At which point did the agent **decide on its own** to call a tool instead of answering directly?
2. Why is it better to have two separate tools (`campaign_metrics` and `compute_roi`) instead of one?
3. When would you *not* use an agent but a plain function? (agent-vs-workflow rule from the slides)
