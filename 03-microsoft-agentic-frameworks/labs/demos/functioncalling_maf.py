from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
import os
from azure.identity import AzureCliCredential
import asyncio

from dotenv import load_dotenv

query = "I need to open raise a question to the IT department, because I am not able to access the network with my password, and it tells me that my account has been deactivated. I also want to speak to a supervisor, because I need to access the network urgently. Please formalize my request by opening a new protocol."

load_dotenv()

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
        "You are a clever agent. Begin your answers by providing the protocol number."
    ),
    tools=[ProtocolNumberGenerator],
)

response = asyncio.run(agent.run(query))

print(response.messages[-1].text)          # generated text, which is empty when functions have to be called