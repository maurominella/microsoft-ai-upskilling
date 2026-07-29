"""
SOLUTION - Exercise 4: Sales Assistant client that delegates to the A2A Pricing Agent.

Run in a SECOND terminal while ex4_pricing_server.py is running:
    python solutions/ex4_sales_client.py

Bonus (B2): if ex4_media_server.py is also running on port 10000, set QUERY_MEDIA = True
to orchestrate both agents into one proposal.
"""
import asyncio
from uuid import uuid4
import httpx
from a2a.client import A2AClient
from a2a.types import SendMessageRequest, MessageSendParams

QUERY_MEDIA = False   # set True after starting ex4_media_server.py on port 10000


async def ask(http, base_url: str, text: str) -> str:
    client = await A2AClient.get_client_from_agent_card_url(http, base_url)
    payload = {
        "message": {
            "role": "user",
            "parts": [{"type": "text", "text": text}],
            "messageId": uuid4().hex,
        }
    }
    req = SendMessageRequest(params=MessageSendParams(**payload))
    resp = await client.send_message(req)
    return resp.model_dump(mode="json", exclude_none=True)


async def main():
    brief = "sector=Travel; impressions=9200000"
    async with httpx.AsyncClient() as http:
        print("=== Pricing Agent (delegated task) ===")
        pricing = await ask(http, "http://localhost:9999", brief)
        print(pricing)

        if QUERY_MEDIA:
            print("\n=== Media Planning Agent (delegated task) ===")
            media = await ask(http, "http://localhost:10000", brief)
            print(media)
            print("\n=== Sales Assistant composed proposal ===")
            print("Combined pricing + availability for the customer (see the two texts above).")


if __name__ == "__main__":
    asyncio.run(main())
