# Lab 03 - Cloud Evaluation

**Duration:** ~45 minutes
**Notebook:** `lab03_cloud_evaluation_solution.ipynb`
**Dataset:** `synthetic_dataset_cloud3.jsonl`
**Documentation:** [Cloud evaluation with the Azure AI Projects SDK](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/cloud-evaluation#cloud-evaluation-preview-with-azure-ai-projects-sdk)

## Objective

Run an evaluation remotely in Microsoft Foundry instead of using local compute. Cloud evaluations are
suited to larger datasets, pre-deployment testing, **CI/CD quality gates**, and post-deployment
monitoring, while keeping results and reports attached to a Foundry project.

By the end you will have:

* a validated JSONL dataset uploaded as a **versioned project asset**,
* an **evaluation definition** that combines built-in and custom evaluators,
* a completed cloud **evaluation run** with per-row results and a Foundry report URL.

## Prerequisites

A Microsoft Foundry project, an evaluation-compatible model deployment, and an authenticated Azure
session (`az login`). Create a `.env` file that provides:

* `FOUNDRY_PROJECT_ENDPOINT`,
* `AZURE_OPENAI_EVALUATION_COMPATIBLE_DEPLOYMENT_NAME`.

The Python environment must include `azure-ai-projects`, `azure-identity`, `openai`, and
`python-dotenv`. The project evaluator library must also contain these custom evaluators:

* `friendliness_evaluator`, version `1`,
* `response_length_score_evaluator`, version `2`.

## Steps

| # | Step | Time | Outcome |
| --- | --- | --- | --- |
| 0 | Load configuration and credentials | 5 min | endpoint, deployment name, and `DefaultAzureCredential` |
| 1 | Create the Foundry project client | 3 min | authenticated `AIProjectClient` |
| 2 | Define the helper functions | 5 min | JSONL validation and collision-safe version handling |
| 3 | Upload the evaluation dataset | 5 min | `data_id` of the versioned project asset |
| 4 | Define the data schema | 5 min | mappings for `query`, `response`, `context`, and `ground_truth` |
| 5 | Configure the testing criteria | 10 min | quality, safety, and custom criteria |
| 6 | Create the evaluation and run | 5 min | cloud run submitted to Microsoft Foundry |
| 7 | Poll and inspect the results | 10 min | final status, report URL, and per-row output items |

**Minimum result in 30 minutes:** steps 0 to 6, with the dataset uploaded and the cloud run submitted.

## Files

```text
03-cloud-evaluation/
├── lab03_cloud_evaluation_starter.ipynb
├── lab03_cloud_evaluation_solution.ipynb   <- complete cloud evaluation workflow
├── lab_utils.py                            <- shared utilities for other workshop labs
├── synthetic_dataset_cloud3.jsonl          <- 10 evaluation records
└── assets/
    └── synthetic_dataset_cloud.jsonl
```

Each record in `synthetic_dataset_cloud3.jsonl` contains `query`, `context`, `response`, and
`ground_truth`. The notebook validates this JSONL file before uploading it.

## Things to notice while you work

* The **evaluation object** says *what* is measured; the **run** applies it to one dataset. Several runs
  under the same evaluation are directly comparable - that is what makes evaluation a regression test.
* Criteria are **declarative**: most failures come from a wrong `{{item.<field>}}` mapping, not from code.
* The evaluation mixes six criteria: deterministic F1, groundedness, relevance, violence safety,
  friendliness, and response length. Model-based criteria receive the configured deployment through
  their initialization parameters.
* Custom evaluators are referenced by both **name and version**, so the definitions published in the
  project evaluator library must match the notebook exactly.
* Dataset versions are **immutable**. The `upload_dataset` helper validates the JSONL, detects existing
  versions, and advances from `1.0` until it finds a usable version.
* Dataset upload, evaluation creation, and run creation are separate service operations. The final cell
  polls the asynchronous run every five seconds until it is completed, failed, or canceled.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| Environment variables are not loaded | place the `.env` file where the notebook process can load it and verify both required variables |
| Authentication fails | run `az login`; the notebook intentionally excludes environment credentials from `DefaultAzureCredential` |
| `ResourceExistsError` on upload | keep the upload helper: it automatically advances to the next available dataset version |
| Dataset upload never appears in the listing | verify project access and service availability; the helper stops after 60 seconds without deleting the new asset |
| The run fails immediately | check that every `data_mapping` field exists in both the item schema and every JSONL record |
| Custom evaluator not found | publish the required evaluator or correct its name and `evaluator_version` in `testing_criteria` |
| `report_url` is empty | wait for a terminal run status; the notebook polls until the run completes, fails, or is canceled |
| Very slow run | model-based criteria invoke the deployment for every record; reduce the dataset or the number of criteria |
