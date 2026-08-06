# Lab 3 — Call your agent via the Responses API

> *Use each agent's Coding panel to run it from your own application code.*

| | |
|---|---|
| **Audience** | developers, data scientists |
| **Duration** | 45–60 minutes |
| **Level** | Intermediate |
| **You will build** | A small script that invokes your agent through the Responses API and streams the result |
| **Plane** | BUILD — Foundry Agent Service (integration) |

> [!NOTE]
> The instructor performs each step live; follow along on your own machine. Replace every `<angle-bracket placeholder>` with your own value.

---

## Prerequisites

- The agent from [Lab 1](lab-01x01-create-a-prompt-agent.md)/[Lab 2](lab-01x02-add-an-mcp-tool.md) and its **agent ID**.
- Python 3.10+ locally, and the ability to install packages in a virtual environment: `pip install openai azure-identity` (or use the shared [environment setup](../../environment_preparation.md)).
- Authentication: **Microsoft Entra ID** (recommended) via `az login`, or an API key.

## Learning objectives

- Find and use the per-agent **Coding** (*View code*) panel in Foundry.
- Authenticate to the Responses API with Entra ID (a bearer token) rather than a key.
- Send a request, read the response, and **stream** tokens.
- Continue a multi-turn conversation with server-side state.

---

## Step 1 — Open the Coding panel

Open your agent in the portal and select the **Code** (or *"View code"*) panel. Foundry generates a ready-to-run snippet for your exact resource: it contains the correct endpoint, API version (**v1**) and model/agent reference. Choose the **Python** tab.

> [!IMPORTANT]
> **Copy from the portal** — Always prefer the snippet the Coding panel gives you; it is pre-filled with your endpoint and version. The code below is the representative shape so you understand each part.

## Step 2 — Set up your environment

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install openai azure-identity
az login   # signs you in for Entra ID auth
```

## Step 3 — Call the agent (Entra ID auth)

Representative Python using a bearer token from Entra ID. Replace the endpoint/model with the values from your Coding panel:

```python
import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default")

client = OpenAI(
    base_url="<your-project-endpoint>/v1",   # from the Coding panel
    api_key=token_provider(),                 # bearer token, not a static key
)

resp = client.responses.create(
    model="<your-model-or-agent>",
    input="Presentati in una frase.",
)
print(resp.output_text)
```

> ✅ **Checkpoint** — You get a one-sentence Italian reply printed to your terminal. If so, your app is now talking to the agent.

## Step 4 — Stream the response

For a responsive UX, stream tokens as they are generated:

```python
stream = client.responses.create(
    model="<your-model-or-agent>",
    input="Elenca 3 usi di un agente per RAI Pubblicità.",
    stream=True,
)
for event in stream:
    if getattr(event, "delta", None):
        print(event.delta, end="", flush=True)
```

## Step 5 — Continue the conversation (server-side state)

The Responses API is stateful. Pass the previous response id to continue a thread without resending history:

```python
first = client.responses.create(model="<m>", input="Il mio nome è Mauro.")
second = client.responses.create(
    model="<m>",
    input="Come mi chiamo?",
    previous_response_id=first.id,   # server keeps the context
)
print(second.output_text)
```

## Step 6 — REST equivalent (optional)

The same call over REST, for non-Python stacks:

```bash
curl "$ENDPOINT/v1/responses" \
  -H "Authorization: Bearer $(az account get-access-token \
       --resource https://ai.azure.com --query accessToken -o tsv)" \
  -H "Content-Type: application/json" \
  -d '{"model":"<your-model>","input":"Ciao"}'
```

---

## Try it yourself (extension)

- Add the MCP tool from [Lab 2](./lab-01x02-add-an-mcp-tool.md) to the call via the `tools` parameter and watch a tool-augmented response.
- Wrap the streaming call in a tiny CLI loop to chat with the agent from your terminal.
- Switch auth from Entra ID to an API key and note when each is appropriate.

## Troubleshooting

| Symptom | Likely cause & fix |
|---------|--------------------|
| 401 Unauthorized | Token/scope wrong — run `az login`, and confirm the resource/scope matches your Coding-panel snippet. |
| 404 / model not found | Wrong model or agent reference — copy the exact value from the Coding panel. |
| Endpoint/region error | The resource region may not support the Responses API v1 — check the panel's endpoint and version. |
| No streamed output | Your SDK version differs — use the streaming shape from your generated snippet; event fields can vary by version. |

## What you learned

You took the agent out of the portal and into code via the Responses API, using the per-agent **Coding** panel, with Entra ID auth, streaming and stateful conversation. In **Lab 4** you publish it and invoke it with its own identity — without OBO.

---

[← Lab 2](./lab-01x02-add-an-mcp-tool.md) · [Session index](../README.md) · **Next:** [Lab 4 — Publish to Agent 365 (without OBO)](./lab-01x04-publish-to-agent365-no-obo.md)
