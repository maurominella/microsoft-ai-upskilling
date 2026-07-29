# Esercizio 3 — Esponi le campagne come server MCP
### Tema: Model Context Protocol (MCP) · Durata core: ~70 min

> **Obiettivo:** costruire un **server MCP** che espone i dati delle campagne di RAI
> Pubblicità come **tool**, **resource** e **prompt**, e poi consumarlo con un **client
> MCP**. Vedrai in pratica il principio "**costruisci una volta, riusa ovunque**": lo stesso
> server potrà essere usato da qualunque agente conforme (Agent Framework, Foundry, …).

**Concetti che fisserai (slide Giorno 1):** architettura client-server di MCP, i *primitivi*
(tools / resources / prompts), il problema M×N → M+N, la riusabilità degli strumenti.

**Documentazione:** MCP <https://modelcontextprotocol.io/> · FastMCP <https://gofastmcp.com/>

> Questo esercizio è **interamente locale**: non servono credenziali cloud per le parti A–C.

---

## Prerequisiti
- Pacchetti da `requirements.txt` (`fastmcp`, `mcp`).
- Il file `rai_campaigns.py` nella stessa cartella.
- Due terminali (uno per il server, uno per il client).

---

## Parte A — Costruisci il server MCP (≈30 min)

Crea `server_campagne.py`. Con **FastMCP** definisci gli strumenti come normali funzioni:
i *type hint* e le *docstring* generano automaticamente lo schema MCP.

```python
from fastmcp import FastMCP
from rai_campaigns import CAMPAGNE, dettaglio_campagna, elenco_campagne, roi

mcp = FastMCP("RAI Campagne MCP")

# --- TOOL: azioni chiamabili dall'agente ---
@mcp.tool
def get_campagna(campaign_id: str) -> dict:
    """Dettaglio completo di una campagna dato il suo id (es. 'CMP-004')."""
    c = dettaglio_campagna(campaign_id)
    return c or {"errore": f"campagna {campaign_id} non trovata"}

@mcp.tool
def lista_campagne() -> list:
    """Elenco sintetico (id, cliente, settore) di tutte le campagne."""
    return elenco_campagne()

@mcp.tool
def top_campagne_per_roi(n: int = 3) -> list:
    """Le prime n campagne ordinate per ROI decrescente, con il valore di ROI%."""
    dati = [{"id": c["id"], "cliente": c["cliente"], "roi_pct": roi(c["id"])}
            for c in CAMPAGNE]
    dati.sort(key=lambda x: x["roi_pct"], reverse=True)
    return dati[:n]

# --- RESOURCE: dati leggibili su cui radicare le risposte ---
@mcp.resource("campagne://tutte")
def risorsa_campagne() -> list:
    """Tutte le campagne come dati grezzi (contesto per l'agente)."""
    return CAMPAGNE

# --- PROMPT: template riutilizzabile ---
@mcp.prompt
def valuta_campagna(campaign_id: str) -> str:
    """Template per valutare una campagna in modo standard."""
    return (
        f"Valuta la campagna {campaign_id}: recupera i dati con gli strumenti, "
        f"calcola il ROI, confrontalo con gli altri e proponi un'azione."
    )

if __name__ == "__main__":
    # Trasporto HTTP: il server ascolta su http://127.0.0.1:8000/mcp
    mcp.run(transport="http", host="127.0.0.1", port=8000)
```

Avvia il server (**primo terminale**):

```bash
python server_campagne.py
```

**Cosa dovresti vedere:** un log che indica il server MCP in ascolto su `127.0.0.1:8000`.
Lascialo in esecuzione.

---

## Parte B — Consuma il server con un client MCP (≈25 min)

Crea `client_campagne.py`. Il client **scopre** gli strumenti e poi ne **chiama** uno —
tutto via protocollo, senza sapere nulla dell'implementazione interna del server.

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        # 1. scoperta: quali strumenti espone il server?
        tools = await client.list_tools()
        print("Strumenti esposti:", [t.name for t in tools])

        # 2. chiamata a uno strumento
        res = await client.call_tool("top_campagne_per_roi", {"n": 3})
        print("Top 3 per ROI:", res.data)

        # 3. lettura di una resource
        risorse = await client.read_resource("campagne://tutte")
        print("Numero campagne nella resource:", len(risorse))

asyncio.run(main())
```

Esegui (**secondo terminale**):

```bash
python client_campagne.py
```

**Cosa dovresti vedere:** l'elenco degli strumenti (`get_campagna`, `lista_campagne`,
`top_campagne_per_roi`) e, in cima alla top-3 per ROI, **CMP-004 (VoloBlu, 134,0%)**.

> Nota: a seconda della versione di FastMCP, il risultato di `call_tool` si legge con
> `res.data` (output strutturato) oppure `res.content`. Se `.data` è vuoto, prova `.content`.

---

## Parte C — Aggiungi un prompt e verifica (≈15 min)

Hai già definito il prompt `valuta_campagna`. Elencalo e recuperalo dal client:

```python
async with Client("http://127.0.0.1:8000/mcp") as client:
    prompts = await client.list_prompts()
    print("Prompt disponibili:", [p.name for p in prompts])
    reso = await client.get_prompt("valuta_campagna", {"campaign_id": "CMP-005"})
    print(reso)
```

**Cosa dovresti vedere:** il prompt `valuta_campagna` e il testo generato per **CMP-005**.
I prompt incapsulano "il modo giusto di chiedere una cosa", riutilizzabile da chiunque.

> ✅ **Checkpoint:** hai un server MCP che espone tool, resource e prompt sui dati campagne,
> e un client che li consuma. È esattamente ciò che un agente farebbe al posto tuo.

---

## 🎯 Opzionale (bonus, ≈15 min)

**B1 — Una nuova tool di confronto.** Aggiungi al server:

```python
from rai_campaigns import roi
@mcp.tool
def confronta_campagne(id_a: str, id_b: str) -> dict:
    """Confronta il ROI di due campagne e indica quale rende di più."""
    ra, rb = roi(id_a), roi(id_b)
    migliore = id_a if (ra or -1e9) >= (rb or -1e9) else id_b
    return {"roi": {id_a: ra, id_b: rb}, "migliore": migliore}
```
Riavvia il server e chiama la tool dal client con `CMP-004` e `CMP-005`.

**B2 — Logging corretto per MCP.** In un server MCP **non** usare `print` su stdout (romperebbe
i messaggi JSON-RPC in modalità stdio): usa il modulo `logging`, che scrive su *stderr*.

```python
import logging
logger = logging.getLogger(__name__)
# dentro una tool:  logger.info("Richiesta top ROI, n=%s", n)
```

**B3 — [Avanzato] Fai scegliere gli strumenti a un modello.** Collega questo server a un LLM
in modo che sia il modello a decidere quale tool usare. Due strade:
- **Lato client (locale, raggiunge 127.0.0.1):** usa l'integrazione MCP dell'**Agent
  Framework** per passare il server come tool a un agente (vedi doc Agent Framework → *MCP*).
- **Via Foundry:** usa il tool `mcp` della **Responses API** (Esercizio 2, bonus), ricordando
  che il server deve essere raggiungibile pubblicamente.

Poni la domanda: *"Qual è la campagna con il ROI più alto e cosa consiglieresti per la peggiore?"*

---

## Verifica finale / domande di riflessione
1. Qual è la differenza tra un **tool**, una **resource** e un **prompt** in MCP?
2. Perché lo stesso server MCP può essere usato da agenti diversi senza modifiche? (M×N → M+N)
3. Che rischio introduce collegare un server MCP **esterno** e non fidato? (prompt injection / XPIA)
