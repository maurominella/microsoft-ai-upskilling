import os
from azure.identity import AzureCliCredential, get_bearer_token_provider
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

query = "I need to open raise a question to the IT department, because I am not able to access the network with my password, and it tells me that my account has been deactivated. I also want to speak to a supervisor, because I need to access the network urgently. Please formalize my request by opening a new protocol."


def ProtocolNumberGenerator():
    """Generates a protocol number for the request."""
    import random
    return str(random.randint(100000, 999999))


token_provider = get_bearer_token_provider(
    AzureCliCredential(),
    "https://ai.azure.com/.default",
)

client = AzureOpenAI(
    azure_ad_token_provider=token_provider,
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

response = client.responses.create(
    model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    input=query,
    tools=[
        {
            "type": "function",
            "name": "ProtocolNumberGenerator",
            "description": "Generates a protocol number for the request",
            "parameters": {
                "type": "object",
                "properties": {}
            },
            "strict": False,
        }
    ]
)


print(response.output_text)          # generated text, which is empty when functions have to be called
print(response.output[0].name)    # function to be called
print(response.output[0].call_id) # function identifier for the call