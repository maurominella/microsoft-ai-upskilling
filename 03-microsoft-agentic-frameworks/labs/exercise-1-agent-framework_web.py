import asyncio
import os
from turtle import st
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.openai import OpenAIChatClient

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

load_dotenv()

# possible queries 
# --> "Introduce yourself in one sentence and tell me how you can help."
# --> "Prepare a draft Back to School TV Campaign Proposal for children 7-10 years old."

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Campaign Analyst</title>
        <style>
            body { font-family: sans-serif; max-width: 720px; margin: 3rem auto; padding: 0 1rem; }
            form { display: flex; gap: 0.5rem; }
            input { flex: 1; padding: 0.75rem; }
            button { padding: 0.75rem 1rem; cursor: pointer; }
            #answer { margin-top: 1.5rem; line-height: 1.6; }
            #answer pre { overflow-x: auto; padding: 1rem; background: #f4f4f4; }
            #answer code { font-family: monospace; }
            #answer > :first-child { margin-top: 0; }
            #answer > :last-child { margin-bottom: 0; }
        </style>
    </head>
    <body>
        <h1>Campaign Analyst</h1>
        <form id="question-form">
            <input id="question" type="text" placeholder="Enter your question" required>
            <button type="submit">Submit</button>
        </form>
        <div id="answer" role="status" aria-live="polite"></div>
        <script src="https://cdn.jsdelivr.net/npm/marked@16.3.0/lib/marked.umd.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/dompurify@3.2.6/dist/purify.min.js"></script>
        <script>
            const form = document.getElementById("question-form");
            const question = document.getElementById("question");
            const answer = document.getElementById("answer");

            form.addEventListener("submit", async (event) => {
                event.preventDefault();
                answer.textContent = "Processing...";

                try {
                    const response = await fetch(
                        `/invoke-agent/query?q=${encodeURIComponent(question.value)}`
                    );
                    if (!response.ok) {
                        throw new Error(`HTTP error ${response.status}`);
                    }
                    const data = await response.json();
                    answer.innerHTML = DOMPurify.sanitize(marked.parse(data.result));
                } catch (error) {
                    answer.textContent = `Unable to get a response: ${error.message}`;
                }
            });
        </script>
    </body>
    </html>
    """

@app.get("/invoke-agent/query")
async def invoke_agent_endpoint(q: str):
    result = await invoke_agent(q)
    return {"status": "Agent invoked", "result": result}

async def invoke_agent(query:str) -> str:
    client = OpenAIChatClient(
        # endpoint not needed since it will be inferred from the environment variable AZURE_OPENAI_ENDPOINT
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        credential=AzureCliCredential(),
    )
    microsoft_learn = MCPStreamableHTTPTool(
        name="microsoft_learn",
        url="https://learn.microsoft.com/api/mcp",
        approval_mode="never_require",
        load_prompts=False,
    )
    agent = Agent(
        client=client,
        name="CampaignAnalyst",
        instructions=(
            "You are an analyst at AdvertSphere Broadcasting. Always answer in English, "
            "concisely and professionally. Use Microsoft Learn tools for questions about "
            "Microsoft technologies."
        ),
        tools=[microsoft_learn],
    )

    async with agent:
        answer = await agent.run(query)
    print(answer.text)
    return answer.text

# asyncio.run(invoke_agent())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)