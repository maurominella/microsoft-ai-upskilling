# Lab 2 — Add an MCP tool to your agent

> *Extend the agent with external tools through the Toolbox / Model Context Protocol.*

| | |
|---|---|
| **Audience** | CSA, developers, data scientists |
| **Duration** | 45–60 minutes |
| **Level** | Intermediate |
| **You will build** | An agent connected to a remote MCP server, invoking an external tool with approval control |
| **Plane** | BUILD — Foundry Agent Service (open standards) |

> [!NOTE]
> The instructor performs each step live; follow along on your own machine. Replace every `<angle-bracket placeholder>` with your own value.

---

## Prerequisites

- The agent from [Lab 1](lab-1-create-a-prompt-agent.md) (or any prompt-based agent in your project).
- A reachable MCP server endpoint (a public sample MCP server, an internal one, or a `Foundry Toolbox` exposed as an MCP endpoint).
- If the MCP server requires auth: permission to create a **project connection** to hold the credential.

## Learning objectives

- Understand **MCP** as the open standard for exposing tools to any LLM client.
- Add a remote MCP server as a tool and authenticate via a project connection.
- Control tool execution with an **approval policy**, and review/approve a tool call.
- Recognise the single **Toolbox** MCP endpoint the agent talks to.

---

## Step 1 — Understand what you are connecting

> [!NOTE]
> **Concept** — MCP (Model Context Protocol) is an open standard that lets a server expose tools and context to any MCP-compatible client — and Foundry Agent Service is such a client. This is what keeps your integrations vendor-neutral.

## Step 2 — Add the MCP tool in the portal

- Open your agent → **Tools** → **Add a tool** → **Model Context Protocol (MCP)**.
- **Server label:** a short name, e.g. `contoso-tools`.
- **Server URL:** your MCP endpoint, e.g. `https://<your-mcp-server>/sse`.
- Optionally scope which of the server's tools the agent may use (*allowed tools*).

## Step 3 — Authenticate via a project connection

If the server is protected, attach a **project connection** that holds the credential (API key or OAuth). Configure it once here — never hard-code secrets in the agent or client code. Public sample servers can be added without a connection.

> [!WARNING]
> **Private endpoints** — If your MCP server is on a private network, ensure the project's networking (VNet / private endpoint) can reach it, otherwise the tool call will time out.

## Step 4 — Set the approval policy

Choose how tool calls are approved. For a first test set `require_approval: always` so you can see and approve each call; switch to `never` for trusted, unattended tools.

## Step 5 — Test the tool from the playground

Ask a question that forces the agent to use the MCP tool. In the run detail you will see: the model deciding to call the tool → (if approval is on) an approval prompt → the tool result returning → the final answer grounded in that result.

> ✅ **Checkpoint** — You can see a tool invocation to your MCP server and a result flowing back into the answer. The agent used the tool rather than guessing.

## Step 6 — The same tool from code (optional)

The MCP tool can also be declared when you call the agent from code (see [Lab 3](lab-3-call-via-responses-api.md)). Representative shape of the tool declaration:

```python
tools = [{
    "type": "mcp",
    "server_label": "contoso-tools",
    "server_url": "https://<your-mcp-server>/sse",
    "require_approval": "never"
}]
# pass tools=tools to the Responses API call (Lab 3)
```

---

## Try it yourself (extension)

- Connect a `Foundry Toolbox` as the MCP endpoint and expose several curated tools behind one URL.
- Restrict *allowed tools* to a subset and confirm the others are not callable.
- Flip approval from `always` to `never` and observe the difference in the run.

## Troubleshooting

| Symptom | Likely cause & fix |
|---------|--------------------|
| Tool never gets called | The question didn't require the tool, or the instruction didn't encourage tool use — ask something only the tool can answer. |
| 401 / 403 from the server | Missing or wrong project connection — re-check the credential in Step 3. |
| Call times out | Server unreachable (private network) or wrong URL — verify connectivity and the endpoint path (often ends in `/sse`). |
| Stuck on approval | `require_approval` is set to `always` — approve the call, or set it to `never` for trusted tools. |

## What you learned

You extended the agent with an external capability over an open protocol, authenticated centrally through a connection, and controlled execution with approvals — all behind a single **Toolbox** MCP endpoint. In **Lab 3** you call this agent from your own code.

---

[← Lab 1](lab-1-create-a-prompt-agent.md) · [Session index](../README.md) · **Next:** [Lab 3 — Call via the Responses API →](lab-3-call-via-responses-api.md)
