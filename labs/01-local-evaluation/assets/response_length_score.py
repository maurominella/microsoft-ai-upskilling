class ResponseLengthScoreEvaluator:
    """
    A code-based evaluator in the Foundry V2 catalog has the following requirements:

    - It must be a standalone function named grade.
    - It must have the signature grade(sample: dict, item: dict) -> float.
    - It must return a single float between 0.0 and 1.0.
    - It must be passed as text in definition.code_text.
    - It must not import local files because the cloud sandbox does not automatically receive them.
    - It must declare deployment_name and pass_threshold, even though it does not use an LLM.

    This evaluator converts response length into a score and considers responses between 20 and 500 characters optimal.
    """

    def __init__(self):
        pass
    # A class is made callable by implementing the special method __call__.
    def __call__(self, *, answer: str, **kwargs):
        return {"result": self.grade({}, {"answer": answer})}

    @staticmethod
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