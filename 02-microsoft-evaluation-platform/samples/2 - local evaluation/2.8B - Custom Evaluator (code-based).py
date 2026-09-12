from utils import initialize
settings = initialize(output=True)

from response_length_score import ResponseLengthScoreEvaluator

response_length_score_evaluator = ResponseLengthScoreEvaluator()
response_length_score = response_length_score_evaluator(answer="What is the speed of light?")

print(response_length_score)

publish_evaluator = True

if publish_evaluator:
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import (
        EvaluatorCategory,
        EvaluatorDefinitionType,
    )

    project_endpoint = settings["foundry_project_endpoint"]
    if not project_endpoint:
        raise ValueError(
            "FOUNDRY_PROJECT_ENDPOINT is required to publish the evaluator"
        )

    code_text = """
def grade(sample: dict, item: dict) -> float:
    answer = item.get("answer", "")

    if not answer:
        return 0.0

    length = len(answer)

    if length < 20:
        return 0.2

    if length > 500:
        return 0.5

    return 1.0
"""

    with AIProjectClient(
        endpoint=project_endpoint,
        credential=settings["credential"],
    ) as project_client:
        published_evaluator = (
            project_client.beta.evaluators.create_version(
                name="response_length_score_evaluator",
                evaluator_version={
                    "name": "response_length_score_evaluator",
                    "categories": [EvaluatorCategory.QUALITY],
                    "display_name": "Response Length Score Evaluator",
                    "description": (
                        "Scores whether a response falls within the optimal length range."
                    ),
                    "definition": {
                        "type": EvaluatorDefinitionType.CODE,
                        "code_text": code_text,
                        "init_parameters": {
                            "type": "object",
                            "properties": {
                                "deployment_name": {"type": "string"},
                                "pass_threshold": {"type": "number"},
                            },
                            "required": [
                                "deployment_name",
                                "pass_threshold",
                            ],
                        },
                        "data_schema": {
                            "type": "object",
                            "required": ["answer"],
                            "properties": {
                                "answer": {"type": "string"},
                            },
                        },
                        "metrics": {
                            "result": {
                                "type": "continuous",
                                "desirable_direction": "increase",
                                "min_value": 0.0,
                                "max_value": 1.0,
                            }
                        },
                    },
                },
            )
        )

    print(
        f"Published evaluator on Foundry V2: {published_evaluator.name} "
        f"(version {published_evaluator.version})"
    )