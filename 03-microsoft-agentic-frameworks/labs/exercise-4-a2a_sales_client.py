import asyncio

from a2a.client import create_client
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest
from google.protobuf.json_format import MessageToDict


async def main():

    for url in ["http://localhost:9999", "http://localhost:10000"]:
        try:
            client = await create_client(url)
            async with client:
                request = SendMessageRequest(
                    message=new_text_message(
                        "sector=Travel; impressions=9200000",
                        role=Role.ROLE_USER,
                    )
                )

                async for response in client.send_message(request):
                    print(MessageToDict(response))
            
        except Exception as e:
            print(f"Failed to connect to {url}: {e}")


asyncio.run(main())