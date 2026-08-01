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

with project.get_openai_client() as client:
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
        previous_response_id=r1.id,   # <-- continuity: the model 'remembers' turn 1
    )
    print("Turn 2:", r2.output_text)


with project.get_openai_client() as client:
    r = client.responses.create(
        model=MODEL,
        tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
        input=(
            "Campaign VoloBlu: budget 150000 EUR, impressions 9,200,000, revenue 351000 EUR. "
            "By running code, compute precisely: ROI% = (revenue-budget)/budget*100 "
            "and CPM in euro = budget/impressions*1000. Answer in English with both values."
        ),
    )
    print(r.output_text)

print("--- Items produced by the Responses API ---")
for item in r.output:
    print("-", item.type)   # e.g. 'reasoning', 'code_interpreter_call', 'message'