# Facilitator Guide — Foundry IQ / Zava Demo

Companion to [`README.md`](./README.md). This is **your** script, timing, and talking track for running the lab live. Students follow the README; you narrate the *why* from here.

---

## Objectives (say these out loud at the start)

By the end, each student can:
1. Explain **what Foundry IQ is** and why grounding belongs in a reusable layer, not baked into each agent.
2. **Build a retrieval agent** in Azure AI Search (knowledge source → knowledge agent) over their own documents.
3. **Attach that retrieval agent to an agent as a Foundry IQ MCP tool** and get grounded, cited answers.
4. Recognize **agentic retrieval** (plan → sub‑queries → rank → synthesize) vs a plain search box.

---

## Suggested timing (~70 min)

| Min | Segment | Your focus |
|----:|---------|-----------|
| 0–8 | **Story** (README §1) | Sell the problem, not the tech. Land the "colleague who read every manual" line. |
| 8–15 | **The data** (§2) | Open the 4 folders. Plant the P4311 / CTL11 thread. |
| 15–20 | **Prereqs** (§3) | Point at the *given* assets; keep it short. |
| 20–40 | **Build the retrieval agent** (§4) | The core. Do 4a → 4b → 4c live. **Show the `activity` + `references`** on the `/retrieve` call — this is the money shot. |
| 40–48 | **Foundry IQ + MCP endpoint** (§5) | Explain MCP as "USB‑C for tools." Copy the endpoint. |
| 48–58 | **Attach as MCP tool** (§6) | Wire the agent; read the instructions aloud. |
| 58–68 | **Run the demo** (§7) | Q1 first, then 1–2 more. Open the tool‑call view every time. |
| 68–70 | **Debrief** (§8) | Map back to the four IQs. Close on the one‑liner. |

---

## The story narration (a script you can read almost verbatim)

> "Forget the architecture for a second. Picture a Zava technician on a factory floor. A machine is throwing a red light. She has a tablet. Somewhere across nine manuals, eleven policies, and a bug list is the answer to a simple question: *do I move it, swap a part, or open a ticket?*
>
> If she guesses wrong, it's a wasted truck‑roll, or a voided warranty, or a line down for no reason. If she reads everything, it's twenty minutes she doesn't have.
>
> We're going to give her a colleague — one that has read every manual and every policy, answers in five seconds, and **shows its sources** so she stays in charge. The thing that makes that colleague trustworthy is **Foundry IQ**. Let me show you how we build it."

Then jump straight to §2 and open the folders.

---

## The "wow" beat — don't skip it

When you run **Q1** (P4311 / CTL11 / "should I move it?"):

1. Let the answer land: **"No — don't move it."**
2. **Then open the activity / tool‑call panel.** Point at the **sub‑queries** the retrieval agent generated. Say: *"I asked one question. It asked itself three."*
3. Point at the **citations** — a manual **and** a policy. Say: *"It didn't just find the red‑light meaning. It found the rule that says she's not allowed to move it. Two different documents, fused into one safe answer."*

That single moment is the whole value proposition. Everything else is plumbing.

---

## Concepts students confuse (be ready)

- **"Isn't this just RAG?"** — It's agentic retrieval: the retrieval step *plans and decomposes*. Show the `activity` to prove it. Classic RAG sends one query; this sends several and ranks across them.
- **"Why MCP instead of just calling the index?"** — Because you build the knowledge **once** and every agent (and non‑Microsoft clients) reuse it through one endpoint, with governance. Decoupling is the point.
- **"Where does the vectorizing happen?"** — Integrated vectorization inside Azure AI Search at index time *and* query time, using the embedding deployment. Students don't hand‑embed anything.
- **"Foundry IQ vs the retrieval agent?"** — The retrieval agent (in Azure AI Search) is the engine; Foundry IQ is the layer that governs it and exposes it (incl. the MCP endpoint) to agents.

---

## Common failure points during the live build

| If this happens… | Do this |
|------------------|---------|
| Knowledge source shows 0 docs | Search managed identity is missing **Storage Blob Data Reader** — grant it, re‑run. |
| `/retrieve` returns answer but no citations | Turn on `includeReferences` in the agent's `knowledgeSources` block. |
| Agent answers without calling the tool | The instructions are too soft. Emphasize **"you MUST call `foundry_iq_zava`"** and confirm the tool is attached. |
| Demo pauses asking to approve the tool | Set MCP tool approval mode to **never**. |
| Q4 (visual) ignores the diagram | You skipped the `chatCompletionModel` (image verbalization) in Step 4a. |

> 🛟 **Safety net:** have the **`/retrieve` REST call from Step 4c pre‑run** in a saved response. If the agent/MCP wiring misbehaves live, you can still show the grounded answer + citations from the retrieval agent itself and narrate the rest.

---

## Map back to the four IQs (your closing slide talk)

> "We grounded on documents Zava owns — that's **Foundry IQ**. Notice the *shape* of what we did: point a knowledge source at data, wrap it in a retrieval agent, expose it over MCP, attach it to the agent. Now swap the knowledge source: a **website** → that's **Web IQ**. **M365** mail and files → **Work IQ**. A **Fabric** semantic model → **Fabric IQ**. Same pattern, four kinds of knowledge. Today you learned the pattern once."

**Close on:** *"We didn't teach the model about Zava. We gave the agent a way to look Zava up — and to show its work."*

---

## Pre‑flight checklist (the night before)

- [ ] Foundry project `zava-foundry` reachable; `gpt-4.1`, `gpt-4.1-mini`, `text-embedding-3-large` deployed.
- [ ] Azure AI Search `zava-search` up; **semantic ranker** enabled; managed identity has blob + AOAI roles.
- [ ] The four folders staged in blob container `zava-knowledge`.
- [ ] Knowledge source + knowledge agent pre‑built in a **backup** project (in case live build runs long).
- [ ] Q1 `/retrieve` response saved as a fallback.
- [ ] MCP endpoint URL copied and tested once.
