# Exercise 2 - From the Responses API to a managed agent
### Topic: Microsoft Foundry & Hosted Agents - Core duration: ~60 min

> **Goal:** use **Microsoft Foundry** from code through the **Responses API** - the *single
> entry point* from the slides - to make a model reason over campaign data, give it the
> **Code Interpreter** tool for exact math, and inspect the *trace*. To close, the conceptual
> steps toward a **Hosted Agent**.

**Concepts you'll cement (Day 1 slides):** the Responses API as the single entry point,
thread = conversation continuity, action tools (Code Interpreter), numeric accuracy,
observability, and the Prompt Agent vs **Hosted Agent** distinction.

**Docs:** azure-ai-projects
<https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme> -
Hosted agents: <https://learn.microsoft.com/azure/ai-foundry/agents/> (Deploy your first hosted agent)

---

## Prerequisites
- Packages from `requirements.txt` (`azure-ai-projects>=2.3.0`, `azure-identity`, `openai`).
- `az login` done, with a role assigned on the Foundry project.
- In `.env`: `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL_NAME` (the model *deployment* name).

Create `es2_foundry.py`. At the top:

```python
import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

load_dotenv()
project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
MODEL = os.environ["FOUNDRY_MODEL_NAME"]
```

---

## Part A - Responses API + continuity (thread) (~20 min)

The Responses API is how **any** code reaches Foundry models. The `previous_response_id`
parameter links turns: it's the **thread** concept from the slides.

```python
with project.get_openai_client() as client:
    r1 = client.responses.create(
        model=MODEL,
        input=(
            "You are an analyst at RAI Pubblicita. In English and in one sentence, "
            "explain what ROI measures for a campaign."
        ),
    )
    print("Turn 1:", r1.output_text)

    r2 = client.responses.create(
        model=MODEL,
        input="And what does CPM measure?",
        previous_response_id=r1.id,   # <-- continuity: the model 'remembers' turn 1
    )
    print("Turn 2:", r2.output_text)
```

**What you should see:** two coherent answers; in the second, the model knows we're still
talking about advertising metrics without being told again.

---

## Part B - The Code Interpreter tool for exact numbers (~25 min)

Models get arithmetic wrong. Let's give the model an **action tool** that *runs code* to
compute ROI and CPM exactly.

```python
with project.get_openai_client() as client:
    r = client.responses.create(
        model=MODEL,
        tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
        input=(
            "Campaign VoloBlu: budget 150000 EUR, impressions 9,200,000, revenue 351000 EUR. "
            "By running code, compute precisely: ROI% = (revenue-budget)/budget*100 "
            "and CPM in euro = budget/impressions*1000. Answer in English with both values."
        ),
    )
    print(r.output_text)
```

**What you should see:** **ROI = 134.0%** and **CPM ~= 16.30 EUR**, computed by running code
(not "by eye"). Same tool as yesterday's Demo 2, here via the SDK.

---

## Part C - Look inside the response (observability) (~15 min)

Each response is made of several *items*: reasoning, the tool call, the final message.
Inspecting them is the in-code equivalent of the *trace* panel.

```python
print("--- Items produced by the Responses API ---")
for item in r.output:
    print("-", item.type)   # e.g. 'reasoning', 'code_interpreter_call', 'message'
```

**What you should see:** among the items there's a **Code Interpreter call**: proof that the
model *acted*, not just generated text.

> Checkpoint: you used Foundry from code via the Responses API, with conversation continuity,
> an action tool and trace inspection. If you stop here, great.

---

## Optional (bonus, ~15 min)

**B1 - Connect your MCP server (bridge to Exercise 3).** The Responses API also accepts an
**MCP** tool. If you completed Exercise 3 and the server is **reachable** (see network note),
add:

```python
tools=[{
    "type": "mcp",
    "server_label": "rai_campaigns",
    "server_url": "https://<public-host>/mcp",   # must be reachable from Foundry
    "require_approval": "never",
}]
```
and ask: *"List the campaigns and tell me which has the highest ROI."* The model will pick the
MCP tools by itself.
> Network note: Foundry is a cloud service, so it **cannot** reach `127.0.0.1`. For this test,
> expose the MCP server with a public tunnel (e.g. `devtunnel`/ngrok); or, to stay local,
> connect the MCP server to a model **client-side** with the Agent Framework (Exercise 3 bonus).

**B2 - Toward the Hosted Agent (reading + sketch).** The Exercise 1 code (Agent Framework) can
become a **Hosted Agent**: you package it as a container/zip and Foundry runs it with a managed
endpoint, scaling and Entra identity. The *additive* pattern is that your code still calls the
Responses API on the project endpoint - exactly what you did here. Path: `azure-ai-projects` ->
`samples/hosted_agents/` and the *Deploy your first hosted agent* guide. (A full container
deploy is beyond the lab time: read the flow and identify what you'd package from your Ex. 1 agent.)

---

## Instructor demo script (solution walkthrough)

> Full runnable solution: [`solutions/ex2_foundry_responses.py`](./solutions/ex2_foundry_responses.py).
> Run it live: `python solutions/ex2_foundry_responses.py`. It prints three labelled sections.

1. **Set the scene.** "Yesterday we said the Responses API is Foundry's single front door.
   Now we walk through that door from Python."
2. **Section A - continuity.** Run the script. "Two turns. In the second one I never repeat
   the topic, yet the model stays on advertising metrics - that's `previous_response_id`, i.e.
   a thread."
3. **Section B - Code Interpreter.** "Here's the important part for anyone who cares about
   correct numbers. I ask for ROI and CPM and force the model to *run code*." Point at the
   output: **134.0%** and **~16.30 EUR**. "It computed, it didn't guess."
4. **Section C - trace.** Point at the printed item types: "See the `code_interpreter_call`?
   That's the audit trail - every action the agent takes is observable, exactly like the trace
   panel from the slides."
5. **Bonus tease.** "In a minute (Exercise 3) we'll build an MCP server; this same Responses
   call can then use it as a tool - that's how build-once/reuse-everywhere pays off."
6. **Close.** "One endpoint, any framework, tools and full observability - that's Foundry in
   one screen."

**Expected output (abridged):**
```
=== A) Responses API + continuity (thread) ===
Turn 1: ROI measures how much revenue a campaign returns relative to its cost...
Turn 2: CPM measures the cost per one thousand impressions...
=== B) Code Interpreter for exact numbers ===
ROI = 134.0%, CPM = 16.30 EUR.
=== C) Inspect the response items (trace) ===
- reasoning
- code_interpreter_call
- message
```
> Note: the exact item labels and wording depend on the model/SDK version; the two computed values should not.

---

## Final check / reflection questions
1. Why is the Responses API called the "single entry point"? What would change if you switched frameworks?
2. What is the practical difference between a **Prompt Agent** and a **Hosted Agent**? When do you need the latter?
3. Why does the Code Interpreter improve reliability over letting the model "do the ROI math" itself?
