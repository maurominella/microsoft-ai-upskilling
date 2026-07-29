"""
SOLUTION - Exercise 2: Foundry Responses API + Code Interpreter.

Run live in front of the class, or use as a reference answer.
Requires: FOUNDRY_PROJECT_ENDPOINT, FOUNDRY_MODEL_NAME (in .env) + `az login`.
Run:  python solutions/ex2_foundry_responses.py
"""
import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

load_dotenv()
project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
MODEL = os.environ["FOUNDRY_MODEL_NAME"]


def main():
    with project.get_openai_client() as client:
        print("\n=== A) Responses API + continuity (thread) ===")
        r1 = client.responses.create(
            model=MODEL,
            input=(
                "You are an analyst at RAI Pubblicita. In English and in one sentence, "
                "explain what ROI measures for a campaign."
            ),
        )
        print("Turn 1:", r1.output_text)

        r2 = client.responses.create(
            model=MODEL,
            input="And what does CPM measure?",
            previous_response_id=r1.id,   # continuity == a 'thread'
        )
        print("Turn 2:", r2.output_text)

        print("\n=== B) Code Interpreter for exact numbers ===")
        r = client.responses.create(
            model=MODEL,
            tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
            input=(
                "Campaign VoloBlu: budget 150000 EUR, impressions 9,200,000, revenue 351000 EUR. "
                "By running code, compute precisely: ROI% = (revenue-budget)/budget*100 and "
                "CPM in euro = budget/impressions*1000. Answer in English with both values."
            ),
        )
        print(r.output_text)

        print("\n=== C) Inspect the response items (trace) ===")
        for item in r.output:
            print("-", item.type)   # e.g. 'reasoning', 'code_interpreter_call', 'message'


if __name__ == "__main__":
    main()
