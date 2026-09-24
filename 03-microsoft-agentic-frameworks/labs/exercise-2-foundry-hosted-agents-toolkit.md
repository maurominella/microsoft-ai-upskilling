# Demo script — Il tuo primo Hosted Agent su Microsoft Foundry

**Workshop:** Agentic AI on Microsoft Foundry · Day 1 — Theme 3 · Hosted Agents
**Demo:** LIVE DEMO 3 — *Building a hosted agent with Microsoft Foundry Toolkit for VS Code*
**Durata indicativa:** 35–45 minuti
**Percorso:** installazione estensione → scelta del sample → esplorazione del progetto (`requirements.txt`, `.env`, `azure.yaml`) → test in locale con Agent Inspector → deploy su Foundry → invocazione con una chiamata **Responses**

> Le etichette dell'interfaccia (menu, pulsanti, nomi dei file) sono riportate **in inglese**, come appaiono nel prodotto. Il catalogo dei sample e i nomi dei comandi possono cambiare tra una release e l'altra dell'estensione: se una voce non coincide, cercatela con la Command Palette (`Ctrl+Shift+P`).

---

## 0. Prerequisiti (da verificare PRIMA della sessione)

| Requisito | Dettaglio |
|---|---|
| Visual Studio Code | versione corrente, con la **Microsoft Foundry Toolkit** extension |
| Python | **3.13** + estensione *Python* per VS Code (incluso il supporto al debugger) |
| Azure CLI | per l'autenticazione locale (`az login`) |
| Sottoscrizione Azure | con un **Foundry project** in una region che supporta gli hosted agent |
| Model deployment | un modello compatibile con il sample; il *Basic Hosted Agent* è configurato per un modello *mini* — usate un deployment già esistente |
| Permessi | ruolo **Foundry Project Manager** a livello di progetto (crea l'agente e assegna i ruoli all'identità dell'agente) |

**Cosa NON serve:** Docker in locale. Il percorso principale di questa demo è il **deploy da codice sorgente** (*Code* + package mode *Remote*): il Toolkit carica uno ZIP del sorgente e Foundry installa le dipendenze durante il provisioning. Docker/ACR servono solo se scegliete esplicitamente il percorso *Container*.

> ⚠️ **Attenzione ai costi:** anche l'esecuzione locale invia le richieste al modello deployato su Foundry, quindi consuma token. Anche CPU e memoria scelte al momento del deploy incidono sui costi di runtime.

---

## 1. Installare l'estensione

1. In VS Code aprite **Extensions** (`Ctrl+Shift+X`).
2. Cercate **Microsoft Foundry Toolkit** e installatela.
3. Compare una nuova icona **Foundry Toolkit** nella **Activity Bar** (barra laterale sinistra). Apritela.
4. Fate il sign-in ad Azure quando richiesto, e selezionate **subscription** e **project** di lavoro.

**Cosa far notare all'aula:** la sidebar ha due blocchi che useremo per tutta la demo — **Developer Tools** (Build: *Create Agent*, *Deploy to Microsoft Foundry*, *Hosted Agent Playground*) e **My Resources** (Agents, Models, Tools).

---

## 2. Creare il progetto da un sample

1. Sidebar **Foundry Toolkit** → **Developer Tools** → **Build** → **Create Agent**.
2. Nella sezione **Code an agent from samples** trovate tre starter "hello-world": **Agent Framework**, **Copilot SDK**, **LangGraph**.
   - Per questa demo: **Agent Framework** (apre direttamente il sample *Basic Responses*).
   - In alternativa **Browse all samples** apre la gallery completa: filtrate per **Language = Python**, **Framework = Agent Framework**, **Protocol Type = Responses** e scegliete **Basic Hosted Agent**.
3. **Next** → nella scheda **Create**:
   - **Workspace Folder**: scegliete la cartella di destinazione (se non è vuota, indicate un **Folder Name** per creare una sottocartella).
   - **Environment Setup**: *Setup with Microsoft Foundry* → subscription + project.
   - **Model Deployment**: selezionate il deployment già esistente.
4. **Create**, poi aprite il **README.md** del progetto generato.

> **Punto didattico:** *Skip for now* genera il codice senza completare la configurazione del modello — dovrete comunque compilarla prima di eseguire. E *Deploy & use new model* crea un **deployment di modello**, non l'hosted agent. Creare i file **non è** un deploy.

### 2.1 Anatomia del progetto generato

Tenete aperta come **workspace root** la cartella che contiene `azure.yaml`.

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

**Da mostrare a schermo, uno per uno:**

- **`main.py`** — la logica dell'agente è **la stessa** vista nelle demo precedenti con Agent Framework. L'unica aggiunta è il guscio che espone l'agente come server **Responses**. Questo è il messaggio chiave dell'intera sezione: *non riscriviamo l'agente per ospitarlo*.
- **`requirements.txt`** — la dichiarazione delle dipendenze. È il file che Foundry userà per ricostruire l'ambiente in cloud nel package mode *Remote*, ed è lo stesso che usate voi in locale. Contiene anche `debugpy` per il debug.
- **`azure.yaml`** — dove vivono runtime, entry point, protocolli e le variabili d'ambiente del servizio. **Rivedetelo e salvatelo prima del deploy**: il deploy risolve i valori dichiarati qui dal `.env` della source directory o dall'ambiente di processo, **non** inoltra automaticamente ogni voce del `.env` locale.
- **`.env`** — configurazione **locale**. Non va mai committata né impacchettata.

---

## 3. Eseguire e testare in locale

```bash
# 1. selezionare l'ambiente Python 3.13
#    Command Palette → "Python: Create Environment" oppure "Python: Select Interpreter"

# 2. installare le dipendenze, dalla source directory del sample
cd src/<nome-sample>
python -m pip install -r requirements.txt

# 3. autenticarsi: le credenziali locali dell'agente arrivano da qui
az login
```

Controllate il `.env` nella source directory e, se il setup non le ha già compilate, valorizzate:

```dotenv
FOUNDRY_PROJECT_ENDPOINT=<endpoint del vostro progetto Foundry>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<nome del model deployment>
```

Poi lanciate l'agente:

1. Vista **Run and Debug** → configurazione **Debug Local Agent HTTP Server** → **F5**.
2. I task avviano il server sulla porta **8088**, aprono **Agent Inspector** e agganciano il debugger.
3. In Agent Inspector inviate un messaggio, ad esempio: *"Suggest a name for a weather app."* — poi una **domanda di follow-up collegata**, per dimostrare la conversazione multi-turno.

**Cosa far notare:**

- Agent Inspector mostra la risposta, le eventuali **tool call**, la **latency waterfall** e la **run timeline**.
- Mettete un **breakpoint** in `main.py` e rilanciate: si ferma davvero. È codice vostro, con il vostro debugger. Questo è l'argomento più convincente per una platea di sviluppatori.
- Aprire Agent Inspector da solo **non** avvia il server. Se la connessione fallisce, controllate nell'ordine: output del terminale, interprete selezionato, dipendenze installate, credenziali (`az login`), porta 8088 libera.

Volendo testare senza l'Inspector, il server locale è un normale endpoint HTTP:

```bash
curl -X POST http://localhost:8088/responses \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello, what can you do?"}'
```

> **Facoltativo:** in GitHub Copilot Chat il comando `/validate-microsoft-foundry-hosted-agent` produce un report del progetto rispetto alle best practice Foundry. È un comando di **chat**, non di terminale, e non sostituisce l'esecuzione dell'agente.

---

## 4. Pubblicare l'agente su Foundry

Fate il deploy solo quando il comportamento locale vi soddisfa.

1. Sidebar **Foundry Toolkit** → **Developer Tools** → **Build** → **Deploy to Microsoft Foundry**.
2. Se compare **Foundry Project Setup**: selezionate subscription e project → **Next**. Altrimenti verificate che il progetto di default sia quello giusto.
3. **Basics**:
   - **Deployment method**: `Code`
   - **Package mode**: `Remote` (il Toolkit impacchetta il sorgente, Foundry ripristina le dipendenze in fase di provisioning)
   - **New agent** → date un nome. *(Per rilasciare una modifica a un agente esistente si sceglie invece **Existing agent**: si crea una **nuova versione**, non si modifica quella precedente.)*
   - **Next**
4. **Review + Deploy** — verificate:
   - **Language / Runtime Version**: `Python 3.13` (deve corrispondere al manifest e al vostro ambiente locale)
   - **Entry Point**: `python3 main.py`
   - **CPU and Memory** (incidono sui costi di runtime)
   - che la **source directory** coincida con il *project path* del servizio in `azure.yaml`
5. **Deploy**, poi seguite le notifiche e il pannello **Output**.

**Verifica (obbligatoria, non saltatela):** una create request andata a buon fine **non** dimostra che il runtime sia pronto.

- **My Resources** → **Agents** → **Hosted Agent** → selezionate il nome dell'agente.
- Nella scheda **Details** attendete che lo stato indichi che l'agente è **running**, e copiate l'**endpoint**.
- Aprite il **Playground** e inviate **lo stesso prompt e lo stesso follow-up** usati in locale.

> **Punto didattico:** esecuzione locale e remota usano credenziali, ambienti di dipendenze e percorsi di rete **diversi**. Una risposta in locale non garantisce una risposta in cloud — per questo ripetiamo lo stesso prompt. E ricordate: il sign-in locale **non** trasferisce i permessi del vostro utente all'agente deployato; l'agente ha una propria **identità Entra dedicata**, creata dalla piattaforma.

Tre modalità di packaging a confronto, da citare in un minuto:

| Modalità | Cosa fa | Quando sceglierla |
|---|---|---|
| **Code + Remote** | il Toolkit impacchetta il sorgente in ZIP, Foundry installa le dipendenze | punto di partenza consigliato — nessuna build Docker locale |
| **Code + Bundled** | il Toolkit esegue il *Package Command* in locale (per Python prepara le wheel in `packages/`) e poi crea lo ZIP | quando servono dipendenze Linux già preparate |
| **Container (ACR)** | build e push dell'immagine tramite ACR (build remota), oppure immagine ACR già pronta | runtime custom, o immagine esistente da riutilizzare |

---

## 5. Invocare l'agente con una chiamata Responses

Il deploy dà all'agente un **endpoint** per uso programmatico: **non serve un passaggio di "publish" separato** per accedervi via API. (La distribuzione su Teams / Microsoft 365 è invece un'attività a parte.)

Copiate l'endpoint dalla scheda **Details** dell'agente, poi:

### 5.1 Dal Toolkit / da riga di comando

```bash
# playground remoto in VS Code:
# Developer Tools → Build → Hosted Agent Playground → selezionate l'agente

# oppure, con la Azure Developer CLI sul progetto hosted-agent:
azd ai agent invoke "Hello, what can you do?"
azd ai agent invoke --local "Hello, what can you do?"   # contro localhost:8088
```

### 5.2 Con un client OpenAI-compatibile (Python)

L'agente espone un endpoint `/responses` **OpenAI-compatible**: qualunque SDK compatibile lo può chiamare.

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

### 5.3 Con `curl`

```bash
curl -X POST "$AGENT_ENDPOINT/responses" \
  -H "Authorization: Bearer $(az account get-access-token \
        --scope https://ai.azure.com/.default --query accessToken -o tsv)" \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello, what can you do?"}'
```

> **Il messaggio da lasciare in aula:** questa è **esattamente** la stessa chiamata che fareste verso un *prompt agent*. Chi consuma l'agente non sa — e non deve sapere — se dietro c'è una configurazione dichiarativa o diecimila righe di codice vostro. È il punto di arrivo di tutta la sezione.

---

## 6. Ciclo di vita: dopo la prima pubblicazione

| Attività | Dove |
|---|---|
| Stato, configurazione, endpoint copiabile | **Details** |
| Provare una versione specifica | selettore di **versione** nel playground (*Automatic* segue la versione scelta dall'endpoint del servizio, **non necessariamente l'ultima**) |
| Sessioni e log di runtime | **Sessions** → log della sessione (i log di runtime richiedono una sessione; l'output di build è separato) |
| Recuperare il sorgente deployato | **Download code asset** (solo per deploy ZIP; un deploy da immagine espone il riferimento all'immagine) |
| Aggiornare il comportamento | modificate il codice, testate in locale, ripetete il deploy con **Existing agent** → nuova versione |
| Qualità e osservabilità | schede **Traces** e **Evaluation** |
| Rimuovere l'agente | **Delete Hosted Agent** (elimina agente, versioni e sessioni; **non** fa pulizia di tutte le risorse Azure collegate) |

---

## 7. Checklist per chi presenta

- [ ] `az login` già fatto e sottoscrizione giusta selezionata
- [ ] Progetto Foundry in una region che supporta gli hosted agent
- [ ] Model deployment compatibile già esistente (non crearlo davanti all'aula)
- [ ] Ambiente Python 3.13 già creato e dipendenze già installate (l'installazione dal vivo è tempo morto)
- [ ] Porta 8088 libera
- [ ] Un prompt e un follow-up decisi in anticipo, da riusare **identici** in locale e in cloud
- [ ] Un agente già deployato come **piano B**, nel caso il deploy dal vivo sia lento
- [ ] Endpoint e nome dell'agente già esportati come variabili d'ambiente per la chiamata Responses finale

---

## 8. Errori frequenti e come risolverli

| Sintomo | Causa probabile |
|---|---|
| Agent Inspector non si connette | il server non è partito (aprire l'Inspector non lo avvia): controllate terminale, interprete, dipendenze, `az login`, porta 8088 |
| `AuthenticationError` in locale | token scaduto → rieseguite `az login` |
| Il deploy "riesce" ma l'agente non risponde | la create request non garantisce il runtime pronto: attendete lo stato *running* in **Details** e leggete l'output del deploy |
| Funziona in locale, fallisce in cloud | credenziali e dipendenze diverse: verificate ciò che `azure.yaml` dichiara come env, e ricordate che il `.env` locale non viene inoltrato per intero |
| Immagine container rifiutata | la piattaforma richiede immagini **x86_64 (linux/amd64)**: su Apple Silicon usate `docker build --platform linux/amd64 .` |
| Variabili mancanti a runtime | dichiaratele nel servizio in `azure.yaml`; per i segreti usate una **connection** del progetto, mai il `.env` impacchettato |

---

## Riferimenti

- Create and deploy a hosted agent in Foundry Toolkit for VS Code — https://code.visualstudio.com/docs/intelligentapps/hosted-agents
- Create hosted agents with Microsoft Foundry Toolkit for VS Code — https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/vs-code-agents-workflow-pro-code
- Deploy a hosted agent — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/deploy-hosted-agent
- Run a hosted agent locally with the Azure Developer CLI — https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/run-hosted-agent-locally
- Hands-on lab: Foundry Toolkit for VS Code — https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab
