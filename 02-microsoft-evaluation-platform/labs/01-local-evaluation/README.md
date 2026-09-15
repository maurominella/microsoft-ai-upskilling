# Lab 01 - Local Evaluation

**Duration:** ~45 minutes (steps 5-7 are optional)
**Run:** `lab01_local_evaluation_solution.ipynb`
**Source material:** `2 - local evaluation/2.1`, `2.2`, `2.3`, `2.4`, `2.5`, `2.6`, `2.7`, `2.8A`, `2.8B`

## Objective

Use `lab01_local_evaluation_solution.ipynb` to measure the quality of an AI application from your
local environment. The notebook moves from individual examples to complete agent conversations and
finally to repeatable batch evaluations. By the end you will be able to answer three questions:

1. How do I score a single query/response pair with an AI judge and interpret its reasoning?
2. How do I score a **real agent conversation**, including its tool calls, loaded from a dataset?
3. How do I run evaluators **in batch**, persist their reports and optionally publish results to Microsoft Foundry?

Local evaluation provides a fast feedback loop for prompt changes, model changes and regression checks.

## Prerequisites

Run the notebook from this folder so that its relative paths resolve correctly. Use a Python environment
with `azure-ai-evaluation 1.18.3`, `azure-ai-projects`, `azure-identity`, `openai` and `python-dotenv`
available, then authenticate with Azure CLI:

```bash
az login
```

Create a `.env` file discoverable from the notebook working directory with these values:

```dotenv
FOUNDRY_PROJECT_ENDPOINT=https://<FOUNDRY-RESOURCE-NAME>.services.ai.azure.com/api/projects/<PROJECT-NAME>
AZURE_OPENAI_ENDPOINT=https://<FOUNDRY-RESOURCE-NAME>.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-5.4-mini
AZURE_OPENAI_EVALUATION_COMPATIBLE_DEPLOYMENT_NAME=gpt-4.1-mini
AZURE_OPENAI_API_VERSION=2025-04-01-preview
```

The notebook uses `DefaultAzureCredential` for authentication. The chat deployment and judge deployment
are deliberately separate: local agent evaluators in SDK 1.18.3 still send `max_tokens`, so the judge must
use a compatible model such as `gpt-4.1-mini` rather than a GPT-5 class deployment.

## What you will use

| Evaluator | Type | What it measures |
| --- | --- | --- |
| `IntentResolutionEvaluator` | AI judge, 1-5 | whether the answer resolves the user intent |
| `ToolCallAccuracyEvaluator` | AI judge, 0/1 per call | whether tool calls are relevant and correctly parameterised |
| `TaskAdherenceEvaluator` | AI judge, 1-5 | whether the agent stays focused on the assigned task |
| `GroundednessEvaluator` (optional) | AI judge, 1-5 | whether the answer is supported by the supplied context |
| `ResponseCompletenessEvaluator` (optional) | AI judge, 1-5 | whether the answer covers the ground truth |
| `FriendlinessEvaluator` (optional) | custom, prompt-based | how warm and approachable the response is |
| `ResponseLengthScoreEvaluator` (optional) | custom, code-based | whether the response length is within the desired range |
| `ViolenceEvaluator`, `SelfHarmEvaluator` (optional) | Foundry service | content-safety severity |

## Steps

Open `lab01_local_evaluation_solution.ipynb`, select the configured Python kernel and run the cells in
order. Steps 0-4 form the core lab; the remaining sections are independent extensions.

| # | Step | Time | Outcome |
| --- | --- | --- | --- |
| 0 | Load `.env`, authenticate and create `model_config` | 3 min | a configured Azure OpenAI judge |
| 1 | Intent Resolution on plain strings | 8 min | good and incomplete answers scored side by side |
| 2 | Evaluate a conversation loaded from disk | 10 min | `query`, `response` and `tool_definitions` split at the last user turn |
| 3 | Tool Call Accuracy and Task Adherence | 10 min | comparison of relevant, irrelevant, brief and complete responses |
| 4 | Batch evaluation with `batch_evaluation()` | 10 min | local JSON reports and aggregated metrics |
| 5 | *Optional* - Groundedness and Response Completeness | 10 min | evaluation of two additional dataset schemas |
| 6 | *Optional* - Custom evaluators | 15 min | prompt-based and code-based metrics, optionally publishable to Foundry |
| 7 | *Optional* - Content safety evaluators | 10 min | service-backed Violence and Self-Harm scores |

**Minimum result in 30 minutes:** complete steps 0-4 for a working local evaluation pipeline with
single-sample, conversation-level and batch scoring.

## Files

```text
01-local-evaluation/
├── lab01_local_evaluation_solution.ipynb      <- notebook to run
├── lab_utils.py                               <- batch evaluation and stdout helpers
├── assets/
│   ├── evaluation_data.jsonl                  <- 5 agent records
│   ├── sample_synthetic_conversations.jsonl   <- 90 conversations with tools
│   ├── groundedness_data.jsonl                <- query / context / response
│   ├── response_completeness_data.jsonl       <- ground_truth / response
│   ├── friendliness.prompty                   <- prompt and output schema for friendliness
│   ├── friend.py                              <- prompt-based custom evaluator
│   └── response_length_score.py               <- code-based custom evaluator
└── evaluation_results/
    ├── tool_call_accuracy.json
    ├── task_adherence.json
    ├── groundedness.json
    └── response_completeness.json
```

Step 4 writes `tool_call_accuracy.json` and `task_adherence.json`. Optional step 5 adds the groundedness
and response-completeness reports. Set `publish_to_foundry = True` in step 4 to also publish a batch run;
local files are always retained.

## Things to notice while you work

* Two responses can both be plausible and score differently: inspect the evaluator's `*_reason` or
  `*_result` fields before trusting the numeric score alone.
* `ToolCallAccuracyEvaluator` averages binary per-call scores, so multiple calls produce a **passing rate**.
* For a conversation, `query` ends at the **last user message** and `response` contains every assistant
  or tool message generated after it.
* Each batch dataset must expose the fields expected by its evaluator. Groundedness uses
  `query`/`context`/`response`, while completeness uses `ground_truth`/`response`.
* `AIAgentConverter` is intentionally not used. In `azure-ai-evaluation 1.18.3` it converts Foundry agent
  runs identified by `thread_id`/`run_id`; that cloud workflow belongs to Lab 03.
* The custom evaluator publication cell is disabled by default. Enable it only when preparing the optional
  Lab 03 flow, and record the returned evaluator version.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `Environment variables not loaded, cell execution stopped` | `.env` was not found from the notebook working directory; create it with the values shown above and restart the kernel |
| `Unrecognized request argument: max_tokens` | the judge points to a GPT-5 class model; set `AZURE_OPENAI_EVALUATION_COMPATIBLE_DEPLOYMENT_NAME` to a `gpt-4.1-mini` class deployment |
| A relative `assets/...` path is not found | Jupyter is running from another directory; set the working directory to `01-local-evaluation` and rerun from step 0 |
| Empty result from the Violence evaluator | SDK 1.18.3 can return inconsistent metric-name casing on refusals; use the notebook's `CaseInsensitiveViolenceEvaluator` subclass |
| Nothing is printed after `evaluate()` | the SDK redirected stdout; `batch_evaluation()` calls `lab_utils.restore_stdout()` before returning |
| `DefaultAzureCredential` fails | run `az login` and verify that the signed-in account can access both Azure OpenAI and the Foundry project |
