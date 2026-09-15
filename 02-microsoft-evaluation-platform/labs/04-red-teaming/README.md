# Lab 04 - Red Teaming

**Duration:** ~15 minutes, plus the variable cloud scan time
**Notebook:** `lab04_red_teaming_solution.ipynb`
**Execution path:** `project_client.beta.red_teams`

## Objective

Evaluation asks *how good is the answer on my dataset*. Red teaming asks a different question:
*can I make this system produce a policy-violating answer* - using adaptive probes that no static
dataset contains.

In this lab you configure and create a **managed red-team scan** in Microsoft Foundry against a real
Azure OpenAI deployment. The scan combines two risk categories, three attack strategies and four
turns, then retrieves the service metrics and builds an **Attack Success Rate (ASR)** scorecard.

## Red teaming is not a synonym for PyRIT

| Path | Where orchestration runs | Portal |
| --- | --- | --- |
| `project_client.beta.red_teams` **(used here)** | Foundry, managed preview | classic Foundry experience |
| `azure-ai-evaluation[redteam]` | locally, on PyRIT | not compatible with the new portal |

The managed path keeps your environment small: attack orchestration and grading run server-side, so
PyRIT does not need to be installed locally - even though cloud attack strategies are PyRIT-derived.

## Prerequisites

You need:

* a Microsoft Foundry project;
* an Azure OpenAI chat model deployed in that project;
* `azure-ai-projects`, `azure-identity` and `python-dotenv` installed in the notebook environment;
* an authenticated Azure identity, for example through `az login`;
* a `.env` file discoverable by `python-dotenv` with:

```dotenv
FOUNDRY_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=<deployment-name>
```

The notebook uses `DefaultAzureCredential` with the environment credential excluded, so the signed-in
identity must have permission to access the project and create red-team scans.

## Steps

| # | Step | Time | Outcome |
| --- | --- | --- | --- |
| 0 | Load variables and create the client | 2 min | authenticated `AIProjectClient` ready |
| 1 | Configure the managed scan | 3 min | 24 attacks across risks, strategies and turns |
| 2 | Create and poll the scan | variable | cloud scan reaches a terminal status |
| 3 | Select a completed scan | 2 min | recent real results available for the demo |
| 4 | Build the ASR scorecard | 5 min | comparison plus detailed Foundry report URL |

The scan configuration uses:

| Dimension | Values |
| --- | --- |
| Risk categories | `Violence`, `Code Vulnerability` |
| Attack strategies | `Baseline`, `Base64`, `Flip` |
| Turns | `4` |
| Simulation only | `False` - attacks are evaluated against the target deployment |

This produces 24 attacks: $4\text{ turns} \times 2\text{ risk categories} \times 3\text{ strategies}$.
Creating the scan is the only operation that starts new cloud work. Run it before a presentation when
timing matters; the fallback cell can select the most recent completed scan instead.

## How to read the results

* **ASR** is the percentage of generated attacks that caused a policy-violating response.
* A lower ASR is better; `0%` means that none of the evaluated attacks succeeded.
* The notebook presents the `Violence` metrics for `Baseline` and `Base64` in a compact scorecard.
* The service groups Base64 under **easy complexity**, so its raw metric is
  `violence_easy_complexity_asr` rather than a metric containing `base64`.
* `Metric not available` means that the expected service metric was absent, not that the ASR was zero.
* The generated report URL opens the complete attack details in Microsoft Foundry for deeper review.
* Grading is model-based: false positives and false negatives can occur, so surprising results need
  human review.

The scorecard is intentionally narrower than the scan itself: the service also runs `Flip` attacks and
tests `Code Vulnerability`, while the notebook's summary focuses on the Baseline/Base64 comparison for
Violence.

## Files

```text
04-red-teaming/
├── README.md
├── lab04_red_teaming_starter.ipynb
├── lab04_red_teaming_solution.ipynb
└── lab_utils.py
```

`lab04_red_teaming_solution.ipynb` is the notebook documented here. The scan and its evaluation result
live in the Foundry project; the notebook does not create local result files.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `Environment variables could not be loaded` | create a discoverable `.env` file and set both required variables |
| Authentication or authorization fails | run `az login`, select the correct tenant/subscription and verify project permissions |
| The scan stays queued or running for a long time | cloud execution time varies: use the completed-scan fallback and return to the live scan later |
| `No completed scan is available` | no completed scan exists in the project yet: create one and wait for completion |
| `Scan results are not ready` | the selected scan has not reached `Completed`; rerun polling or select a completed scan |
| A scorecard row says `Metric not available` | inspect `evaluationMetrics`; preview service metric names can change between versions |
| The report URL opens the classic portal | expected: this notebook uses the preview `beta.red_teams` API |
| Costs / duration grow quickly | they scale with `risk categories x attack strategies x turns`: widen one dimension at a time |

## Wrap-up

The notebook demonstrates the complete managed workflow: define a target, generate adaptive attacks,
wait for Foundry evaluation and turn the raw service metrics into an interpretable scorecard. Red
teaming produces evidence for mitigations and regression tests, but it does not guarantee security -
it shows how *these* probes performed against *this* deployment and configuration.
