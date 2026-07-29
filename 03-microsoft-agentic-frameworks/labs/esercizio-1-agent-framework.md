# Esercizio 1 — Il tuo primo agente per l'analisi campagne
### Tema: Microsoft Agent Framework · Durata core: ~55 min

> **Obiettivo:** costruire, con il **Microsoft Agent Framework**, un agente che
> *ragiona su un obiettivo* e *chiama function tool* per rispondere a domande reali
> sulle campagne di RAI Pubblicità (metriche, ROI, confronti). Vedrete dal vivo il
> **ciclo agentico** (percepire → ragionare → agire con un tool → osservare) di cui
> abbiamo parlato ieri.

**Concetti che fisserai (slide Giorno 1):** anatomia di un agente (modello + istruzioni +
strumenti), function tool, ciclo agentico, osservabilità delle chiamate agli strumenti.

**Documentazione:** <https://learn.microsoft.com/agent-framework/> ·
Function tools: <https://learn.microsoft.com/agent-framework/agents/tools/function-tools>

---

## Prerequisiti
- Pacchetti da `requirements.txt` installati (`agent-framework`, `azure-identity`).
- `az login` eseguito.
- In `.env`: `AZURE_OPENAI_ENDPOINT` e `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`.
- Il file `rai_campaigns.py` (fornito) nella stessa cartella.

Crea un file `es1_agente.py` e lavora lì. All'inizio del file carica il `.env`:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Parte A — Un agente minimale (≈10 min)

Il cuore dell'Agent Framework: modello + istruzioni. Ancora **senza strumenti**.

```python
import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

async def main():
    agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
        name="AnalistaCampagne",
        instructions=(
            "Sei un analista di RAI Pubblicità. Rispondi sempre in italiano, "
            "in modo conciso e professionale."
        ),
    )
    risposta = await agent.run("Presentati in una frase e dimmi come puoi aiutarmi.")
    print(risposta.text)

asyncio.run(main())
```

**Cosa dovresti vedere:** una breve presentazione dell'agente. Fin qui è un semplice
assistente conversazionale: capisce e risponde, ma non *fa* nulla.

---

## Parte B — Aggiungi un function tool (≈20 min)

Diamo all'agente uno **strumento**: una normale funzione Python. L'Agent Framework
genera lo schema dello strumento dai *type hint* e dalla *docstring*; con `Annotated` +
`Field` descriviamo i parametri al modello.

```python
from typing import Annotated
from pydantic import Field
from rai_campaigns import dettaglio_campagna

def metriche_campagna(
    campaign_id: Annotated[str, Field(description="Codice campagna, es. 'CMP-004'")]
) -> str:
    """Restituisce budget, impression, conversioni e revenue di una campagna RAI Pubblicità."""
    c = dettaglio_campagna(campaign_id)
    if not c:
        return f"Nessuna campagna trovata con id {campaign_id}."
    return (
        f"{c['cliente']} ({c['id']}, settore {c['settore']}): "
        f"budget {c['budget_eur']} EUR, impression {c['impressions']}, "
        f"conversioni {c['conversioni']}, revenue {c['revenue_eur']} EUR."
    )
```

Registra lo strumento sull'agente e poni una domanda che **obbliga** a usarlo:

```python
agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    name="AnalistaCampagne",
    instructions=(
        "Sei un analista di RAI Pubblicità. Rispondi in italiano. "
        "Usa gli strumenti per recuperare i dati: non inventare numeri."
    ),
    tools=[metriche_campagna],
)
risposta = await agent.run("Dammi le metriche principali della campagna CMP-004.")
print(risposta.text)
```

**Cosa dovresti vedere:** la risposta riporta i numeri **reali** di VoloBlu presi dallo
strumento (revenue 351000 EUR, ecc.), non valori inventati. Questo è il *grounding* sui dati.

---

## Parte C — Due strumenti + ragionamento a più passi (≈15 min)

Aggiungiamo un secondo strumento che calcola il ROI, così l'agente **concatena** più
chiamate (prima recupera i dati, poi calcola).

```python
def calcola_roi(
    revenue_eur: Annotated[float, Field(description="Ricavi in euro")],
    budget_eur: Annotated[float, Field(description="Budget speso in euro")],
) -> str:
    """Calcola il ROI percentuale: (revenue - budget) / budget * 100."""
    valore = (revenue_eur - budget_eur) / budget_eur * 100
    return f"ROI = {valore:.1f}%"

agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    name="AnalistaCampagne",
    instructions=(
        "Sei un analista di RAI Pubblicità. Rispondi in italiano. Usa gli strumenti: "
        "recupera i dati con 'metriche_campagna' e calcola con 'calcola_roi'."
    ),
    tools=[metriche_campagna, calcola_roi],
)
risposta = await agent.run(
    "Tra le campagne CMP-004 e CMP-005, quale ha il ROI migliore e di quanto? Mostra i valori."
)
print(risposta.text)
```

**Cosa dovresti vedere:** l'agente conclude che **CMP-004 (VoloBlu, ROI 134,0%)** batte
**CMP-005 (TeleCasa, ROI −10,0%)**. Nota che per arrivarci ha chiamato gli strumenti più
volte: è il **ciclo agentico** in azione.

> ✅ **Checkpoint:** hai un agente che ragiona e usa strumenti per rispondere a una
> domanda di business reale. Se ti fermi qui, sei perfettamente in linea.

---

## 🎯 Opzionale (bonus, ≈10–15 min)

**B1 — Conversazione a più turni (memoria di sessione).** Usa un *thread* per mantenere
il contesto tra domande successive:

```python
thread = agent.get_new_thread()
print((await agent.run("Qual è il ROI di CMP-001?", thread=thread)).text)
print((await agent.run("E rispetto a CMP-003, quale conviene?", thread=thread)).text)
```
Nota come nella seconda domanda l'agente "ricorda" CMP-001 senza doverlo ripetere.

**B2 — Un terzo strumento per l'intero portafoglio.** Aggiungi:

```python
from rai_campaigns import elenco_campagne
def lista_campagne() -> list:
    """Elenco (id, cliente, settore) di tutte le campagne del portafoglio."""
    return elenco_campagne()
```
Poi chiedi: *"Qual è la campagna con il ROI più alto del portafoglio?"* e osserva l'agente
iterare (elenca → recupera → calcola) fino alla risposta (**CMP-004**).

**B3 — Ispeziona le chiamate agli strumenti (osservabilità).** Dopo un `run`, stampa i
messaggi prodotti per vedere le *function call* e i loro risultati:

```python
resp = await agent.run("Qual è il ROI di CMP-002?")
for m in resp.messages:
    print(m)   # cerca i contenuti di tipo function_call / function_result
```
È l'equivalente "in codice" del pannello di *trace* visto a slide.

---

## Verifica finale / domande di riflessione
1. In che punto l'agente ha **deciso da solo** di chiamare uno strumento invece di rispondere direttamente?
2. Perché conviene avere due strumenti separati (`metriche_campagna` e `calcola_roi`) invece di uno solo?
3. Quando *non* useresti un agente ma una semplice funzione? (regola vista a slide: agente vs workflow)
