import asyncio
import os

from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

client = FoundryChatClient(
  project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
  model=os.environ["FOUNDRY_MODEL_NAME"],
  credential=AzureCliCredential())

agent = client.as_agent(
name="HelloAgent",
instructions="You are a concise assistant.")

resp = asyncio.run(agent.run("What is your name?"))
print(resp.text)