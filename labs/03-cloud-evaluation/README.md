# Lab 03 - Cloud Evaluation

**Duration:** ~45 minutes (steps 7-8 are optional)
**Start from:** `lab03_cloud_evaluation_starter.ipynb`
**Reference solution:** `lab03_cloud_evaluation_solution.ipynb`
**Source material:** `4 - cloud evaluation/4.1 - Cloud Evaluation.ipynb`

## Objective

Move evaluation from your laptop to Microsoft Foundry. Local runs are ideal for prototyping on small
data; cloud runs are what you need when the dataset grows, when results must be tracked in a project,
and when evaluation becomes a **gate in a CI/CD pipeline** or a post-deployment monitor.

By the end you will have:

* a dataset uploaded as a **versioned project asset**,
* an **evaluation definition** (what is measured) reusable across runs,
* a completed **run** with per-row results and a portal report URL.

## Prerequisites

A Foundry project (`FOUNDRY_PROJECT_ENDPOINT`) and `az login`. The optional step 7 additionally requires
the custom evaluators published in the optional step of **Lab 01**.

## Steps

| # | Step | Time | Outcome |
| --- | --- | --- | --- |
| 0 | Configuration and project client | 3 min | `AIProjectClient` + OpenAI client |
| 1 | Inspect the dataset | 5 min | you know the four fields you must map |
| 2 | Helper functions (ready to run) | 2 min | JSONL validation and version handling |
| 3 | Upload the dataset | 5 min | `data_id` of the versioned asset |
| 4 | Data source config and testing criteria | 15 min | deterministic + AI judge + safety criteria |
| 5 | Create the evaluation and the run | 10 min | run submitted to the service |
| 6 | Poll and read results | 10 min | status, report URL, per-row scores |
| 7 | *Optional* - add your custom evaluators from Lab 01 | 10 min | catalog evaluators in a cloud run |
| 8 | *Optional* - evaluate the dataset generated in Lab 02 | 15 min | the full generate -> evaluate loop |

**Minimum result in 30 minutes:** steps 0 to 6, with `builtin.f1_score` plus one AI judge.

## Files

```text
03-cloud-evaluation/
├── lab03_cloud_evaluation_starter.ipynb
├── lab03_cloud_evaluation_solution.ipynb
├── lab_utils.py
└── assets/
    └── synthetic_dataset_cloud.jsonl   <- 10 records: query / context / response / ground_truth
```

## Things to notice while you work

* The **evaluation object** says *what* is measured; the **run** applies it to one dataset. Several runs
  under the same evaluation are directly comparable - that is what makes evaluation a regression test.
* Criteria are **declarative**: most failures come from a wrong `{{item.<field>}}` mapping, not from code.
* Not all evaluators are AI judges: `builtin.f1_score` is deterministic and needs no model, while
  `builtin.groundedness` and `builtin.relevance` need `initialization_parameters={"model": ...}`.
* Dataset versions are **immutable**: re-uploading the same version fails, which is why `upload_dataset`
  walks forward to the first free version.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `ResourceExistsError` on upload | that version already exists: the helper increments it automatically, keep the helper |
| The run fails immediately | check the `data_mapping`: every referenced field must exist in the item schema and in the JSONL |
| `report_url` is empty | the run has not completed yet: keep polling |
| Custom evaluator not found | it was never published (Lab 01, optional step) or the `evaluator_version` is wrong: check it in the portal |
| Very slow run | AI-judge criteria call a model for every row: reduce the dataset or the number of criteria |
