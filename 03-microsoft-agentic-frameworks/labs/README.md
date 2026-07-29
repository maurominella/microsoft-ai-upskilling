# RAI Pubblicità — Upskilling · Giornata 2
## Esercitazioni pratiche (deep dive tecnico)

Benvenuti alla parte hands-on. Dopo la Giornata 1 (visione, architetture e demo)
oggi mettete **le mani sulla tastiera**. Queste quattro esercitazioni ricalcano i
quattro temi visti a slide e servono a **fissare i concetti** costruendo e facendo
girare codice Python reale, sempre su casi vicini al business di RAI Pubblicità
(campagne, ROI, pricing, media planning, valutazioni).

Tutte le esercitazioni sono in **Python**.

---

## Indice delle esercitazioni

| # | Esercizio | Tema (slide Giorno 1) | Durata | Cosa costruisci |
|---|-----------|-----------------------|:------:|-----------------|
| 1 | [Il tuo primo agente per l'analisi campagne](./esercizio-1-agent-framework.md) | **Microsoft Agent Framework** | **55 min** | Un agente che ragiona e usa *function tool* per rispondere su ROI e metriche delle campagne |
| 2 | [Dalla Responses API all'agente gestito](./esercizio-2-foundry-hosted-agents.md) | **Foundry & Hosted Agents** | **60 min** | Uso della **Responses API** di Foundry con Code Interpreter, tracciamento e passi verso l'Hosted Agent |
| 3 | [Esponi le campagne come server MCP](./esercizio-3-mcp.md) | **Model Context Protocol** | **70 min** | Un **server MCP** che espone tool, resource e prompt sui dati campagne, con un client che li consuma |
| 4 | [Agenti che collaborano: pricing & media planning](./esercizio-4-a2a.md) | **Agent-to-Agent (A2A)** | **55 min** | Un **agente remoto A2A** (pricing) e un agente client che lo scopre via *Agent Card* e gli delega un task |

**Totale core: 4 ore (240 min).**
Ogni esercizio ha una sezione **🎯 Opzionale (bonus)**: se un esercizio vi appassiona
potete proseguire lì; altrimenti fermatevi e passate al successivo, restando in orario.

> ⏸️ **Ritmo suggerito:** una pausa di ~15 min dopo l'Esercizio 2 (a metà mattinata).

---

## Prerequisiti

- **Ambiente Python già configurato** (creazione/attivazione dell'ambiente vista in precedenza).
- Installate i pacchetti con il file **[`requirements.txt`](./requirements.txt)** (unico per tutti gli esercizi).
- **Accesso a Microsoft Foundry / Azure OpenAI** già predisposto (Esercizi 1 e 2).
  Autenticazione via Entra ID: eseguite `az login` prima di partire.
- Variabili d'ambiente (es. in un file `.env` nella cartella degli esercizi):

  ```dotenv
  # Foundry (Esercizio 2, e opzionale Esercizio 1 via Foundry)
  FOUNDRY_PROJECT_ENDPOINT=https://<il-tuo-account>.services.ai.azure.com/api/projects/<il-tuo-progetto>
  FOUNDRY_MODEL_NAME=<nome-deployment-del-modello>   # es. gpt-4o-mini

  # Azure OpenAI (Esercizio 1 con Agent Framework)
  AZURE_OPENAI_ENDPOINT=https://<il-tuo-endpoint>.openai.azure.com/
  AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=<nome-deployment-del-modello>
  ```

- I moduli/porta locali usati: MCP → `127.0.0.1:8000`, A2A → `localhost:9999`.

---

## Dati condivisi: `rai_campaigns.py`

Tutti gli esercizi riusano lo stesso piccolo dataset sintetico di 5 campagne, nel file
**[`rai_campaigns.py`](./rai_campaigns.py)** (già incluso in questa cartella). Espone:

- `CAMPAGNE` — lista di dizionari con budget, impression, click, conversioni, revenue…
- `elenco_campagne()`, `dettaglio_campagna(id)`, `roi(id)`, `cpm(id)`

Sanity check rapido:

```bash
python rai_campaigns.py
```

Output atteso (ROI = (revenue − budget) / budget):

```
CMP-001 AutoMilano    ROI   75.0%  CPM  14.29 EUR
CMP-002 BancaVerde    ROI   46.7%  CPM  17.65 EUR
CMP-003 FreschErba    ROI   60.0%  CPM   8.82 EUR
CMP-004 VoloBlu       ROI  134.0%  CPM  16.30 EUR
CMP-005 TeleCasa      ROI  -10.0%  CPM  18.60 EUR
```

Nota di lettura: **VoloBlu (CMP-004)** è la campagna con il ROI migliore, **TeleCasa
(CMP-005)** è in perdita. Torneranno spesso negli esercizi.

---

## ⚠️ Nota importante sulle versioni

Agent Framework, Foundry Agent Service (A2A tool), MCP e A2A sono tecnologie **recenti
e in rapida evoluzione**. Se un `import`, un nome di classe o un parametro non
corrisponde esattamente alla versione installata nel vostro ambiente, **consultate la
documentazione linkata in ogni esercizio**: l'obiettivo non è la sintassi esatta di una
release, ma **fissare i concetti** (agente + tool, Responses API, server MCP, delega A2A).
I frammenti di codice seguono le API documentate al momento della stesura.

---

## Come useremo i risultati

A fine mattinata avrete costruito, con le vostre mani, un piccolo pezzo di ciascuno dei
quattro livelli dello stack agentico visto ieri: **costruire** (Agent Framework),
**eseguire** (Foundry), **collegare agli strumenti** (MCP) e **far collaborare gli agenti**
(A2A). È esattamente l'architettura di riferimento della slide finale del Giorno 1.

Buon lavoro! 🚀
