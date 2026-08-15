import os, sys
from dotenv import load_dotenv  # requires python-dotenv
from azure.identity import DefaultAzureCredential

# set the path to this file's directory as the current working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not load_dotenv("./../credentials_my.env"):
    print(f"Environment variables not loaded from {os.getcwd()}, cell execution stopped")
    sys.exit()

def initialize(output: bool = False):
    openai_api_version = os.environ["AZURE_OPENAI_API_VERSION"]
    azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    foundry_project_endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")

    # gpt-4.1-mini is the latest working model because later models require max_completion_tokens, while this evaluator sends max_tokens
    azure_evaluation_compatible_deployment_name = os.environ[
        "AZURE_OPENAI_EVALUATION_COMPATIBLE_DEPLOYMENT_NAME"
    ]

    credential = DefaultAzureCredential()

    if output:
        print(f"azure_openai_endpoint: {azure_openai_endpoint}")
        print(f"foundry_project_endpoint: {foundry_project_endpoint}")
        print(f"azure_evaluation_compatible_deployment_name: {azure_evaluation_compatible_deployment_name}")
        print(f"openai_api_version: {openai_api_version}")

    return {
        "openai_api_version": openai_api_version,
        "azure_openai_endpoint": azure_openai_endpoint,
        "foundry_project_endpoint": foundry_project_endpoint,
        "azure_evaluation_compatible_deployment_name": azure_evaluation_compatible_deployment_name,
        "credential": credential,
    }


def prepare_ground_truth_and_response(file_path:str = "response_completeness_data.jsonl"):
    """
    Prepare the ground truth and response for evaluation.
    This function can be modified to preprocess the inputs as needed.
    """
    import json
    from pathlib import Path

    data = [
        {
            "response": "The temperature of Seattle now is 70 degrees. Based on the temperature, having an outdoor office party is recommended.",
            "ground_truth": "The temperature of Seattle now is 50 degrees. It will be recommended to bring a jacket in the evening.",
        },
        {
            "response": 'The email draft "Project Plan" is attached. Please review and provide feedback.',
            "ground_truth": 'The email draft "Project Plan" is attached. Please review and provide feedback by EOD.',
        },
        {
            "response": "Based on the retrieved documents, the shareholder meeting discussed the operational efficiency of the company and financing options.",
            "ground_truth": "The shareholder meeting discussed the compensation package of the company CEO.",
        },
        {
            "response": "The calendar API returns an error code 500. Please check the server logs for more details.",
            "ground_truth": "The meeting is scheduled for 2 PM tomorrow. Please confirm your availability by EOD.",
        },
    ]

    with Path.open(file_path, "w") as file:
        for line in data:
            file.write(json.dumps(line) + "\n")


def prepare_query_context_response(file_path:str = "groundedness_data.jsonl"):
    """
    Prepare query, context and response for evaluation.
    This function can be modified to preprocess the inputs as needed.
    """
    import json
    from pathlib import Path

    data = [
        {
            "query": "Which tent is the most waterproof?",
            "context": "The Alpine Explorer Tent is the second most water-proof of all tents available.",
            "response": "The Alpine Explorer Tent is the most waterproof.",
        },
        {
            "query": "What is the return period for an unopened tent?",
            "context": "Unopened tents may be returned within 30 days of purchase for a full refund.",
            "response": "An unopened tent can be returned within 30 days for a full refund.",
        },
        {
            "query": "What features does the Trail Breeze Tent include?",
            "context": "The Trail Breeze Tent sleeps four people and includes two doors and a mesh roof.",
            "response": "The Trail Breeze Tent sleeps four people and has two doors.",
        },
        {
            "query": "Is the Summit Dome Tent suitable for winter camping?",
            "context": "The Summit Dome Tent is a lightweight three-season tent designed for spring, summer, and fall.",
            "response": "Yes. Its insulated walls and snow skirt make it ideal for severe winter conditions.",
        },
        {
            "query": "How much does the River Camp Tent weigh?",
            "context": "The River Camp Tent has a floor area of 45 square feet and accommodates three campers.",
            "response": "The River Camp Tent weighs 6.5 pounds.",
        },
    ]

    with Path.open(file_path, "w") as file:
        for line in data:
            file.write(json.dumps(line) + "\n")



def batch_evaluation(
        eval_name: str,
        eval_object,
        eval_data_path: str,
        eval_output_path: str="evaluation_results",
        publish_to_foundry:bool = False,
        foundry_project_endpoint: str = None,
        ) -> tuple[str, dict]:
    """
    Perform batch evaluation of a metric, using its Evaluator.
    This function can be modified to read from a file or database as needed.
    """
    
    from pathlib import Path
    from azure.ai.evaluation import evaluate

    project_endpoint = (
        foundry_project_endpoint.strip() or None
        if publish_to_foundry and foundry_project_endpoint
        else None
    )

    if publish_to_foundry and not project_endpoint:
        raise ValueError(
            "FOUNDRY_PROJECT_ENDPOINT must be set when publish_to_foundry is True."
        )

    output_path = Path(f"{eval_output_path}/{eval_name}.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    response = evaluate(
        data=eval_data_path,
        evaluation_name=f"{eval_name.replace("_", " ").title()} Evaluation",
        evaluators={
            eval_name: eval_object,
        },
        azure_ai_project=project_endpoint,
        output_path=output_path,
    )

    # restore output_path to stdout
    import sys
    (type(sys.stdout).__module__, type(sys.stdout).__name__)

    while hasattr(sys.stdout, "_prev_out"):
        sys.stdout = sys.stdout._prev_out

    while hasattr(sys.stderr, "_prev_out"):
        sys.stderr = sys.stderr._prev_out

    
    return output_path._str, response