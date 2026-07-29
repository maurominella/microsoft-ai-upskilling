# Esercizio 2 — Dalla Responses API all'agente gestito
### Tema: Microsoft Foundry & Hosted Agents · Durata core: ~60 min

> **Obiettivo:** usare **Microsoft Foundry** dal codice attraverso la **Responses API**
> — il *punto d'ingresso unico* visto a slide — per far ragionare un modello sui dati di
> campagna, dargli lo strumento **Code Interpreter** per calcoli esatti, e ispezionare il
> *trace*. In chiusura, i passi concettuali verso l'**Hosted Agent**.

**Concetti che fisserai (slide Giorno 1):** Responses API come entry point unico, thread =
continuità della conversazione, tool di azione (Code Interpreter), accuratezza numerica,
osservabilità, e la distinzione Prompt Agent / **Hosted Agent**.

**Documentazione:** azure-ai-projects
<https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme> ·
Hosted agents: <https://learn.microsoft.com/azure/ai-foundry/agents/> (Deploy your first hosted agent)

---

## Prerequisiti
- Pacchetti da `requirements.txt` (`azure-ai-projects>=2.3.0`, `azure-identity`, `openai`).
- `az login` eseguito, con un ruolo assegnato sul progetto Foundry.
- In `.env`: `FOUNDRY_PROJECT_ENDPOINT` e `FOUNDRY_MODEL_NAME` (nome del *deployment* del modello).

Crea `es2_foundry.py`. All'inizio:

```python
import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

load_dotenv()
project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
MODEL = os.environ["FOUNDRY_MODEL_NAME"]
```

---

## Parte A — Responses API + continuità (thread) (≈20 min)

La Responses API è il modo con cui **qualunque** codice raggiunge i modelli di Foundry.
Il parametro `previous_response_id` collega i turni: è il concetto di **thread** visto a slide.

```python
with project.get_openai_client() as client:
    r1 = client.responses.create(
        model=MODEL,
        input=(
            "Sei un analista di RAI Pubblicità. In italiano e in una frase, "
            "spiega cosa misura il ROI di una campagna."
        ),
    )
    print("Turno 1:", r1.output_text)

    r2 = client.responses.create(
        model=MODEL,
        input="E il CPM, invece, cosa misura?",
        previous_response_id=r1.id,   # <-- continuità: il modello 'ricorda' il turno 1
    )
    print("Turno 2:", r2.output_text)
```

**Cosa dovresti vedere:** due risposte coerenti; nella seconda il modello sa che stiamo
ancora parlando di metriche pubblicitarie senza doverglielo ripetere.

---

## Parte B — Il tool Code Interpreter per numeri esatti (≈25 min)

I modelli sbagliano l'aritmetica. Diamo al modello uno **strumento di azione** che
*esegue codice* per calcolare ROI e CPM in modo esatto.

```python
with project.get_openai_client() as client:
    r = client.responses.create(
        model=MODEL,
        tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
        input=(
            "Campagna VoloBlu: budget 150000 EUR, impression 9.200.000, revenue 351000 EUR. "
            "Eseguendo codice, calcola con precisione: ROI% = (revenue-budget)/budget*100 "
            "e CPM in euro = budget/impression*1000. Rispondi in italiano con i due valori."
        ),
    )
    print(r.output_text)
```

**Cosa dovresti vedere:** **ROI = 134,0%** e **CPM ≈ 16,30 EUR**, calcolati eseguendo
codice (non "a occhio"). È lo stesso strumento della Demo 2 di ieri, qui via SDK.

---

## Parte C — Guarda dentro la risposta (osservabilità) (≈15 min)

Ogni risposta è composta da più *item*: ragionamento, chiamata al tool, messaggio finale.
Ispezionarli è l'equivalente in codice del pannello di *trace*.

```python
print("--- Item prodotti dalla Responses API ---")
for item in r.output:
    print("-", item.type)   # es. 'reasoning', 'code_interpreter_call', 'message'
```

**Cosa dovresti vedere:** tra gli item compare una **chiamata al Code Interpreter**: la
prova che il modello ha *agito*, non solo generato testo.

> ✅ **Checkpoint:** hai usato Foundry dal codice tramite la Responses API, con continuità
> di conversazione, uno strumento di azione e l'ispezione del trace. Se ti fermi qui, ottimo.

---

## 🎯 Opzionale (bonus, ≈15 min)

**B1 — Collega il tuo server MCP (ponte con l'Esercizio 3).** La Responses API accetta anche
tool di tipo **MCP**. Se hai completato l'Esercizio 3 e il server è **raggiungibile**
(vedi nota di rete sotto), aggiungi:

```python
tools=[{
    "type": "mcp",
    "server_label": "rai_campagne",
    "server_url": "https://<host-pubblico>/mcp",   # deve essere raggiungibile da Foundry
    "require_approval": "never",
}]
```
e chiedi: *"Elenca le campagne e dimmi quale ha il ROI più alto."* Il modello sceglierà da
solo gli strumenti MCP.
> 🔌 **Nota di rete:** Foundry è un servizio cloud, quindi **non** raggiunge `127.0.0.1`.
> Per questa prova esponi il server MCP con un tunnel pubblico (es. `devtunnel`/ngrok) oppure,
> se vuoi restare in locale, collega il server MCP a un modello **lato client** con l'Agent
> Framework (Esercizio 3, bonus).

**B2 — Verso l'Hosted Agent (lettura + schizzo).** Il codice dell'Esercizio 1 (Agent
Framework) può diventare un **Hosted Agent**: lo impacchetti come container/zip e Foundry lo
esegue con endpoint gestito, scaling e identità Entra. Il pattern *additivo* è che il tuo
codice chiama comunque la Responses API sull'endpoint di progetto — come hai fatto qui.
Percorso: `azure-ai-projects` → `samples/hosted_agents/` e la guida *Deploy your first hosted
agent*. (Il deploy completo del container va oltre i tempi del lab: leggi il flusso e prova a
individuare, nel tuo agente dell'Es. 1, cosa impacchetteresti.)

---

## Verifica finale / domande di riflessione
1. Perché la Responses API è definita "punto d'ingresso unico"? Cosa cambierebbe cambiando framework?
2. Che differenza pratica c'è tra un **Prompt Agent** e un **Hosted Agent**? Quando serve il secondo?
3. Perché il Code Interpreter migliora l'affidabilità rispetto a far calcolare il ROI "al modello"?
