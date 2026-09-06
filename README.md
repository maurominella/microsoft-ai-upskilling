# Microsoft AI Upskilling

**Build, evaluate, and govern production-grade AI agents on Microsoft Foundry — a hands-on, three-session program with runnable code, not just slides.**

<p align="center">
  <img src="./AdvertSphere Broadcasting.jpg" alt="AdvertSphere Broadcasting" width="640">
</p>

Everything is taught against **one coherent business scenario** — *AdvertSphere Broadcasting (ASB)*, a fictional advertising concessionaire spanning TV, radio, streaming, digital, and social. Every demo, lab, and evaluation builds on the same realistic context, so you're solving a real-shaped problem instead of disconnected toy examples.

---

## What you'll take home

Not a deck you skim once — a **working mental model** of the Microsoft agent platform, plus **twelve hands-on labs (four per session)** and reference code you can run, adapt, and bring back to your own projects.

**If you build AI** — developers, Cloud Solution Architects, data scientists — you'll leave able to:

- Stand up an agent on **Microsoft Foundry**, extend it with a real **MCP tool** (with approval control), and call it from your own code through the **Responses API**.
- **Evaluate it like you mean it** — AI-judge, groundedness, content-safety and **custom evaluators**, run both locally and as cloud jobs.
- **Pressure-test it before your users do** — synthetic & adversarial data generation, jailbreak and **red-teaming** simulations.
- Compose agents with the **Microsoft Agent Framework** and connect them over **open protocols (MCP, A2A)** instead of bespoke glue.

**If you own the platform** — architecture, governance, strategy — you'll leave with:

- A clear **build → ground → govern** map: how one agent becomes a grounded agent, then a *governed* fleet.
- How every agent gets a **first-class identity (Entra Agent ID)** and is published and governed with **Agent 365** — including invocation with an agent's **own app-only identity (no OBO)**.
- A defensible **evaluation & safety story** to put in front of risk, security, and compliance stakeholders.
- The vocabulary to tell **architecture from hype** when teams pitch "agentic" everything.

---

## The three sessions

Each session is **8 hours over two consecutive days** — Day 1 vision & architecture (leadership + technical), Day 2 hands-on labs (technical roles). **Four labs per session — twelve in total.**

| # | Session | What you'll master | Day-2 hands-on |
|---|---------|--------------------|----------------|
| 1 | [**Microsoft AI Platform**](01-microsoft-ai-platform/) | Foundry architecture; build, ground & govern agents; Agent 365 | Prompt agent → MCP tool → Responses API → publish to Agent 365 |
| 2 | [**GenAI Evaluation**](02-microsoft-evaluation-platform/) | Metrics, local & cloud evaluation, custom evaluators, red teaming | Local eval → dataset generation → cloud eval → red teaming |
| 3 | [**Agentic Frameworks**](03-microsoft-agentic-frameworks/) | Semantic Kernel → Agent Framework, MCP, A2A, fleet governance | Build & connect agents across open protocols |

---

## Start here

1. Complete the shared **[Environment Preparation](environment_preparation.md)** once — Azure access + tooling + Python via `uv` (~30–45 min, reused by every session).
2. Open the session you're attending — begin with **[Session 1 — Microsoft AI Platform](01-microsoft-ai-platform/)**.

📖 Full program details, repository layout and setup live in **[PROGRAM-GUIDE.md](PROGRAM-GUIDE.md)**.

---

> [!IMPORTANT]
> **Personal, unofficial** repository — **not** an official Microsoft product. A **work in progress** 🚧, provided **for learning only**, **not a substitute for official Microsoft documentation**, and **not maintained over time** (some features are in **Preview** and change frequently). Please read the full **[Disclaimer](disclaimer.md)**.
>
> The **authoritative, maintained** samples remain Microsoft's official repository: **https://github.com/microsoft-foundry/foundry-samples/**

Released under the [MIT License](LICENSE) — free to use, copy, modify and redistribute with attribution; provided **"as is", without warranty or support**.

*Prepared by Mauro Minella — Sr. Cloud Solution Architect (Cloud AI & Apps), Microsoft.*
