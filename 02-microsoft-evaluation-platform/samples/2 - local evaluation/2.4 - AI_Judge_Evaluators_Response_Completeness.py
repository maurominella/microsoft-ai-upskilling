import json, warnings
from utils import initialize, batch_evaluation

# Initialize Response Completeness Evaluator
from azure.ai.evaluation import ResponseCompletenessEvaluator, AzureOpenAIModelConfiguration

settings = initialize(output=True)

warnings.filterwarnings("ignore")

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=settings["azure_openai_endpoint"],
    azure_deployment=settings["azure_evaluation_compatible_deployment_name"],
    api_version=settings["openai_api_version"],
)

response_completeness_evaluator = ResponseCompletenessEvaluator(
    model_config, credential=settings["credential"]
)


# Constants
eval_data_path           = "response_completeness_data.jsonl"
eval_name                = "response_completeness"
eval_output_path         = "evaluation_results"
publish_to_foundry       = True
foundry_project_endpoint = settings["foundry_project_endpoint"]


# Samples

# +++++ agent response is complete +++++
result = response_completeness_evaluator(
    ground_truth = "Itinery: Day 1 take a train to visit the downtown area for city sightseeing; Day 2 rests in hotel.",
    response     = "Itinery: Day 1 check out the downtown district of the city on train; for Day 2, we can rest in hotel.",
)
# print the result dictionary pretty in the console
print(json.dumps(result, indent=4))

# +++++ agent response is incomplete +++++
result = response_completeness_evaluator(
    ground_truth = "The order with ID 123 has been shipped and is expected to be delivered on March 15, 2025. However, the order with ID 124 is delayed and should now arrive by March 20, 2025.",
    response     = "The order with ID 124 is delayed and should now arrive by March 20, 2025.",
)
# print the result dictionary pretty in the console
print(json.dumps(result, indent=4))


# prepare ground truth and response for evaluation
from utils import prepare_ground_truth_and_response
prepare_ground_truth_and_response(file_path=eval_data_path)

# prepare_ground_truth_and_response
local_path, evaluation_result = batch_evaluation(
    eval_data_path=eval_data_path,
    eval_name=eval_name,
    eval_object=response_completeness_evaluator,
    eval_output_path=eval_output_path,
    publish_to_foundry=publish_to_foundry,
    foundry_project_endpoint=foundry_project_endpoint,
    )

print(f"Relative local path for evaluation results: {local_path}")
print(f"Microsoft Foundry URL (to be checked using the classic Foundry portal): {evaluation_result.get("studio_url")}")