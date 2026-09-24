# Demo script — Your first Hosted Agent on Microsoft Foundry

**Workshop:** Agentic AI on Microsoft Foundry · Day 1 — Theme 3 · Hosted Agents
**Demo:** LIVE DEMO 3 — *Building a hosted agent with Microsoft Foundry Toolkit for VS Code*
**Duration (approx.):** 35–45 minutes
**Path:** install the extension → pick the sample → explore the project (`requirements.txt`, `.env`, `azure.yaml`) → test locally with Agent Inspector → deploy to Foundry → invoke it with a **Responses** call

> The interface labels (menus, buttons, file names) are given **in English**, as they appear in the product. The sample catalog and the command names can change from one release of the extension to the next: if an entry doesn't match, look it up with the Command Palette (`Ctrl+Shift+P`).

---

## 0. Prerequisites (check them BEFORE the session)

| Requirement | Detail |
|---|---|
| Visual Studio Code | current version, with the **Microsoft Foundry Toolkit** extension |
| Python | **3.13** + the *Python* extension for VS Code (debugger support included) |
| Azure CLI | for local authentication (`az login`) |
| Azure subscription | with a **Foundry project** in a region that supports hosted agents |
| Model deployment | a model compatible with the sample; the *Basic Hosted Agent* is configured for a *mini* model — use a deployment that already exists |
| Permissions | **Foundry Project Manager** role at project level (it creates the agent and assigns the roles to the agent's identity) |

**What you do NOT need:** Docker locally. The main path of this demo is **deploying from source** (*Code* + *Remote* package mode): the Toolkit uploads a ZIP of the source and Foundry installs the dependencies during provisioning. Docker/ACR are only needed if you explicitly choose the *Container* path.

> ⚠️ **Watch the cost:** even running locally sends the requests to the model deployed on Foundry, so it consumes tokens. The CPU and memory you pick at deploy time also affect runtime costs.

---

## 1. Install the extension

1. In VS Code open **Extensions** (`Ctrl+Shift+X`).
2. Search for **Microsoft Foundry Toolkit** and install it.
3. A new **Foundry Toolkit** icon appears in the **Activity Bar** (the left-hand sidebar). Open it.
4. Sign in to Azure when prompted, and select the **subscription** and **project** you'll work with.

**What to point out to the room:** the sidebar has two blocks we'll use throughout the demo — **Developer Tools** (Build: *Create Agent*, *Deploy to Microsoft Foundry*, *Hosted Agent Playground*) and **My Resources** (Agents, Models, Tools).

---

## 2. Create the project from a sample

1. **Foundry Toolkit** sidebar → **Developer Tools** → **Build** → **Create Agent**.
2. Under **Code an agent from samples** you'll find three "hello-world" starters: **Agent Framework**, **Copilot SDK**, **LangGraph**.
   - For this demo: **Agent Framework** (it opens the *Basic Responses* sample directly).
   - Alternatively, **Browse all samples** opens the full gallery: filter by **Language = Python**, **Framework = Agent Framework**, **Protocol Type = Responses** and pick **Basic Hosted Agent**.
3. **Next** → on the **Create** tab:
   - **Workspace Folder**: choose the target folder (if it isn't empty, provide a **Folder Name** to create a subfolder).
   - **Environment Setup**: *Setup with Microsoft Foundry* → subscription + project.
   - **Model Deployment**: select the deployment that already exists.
4. **Create**, then open the **README.md** of the generated project.

> **Teaching point:** *Skip for now* generates the code without completing the model configuration — you'll still have to fill it in before running. And *Deploy & use new model* creates a **model deployment**, not the hosted agent. Creating the files is **not** a deploy.

### 2.1 Anatomy of the generated project

Keep the folder that contains `azure.yaml` open as the **workspace root**.

```
azure.yaml                      ← dichiara il servizio hosted-agent:
                                  source dir, runtime, protocols, deploy config
src/<nome-sample>/
  ├─ main.py                    ← implementa l'agente e avvia il server Responses
  ├─ requirements.txt           ← le dipendenze Python dell'agente
  ├─ .env                       ← config locale (creato dal Toolkit da .env.example)
  ├─ .env.example
  └─ .dockerignore              ← esclude .env, venv e cache Python
.vscode/
  ├─ launch.json                ← "Debug Local Agent HTTP Server"
  └─ tasks.json                 ← avvio server + apertura Agent Inspector
```

**To show on screen, one by one:**

- **`main.py`** — the agent logic is **the same** you saw in the earlier Agent Framework demos. The only addition is the shell that exposes the agent as a **Responses** server. This is the key message of the whole section: *we don't rewrite the agent in order to host it*.
- **`requirements.txt`** — the dependency declaration. It's the file Foundry will use to rebuild the environment in the cloud in *Remote* package mode, and it's the same one you use locally. It also contains `debugpy` for debugging.
- **`azure.yaml`** — where the runtime, entry point, protocols and the service's environment variables live. **Review it and save it before deploying**: the deploy resolves the values declared here from the `.env` in the source directory or from the process environment, it does **not** automatically forward every entry of your local `.env`.
- **`.env`** — **local** configuration. It must never be committed or packaged.

---

## 3. Run and test locally

```bash
# 1. selezionare l'ambiente Python 3.13
#    Command Palette → "Python: Create Environment" oppure "Python: Select Interpreter"

# 2. installare le dipendenze, dalla source directory del sample
cd src/<nome-sample>
python -m pip install -r requirements.txt

# 3. autenticarsi: le credenziali locali dell'agente arrivano da qui
az login
```

Check the `.env` in the source directory and, if setup hasn't already filled them in, set:

```dotenv
FOUNDRY_PROJECT_ENDPOINT=<endpoint del vostro progetto Foundry>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<nome del model deployment>
```

Then start the agent:

1. **Run and Debug** view → **Debug Local Agent HTTP Server** configuration → **F5**.
2. The tasks start the server on port **8088**, open **Agent Inspector** and attach the debugger.
3. In Agent Inspector send a message, for example: *"Suggest a name for a weather app."* — then a **related follow-up question**, to demonstrate the multi-turn conversation.

**What to point out:**

- Agent Inspector shows the response, any **tool calls**, the **latency waterfall** and the **run timeline**.
- Put a **breakpoint** in `main.py` and run again: it really does stop. It's your code, with your debugger. This is the most convincing argument for a developer audience.
- Opening Agent Inspector on its own does **not** start the server. If the connection fails, check in this order: terminal output, selected interpreter, installed dependencies, credentials (`az login`), port 8088 free.

If you want to test without the Inspector, the local server is an ordinary HTTP endpoint:

```bash
curl -X POST http://localhost:8088/responses \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello, what can you do?"}'
```

> **Optional:** in GitHub Copilot Chat the `/validate-microsoft-foundry-hosted-agent` command produces a report on the project against Foundry best practices. It's a **chat** command, not a terminal one, and it does not replace running the agent.

---

## 4. Publish the agent to Foundry

Only deploy once you're happy with the local behavior.

1. **Foundry Toolkit** sidebar → **Developer Tools** → **Build** → **Deploy to Microsoft Foundry**.
2. If **Foundry Project Setup** appears: select subscription and project → **Next**. Otherwise check that the default project is the right one.
3. **Basics**:
   - **Deployment method**: `Code`
   - **Package mode**: `Remote` (the Toolkit packages the source, Foundry restores the dependencies at provisioning time)
   - **New agent** → give it a name. *(To ship a change to an existing agent you pick **Existing agent** instead: that creates a **new version**, it does not modify the previous one.)*
   - **Next**
4. **Review + Deploy** — check:
   - **Language / Runtime Version**: `Python 3.13` (it must match the manifest and your local environment)
   - **Entry Point**: `python3 main.py`
   - **CPU and Memory** (they affect runtime costs)
   - that the **source directory** matches the service's *project path* in `azure.yaml`
5. **Deploy**, then follow the notifications and the **Output** panel.

**Verification (mandatory, don't skip it):** a create request that succeeded does **not** prove the runtime is ready.

- **My Resources** → **Agents** → **Hosted Agent** → select the agent's name.
- On the **Details** tab wait until the status says the agent is **running**, and copy the **endpoint**.
- Open the **Playground** and send **the same prompt and the same follow-up** you used locally.

> **Teaching point:** local and remote execution use **different** credentials, dependency environments and network paths. A response locally does not guarantee a response in the cloud — that's why we repeat the same prompt. And remember: signing in locally does **not** transfer your user's permissions to the deployed agent; the agent has its own **dedicated Entra identity**, created by the platform.

Three packaging modes compared, worth a minute:

| Mode | What it does | When to choose it |
|---|---|---|
| **Code + Remote** | the Toolkit packages the source into a ZIP, Foundry installs the dependencies | recommended starting point — no local Docker build |
| **Code + Bundled** | the Toolkit runs the *Package Command* locally (for Python it prepares the wheels in `packages/`) and then creates the ZIP | when you need Linux dependencies prepared up front |
| **Container (ACR)** | build and push of the image via ACR (remote build), or an ACR image that's already available | custom runtime, or an existing image to reuse |

---

## 5. Invoke the agent with a Responses call

The deploy gives the agent an **endpoint** for programmatic use: **no separate "publish" step is needed** to reach it via API. (Distribution to Teams / Microsoft 365 is a separate activity.)

Copy the endpoint from the agent's **Details** tab, then:

### 5.1 From the Toolkit / from the command line

```bash
# playground remoto in VS Code:
# Developer Tools → Build → Hosted Agent Playground → selezionate l'agente

# oppure, con la Azure Developer CLI sul progetto hosted-agent:
azd ai agent invoke "Hello, what can you do?"
azd ai agent invoke --local "Hello, what can you do?"   # contro localhost:8088
```

### 5.2 With an OpenAI-compatible client (Python)

The agent exposes an **OpenAI-compatible** `/responses` endpoint: any compatible SDK can call it.

```python
import os
from azure.identity import AzureCliCredential, get_bearer_token_provider
from openai import OpenAI

credential = AzureCliCredential()
token_provider = get_bearer_token_provider(
    credential, "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url=os.environ["AGENT_ENDPOINT"],   # endpoint copiato da Details
    api_key=token_provider(),                # token Entra, non una chiave statica
)

resp = client.responses.create(
    model=os.environ["AGENT_NAME"],
    input="Hello, what can you do?",
)
print(resp.output_text)

# secondo turno: la piattaforma gestisce la history della conversazione
follow_up = client.responses.create(
    model=os.environ["AGENT_NAME"],
    input="And can you make it shorter?",
    previous_response_id=resp.id,
)
print(follow_up.output_text)
```

### 5.3 With `curl`

```bash
curl -X POST "$AGENT_ENDPOINT/responses" \
  -H "Authorization: ****** account get-access-token \
        --scope https://ai.azure.com/.default --query accessToken -o tsv)" \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello, what can you do?"}'
```

> **The message to leave the room with:** this is **exactly** the same call you'd make against a *prompt agent*. Whoever consumes the agent doesn't know — and doesn't need to know — whether there's a declarative configuration or ten thousand lines of your code behind it. That's the destination of this entire section.

---

## 6. Lifecycle: after the first publish

| Activity | Where |
|---|---|
| Status, configuration, copyable endpoint | **Details** |
| Try a specific version | **version** selector in the playground (*Automatic* follows the version chosen by the service endpoint, **not necessarily the latest**) |
| Sessions and runtime logs | **Sessions** → session log (runtime logs require a session; build output is separate) |
| Retrieve the deployed source | **Download code asset** (only for ZIP deploys; an image deploy exposes the image reference) |
| Update the behavior | change the code, test locally, deploy again with **Existing agent** → new version |
| Quality and observability | **Traces** and **Evaluation** tabs |
| Remove the agent | **Delete Hosted Agent** (deletes agent, versions and sessions; it does **not** clean up every related Azure resource) |

---

## 7. Checklist for the presenter

- [ ] `az login` already done and the right subscription selected
- [ ] Foundry project in a region that supports hosted agents
- [ ] A compatible model deployment already in place (don't create it in front of the room)
- [ ] Python 3.13 environment already created and dependencies already installed (installing live is dead time)
- [ ] Port 8088 free
- [ ] A prompt and a follow-up decided in advance, to be reused **identically** locally and in the cloud
- [ ] An already-deployed agent as a **plan B**, in case the live deploy is slow
- [ ] Endpoint and agent name already exported as environment variables for the final Responses call

---

## 8. Common errors and how to fix them

| Symptom | Likely cause |
|---|---|
| Agent Inspector won't connect | the server didn't start (opening the Inspector doesn't start it): check terminal, interpreter, dependencies, `az login`, port 8088 |
| `AuthenticationError` locally | expired token → run `az login` again |
| The deploy "succeeds" but the agent doesn't respond | the create request doesn't guarantee the runtime is ready: wait for the *running* status in **Details** and read the deploy output |
| Works locally, fails in the cloud | different credentials and dependencies: check what `azure.yaml` declares as env, and remember that the local `.env` is not forwarded in full |
| Container image rejected | the platform requires **x86_64 (linux/amd64)** images: on Apple Silicon use `docker build --platform linux/amd64 .` |
| Variables missing at runtime | declare them on the service in `azure.yaml`; for secrets use a project **connection**, never the packaged `.env` |

---

## References

- Create and deploy a hosted agent in Foundry Toolkit for VS Code — https://code.visualstudio.com/docs/intelligentapps/hosted-agents
- Create hosted agents with Microsoft Foundry Toolkit for VS Code — https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/vs-code-agents-workflow-pro-code
- Deploy a hosted agent — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/deploy-hosted-agent
- Run a hosted agent locally with the Azure Developer CLI — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/run-hosted-agent-locally
- Hands-on lab: Foundry Toolkit for VS Code — https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab
