import asyncio
import os
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

load_dotenv()

async def main():
    client = OpenAIChatClient(
        # endpoint not needed since it will be inferred from the environment variable AZURE_OPENAI_ENDPOINT
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        credential=AzureCliCredential(),
    )
    agent = Agent(
        client=client,
        name="CampaignAnalyst",
        instructions=(
            "You are an analyst at AdvertSphere Broadcasting. Always answer in English, "
            "concisely and professionally."
        )
    )
    answer = await agent.run("Introduce yourself in one sentence and tell me how you can help.")
    print(answer.text)

if __name__ == "__main__":
    asyncio.run(main())