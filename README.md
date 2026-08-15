# Microsoft AI Upskilling

## Workshop scenario: AdvertSphere Broadcasting (***ASB***)

<p align="center">
    <img src="./_IMAGES/AdvertSphere Broadcasting.jpg" alt="AdvertSphere Broadcasting" width="720">
</p>

> [!NOTE]
> **AdvertSphere Broadcasting (in short: ***ASB***) is a fictional company created exclusively for this workshop.** It is used consistently throughout the examples, exercises, simulations, and presentation materials to provide a realistic and coherent business context.

AdvertSphere Broadcasting is the advertising concessionaire of the fictional AdvertSphere Group. It manages commercial inventory across the group’s television, radio, streaming, digital, and social channels, providing advertisers with unified access to its total video and total audio media portfolio.

As the commercial gateway to the AdvertSphere media ecosystem, the company coordinates advertising formats and strategy across linear and digital environments, drives sales and commercial innovation, and supports selected third-party publishers through radio and digital partnerships. Editorial responsibility remains with AdvertSphere Media, while advertising strategy, sales, and commercial innovation are centralized within AdvertSphere Broadcasting.

---

## Workshop overview

A hands-on training programme on **Microsoft Foundry** and the Microsoft AI platform, delivered as **three onsite sessions** of **8 hours each** (every session split into **two 4-hour days**: Day 1 vision & architecture, Day 2 hands-on labs).

This repository collects, for each session, the **slides** (PDF), the **hands-on exercises**, and a shared **lab environment setup**.

---

## Sessions

| # | Session | Focus | Status |
|---|---------|-------|--------|
| 1 | [Microsoft AI Platform](01-microsoft-ai-platform/) | Foundry vision & architecture, agents, grounding, governance | ✅ **Complete** |
| 2 | [AI Evaluation](./02-microsoft-evaluation-platform/) | Evaluation, custom evaluators, synthetic data, red teaming | 🚧 Work in progress |
| 3 | [AI Innovations & Recent Announcements](./03-microsoft-agentic-frameworks/) | Agent Framework, MCP, A2A, Agent 365 governance | ✅ **Complete** |

### 1 · Microsoft AI Platform  ✅
*Mix of overview, architecture, demos and specific use cases.*
- AI Foundry Vision and Architecture · AI Services in AI Foundry · AI Agent Service
- **Audience:** IT / Cloud Architect · Data Platform / AI Platform Owner · IT Governance / IT Strategy · Innovation Manager / Digital Transformation · business application leads (high-level)

### 2 · Development-phase supervision  🚧
*Mix of overview, architecture, demos and specific use cases.*
- Key concepts and tools in AI Foundry · Manual vs cloud evaluation · Synthetic & simulated automatic data generation · Custom evaluators · Red-teaming attacks in action
- **Audience:** AI / ML Engineers · Software Developers (backend / integration) · Data Engineers · AI Solution Architects · Application Quality / Testing leads · Security Engineering (red teaming)

### 3 · AI Innovations & Recent Announcements  ✅
*Mix of overview, architecture, demos and specific use cases.*
- From Microsoft Semantic Kernel to Agent Framework · Model Context Protocol (MCP) · A2A (Agent-to-Agent) Protocol · Agent 365 for agents governance
- **Audience:** AI / Solution Engineers · Software Developers (backend / integration) · IT Architecture · AI Solution Architects · IT Governance / IT Strategy

---

## Repository structure

```text
microsoft-ai-upskilling/
├── README.md                              ← you are here
├── environment_preparation.md             ← shared, one-time lab setup (do this first)
├── .env.example                           ← template for the real .env file
├── .gitignore
├── 01-microsoft-ai-platform/              ← Session 1
│   ├── README.md
│   ├── requirements.txt
│   ├── slides/   (Day-1 deck PDF is here)
│   └── labs/     → lab-1 … lab-4
├── 02-development-supervision/            ← Session 2
│   ├── README.md
│   ├── requirements.txt
│   ├── slides/   (Day-1 deck PDF is here)
│   └── labs/     → lab-1 … lab-4
└── 03-ai-innovations/                     ← Session 3
    ├── README.md
    ├── requirements.txt
    ├── slides/   (Day-1 deck PDF is here)
    └── labs/     → lab-1 … lab-4
```

Each session folder is self-describing; the two upcoming sessions will follow the same layout (`slides/` + `labs/`).

---

## Getting started

1. Complete the shared **[Environment Preparation](environment_preparation.md)** once (Azure access + tooling + Python via `uv`).
2. Open the session you're attending — start with **[Session 1 — Microsoft AI Platform](01-microsoft-ai-platform/)**.

---

## How to synch the folder "02-microsoft-evaluation-platform"
This folder mirrors the repo https://github.com/maurominella/genai_evaluation.
- The following command has to be run just the first time we need to add the external repo into the local folder:
```bash
git subtree add --prefix=02-microsoft-evaluation-platform \
https://github.com/maurominella/genai_evaluation.git main --squash

```

- The following command updates that folder when the source is updated:
```bash
git subtree pull --prefix=02-microsoft-evaluation-platform \
https://github.com/maurominella/genai_evaluation.git main --squash
```

- After that, the next commands add, commit and push the Microsoft AI Upskilling repo:
```bash
git add .
git commit -m "Initial subtree import of genai_evaluation"
git push 
```
---

## License & disclaimer

Released under the [MIT License](LICENSE) — you are free to use, copy, modify and redistribute this material, with attribution. It is provided **"as is", without warranty or support**.

> [!IMPORTANT]
> **Please read the full [Disclaimer](disclaimer.md) before using these materials.** In brief: this is a **personal, unofficial** repository (**not** an official Microsoft product); it is a **work in progress**; it is provided for **learning only** and is **not a substitute for official Microsoft documentation**; and it is **not maintained over time** — some technologies are in **Preview** and change frequently, so no guarantees are given.
>
> The **authoritative, maintained** samples remain Microsoft's official repository: **https://github.com/microsoft-foundry/foundry-samples/**

---

*Prepared by Mauro Minella — Sr. Cloud Solution Architect -Cloud AI & Apps-, Microsoft.*