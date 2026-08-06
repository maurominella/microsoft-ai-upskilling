# Session 1 — Microsoft AI Platform

> Vision, architecture and hands-on with **Microsoft Foundry**: from one agent, to a grounded agent, to a governed fleet.

[← All sessions](../README.md) · **Status:** ✅ Complete

An 8-hour session delivered over **two 4-hour days**:

- **Day 1 — Vision & Architecture** (for leadership + technical): principles, architecture and live demos. → see [Slides](#slides).
- **Day 2 — Hands-on** (for technical roles): four step-by-step labs. → see [Labs](#labs).

**Audience:** Cloud Solution Architects, developers, data scientists, and platform/architecture leads · **Format:** instructor-led, with follow-along on your own machine.

> [!TIP]
> **New here? Start with [Environment Preparation](../environment_preparation.md)** (at the repo root) to get your machine and Azure access ready (~30–45 min, done once, reused by every session).

---

## Slides

Day-1 deck (English slides, detailed speaker notes). Export your final version to PDF and place it in [`slides/`](slides/) as `Foundry-Agent-Service-Day1.pdf`.

---

## The learning arc

The Day-2 labs build on one another and map onto the platform's planes — **build → extend → integrate → publish**:

| Plane | Idea | Lab |
|-------|------|-----|
| **BUILD** | Create one agent | Lab 1 |
| **BUILD** | Extend it with tools | Lab 2 |
| **BUILD** | Call it from your code | Lab 3 |
| **GOVERN** | Publish & govern the fleet | Lab 4 |

> One agent → a tool-using agent → an agent your apps can call → a published, governed agent.

---

## Labs

| # | Lab | What you build | Time | Level |
|---|-----|----------------|------|-------|
| 1 | [Create a prompt-based agent](labs/lab-1-create-a-prompt-agent.md) | A named agent with instructions + a built-in tool, tested in the playground | 45–60 min | Foundational |
| 2 | [Add an MCP tool](labs/lab-2-add-an-mcp-tool.md) | An agent connected to a remote MCP server, with approval control | 45–60 min | Intermediate |
| 3 | [Call via the Responses API](labs/lab-3-call-via-responses-api.md) | A script that invokes the agent from code and streams the result | 45–60 min | Intermediate |
| 4 | [Publish to Agent 365 (without OBO)](labs/lab-4-publish-to-agent365-no-obo.md) | A published, governed agent invoked with its own identity (app-only) | 45–60 min | Advanced |

---

## Setup & prerequisites

> [!IMPORTANT]
> **Set up your environment first.** Complete the one-time **[Environment Preparation](../environment_preparation.md)** guide (repo root) before Lab 1, and install the Python dependencies in **[`requirements.txt`](requirements.txt)** (this folder).

Short version:

- An **Azure subscription** and access to the **Microsoft Foundry** portal (`ai.azure.com`).
- A Foundry **project** with at least one **model deployed** (a chat/reasoning model).
- Role **Azure AI User** (or higher) on the project.
- For the code labs (3 & 4): **Python 3.10+** with `uv`.
- For Lab 4: appropriate **Agent 365 / Entra Agent ID** licensing and roles (see that lab).

---

## Folder contents

```text
01-microsoft-ai-platform/
├── README.md                              ← you are here
├── requirements.txt                       ← Python dependencies (installed with uv)
├── slides/                                ← your Day-1 deck PDF is here
└── labs/
    ├── lab-1-create-a-prompt-agent.md
    ├── lab-2-add-an-mcp-tool.md
    ├── lab-3-call-via-responses-api.md
    └── lab-4-publish-to-agent365-no-obo.md
```

---

## How to use

> [!NOTE]
> The instructor performs each step live; follow along on your own machine at your own pace. Replace every `<angle-bracket placeholder>` with your own value.

> [!IMPORTANT]
> Code snippets are **representative**. Where a step says *"copy from the portal"*, prefer the exact snippet Foundry generates for **your** resource. Some of these technologies are in **preview/Beta** and change over time — the authoritative, maintained samples live in the official Microsoft repository: **https://github.com/microsoft-foundry/foundry-samples/**
