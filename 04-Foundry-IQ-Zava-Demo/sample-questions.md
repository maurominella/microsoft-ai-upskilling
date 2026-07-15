# Sample Questions — Zava Field‑Support Agent

Grounded test prompts for **Step 7** of the lab. Each one is answerable **only** from the Zava corpus, and each shows a different Foundry IQ strength. Expected answers are written from the actual source documents so you can verify the agent is truly grounded (and not improvising).

> **How to run:** paste into the agent playground in order. After each answer, open the **tool‑call / activity** panel and show the retrieved **sub‑queries** and **cited chunks** — that's the proof it's Foundry IQ, not the base model.

---

## Q1 — The star: multi‑document + a policy "stop" ⭐

**Ask:**
> *"A P4311 edge node keeps showing an intermittent red CTL11 light. Should I move it to a better spot in the plant?"*

**Good answer contains:**
- **No — do not relocate the unit yet.**
- On **firmware 1.12**, an intermittent red **CTL11** (8–20 s, packet loss < 0.1%) is a **known false positive** → classification **`anomaly‑ctl11‑fw112`**.
- First: run **`fw show version`** and **`diag ctl11 snapshot`**; **monitor 24 h**; do **not** move the unit during initial monitoring.
- Zava's **On‑Site Equipment Movement Policy** lists "moving equipment to resolve intermittent CTL11 Red" as a **prohibited** action (it masks the link‑timing anomaly and invalidates the baseline).

**Draws on:** `manuals/IOT Edge Control Node.md` (indicator + firmware anomaly) **+** `policy/11_Edge_Equipement_Guidelines.md` (Network Stability triage + On‑Site Movement Policy) **+** `softwareissues/zava_software_issues.json` (known issue).

**Why it lands:** three folders, one question, and the *right* answer is to **not act** — a naïve keyword search over just the manual would miss the policy prohibition.

---

## Q2 — A crisp policy threshold (repair vs replace)

**Ask:**
> *"The graphene vapor reclaim tank's filter efficiency dropped to 82%. Do I repair or replace it?"*

**Good answer contains:**
- **Replace** the **Graphene Filter Membrane (Part #GVT‑FM07)**.
- Policy rule: replace when filtration efficiency drops **below 85%** (per **ASTM D3862**) — 82% is below threshold.
- Log the decision in the **Maintenance Management System (MMS)** with justification and technician signature.

**Draws on:** `policy/2_Repair_vs_Replace_Guidelines.md` (**+** `manuals/Graphene Vapor Reclaim Tank.md` for context).

**Why it lands:** the agent applies a **numeric threshold from a policy** and returns the exact part number — precision a summary‑style RAG usually blurs.

---

## Q3 — A numeric decision with an authorization boundary (power adapter)

**Ask:**
> *"A P4311's power adapter reads 21.8 V under load and the PWR LED is off. What do I do, and am I allowed to swap it?"*

**Good answer contains:**
- This is **undervoltage** (symptom code **PAD‑UV**): measured output **< 22.5 V** under load with PWR off → **replacement is authorized**.
- A **Field Technician may provisionally approve** the swap for a **single unit** if the part is in local stock (Regional Support Lead needed for >3 units or a site‑wide pattern).
- Procedure: graceful shutdown → disconnect AC, wait 10 s → install a matching **24 V** approved adapter (e.g. **AD‑60W‑24**) → verify **24.0 V ±5%** → confirm PWR LED solid green → log the batch/lot code.

**Draws on:** `policy/11_Edge_Equipement_Guidelines.md` (Power Adapter & Cord Replacement Policy) **+** `manuals/IOT Edge Control Node.md` (adapter spec AD‑60W‑24).

**Why it lands:** the answer respects an **authorization matrix**, not just a technical fix — exactly the "policy‑aware" behavior that makes an agent safe to deploy.

---

## Q4 — Multimodal grounding (uses the `manualsvisuals` folder)

**Ask:**
> *"What does the digital printing & lacing stand look like, and how do I load the substrate?"*

**Good answer contains:**
- A short visual description derived from the **verbalized image** `printinglacingstand.png`.
- The load/setup steps from the corresponding manual.

**Draws on:** `manualsvisuals/OQTR_Digital_Printing_and_Lacing_Stand.md` + `manualsvisuals/printinglacingstand.png` (image verbalization).

**Why it lands:** shows Foundry IQ grounding on **diagrams**, not just text — a differentiator when configured with an image‑verbalization model.

---

## Q5 — Grounding guardrail (should politely refuse)

**Ask:**
> *"What's Zava's paternity‑leave policy?"*

**Good answer contains:**
- **"I don't have that information in the Zava knowledge base."** No invented HR policy.

**Draws on:** *nothing* — there is no HR content in the corpus.

**Why it lands:** proves the agent answers from **retrieved Zava knowledge**, not the base model's world knowledge. This is the trust test executives always ask about.

---

## Q6 — Precision recall across near‑duplicates (bonus)

**Ask:**
> *"What's the difference between the P4311 and the P4324 edge control nodes?"*

**Good answer contains:**
- **P4311**: 1 Ethernet port, ~4.5 W max USB output, **AD‑60W‑24** adapter (24 V / 2.5 A), lower thermal headroom.
- **P4324**: 2 Ethernet ports, ~7.5 W max USB output, **AD‑90W‑24** adapter (24 V / 3.75 A), redundant relay outputs.

**Draws on:** `manuals/IOT Edge Control Node.md` (comparison table).

**Why it lands:** the two models are described in the *same* document with very similar text — the agent has to retrieve the **right rows** and not conflate them.

---

### Quick coverage map

| Question | manuals | manualsvisuals | policy | softwareissues | Skill shown |
|----------|:------:|:-------------:|:------:|:--------------:|-------------|
| Q1 CTL11 move? | ✅ | | ✅ | ✅ | Multi‑doc + policy "stop" |
| Q2 filter 82% | ✅ | | ✅ | | Numeric policy threshold |
| Q3 adapter 21.8 V | ✅ | | ✅ | | Authorization boundary |
| Q4 lacing stand | | ✅ | | | Multimodal grounding |
| Q5 paternity leave | | | | | Honest refusal |
| Q6 P4311 vs P4324 | ✅ | | | | Precise recall |
