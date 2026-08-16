# Lab 01 - Local Evaluation

**Duration:** ~45 minutes (steps 5-7 are optional)
**Start from:** `lab01_local_evaluation_starter.ipynb`
**Reference solution:** `lab01_local_evaluation_solution.ipynb`
**Source material:** `2 - local evaluation/2.1`, `2.2`, `2.3`, `2.4`, `2.5`, `2.6`, `2.7A`, `2.7B`

## Objective

Learn to measure the quality of an AI application **on your own machine**, before any cloud
infrastructure is involved. By the end you will be able to answer three questions:

1. How do I score a single query/response pair with an AI judge, and how do I read the reasoning?
2. How do I score a **real agent conversation**, with tool calls, loaded from a dataset?
3. How do I run the same evaluators **in batch** over a dataset and persist a comparable report?

Local evaluation is the fastest feedback loop you have: it is where prompt changes, model changes and
regression checks get their first verdict.

## What you will use

| Evaluator | Type | What it measures |
| --- | --- | --- |
| `IntentResolutionEvaluator` | AI judge, 1-5 | did the answer actually resolve the user intent |
| `ToolCallAccuracyEvaluator` | AI judge, 0/1 per call | are the tool calls relevant and correctly parameterised |
| `TaskAdherenceEvaluator` | AI judge, 1-5 | did the agent stick to the assigned task |
| `GroundednessEvaluator` (optional) | AI judge, 1-5 | is the answer supported by the provided context |
| `ResponseCompletenessEvaluator` (optional) | AI judge, 1-5 | does the answer cover the ground truth |
| `ViolenceEvaluator`, `SelfHarmEvaluator` (optional) | Foundry service | content safety |
| `FriendlinessEvaluator`, `ResponseLengthScoreEvaluator` (optional) | custom | your own metrics |

## Steps

| # | Step | Time | Outcome |
| --- | --- | --- | --- |
| 0 | Configuration and `model_config` | 3 min | ready-to-run cells |
| 1 | Intent Resolution on plain strings | 8 min | a good and a bad score, side by side |
| 2 | Evaluate a conversation loaded from disk | 10 min | query/response split at the last user turn |
| 3 | Tool Call Accuracy and Task Adherence | 10 min | passing rate drops when a call is irrelevant |
| 4 | Batch evaluation with `evaluate()` | 10 min | `evaluation_results/*.json` + aggregated metrics |
| 5 | *Optional* - Groundedness and Response Completeness | 10 min | two more dataset shapes |
| 6 | *Optional* - Custom evaluators (prompt-based and code-based) | 15 min | your own metric, publishable to Foundry |
| 7 | *Optional* - Content safety evaluators | 10 min | service-backed Violence / SelfHarm scores |

**Minimum result in 30 minutes:** steps 0 to 4. That is already a complete local evaluation pipeline.

## Files

```text
01-local-evaluation/
├── lab01_local_evaluation_starter.ipynb
├── lab01_local_evaluation_solution.ipynb
├── lab_utils.py
└── assets/
    ├── evaluation_data.jsonl                  <- 5 agent records (query / response / tool_definitions)
    ├── sample_synthetic_conversations.jsonl   <- 90 agent conversations with tools
    ├── groundedness_data.jsonl                <- query / context / response
    ├── response_completeness_data.jsonl       <- ground_truth / response
    ├── friendliness.prompty + friend.py       <- prompt-based custom evaluator
    └── response_length_score.py               <- code-based custom evaluator
```

Results are written to `evaluation_results/` inside this folder.

## Things to notice while you work

* Two responses can both be *correct* and score very differently: read `intent_resolution_reason`
  before trusting the number.
* `ToolCallAccuracyEvaluator` averages the per-call binary scores, so it behaves like a **passing rate**.
* The conversation split is the part people get wrong: `query` ends at the **last user message**,
  `response` is everything generated after it.
* `AIAgentConverter` is not needed here: in `azure-ai-evaluation 1.18.3` it converts *Foundry* agent
  runs identified by `thread_id`/`run_id`, which is a cloud workflow (Lab 03).

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `Unrecognized request argument: max_tokens` | the judge deployment is a GPT-5 class model: point `AZURE_OPENAI_EVALUATION_COMPATIBLE_DEPLOYMENT_NAME` to a `gpt-4.1-mini` class deployment |
| `FileNotFoundError: credentials_my.env` | the file is not in any parent folder of this notebook; put it in the repository root |
| Empty dict from a content-safety evaluator | metric-name casing issue of SDK 1.18.3 on refusals: use the `CaseInsensitiveViolenceEvaluator` subclass from the solution |
| Nothing is printed after `evaluate()` | the SDK redirects stdout: `lab_utils.restore_stdout()` puts it back (already called by `batch_evaluation`) |
| `DefaultAzureCredential` failures | run `az login` and check that the account can access the Foundry project |
