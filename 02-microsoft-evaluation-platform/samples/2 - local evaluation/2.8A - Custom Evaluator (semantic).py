from openai import AzureOpenAI
from azure.identity import get_bearer_token_provider
from utils import initialize
settings = initialize(output=True)

from friend import FriendlinessEvaluator

token_provider = get_bearer_token_provider(
    settings["credential"],
    "https://cognitiveservices.azure.com/.default",
)

client = AzureOpenAI(
    azure_ad_token_provider=token_provider,
    api_version=settings["openai_api_version"],
    azure_endpoint=settings["azure_openai_endpoint"],
)

friendliness_eval = FriendlinessEvaluator(
    client=client, model=settings["azure_evaluation_compatible_deployment_name"])

result = friendliness_eval(
    response="I'm very sorry. I'll be happy to help resolve this issue."
)

result = friendliness_eval(
    response="I won't apologize for my behaviour!!"
)

print(result)
# {"score": 5, "reason": "..."}

publish_evaluator = True

if publish_evaluator:
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import EvaluatorCategory, EvaluatorDefinitionType

    project_endpoint = settings["foundry_project_endpoint"]
    if not project_endpoint:
        raise ValueError("FOUNDRY_PROJECT_ENDPOINT is required to publish the evaluator")

    with AIProjectClient(
        endpoint=project_endpoint,
        credential=settings["credential"],
    ) as project_client:
        published_evaluator = project_client.beta.evaluators.create_version(
            name="friendliness_evaluator",
            evaluator_version={
                "name": "friendliness_evaluator",
                "categories": [EvaluatorCategory.QUALITY],
                "display_name": "Friendliness Evaluator",
                "description": "Evaluates the warmth and approachability of a response.",
                "definition": {
                    "type": EvaluatorDefinitionType.PROMPT,
                    "prompt_text": friendliness_eval.prompt_template,
                    "init_parameters": {
                        "type": "object",
                        "properties": {
                            "deployment_name": {"type": "string"},
                            "threshold": {"type": "number"},
                        },
                        "required": ["deployment_name", "threshold"],
                    },
                    "data_schema": {
                        "type": "object",
                        "properties": {
                            "response": {"type": "string"},
                        },
                        "required": ["response"],
                    },
                    "metrics": {
                        "friendliness": {
                            "type": "ordinal",
                            "desirable_direction": "increase",
                            "min_value": 1,
                            "max_value": 5,
                        }
                    },
                },
            },
        )

    print(
        f"Published evaluator on Foundry V2: {published_evaluator.name} "
        f"(version {published_evaluator.version})"
    )