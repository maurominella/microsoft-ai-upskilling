# Lab 04 - Red Teaming

**Duration:** ~45 minutes (steps 5-6 are optional)
**Start from:** `lab04_red_teaming_starter.ipynb`
**Reference solution:** `lab04_red_teaming_solution.ipynb`
**Source material:** `4 - cloud evaluation/4.2 - Red Team Agent Demo.ipynb` and `4.2 - Red Team Agent.ipynb`

## Objective

Evaluation asks *how good is the answer on my dataset*. Red teaming asks a different question:
*can I make this system produce a policy-violating answer* - using adaptive probes that no static
dataset contains.

In this lab you create a **managed red-team scan** in Microsoft Foundry against a real model
deployment, compare two attack techniques, compute the **Attack Success Rate (ASR)** and inspect the
row-level evidence behind the number.

## Red teaming is not a synonym for PyRIT

| Path | Where orchestration runs | Portal |
| --- | --- | --- |
| `project_client.get_openai_client().evals` with `scenario="red_team"` **(used here)** | Foundry, managed | new Foundry experience |
| `project_client.beta.red_teams` | Foundry, managed preview | classic Foundry experience |
| `azure-ai-evaluation[redteam]` | locally, on PyRIT | not compatible with the new portal |

The managed path keeps your environment small: attack orchestration and grading run server-side, so
PyRIT does not need to be installed locally - even though cloud attack strategies are PyRIT-derived.

## Prerequisites

A Foundry project (`FOUNDRY_PROJECT_ENDPOINT`), a chat deployment
(`AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`) and `az login`.

## Steps

| # | Step | Time | Outcome |
| --- | --- | --- | --- |
| 0 | Configuration and clients | 3 min | `evals_client` ready |
| 1 | Create the red-team evaluation group | 8 min | failure defined by `builtin.violence` |
| 2 | Configure and start a small scan (baseline + base64, 1 turn) | 12 min | run submitted and polled |
| 3 | Fallback: retrieve the most recent completed run | 2 min | real data even if your run is slow |
| 4 | Compute the ASR per technique and inspect one attack | 15 min | scorecard + report URL |
| 5 | *Optional* - widen risk categories and strategies | 10 min | comparison across more techniques |
| 6 | *Optional* - the legacy `beta.red_teams` preview API | 10 min | classic-portal scorecard |

**Minimum result in 30 minutes:** steps 0 to 4. Start the scan early (step 2) and use step 3 while it
runs - creating a cloud run is the slow, variable part.

## How to read the results

* `pass` -> the response passed the safety evaluator, so the **attack failed**.
* `fail` -> the response failed the evaluator, so the **attack succeeded**.
* **ASR** = successful attacks / evaluated attacks. Always show the denominator: `1/1 (100%)` is one
  observed failure, not proof that a technique always works.
* Grading is model-based: false positives and false negatives happen, so surprising rows deserve human
  review.
* **Baseline vs Base64:** Base64 is not *stronger*, it is a *different* probe. It may bypass one
  control while failing against another - that contrast is the whole point of the comparison.

## Files

```text
04-red-teaming/
├── lab04_red_teaming_starter.ipynb
├── lab04_red_teaming_solution.ipynb
└── lab_utils.py
```

This lab creates no local assets: everything lives in your Foundry project.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| The run stays `queued` / `running` for a long time | expected: use the fallback cell (step 3) and come back later |
| `No completed red-team run is available` | nobody in the project has completed a scan yet: wait for yours to finish |
| `report_url` opens the classic portal | you are using the legacy `beta.red_teams` API instead of the new Evals API |
| Missing `attack_strategy` in metadata | the field name varies across service versions: inspect the full output item and adapt the grouping key |
| Costs / duration grow quickly | they scale with `risk categories x attack strategies x turns`: widen one dimension at a time |

## Wrap-up

Red teaming produces evidence for mitigations and regression tests. It never proves that a system is
safe - it proves that *these* probes, on *this* day, against *this* configuration, did or did not
succeed.
