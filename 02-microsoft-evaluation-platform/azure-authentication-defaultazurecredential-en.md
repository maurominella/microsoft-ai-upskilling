# Azure Authentication with bearer tokens and `DefaultAzureCredential`: what changed by 2026

When working with Azure services, we need to keep three concepts separate: **identity**, **token audience**, and **authorization**. Many authentication problems arise from mixing them together.

## Resource, audience, and scope

Microsoft Entra ID issues an access token for a specific **audience**, meaning the service expected to accept it. The audience does not necessarily match the REST endpoint being called.

For example:

- Azure Resource Manager: `https://management.azure.com/`
- Azure Key Vault: `https://vault.azure.net`
- Azure Service Bus: `https://servicebus.azure.net/`
- Azure Event Hubs: `https://eventhubs.azure.net/`
- Azure SQL: `https://database.windows.net/`
- Microsoft Graph: `https://graph.microsoft.com/`
- Azure AI Search: `https://search.azure.com/`

Azure AD Graph, identified by `https://graph.windows.net/`, is now legacy. New applications should use Microsoft Graph.

With Azure CLI, we can request a token using the v1 resource-based syntax:

```bash
az account get-access-token --resource https://search.azure.com
```

Azure Identity and modern OAuth 2.0 flows generally use the equivalent scope ending in `/.default`:

```python
token = credential.get_token("https://search.azure.com/.default")
```

`/.default` asks Entra ID for a token containing the permissions already configured for that application or identity. It does not mean "grant every permission."

It is also incorrect to assume that the audience is always a global endpoint. This is true for many services, but some, such as certain healthcare APIs, use the URL of the specific service instance. Always verify the service documentation.

## A valid token does not guarantee access

Obtaining a bearer token proves that Entra ID recognized the identity. It does not prove that the identity is authorized to perform the requested operation.

For a request to succeed, all these elements must be correct:

1. Tenant and identity.
2. Audience or scope.
3. Endpoint and API version.
4. RBAC role assigned to the correct principal.
5. Scope of the RBAC assignment: subscription, resource group, account, or project.

A service can therefore return `401 PermissionDenied` even when the token itself is perfectly valid.

## Azure OpenAI and Microsoft Foundry

Several API surfaces coexist in 2026. Classic Azure OpenAI APIs still commonly use:

```python
"https://cognitiveservices.azure.com/.default"
```

The newer Microsoft Foundry Models v1 API instead documents:

```python
"https://ai.azure.com/.default"
```

V1 endpoints take forms such as:

```text
https://<resource>.openai.azure.com/openai/v1/
https://<resource>.services.ai.azure.com/openai/v1/
```

The endpoint, deployment, and scope must be selected as one coherent set. Copying a scope from an example for a different API generation is not reliable.

## The "magic" of `DefaultAzureCredential`

`DefaultAzureCredential`, available in Azure Identity libraries for the main programming languages, is a preconfigured credential chain. In Python, it broadly attempts:

1. `EnvironmentCredential`
2. `WorkloadIdentityCredential`
3. `ManagedIdentityCredential`
4. Cached credentials or Visual Studio Code credentials
5. `AzureCliCredential`
6. `AzurePowerShellCredential`
7. `AzureDeveloperCliCredential`
8. Brokered authentication, when available

The chain stops as soon as one credential successfully acquires a token. This is the crucial detail: **it does not necessarily select the identity we think we are using**.

If `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and `AZURE_CLIENT_SECRET` are present in the environment, `EnvironmentCredential` is attempted before the Azure CLI session. Running `az logout` followed by `az login` changes nothing in that situation: the code continues using the service principal configured through environment variables.

Furthermore, fallback applies to token acquisition. If a credential obtains a token but the service returns `401` or `403`, `DefaultAzureCredential` does not retry the request with a second identity.

This is exactly what we observed: the notebook acquired a token for a service principal defined in `.env`, while the Foundry roles had been assigned to the user authenticated through Azure CLI.

## Preserving compatibility without ambiguity

During development, we can continue using `DefaultAzureCredential`, but we should control its chain:

```python
credential = DefaultAzureCredential(
    exclude_environment_credential=True
)
```

Recent Azure Identity versions also let us configure it through `AZURE_TOKEN_CREDENTIALS`:

```bash
export AZURE_TOKEN_CREDENTIALS=dev
```

Alternatively, we can restrict it to one credential:

```bash
export AZURE_TOKEN_CREDENTIALS=AzureCliCredential
```

```python
credential = DefaultAzureCredential(require_envvar=True)
```

When we want an explicit chain, we can use `ChainedTokenCredential`:

```python
credential = ChainedTokenCredential(
    AzureCliCredential(),
    AzureDeveloperCliCredential(),
)
```

For production, Microsoft often recommends a deterministic credential, normally `ManagedIdentityCredential`, rather than a long implicit chain:

```python
credential = ManagedIdentityCredential()
```

The modern principle is no longer simply "the same code everywhere." It is **the same `TokenCredential` contract, with intentional and verifiable identity selection for each environment**.

## Diagnostics

To determine which credential was selected, enable Azure Identity logging:

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("azure.identity").setLevel(logging.DEBUG)
```

`DEBUG` logs can contain sensitive identifiers and should not be shared indiscriminately.

It is also useful to compare the token's `oid` claim with the object ID of the Azure CLI user:

```bash
az ad signed-in-user show --query id -o tsv
```

The main lesson is this: `DefaultAzureCredential` does not mean "use my Azure login." It means "use the first configured identity that can acquire a token." The convenience remains valuable, but in 2026 it should be paired with explicit configuration, logging, and role assignments for the principal actually being used.

## References

- [Credential chains in the Azure Identity library for Python](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains)
- [DefaultAzureCredential for Python](https://learn.microsoft.com/python/api/azure-identity/azure.identity.defaultazurecredential)
- [Azure CLI: `az account get-access-token`](https://learn.microsoft.com/cli/azure/account#az-account-get-access-token)
- [Microsoft Entra ID authentication for Azure OpenAI](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/managed-identity)
- [Microsoft Foundry Models: keyless authentication](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/configure-entra-id)
