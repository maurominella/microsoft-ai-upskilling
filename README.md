# Generative AI Evaluation

This repository contains examples, notebooks, hands-on labs, and workshop materials for evaluating generative AI applications with Microsoft Foundry.

## Environment Setup

Before running the notebooks or labs, follow the instructions in [environment_preparation.md](./environment_preparation.md) to:

- install Git and clone the repository;
- install `uv` and create the Python 3.13 virtual environment;
- install the required dependencies;
- configure the Jupyter kernel for VS Code.

Some exercises also require a configured `credentials_my.env` file and an authenticated Azure session.

## Modules

| Module | Topic | Contents |
| --- | --- | --- |
| 0 | [Dataset Preparation](./0%20-%20dataset%20preparation/) | Build datasets and manage dataset records for evaluation workflows. |
| 1 | [Metrics](./1%20-%20metrics/) | Explore evaluation metrics, metric definitions, and worked examples. |
| 2 | [Local Evaluation](./2%20-%20local%20evaluation/) | Run AI-judge, content safety, groundedness, response completeness, and custom evaluators locally. |
| 3 | [Synthetic Data Generation](./3%20-%20syntetic%20data%20generation/) | Generate synthetic conversations, run adversarial simulations, and explore jailbreak attacks. |
| 4 | [Cloud Evaluation](./4%20-%20cloud%20evaluation/) | Run cloud evaluations and managed red-team exercises in Microsoft Foundry. |

## Hands-on Labs

The [labs](./labs/) directory contains four guided workshop exercises, each with a starter notebook, a completed solution, supporting assets, and troubleshooting guidance:

1. [Local Evaluation](./labs/01-local-evaluation/README.md)
2. [Dataset Generation](./labs/02-dataset-generation/README.md)
3. [Cloud Evaluation](./labs/03-cloud-evaluation/README.md)
4. [Red Teaming](./labs/04-red-teaming/README.md)

See the [Hands-on Labs Guide](./labs/README.md) for prerequisites, the suggested workshop schedule, and the recommended learning path.

## Slides

The workshop slide deck is available in the [slides](./slides/) directory:

- [AI Evaluation in Microsoft Foundry](./slides/2x01_AI_Evaluation_in_%20Microsoft_Foundry_v1.02.pdf)
