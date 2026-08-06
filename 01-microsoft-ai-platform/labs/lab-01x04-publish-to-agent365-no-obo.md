# Lab 4 — Publish to Agent 365 (without OBO)

> *Publish the agent, govern it, and invoke it with its own identity — not on behalf of a user.*

| | |
|---|---|
| **Audience** | developers, plus platform/identity admins |
| **Duration** | 45–60 minutes |
| **Level** | Advanced |
| **You will build** | A published, governed agent invoked with an app-only (agent) token via the client-credentials flow |
| **Plane** | GOVERN — Agent 365 + Entra Agent ID |

> [!NOTE]
> The instructor performs each step live; follow along on your own machine. Replace every `<angle-bracket placeholder>` with your own value.

---

## Prerequisites

- The agent from Labs [1](lab-1-create-a-prompt-agent.md)–[3](lab-3-call-via-responses-api.md) (with its agent ID).
- Appropriate licensing/enrolment for Agent 365 (e.g. Microsoft 365 Copilot / E7 / Frontier), and the ability to view the **Microsoft 365 admin center → Agents**.
- Entra roles as applicable: `Agent ID Developer/Administrator` and `Agent Registry Administrator`.
- For the code step: the agent's app (client) ID and a client secret or certificate, plus your tenant ID.

## Learning objectives

- Publish a Foundry agent and confirm it **auto-registers** in the Agent 365 registry.
- Read the agent's **Entra Agent ID** (blueprint → instance → agent user).
- Understand **OBO vs app-only**, and invoke the agent with its own identity — **without OBO**.
- See the governance controls Agent 365 applies (visibility, block/quarantine, policy).

---

## Step 1 — Publish the agent

From the agent in Foundry, choose **Publish** and target **Microsoft Teams** and/or **Microsoft 365 Copilot**. Confirm. In a real tenant the agent becomes available to authorised users in those surfaces.

## Step 2 — Verify in the Agent 365 registry

Open the **Microsoft 365 admin center → Agents**. Your agent appears in the registry automatically, because agents built in Foundry are integrated with the registry — no separate registration step. Inspect its owner, source (Foundry) and its Entra Agent ID.

> [!NOTE]
> **Registry vs identity** — Agent 365 (in the M365 admin center) is where you *discover, monitor and govern* agents across the tenant. Microsoft Entra Agent ID is where the agent's *identity, permissions and security controls* live. Same agent, two lenses.

## Step 3 — Read the agent's identity

An Agent 365 identity has three parts, worth recognising before you authenticate as the agent:

- **Blueprint** — the app template: Entra app registration, required Graph permissions, auth config.
- **Instance** — a specific deployment with its own agent ID and service principal.
- **Agent user** — the runtime identity that appears in your organisation (can hold a mailbox, appear in the org chart).

## Step 4 — OBO vs. app-only (the key distinction)

> [!IMPORTANT]
> **Why "without OBO"** — *On-Behalf-Of* (OBO) means the agent acts as a signed-in user, carrying that user's delegated permissions. *App-only* (client-credentials) means the agent acts as **itself** — its own identity, its own permissions, with **no user** in the loop. This lab uses app-only: ideal for autonomous/back-end scenarios where there is no interactive user.

Contrast at a glance:

- **OBO (not used here):** token acquired with a *user assertion*; scopes are the user's *delegated* permissions.
- **App-only (this lab):** token acquired with *client credentials*; scope is the target resource's `.default` — the agent's own permissions.

## Step 5 — Acquire an app-only token and call the agent

Representative Python (MSAL) that authenticates as the agent — no user — and calls the agent's endpoint:

```python
import msal, requests

TENANT   = "<tenant-id>"
CLIENT   = "<agent-app-client-id>"          # the agent's own app identity
SECRET   = "<agent-client-secret-or-cert>"
RESOURCE = "<agent-endpoint-or-api>"        # the resource you are calling

app = msal.ConfidentialClientApplication(
    client_id=CLIENT,
    authority=f"https://login.microsoftonline.com/{TENANT}",
    client_credential=SECRET,
)
# client-credentials flow => app-only token, NO user (this is the 'no OBO' part)
token = app.acquire_token_for_client(scopes=[f"{RESOURCE}/.default"])

r = requests.post(
    "<agent-invoke-endpoint>",
    headers={"Authorization": f"Bearer {token['access_token']}"},
    json={"input": "Ciao dal flusso app-only."},
)
print(r.status_code, r.text)
```

> ✅ **Checkpoint** — The token is issued with **no interactive user**, and the agent responds. You have invoked it as itself — the app-only / no-OBO path.

> [!WARNING]
> **For comparison only** — The OBO path would instead call `app.acquire_token_on_behalf_of(user_assertion=<user-token>, scopes=[...])` — note the required user token. This lab deliberately avoids that.

## Step 6 — Apply governance

Back in the Agent 365 admin experience, explore the controls now available for this agent:

- **Visibility** — who in the tenant can discover and use it.
- **Block / quarantine** — stop it from being used or from reaching resources.
- **Policy & Conditional Access** — apply risk-based access to its identity (Entra).

---

## Try it yourself (extension)

- Assign the agent to a **Custom** collection so only one group can discover it, then verify visibility changed.
- Apply a **Conditional Access** policy targeting the agent identity and observe enforcement.
- Compare the app-only call above with an OBO call and inspect the difference in the token claims.

## Troubleshooting

| Symptom | Likely cause & fix |
|---------|--------------------|
| Agent not in the registry | Publishing didn't complete, or you lack registry visibility — re-check Step 1 and your Entra role. |
| `AADSTS700016` / invalid client | Wrong client ID or secret/cert — verify the agent's app registration values. |
| Token has no permissions | The app identity lacks the resource role — grant the app-only permission (admin consent) for the target resource. |
| 403 calling the agent | Governance blocked it, or least-privilege denies the resource — check visibility/quarantine and role assignments. |

## What you learned

You closed the full lifecycle: an agent **built** in Foundry (Lab 1), **extended** (Lab 2), **called** from code (Lab 3), and now **published**, governed in Agent 365, and invoked with its own identity via the client-credentials flow — **without OBO**. Build → Ground → Govern, end to end.

---

[← Lab 3](lab-3-call-via-responses-api.md) · [Session index](../README.md)
