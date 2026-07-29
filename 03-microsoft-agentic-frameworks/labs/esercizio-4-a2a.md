# Esercizio 4 — Agenti che collaborano: pricing & media planning
### Tema: Agent-to-Agent (A2A) · Durata core: ~55 min

> **Obiettivo:** costruire un **agente remoto A2A** (un "Pricing Agent" che preventiva le
> campagne) e un **agente client** ("Sales Assistant") che lo **scopre** tramite la sua
> *Agent Card* e gli **delega un task** via protocollo A2A. Vedrai in pratica la
> collaborazione *orizzontale* tra agenti, complementare a MCP.

**Concetti che fisserai (slide Giorno 1):** Agent Card (chi è / cosa sa fare / dove
risponde), delega di un task tra agenti, ciclo client ↔ remote agent, differenza MCP (agente↔strumenti)
vs A2A (agente↔agente).

**Documentazione:** A2A <https://a2a-protocol.org/> · SDK Python `a2a-sdk`
<https://github.com/a2aproject/a2a-python>

> ⚠️ `a2a-sdk` evolve rapidamente: se un nome di classe/campo differisce dalla tua versione,
> adatta seguendo la doc linkata. L'obiettivo è vedere in azione **Agent Card + delega del task**.
> Questo esercizio è **locale** e la logica di pricing è deterministica (nessuna credenziale cloud richiesta).

---

## Prerequisiti
- Pacchetti da `requirements.txt` (`a2a-sdk`, `uvicorn`, `httpx`).
- Due terminali (server + client).

---

## Parte A — L'agente remoto: Pricing Agent (≈25 min)

Un agente A2A pubblica una **Agent Card** (biglietto da visita leggibile dalle macchine) e
implementa un **AgentExecutor** con la sua logica. Crea `server_pricing.py`:

```python
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from a2a.types import AgentCard, AgentSkill, AgentCapabilities

# --- Logica di pricing deterministica: CPM base per settore ---
CPM_BASE = {"Automotive": 18.0, "Finance": 22.0, "FMCG": 12.0,
            "Travel": 16.0, "Telco": 14.0, "default": 15.0}

def preventivo(brief: str) -> str:
    # brief atteso, es.: "settore=Travel; impression=9200000"
    parti = dict(p.split("=") for p in brief.replace(" ", "").split(";") if "=" in p)
    settore = parti.get("settore", "default")
    impressions = float(parti.get("impression", 5_000_000))
    cpm = CPM_BASE.get(settore, CPM_BASE["default"])
    prezzo = impressions / 1000 * cpm
    return (f"Preventivo — settore {settore}: {impressions:,.0f} impression "
            f"x CPM {cpm} EUR = {prezzo:,.0f} EUR.")

class PricingAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        richiesta = context.get_user_input()          # testo inviato dal client
        event_queue.enqueue_event(new_agent_text_message(preventivo(richiesta)))
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel non supportato")

# --- Skill + Agent Card ---
skill = AgentSkill(
    id="preventivo_campagna",
    name="Preventivo campagna",
    description="Calcola un preventivo pubblicitario da un brief (settore, impression).",
    tags=["pricing", "advertising"],
    examples=["settore=Travel; impression=9200000"],
)
agent_card = AgentCard(
    name="Pricing Agent RAI",
    description="Agente di preventivazione campagne per RAI Pubblicità.",
    url="http://localhost:9999/",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(),
    skills=[skill],
)

if __name__ == "__main__":
    handler = DefaultRequestHandler(
        agent_executor=PricingAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )
    app = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(app.build(), host="0.0.0.0", port=9999)
```

Avvia il server (**primo terminale**):

```bash
python server_pricing.py
```

**Cosa dovresti vedere:** Uvicorn in ascolto su `http://0.0.0.0:9999`. La Agent Card è
pubblicata automaticamente su `http://localhost:9999/.well-known/agent-card.json`
(su alcune versioni: `.../agent.json`). Aprila nel browser per vedere il "biglietto da visita".

---

## Parte B — Il client: Sales Assistant che delega (≈20 min)

Il client **scopre** l'agente remoto dalla sua Agent Card e gli **delega** il compito.
Crea `client_sales.py`:

```python
import asyncio
from uuid import uuid4
import httpx
from a2a.client import A2AClient
from a2a.types import SendMessageRequest, MessageSendParams

async def main():
    async with httpx.AsyncClient() as http:
        # 1. scoperta via Agent Card (legge /.well-known/agent-card.json)
        client = await A2AClient.get_client_from_agent_card_url(
            http, "http://localhost:9999"
        )

        # 2. delega del task all'agente remoto
        payload = {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": "settore=Travel; impression=9200000"}],
                "messageId": uuid4().hex,
            }
        }
        req = SendMessageRequest(params=MessageSendParams(**payload))
        resp = await client.send_message(req)

        # 3. il Sales Assistant compone/usa la risposta ricevuta
        print(resp.model_dump(mode="json", exclude_none=True))

asyncio.run(main())
```

Esegui (**secondo terminale**):

```bash
python client_sales.py
```

**Cosa dovresti vedere:** una risposta JSON con il testo del preventivo, es.
*"settore Travel: 9.200.000 impression x CPM 16.0 EUR = 147.200 EUR"*. Il client **non**
contiene la logica di pricing: l'ha **delegata** all'agente remoto — è A2A in azione.

---

## Parte C — Osserva Agent Card e ciclo del task (≈10 min)

1. Apri nel browser la Agent Card e individua i tre elementi chiave: **chi è** (`name`,
   `description`), **cosa sa fare** (`skills`), **dove risponde** (`url`).
2. Nel JSON di risposta del client, individua il messaggio prodotto dall'agente (`role: "agent"`)
   e il suo `text`.

> ✅ **Checkpoint:** hai un agente remoto con la sua Agent Card e un agente client che lo
> scopre e gli delega un compito. È il "chiama un collega di un altro reparto" della slide MCP-vs-A2A.

---

## 🎯 Opzionale (bonus, ≈15 min)

**B1 — Un secondo agente remoto: Media Planning.** Duplica `server_pricing.py` in
`server_media.py`: cambia porta (`10000`), Agent Card (`name="Media Planning Agent RAI"`,
`url="http://localhost:10000/"`) e la logica dell'executor, che dato un brief restituisce la
disponibilità di spazi, es.:

```python
def disponibilita(brief: str) -> str:
    parti = dict(p.split("=") for p in brief.replace(" ", "").split(";") if "=" in p)
    settore = parti.get("settore", "n/d")
    return f"Media planning — settore {settore}: 3 slot TV prime-time e 5 pacchetti digital disponibili a marzo."
```

**B2 — Orchestra i due agenti dal client.** Nel `client_sales.py`, dopo aver interrogato il
Pricing Agent (9999), interroga anche il Media Planning Agent (10000) e **componi** le due
risposte in un'unica proposta per il cliente. Questo è il pattern "assistente vendite che
coordina più specialisti" della slide.

**B3 — [Avanzato] Rendi il Pricing Agent 'intelligente'.** Sostituisci la logica
deterministica con una chiamata a un modello (Agent Framework, Es. 1, oppure Responses API,
Es. 2) dentro `execute()`, così il preventivo tiene conto anche di stagionalità e settore in
linguaggio naturale. La Agent Card e il protocollo restano identici: cambi solo *come*
l'agente produce la risposta.

---

## Verifica finale / domande di riflessione
1. A cosa serve la **Agent Card** e perché è "leggibile dalle macchine"?
2. Qual è la differenza tra usare uno **strumento MCP** e **delegare a un agente A2A**? (verticale vs orizzontale)
3. Nel caso RAI, quali capacità terresti come **agenti separati** (A2A) invece di funzioni interne? Perché?
