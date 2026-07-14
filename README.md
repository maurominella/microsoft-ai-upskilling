# Microsoft AI Upskilling

A hands-on training programme on **Microsoft Foundry** and the Microsoft AI platform, delivered as **three onsite sessions** of **8 hours each** (every session split into **two 4-hour days**: Day 1 vision & architecture, Day 2 hands-on labs).

This repository collects, for each session, the **slides** (PDF), the **hands-on exercises**, and a shared **lab environment setup**.

---

## Sessions

| # | Session | Focus | Status |
|---|---------|-------|--------|
| 1 | [**Microsoft AI Platform**](01-microsoft-ai-platform/) | Foundry vision & architecture, agents, grounding, governance | ✅ **Complete** |
| 2 | [Development-phase supervision](02-development-supervision/) | Evaluation, custom evaluators, synthetic data, red teaming | 🚧 Coming soon |
| 3 | [AI Innovations & Recent Announcements](03-ai-innovations/) | Agent Framework, MCP, A2A, Agent 365 governance | 🚧 Coming soon |

### 1 · Microsoft AI Platform  ✅
*Mix of overview, architecture, demos and specific use cases.*
- AI Foundry Vision and Architecture · AI Services in AI Foundry · AI Agent Service
- **Audience:** IT / Cloud Architect · Data Platform / AI Platform Owner · IT Governance / IT Strategy · Innovation Manager / Digital Transformation · business application leads (high-level)

### 2 · Development-phase supervision  🚧
*Mix of overview, architecture, demos and specific use cases.*
- Key concepts and tools in AI Foundry · Manual vs cloud evaluation · Synthetic & simulated automatic data generation · Custom evaluators · Red-teaming attacks in action
- **Audience:** AI / ML Engineers · Software Developers (backend / integration) · Data Engineers · AI Solution Architects · Application Quality / Testing leads · Security Engineering (red teaming)

### 3 · AI Innovations & Recent Announcements  🚧
*Mix of overview, architecture, demos and specific use cases.*
- From Microsoft Semantic Kernel to Agent Framework · Model Context Protocol (MCP) · A2A (Agent-to-Agent) Protocol · Agent 365 for agents governance
- **Audience:** AI / Solution Engineers · Software Developers (backend / integration) · IT Architecture · AI Solution Architects · IT Governance / IT Strategy

---

## Repository structure

```text
microsoft-ai-upskilling/
├── README.md                              ← you are here
├── environment_preparation.md             ← shared, one-time lab setup (do this first)
├── .gitignore
├── 01-microsoft-ai-platform/              ← Session 1 (complete)
│   ├── README.md
│   ├── requirements.txt
│   ├── slides/   (add your Day-1 deck PDF here)
│   └── labs/     → lab-1 … lab-4
├── 02-development-supervision/            ← Session 2 (placeholder)
│   └── README.md
└── 03-ai-innovations/                     ← Session 3 (placeholder)
    └── README.md
```

Each session folder is self-describing; the two upcoming sessions will follow the same layout (`slides/` + `labs/`).

---

## Getting started

1. Complete the shared **[Environment Preparation](environment_preparation.md)** once (Azure access + tooling + Python via `uv`).
2. Open the session you're attending — start with **[Session 1 — Microsoft AI Platform](01-microsoft-ai-platform/)**.

---

## License & disclaimer

Released under the [MIT License](LICENSE) — you are free to use, copy, modify and redistribute this material, with attribution.

> [!IMPORTANT]
> This material is provided **"as is", without warranty and without support**. It is intended for **learning and comprehension** and is **not officially maintained over time**. Some of the technologies covered are in **preview/Beta** and change frequently, so **no guarantees** are given that the samples keep working as-is. The MIT License above disclaims warranty and liability accordingly.
>
> The **authoritative, maintained** repository of samples remains Microsoft's official one: **https://github.com/microsoft-foundry/foundry-samples/**

> [!NOTE]
> This is a **personal, unofficial** repository prepared for a specific training engagement. It is **not an official Microsoft product** and does not represent Microsoft.

---

*Prepared by Mauro Minella — Senior Cloud Solution Architect, Microsoft.*
