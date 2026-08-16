# Hands-on labs - Foundry AI Evaluation workshop (day 2)

Four practical labs, **~45 minutes each**, built on the notebooks of this repository.
Each lab starts from something that works in the first 10 minutes and grows in complexity, so a
30-minute run still produces a concrete result. The final step of every lab is marked **optional** and
can be completed after the workshop.

| # | Lab | What you build | Source material |
| --- | --- | --- | --- |
| 1 | [Local Evaluation](./01-local-evaluation/README.md) | AI-judge evaluators on single samples, on a real agent conversation and in batch; custom evaluators | `2 - local evaluation` |
| 2 | [Dataset generation](./02-dataset-generation/README.md) | Grounded synthetic conversations with `Simulator`, then `AdversarialSimulator`, UPIA and XPIA | `3 - syntetic data generation` |
| 3 | [Cloud Evaluation](./03-cloud-evaluation/README.md) | Versioned dataset, evaluation definition and cloud run in Microsoft Foundry | `4 - cloud evaluation` |
| 4 | [Red Teaming](./04-red-teaming/README.md) | Managed red-team scan, Attack Success Rate per technique, Foundry report | `4 - cloud evaluation` |

## Suggested schedule (4 hours)

| Time | Activity |
| --- | --- |
| 0:00 - 0:10 | Introduction, credentials check, `az login` |
| 0:10 - 0:55 | Lab 1 - Local Evaluation |
| 0:55 - 1:40 | Lab 2 - Dataset generation |
| 1:40 - 1:55 | Break |
| 1:55 - 2:40 | Lab 3 - Cloud Evaluation |
| 2:40 - 3:25 | Lab 4 - Red Teaming |
| 3:25 - 4:00 | Optional steps, questions, wrap-up |

Labs 1 and 2 are independent. Lab 3 is more interesting after the optional step of Lab 1 (custom
evaluators published to the Foundry catalog) and can reuse the dataset generated in Lab 2. Lab 4 is
independent but lands better after Lab 3.

## How each lab is organised

```text
labs/
├── README.md                     <- this file
├── 01-local-evaluation/
│   ├── README.md                 <- objective, steps, timing, troubleshooting
│   ├── lab01_..._starter.ipynb   <- notebook with TODOs: start here
│   ├── lab01_..._solution.ipynb  <- complete version
│   ├── lab_utils.py              <- credentials loading and shared helpers
│   └── assets/                   <- datasets, prompty files, custom evaluators
├── 02-dataset-generation/
├── 03-cloud-evaluation/
└── 04-red-teaming/
```

Work in the **starter** notebook and keep the **solution** one as a safety net: opening it is not
cheating, falling behind and losing the thread is the only real failure mode.

## Before you start

The Python environment is already prepared for you:

```text
azure-ai-projects==2.4.0
azure-identity==1.25.3
azure-ai-evaluation==1.18.3
prompty[foundry,jinja2]==2.0.0b3
python-dotenv==1.2.2
jupyter==1.1.1
kagglehub==1.0.2
```

Two things must be in place:

1. **`credentials_my.env`** - the labs look for it automatically, walking up from the notebook folder
   (repository root or a `config` subfolder). It must define:

   ```text
   FOUNDRY_PROJECT_ENDPOINT=...
   AZURE_OPENAI_ENDPOINT=...
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=...
   AZURE_OPENAI_EVALUATION_COMPATIBLE_DEPLOYMENT_NAME=...
   AZURE_OPENAI_API_VERSION=...
   ```

2. **Azure sign-in** - every lab authenticates with `DefaultAzureCredential`, so run `az login` in a
   terminal before opening the notebooks.

> **Judge model.** `AZURE_OPENAI_EVALUATION_COMPATIBLE_DEPLOYMENT_NAME` must point to a `gpt-4.1-mini`
> class deployment: the local agent evaluators of `azure-ai-evaluation 1.18.3` still send the legacy
> `max_tokens` parameter, while newer GPT-5 deployments require `max_completion_tokens`.
> `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` is the *application* model and can be a newer one.

## Ground rules

* **Run the notebook from its own folder**, so the relative paths (`assets/...`) resolve.
* Cloud operations (Labs 3 and 4) create real resources in your Foundry project and consume tokens:
  keep the requested number of results small.
* Every evaluator returns a `*_reason` / `*_result` field: the score alone is never the answer.
