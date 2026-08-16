import json, warnings
from utils import initialize, batch_evaluation

# Initialize Response Completeness Evaluator
from azure.ai.evaluation import GroundednessEvaluator, GroundednessProEvaluator, AzureOpenAIModelConfiguration

settings = initialize(output=True)

warnings.filterwarnings("ignore")

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=settings["azure_openai_endpoint"],
    azure_deployment=settings["azure_evaluation_compatible_deployment_name"],
    api_version=settings["openai_api_version"],
)

groundedness_evaluator = GroundednessEvaluator(
    model_config, credential=settings["credential"]
)


# Constants
eval_data_path           = "groundedness_data.jsonl"
eval_name                = "groundedness"
eval_output_path         = "evaluation_results"
publish_to_foundry       = True
foundry_project_endpoint = settings["foundry_project_endpoint"]


# Samples

# +++++ agent response is complete +++++

query_response = dict(
    query="Which tent is the most waterproof?",
    context="The Alpine Explorer Tent is the second most water-proof of all tents available.",
    response="The Alpine Explorer Tent is the most waterproof."
)

# Running Groundedness Evaluator
groundedness_score = groundedness_evaluator(
    **query_response
)

# print the result dictionary pretty in the console
print(json.dumps(groundedness_score, indent=4))


# prepare ground truth and response for evaluation
from utils import prepare_query_context_response
prepare_query_context_response(file_path=eval_data_path)

# prepare_ground_truth_and_response
local_path, evaluation_result = batch_evaluation(
    eval_data_path=eval_data_path,
    eval_name=eval_name,
    eval_object=groundedness_evaluator,
    eval_output_path=eval_output_path,
    publish_to_foundry=publish_to_foundry,
    foundry_project_endpoint=foundry_project_endpoint,
    )

print(f"Relative local path for evaluation results: {local_path}")
print(f"Microsoft Foundry URL (to be checked using the classic Foundry portal): {evaluation_result.get("studio_url")}")