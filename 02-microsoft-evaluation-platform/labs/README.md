# Hands-on labs - Foundry AI Evaluation workshop (day 2)

Four practical labs for a **4-hour hands-on session**, built on the notebooks of this repository.
The path moves from local quality checks and synthetic conversations to cloud evaluation and managed
red teaming. Labs 1 and 3 produce a concrete result in about 30 minutes; Lab 4 has a short setup, but
its managed scan can take a variable amount of time to complete.

| # | Lab | What you build | Duration |
| --- | --- | --- | --- |
| 1 | [Local Evaluation](./01-local-evaluation/README.md) | AI-judge evaluation on single samples, real agent conversations and batches; optional custom and safety evaluators | ~45 min |
| 2 | [Dataset generation](./02-dataset-generation/README.md) | A Prompty-based chat application and a grounded, multi-turn synthetic conversation with `Simulator` | 30-40 min |
| 3 | [Cloud Evaluation](./03-cloud-evaluation/README.md) | A versioned dataset, evaluation definition and cloud run with built-in and custom evaluators | ~45 min |
| 4 | [Red Teaming](./04-red-teaming/README.md) | A managed red-team scan and an Attack Success Rate scorecard linked to the Foundry report | ~15 min, plus scan time |

## Suggested schedule (4 hours)

| Time | Activity |
| --- | --- |
| 0:00 - 0:10 | Introduction, credentials check, `az login` |
| 0:10 - 0:55 | Lab 1 - Local Evaluation |
| 0:55 - 1:35 | Lab 2 - Dataset generation |
| 1:35 - 1:50 | Break |
| 1:50 - 2:35 | Lab 3 - Cloud Evaluation |
| 2:35 - 2:50 | Lab 4 - Configure and launch the managed scan |
| 2:50 - 3:30 | Lab 4 - Inspect a completed scan and build the ASR scorecard |
| 3:30 - 4:00 | Optional Lab 1 extensions, questions and wrap-up |

Labs 1 and 2 are independent. Lab 2 keeps its generated conversation in memory and does not create the
dataset used by Lab 3. Lab 3 uses its included JSONL dataset and requires the two custom evaluators
listed below to already exist in the Foundry project evaluator library. Lab 4 is independent, but its
comparison between evaluation and red teaming lands better after Lab 3. Because scan duration varies,
launch the scan early or use the notebook's fallback to select a recent completed scan.

## How each lab is organised

```text
labs/
├── README.md                     <- this file
├── 01-local-evaluation/
│   ├── README.md                 <- objective, steps, timing, troubleshooting
│   ├── lab01_..._starter.ipynb   <- starter notebook, where available
│   ├── lab01_..._solution.ipynb  <- notebook documented by the lab README
│   ├── lab_utils.py              <- credentials loading and shared helpers
│   └── assets/                   <- datasets, prompty files, custom evaluators
├── 02-dataset-generation/
├── 03-cloud-evaluation/
└── 04-red-teaming/
```

Each lab README documents the **solution** notebook as the complete, ready-to-run path. Where a starter
notebook is provided, use it for the exercise and keep the solution open as a safety net: opening it is
not cheating, falling behind and losing the thread is the only real failure mode.

## Before you start

The Python environment is already prepared for you:

```text
azure-ai-projects==2.4.0
azure-identity==1.25.3
azure-ai-evaluation==1.18.3
openai
prompty[foundry,jinja2]==2.0.0b3
python-dotenv==1.2.2
jupyter==1.1.1
kagglehub==1.0.2
```

Three things must be in place:

1. **`.env`** - make it discoverable by `python-dotenv` from the notebook working directory. Across the
   four labs, it can define:

   ```text
   FOUNDRY_PROJECT_ENDPOINT=...
   AZURE_OPENAI_ENDPOINT=...
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=...
   AZURE_OPENAI_EVALUATION_COMPATIBLE_DEPLOYMENT_NAME=...
   AZURE_OPENAI_API_VERSION=...
   ```

2. **Azure sign-in** - every lab authenticates with `DefaultAzureCredential`, so run `az login` in a
   terminal before opening the notebooks.

3. **Custom evaluators for Lab 3** - the Foundry project evaluator library must contain
   `friendliness_evaluator` version `1` and `response_length_score_evaluator` version `2`. Lab 1 shows
   how custom evaluators work and includes an optional publication flow.

> **Judge model.** `AZURE_OPENAI_EVALUATION_COMPATIBLE_DEPLOYMENT_NAME` must point to a `gpt-4.1-mini`
> class deployment: the local agent evaluators of `azure-ai-evaluation 1.18.3` still send the legacy
> `max_tokens` parameter, while newer GPT-5 deployments require `max_completion_tokens`.
> `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` is the *application* model and can be a newer one.

## Ground rules

* **Run the notebook from its own folder**, so the relative paths (`assets/...`) resolve.
* Cloud operations (Labs 3 and 4) create real resources in your Foundry project and consume tokens:
  keep the requested number of results small.
* Inspect evaluator reasoning and result fields alongside numeric scores; the score alone is never the
   answer.
* Red-team ASR is evidence about the selected risks, strategies and target configuration, not a
   guarantee of security.
