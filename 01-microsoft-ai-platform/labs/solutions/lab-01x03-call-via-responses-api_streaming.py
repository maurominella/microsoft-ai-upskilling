from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

project_endpoint = "https://mm-ai-upskilling-project-resourc.services.ai.azure.com/api/projects/ai-upskilling-project"

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=AzureCliCredential(),
)

my_agent = "asb-assistant-01"
my_version = "4"

openai_client = project_client.get_openai_client()

# Reference the agent and stream its response
stream = openai_client.responses.create(
    input=[{"role": "user", "content": "Tell me what you can help with."}],
    extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)