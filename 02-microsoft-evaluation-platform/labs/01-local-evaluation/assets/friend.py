import json
from pathlib import Path

class FriendlinessEvaluator:
    def __init__(self, client, *, model):

        self._client = client
        self._model = model

        prompty_path = Path(__file__).with_name("friendliness.prompty")
        prompty = prompty_path.read_text(encoding="utf-8")
        parts = prompty.split("---", maxsplit=2)
        if len(parts) != 3:
            raise ValueError(f"Invalid Prompty front matter in {prompty_path}")
        self._template = parts[2].strip()

    @property
    def prompt_template(self):
        return self._template

    def __call__(self, *, response: str, **kwargs):
        prompt = self._template.replace("{{response}}", response)
        llm_response = self._client.responses.create(
            model=self._model,
            input=prompt,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "friendliness_result",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "result": {"type": "integer", "minimum": 1, "maximum": 5},
                            "reason": {"type": "string"},
                        },
                        "required": ["result", "reason"],
                        "additionalProperties": False,
                    },
                }
            },
        )

        result = json.loads(llm_response.output_text)

        if not 1 <= result["result"] <= 5:
            raise ValueError("Friendliness score must be between 1 and 5")

        return {"score": result["result"], "reason": result["reason"]}