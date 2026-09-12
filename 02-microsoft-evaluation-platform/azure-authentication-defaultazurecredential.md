# Azure Authentication con bearer token e `DefaultAzureCredential`: cosa è cambiato nel 2026

Quando lavoriamo con i servizi Azure dobbiamo tenere separati tre concetti: **identità**, **destinatario del token** e **autorizzazioni**. Molti problemi di autenticazione nascono proprio dal confonderli.

## Resource, audience e scope

Un access token è emesso da Microsoft Entra ID per una determinata **audience**, cioè il servizio che dovrà accettarlo. L'audience non coincide necessariamente con l'endpoint REST chiamato.

Per esempio:

- Azure Resource Manager: `https://management.azure.com/`
- Azure Key Vault: `https://vault.azure.net`
- Azure Service Bus: `https://servicebus.azure.net/`
- Azure Event Hubs: `https://eventhubs.azure.net/`
- Azure SQL: `https://database.windows.net/`
- Microsoft Graph: `https://graph.microsoft.com/`
- Azure AI Search: `https://search.azure.com/`

Azure AD Graph, identificato da `https://graph.windows.net/`, è ormai legacy: per le nuove applicazioni bisogna usare Microsoft Graph.

Con Azure CLI possiamo richiedere un token usando la sintassi v1 basata sulla risorsa:

```bash
az account get-access-token --resource https://search.azure.com
```

Con Azure Identity e i protocolli OAuth 2.0 moderni si usa generalmente lo scope equivalente, terminato da `/.default`:

```python
token = credential.get_token("https://search.azure.com/.default")
```

`/.default` chiede a Entra ID un token contenente le autorizzazioni già configurate per quell'applicazione o identità. Non significa "assegna tutte le autorizzazioni".

È inoltre sbagliato affermare che l'audience sia sempre un endpoint globale. Per molti servizi lo è, ma alcuni servizi, come determinate API sanitarie, usano l'URL della specifica istanza. Bisogna quindi verificare la documentazione del servizio.

## Un token valido non garantisce l'accesso

Ottenere un bearer token dimostra che Entra ID ha riconosciuto l'identità. Non dimostra che tale identità sia autorizzata a eseguire l'operazione richiesta.

Perché una chiamata funzioni devono essere corretti tutti questi elementi:

1. Tenant e identità.
2. Audience o scope.
3. Endpoint e versione dell'API.
4. Ruolo RBAC assegnato al principal corretto.
5. Scope dell'assegnazione RBAC: subscription, resource group, account o progetto.

Un `401 PermissionDenied` può quindi essere restituito anche quando il token è perfettamente valido.

## Azure OpenAI e Microsoft Foundry

Nel 2026 convivono diverse superfici API. Con le API Azure OpenAI classiche si incontra ancora frequentemente:

```python
"https://cognitiveservices.azure.com/.default"
```

La nuova API Microsoft Foundry Models v1 documenta invece:

```python
"https://ai.azure.com/.default"
```

Gli endpoint v1 assumono forme come:

```text
https://<resource>.openai.azure.com/openai/v1/
https://<resource>.services.ai.azure.com/openai/v1/
```

Endpoint, deployment e scope devono quindi essere scelti come insieme coerente. Non è prudente copiare lo scope da un esempio relativo a una diversa generazione dell'API.

## La "magia" di `DefaultAzureCredential`

`DefaultAzureCredential`, disponibile nelle librerie Azure Identity dei principali linguaggi, è una catena preconfigurata di credenziali. In Python prova indicativamente:

1. `EnvironmentCredential`
2. `WorkloadIdentityCredential`
3. `ManagedIdentityCredential`
4. Credenziali memorizzate o di Visual Studio Code
5. `AzureCliCredential`
6. `AzurePowerShellCredential`
7. `AzureDeveloperCliCredential`
8. Autenticazione tramite broker, quando disponibile

La catena si ferma appena una credenziale riesce a ottenere un token. Questo è il dettaglio decisivo: **non sceglie necessariamente l'identità con cui pensiamo di lavorare**.

Se nell'ambiente sono presenti `AZURE_CLIENT_ID`, `AZURE_TENANT_ID` e `AZURE_CLIENT_SECRET`, `EnvironmentCredential` viene provata prima della sessione Azure CLI. Un successivo `az logout` o `az login` non cambia nulla: il codice continuerà a usare il service principal configurato nelle variabili d'ambiente.

Inoltre, il fallback riguarda l'acquisizione del token. Se una credenziale ottiene un token ma il servizio restituisce `401` o `403`, `DefaultAzureCredential` non riprova la richiesta usando una seconda identità.

È esattamente ciò che abbiamo osservato: il notebook otteneva un token per un service principal definito nella `.env`, mentre i ruoli Foundry erano assegnati all'utente autenticato tramite Azure CLI.

## Come mantenere la compatibilità senza ambiguità

In sviluppo possiamo continuare a usare `DefaultAzureCredential`, ma dobbiamo controllarne la catena:

```python
credential = DefaultAzureCredential(
    exclude_environment_credential=True
)
```

Nelle versioni recenti di Azure Identity possiamo configurarla anche tramite `AZURE_TOKEN_CREDENTIALS`:

```bash
export AZURE_TOKEN_CREDENTIALS=dev
```

Oppure limitarla a una credenziale specifica:

```bash
export AZURE_TOKEN_CREDENTIALS=AzureCliCredential
```

```python
credential = DefaultAzureCredential(require_envvar=True)
```

Quando vogliamo una catena esplicita possiamo usare `ChainedTokenCredential`:

```python
credential = ChainedTokenCredential(
    AzureCliCredential(),
    AzureDeveloperCliCredential(),
)
```

In produzione Microsoft raccomanda spesso una credenziale deterministica, normalmente `ManagedIdentityCredential`, invece di una lunga catena implicita:

```python
credential = ManagedIdentityCredential()
```

Il principio moderno non è più semplicemente "lo stesso codice ovunque", ma **lo stesso contratto `TokenCredential`, con una selezione dell'identità intenzionale e verificabile per ciascun ambiente**.

## Diagnostica

Per capire quale credenziale è stata scelta, abilitiamo i log di Azure Identity:

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("azure.identity").setLevel(logging.DEBUG)
```

I log di livello `DEBUG` possono contenere identificatori sensibili e non devono essere pubblicati indiscriminatamente.

È utile anche confrontare l'`oid` del token con l'object ID dell'utente CLI:

```bash
az ad signed-in-user show --query id -o tsv
```

La lezione più importante è questa: `DefaultAzureCredential` non significa "usa il mio login Azure". Significa "usa la prima identità configurata che riesce a ottenere un token". La comodità rimane, ma nel 2026 va accompagnata da configurazione esplicita, logging e ruoli assegnati al principal realmente utilizzato.

## Riferimenti

- [Credential chains in the Azure Identity library for Python](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains)
- [DefaultAzureCredential per Python](https://learn.microsoft.com/python/api/azure-identity/azure.identity.defaultazurecredential)
- [Azure CLI: `az account get-access-token`](https://learn.microsoft.com/cli/azure/account#az-account-get-access-token)
- [Microsoft Entra ID authentication for Azure OpenAI](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/managed-identity)
- [Microsoft Foundry Models: keyless authentication](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/configure-entra-id)
