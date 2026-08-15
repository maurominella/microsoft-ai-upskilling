"""
Shared helpers for the workshop labs (day 2 - hands on).

The only thing this module does is:
  * locate the `credentials_my.env` file used by the repository notebooks,
  * expose the environment values as a plain dictionary,
  * offer a small batch-evaluation wrapper reused by several labs.

The file is searched upwards starting from the notebook folder, so the labs
work both when they live inside the repository and when the `labs` folder is
copied somewhere else, as long as `credentials_my.env` sits in one of the
parent folders (the repository root is the usual location).
"""

from pathlib import Path
import os


def find_credentials(filename: str = "credentials_my.env", start: Path | None = None) -> Path:
    start = (start or Path.cwd()).resolve()
    for folder in [start, *start.parents]:
        candidate = folder / filename
        if candidate.is_file():
            return candidate
        candidate = folder / "config" / filename
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        f"{filename} not found starting from {start}. "
        "Place it in the repository root (or in a ./config folder) as described in the main README."
    )


def load_settings(verbose: bool = False) -> dict:
    from dotenv import load_dotenv  # requires python-dotenv
    from azure.identity import DefaultAzureCredential

    credentials_path = find_credentials()
    load_dotenv(credentials_path, override=True)

    settings = {
        "credentials_path": str(credentials_path),
        "openai_api_version": os.environ["AZURE_OPENAI_API_VERSION"],
        "azure_openai_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
        "foundry_project_endpoint": os.environ.get("FOUNDRY_PROJECT_ENDPOINT"),
        "azure_openai_deployment_name": os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        # gpt-4.1-mini class model: local agent evaluators still send `max_tokens`
        "azure_evaluation_compatible_deployment_name": os.environ[
            "AZURE_OPENAI_EVALUATION_COMPATIBLE_DEPLOYMENT_NAME"
        ],
        "credential": DefaultAzureCredential(),
    }

    if verbose:
        for key in (
            "credentials_path",
            "azure_openai_endpoint",
            "foundry_project_endpoint",
            "azure_openai_deployment_name",
            "azure_evaluation_compatible_deployment_name",
            "openai_api_version",
        ):
            print(f"{key}: {settings[key]}")

    return settings


def restore_stdout():
    """azure-ai-evaluation redirects stdout/stderr during batch runs; put them back."""
    import sys

    while hasattr(sys.stdout, "_prev_out"):
        sys.stdout = sys.stdout._prev_out
    while hasattr(sys.stderr, "_prev_out"):
        sys.stderr = sys.stderr._prev_out


def batch_evaluation(
    eval_name: str,
    eval_object,
    eval_data_path: str,
    eval_output_path: str = "evaluation_results",
    publish_to_foundry: bool = False,
    foundry_project_endpoint: str | None = None,
) -> tuple[str, dict]:
    """Run `evaluate()` over a JSONL dataset and optionally publish results to Foundry."""
    from pathlib import Path
    from azure.ai.evaluation import evaluate

    project_endpoint = (
        foundry_project_endpoint.strip() or None
        if publish_to_foundry and foundry_project_endpoint
        else None
    )

    if publish_to_foundry and not project_endpoint:
        raise ValueError("FOUNDRY_PROJECT_ENDPOINT must be set when publish_to_foundry is True.")

    output_path = Path(f"{eval_output_path}/{eval_name}.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    response = evaluate(
        data=eval_data_path,
        evaluation_name=f"{eval_name.replace('_', ' ').title()} Evaluation",
        evaluators={eval_name: eval_object},
        azure_ai_project=project_endpoint,
        output_path=output_path,
    )

    restore_stdout()
    return str(output_path), response
