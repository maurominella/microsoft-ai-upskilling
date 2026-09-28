from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
import os
from azure.identity import AzureCliCredential
import asyncio
from dotenv import load_dotenv
load_dotenv()

query = "I need to open raise a question to the IT departmen. Please formalize my request by opening a new protocol."

def ProtocolNumberGenerator():
    """Generates a protocol number for the request."""
    import random
    return str(random.randint(100000, 999999))


client = OpenAIChatClient(
    model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    credential=AzureCliCredential(),
)

agent = Agent(
    client=client,
    name="CampaignAnalyst",
    instructions=(
        "You are a clever agent."
    ),
    tools=[ProtocolNumberGenerator],
)

response = asyncio.run(agent.run(query))

for m in response.messages:
    print("*"*10,"\n")
    print(f"author: {m.author_name},\nrole: {m.role},\ntext: {m.text},\ncall_id: {m.contents[0].call_id},\nresult: {m.contents[0].result}\n")