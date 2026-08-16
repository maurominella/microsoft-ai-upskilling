# Lab 02 - Dataset generation (Simulator and Adversarial Simulator)

**Duration:** ~45 minutes (step 7 is optional)
**Start from:** `lab02_dataset_generation_starter.ipynb`
**Reference solution:** `lab02_dataset_generation_solution.ipynb`
**Source material:** `3 - syntetic data generation/3.1`, `3.2`, `3.3`

## Objective

You cannot evaluate what you cannot measure, and you cannot measure without data. This lab solves the
cold-start problem: **generate the evaluation dataset before production traffic exists**.

Two halves:

1. **Non-adversarial** - `Simulator` drives a Prompty-based application through a grounded
   conversation built from your own documents.
2. **Adversarial** - `AdversarialSimulator` generates attacks against the application, and the optional
   step compares baseline requests, **direct** injections (UPIA) and **indirect** injections (XPIA).

The key idea to take home: **the simulator generates the attack, it does not protect the application**.
The callback is only a protocol adapter; the safety decision belongs to the application under test.
Here that application is a small *safety reviewer* Prompty that answers with
`Decision / Risk / Reason / Safe response`, so its behaviour is explicit and inspectable.

## Steps

| # | Step | Time | Outcome |
| --- | --- | --- | --- |
| 0 | Configuration | 3 min | ready-to-run cells |
| 1 | Write and smoke-test the Prompty application | 8 min | the application under test answers |
| 2 | Continue an existing conversation by hand | 7 min | you see what the simulator will automate |
| 3 | Implement the Simulator callback | 5 min | the chat protocol adapter |
| 4 | Generate a grounded conversation and save it as JSONL | 12 min | `generated_datasets/simulated_conversations.jsonl` |
| 5 | The adversarial target application | 5 min | the safety-reviewer Prompty |
| 6 | Run an adversarial simulation and persist it | 8 min | `safety_assessments/<timestamp>_<scenario>.json` |
| 7 | *Optional* - UPIA (`DirectAttackSimulator`) and XPIA (`IndirectAttackSimulator`) | 15 min | baseline vs jailbreak comparison |

**Minimum result in 30 minutes:** steps 0 to 4 give you a reusable synthetic dataset; steps 5-6 add the
adversarial baseline.

## Files

```text
02-dataset-generation/
├── lab02_dataset_generation_starter.ipynb
├── lab02_dataset_generation_solution.ipynb
├── lab_utils.py
└── assets/
    ├── documents_excerpt.txt                  <- grounding data (excerpt of data/documents.txt)
    ├── friendly_conversation_history_en.txt   <- sample conversation history (EN)
    ├── friendly_conversation_history_it.txt   <- sample conversation history (IT)
    ├── conversation_simulation.prompty        <- written by the notebook
    └── adversarial_simulation.prompty         <- written by the notebook
```

Generated output goes to `generated_datasets/` and `safety_assessments/` inside this folder.

## Concepts you should be able to explain afterwards

| Term | Meaning |
| --- | --- |
| **Jailbreak** | the attacker's *objective*: make the application operate outside its restrictions |
| **Prompt injection** | the *mechanism*: untrusted data interpreted as an instruction |
| **UPIA** | user prompt injected attack - the malicious instruction sits in the user message |
| **XPIA** | cross-domain prompt injected attack - it hides in retrieved/external content, while the visible request stays benign |
| **Blocked attempt** | the application detected/refused the attack: a *successful* test, not a compromise |

| Simulator | Where the attack lives | Purpose |
| --- | --- | --- |
| `AdversarialSimulator` | in the nature of the request | safety baseline |
| `DirectAttackSimulator` | in the user message (UPIA) | compare `regular` and `jailbreak` groups |
| `IndirectAttackSimulator` | in external content (XPIA) | verify retrieved content is treated as data |

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `TypeError: object str can't be used in 'await' expression` | `prompty 2.0.0b3` `invoke_async()` is incompatible with the Entra ID token provider: call the synchronous `prompty.invoke` through `asyncio.to_thread` |
| `Unexpected user-simulator response` | SDK 1.18.3 wraps the Prompty answer in `llm_output`: use the `CompatibleSimulator` subclass |
| The prompty file is not found | run the notebook from its own folder, so `assets/...` resolves |
| The adversarial simulation is very slow | lower `max_simulation_results`: each result is a full conversation |
| `FOUNDRY_PROJECT_ENDPOINT` errors | the adversarial simulators are service-backed and require a Foundry project |
