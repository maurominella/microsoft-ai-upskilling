import asyncio
from a2a.client import create_client
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest

CAMPAIGN_BRIEF = "sector=Travel; impressions=9200000"

async def main():
    client = await create_client("http://localhost:9999")
    async with client:
        request = SendMessageRequest(
            message=new_text_message(
                CAMPAIGN_BRIEF,
                role=Role.ROLE_USER,
            )
        )

        async for response in client.send_message(request):
            print(response.message.parts)
            
            
asyncio.run(main())