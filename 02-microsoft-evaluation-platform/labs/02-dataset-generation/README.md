# Lab 02 - Generate simulated data for evaluation

**Estimated duration:** 30-40 minutes

**Notebook:** `lab02_dataset_generation_solution.ipynb`

## Objective

In this lab you will run a complete example that uses the Azure AI Evaluation SDK `Simulator` to generate a grounded, multi-turn conversation before production data is available.

You will:

1. configure access to an Azure OpenAI deployment and a Microsoft Foundry project;
2. create a Prompty-based chat application;
3. test the application with a single prompt and an existing conversation history;
4. extend the sample conversation manually;
5. connect the application to `Simulator` through an asynchronous callback;
6. generate and inspect a five-turn conversation grounded in a local document.

This notebook covers non-adversarial conversation simulation. It does not run adversarial, direct prompt injection, or indirect prompt injection simulations.

## Prerequisites

Before starting, verify that:

- the workshop Python environment and Jupyter kernel are available;
- the dependencies used by the notebook are installed, including `azure-ai-evaluation`, `azure-identity`, `openai`, `prompty`, and `python-dotenv`;
- you are authenticated to Azure with an identity supported by `DefaultAzureCredential`;
- your identity can access the configured Azure OpenAI deployment and Microsoft Foundry project;
- a `.env` file is available and can be discovered by `python-dotenv`.

The notebook expects these environment variables:

```dotenv
AZURE_OPENAI_API_VERSION=<api-version>
AZURE_OPENAI_ENDPOINT=<azure-openai-endpoint>
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=<chat-model-deployment>
FOUNDRY_PROJECT_ENDPOINT=<foundry-project-endpoint>
```

Open `lab02_dataset_generation_solution.ipynb` from the `02-dataset-generation` folder. Relative paths in the notebook depend on this working directory.

## Lab files

```text
02-dataset-generation/
├── lab02_dataset_generation_solution.ipynb  <- run this notebook
├── README.md
└── eval_assets/
   ├── conversation_simulation.prompty       <- created or overwritten by the notebook
   ├── friendly_conversation_history_en.txt
   └── friendly_conversation_history_it.txt

../data/
└── documents.txt                            <- grounding source
```

## Instructions

Run the notebook from top to bottom. All code is already complete and ready to execute.

### 1. Configure authentication and the model

Run cells 2 and 3.

The setup code:

- loads the environment variables from `.env`;
- creates a `DefaultAzureCredential` with the environment credential excluded;
- derives the OpenAI-compatible endpoint from `FOUNDRY_PROJECT_ENDPOINT`;
- registers a credential-backed Prompty connection named `workshop-foundry`;
- creates the `AzureOpenAIModelConfiguration` used by the simulator.

Confirm that the four configuration values are printed and that no endpoint or authentication error is raised.

### 2. Create the Prompty application

Read cell 4, then run cell 5.

The cell writes `eval_assets/conversation_simulation.prompty`. The Prompty accepts three inputs:

- `context`: grounding information for the answer;
- `query`: the latest user message;
- `conversation_history`: the preceding messages, represented as a Prompty `thread`.

The application uses the registered `workshop-foundry` connection so that Prompty and the notebook use the same Azure credential. Running the cell overwrites the existing Prompty file.

### 3. Smoke-test the application

Run cell 7.

The `run_application` function wraps `prompty.invoke()` and provides the three inputs expected by the Prompty. The included request asks how to make pizza at home and renders the response as Markdown. A successful response confirms that the application works before it is connected to the simulator.

### 4. Load and inspect a sample conversation

Run cells 8 and 9.

Cell 8 loads `friendly_conversation_history_it.txt` and displays the parsed JSON conversation. To use the English sample instead, change the file name to `friendly_conversation_history_en.txt`.

Cell 9:

1. prints each message number, role, and content;
2. passes the latest item as the current query and all preceding items as conversation history;
3. invokes the Prompty application and prints its response.

### 5. Extend the conversation manually

Run cell 11.

The cell appends the previous model response to `conversation_history`, displays the updated conversation, and invokes the application again to generate another response. Run the cell more than once to observe the conversation continue.

This manual flow demonstrates the same message handling that the simulator callback automates.

### 6. Review the simulator callback

Read cell 12, then run cell 13.

The asynchronous `callback` function:

1. separates the latest message from the prior history;
2. extracts its grounding context;
3. invokes the synchronous Prompty application with `asyncio.to_thread()`;
4. appends the assistant response;
5. returns the updated messages in the protocol expected by `Simulator`.

The worker thread keeps the callback asynchronous while avoiding a known incompatibility between the Prompty v2 beta asynchronous client and the Entra ID token provider used by this notebook.

### 7. Prepare grounding data and initialize the simulator

Run cells 15 and 16.

The notebook reads `../data/documents.txt` as the grounding source and prints a preview of its first 1,000 characters. It then creates `CompatibleSimulator`, a small compatibility subclass that normalizes the wrapped `llm_output` returned by `azure-ai-evaluation==1.18.3`.

### 8. Generate and inspect the conversation

Run cells 17 and 18.

The simulation starts with a predefined Italian question grounded in `source_text`. The user simulator generates the following turns, while the callback produces the assistant responses. The SDK's embedded user-simulator Prompty receives the same Azure credential used by the application.

`max_conversation_turns=5` creates up to five user/assistant exchanges. Cell 18 prints the generated messages in chronological order. Verify that:

- user and assistant roles alternate;
- the answers remain related to the grounding document;
- earlier messages influence later turns;
- the result is available in `outputs[0]["messages"]`.

The notebook keeps the generated conversation in memory and does not write a dataset file to disk.

## Completion checklist

- [ ] The environment configuration is loaded and printed.
- [ ] The Prompty smoke test returns a response.
- [ ] The sample conversation and generated responses are printed.
- [ ] One or more additional turns are appended and displayed.
- [ ] The grounding text is loaded from `../data/documents.txt`.
- [ ] The simulator produces and prints a multi-turn conversation.

## Key concepts

| Concept | What to remember |
| --- | --- |
| Prompty | A portable prompt asset containing model configuration, typed inputs, and a template. |
| Grounding context | Source information supplied to keep generated answers tied to known content. |
| Conversation history | Previous messages passed separately from the latest query. |
| Callback | The adapter between the Evaluation SDK chat protocol and the application under test. |
| Simulator | The component that generates synthetic user turns and orchestrates the conversation. |
| Seed turn | The predefined first user message used to start this simulation deterministically. |
| Compatibility subclass | A temporary adapter that normalizes the simulator response format returned by the pinned SDK version. |

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| Environment variables are not loaded | Make sure a readable `.env` file is available to `python-dotenv`, then restart the kernel and run from cell 2. |
| A required environment variable raises `KeyError` | Add the missing variable listed in the prerequisites to `.env`. |
| `FOUNDRY_PROJECT_ENDPOINT must be set` | Add a valid Microsoft Foundry project endpoint to `.env`. |
| The endpoint is reported as invalid | Use a project endpoint whose host ends with `.services.ai.azure.com`. |
| Authentication or authorization fails | Sign in to Azure and verify that the selected identity has access to both the project and model deployment. The notebook excludes environment-based credentials. |
| A relative file cannot be found | Start the notebook with `02-dataset-generation` as the working directory and verify that `../data/documents.txt` exists. |
| `TypeError: object str can't be used in 'await' expression` | Keep the callback's synchronous `prompty.invoke()` call wrapped with `asyncio.to_thread()` for `prompty[foundry,jinja2]==2.0.0b3`. |
| `Unexpected user-simulator response` | Use the provided `CompatibleSimulator`; it unwraps the `llm_output` returned by `azure-ai-evaluation==1.18.3`. |