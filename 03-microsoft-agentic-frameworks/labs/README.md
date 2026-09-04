# Agentic Frameworks - Upskilling - Day 2
## Hands-on Exercises (technical deep dive)

Welcome to the hands-on part. After Day 1 (vision, architectures and demos), today you
put your **hands on the keyboard**. These four exercises mirror the four Day 1 topics and
are meant to **cement the concepts** by building and running real Python code, always on
cases close to AdvertSphere Broadcasting's business (campaigns, ROI, pricing, media planning, evaluation).

All exercises are in **Python**.

---

## Exercise index

| # | Exercise | Topic (Day 1 slides) | Duration | What you build |
|---|----------|----------------------|:--------:|----------------|
| 1 | [Your first campaign-analysis agent](./exercise-1-agent-framework.md) | **Microsoft Agent Framework** | **55 min** | An agent that reasons and uses *function tools* to answer questions about campaign ROI and metrics |
| 2 | [From the Responses API to a managed agent](./exercise-2-foundry-hosted-agents.md) | **Foundry & Hosted Agents** | **60 min** | Using Foundry's **Responses API** with Code Interpreter, tracing, and steps toward a Hosted Agent |
| 3 | [Expose the campaigns as an MCP server](./exercise-3-mcp.md) | **Model Context Protocol** | **70 min** | An **MCP server** exposing tools, resources and prompts over the campaign data, plus a client that consumes it |
| 4 | [Agents that collaborate: pricing & media planning](./exercise-4-a2a.md) | **Agent-to-Agent (A2A)** | **55 min** | A remote **A2A agent** (pricing) and a client agent that discovers it via its *Agent Card* and delegates a task |

**Core total: 4 hours (240 min).**
Each exercise has an **Optional (bonus)** section: if an exercise grabs you, keep going there;
otherwise stop and move on to the next one, staying on schedule.

Each exercise also ends with an **Instructor demo script (solution walkthrough)** — a
step-by-step "run it live" track. The **fully runnable solutions** are in the
[`solutions/`](./solutions) folder, so you can either demo them in front of the class or
check your own work when practising on your own.

> Suggested pacing: one ~15-min break after Exercise 2 (mid-morning).

---

## Prerequisites

- **Python environment already set up** (creation/activation covered previously).
- Install the packages with **[`requirements.txt`](./requirements.txt)** (single file for all exercises).
- **Access to Microsoft Foundry / Azure OpenAI** already provisioned (Exercises 1 and 2).
  Authentication via Entra ID: run `az login` before you start.
- Environment variables (e.g. in a `.env` file in the exercises folder):

  ```dotenv
  # Foundry (Exercise 2, and optional Exercise 1 via Foundry)
  FOUNDRY_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
  FOUNDRY_MODEL_NAME=<model-deployment-name>       # e.g. gpt-4o-mini

  # Azure OpenAI (Exercise 1 with Agent Framework)
  AZURE_OPENAI_ENDPOINT=https://<your-endpoint>.openai.azure.com/
  AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=<model-deployment-name>
  ```

- Local ports used: MCP -> `127.0.0.1:8000`, A2A -> `localhost:9999` (and `10000` for the bonus).

---

## Shared data: `rai_campaigns.py`

All exercises reuse the same small synthetic dataset of 5 campaigns, in
**[`rai_campaigns.py`](./rai_campaigns.py)** (included in this folder). It exposes:

- `CAMPAIGNS` — list of dicts with budget, impressions, clicks, conversions, revenue...
- `list_campaigns()`, `get_campaign(id)`, `roi(id)`, `cpm(id)`

Quick sanity check:

```bash
python rai_campaigns.py
```

Expected output (ROI = (revenue - budget) / budget):

```
CMP-001 AutoMilano   ROI   75.0%  CPM  14.29 EUR
CMP-002 BancaVerde   ROI   46.7%  CPM  17.65 EUR
CMP-003 FreschErba   ROI   60.0%  CPM   8.82 EUR
CMP-004 VoloBlu      ROI  134.0%  CPM  16.30 EUR
CMP-005 TeleCasa     ROI  -10.0%  CPM  18.60 EUR
```

Reading note: **VoloBlu (CMP-004)** is the best-ROI campaign, **TeleCasa (CMP-005)** is
losing money. Both come up repeatedly across the exercises.

---

## Solutions folder

The [`solutions/`](./solutions) folder contains a ready-to-run script for each exercise:

| Exercise | Solution file(s) |
|----------|------------------|
| 1 | `ex1_agent_framework.py` |
| 2 | `ex2_foundry_responses.py` |
| 3 | `ex3_mcp_server.py`, `ex3_mcp_client.py` |
| 4 | `ex4_pricing_server.py`, `ex4_sales_client.py`, `ex4_media_server.py` (bonus) |

Copy `rai_campaigns.py` next to the solution scripts (or run them from this folder) so the
imports resolve.

---

## Important note on versions

Agent Framework, the Foundry Agent Service (A2A tool), MCP and A2A are **recent, fast-moving**
technologies. If an `import`, a class name or a parameter does not exactly match the version
installed in your environment, **check the documentation linked in each exercise**: the goal is
not the exact syntax of a release, but to **cement the concepts** (agent + tools, Responses API,
MCP server, A2A delegation). The code snippets follow the APIs documented at the time of writing.

---

## How we'll use the results

By the end of the morning you'll have built, with your own hands, a small piece of each of the
four layers of yesterday's agentic stack: **build** (Agent Framework), **run** (Foundry),
**connect to tools** (MCP) and **let agents collaborate** (A2A). That is exactly the reference
architecture from the final slide of Day 1.

Have fun!
