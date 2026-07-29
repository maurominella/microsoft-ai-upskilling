"""
Dati sintetici di campagne pubblicitarie — RAI Pubblicità (uso didattico).
Nessun dato reale: serve solo come base comune per tutte le esercitazioni
della Giornata 2. Importa questo modulo dagli esercizi 1, 3 e 4.

Metriche per campagna:
- budget_eur   : investimento speso
- impressions  : impression erogate
- clicks       : click totali
- conversioni  : conversioni attribuite
- revenue_eur  : ricavi attribuiti alla campagna
"""

CAMPAGNE = [
    {"id": "CMP-001", "cliente": "AutoMilano", "settore": "Automotive",
     "budget_eur": 120000, "impressions": 8_400_000, "clicks": 42_000,
     "conversioni": 1_260, "revenue_eur": 210000, "canale": "TV+Digital",
     "inizio": "2026-01-07", "fine": "2026-02-04"},
    {"id": "CMP-002", "cliente": "BancaVerde", "settore": "Finance",
     "budget_eur": 90000, "impressions": 5_100_000, "clicks": 20_400,
     "conversioni": 612, "revenue_eur": 132000, "canale": "Digital",
     "inizio": "2026-01-14", "fine": "2026-02-11"},
    {"id": "CMP-003", "cliente": "FreschErba", "settore": "FMCG",
     "budget_eur": 60000, "impressions": 6_800_000, "clicks": 34_000,
     "conversioni": 1_700, "revenue_eur": 96000, "canale": "TV",
     "inizio": "2026-02-01", "fine": "2026-02-28"},
    {"id": "CMP-004", "cliente": "VoloBlu", "settore": "Travel",
     "budget_eur": 150000, "impressions": 9_200_000, "clicks": 55_200,
     "conversioni": 2_208, "revenue_eur": 351000, "canale": "TV+Digital",
     "inizio": "2026-02-10", "fine": "2026-03-10"},
    {"id": "CMP-005", "cliente": "TeleCasa", "settore": "Telco",
     "budget_eur": 80000, "impressions": 4_300_000, "clicks": 12_900,
     "conversioni": 387, "revenue_eur": 72000, "canale": "Digital",
     "inizio": "2026-02-18", "fine": "2026-03-18"},
]

# Benchmark di ROI medio per settore (sintetico), usato in alcuni esercizi
ROI_MEDIO_SETTORE = {
    "Automotive": 55.0, "Finance": 40.0, "FMCG": 50.0, "Travel": 90.0, "Telco": 20.0
}


def elenco_campagne():
    """Elenco sintetico (id, cliente, settore) di tutte le campagne."""
    return [{"id": c["id"], "cliente": c["cliente"], "settore": c["settore"]}
            for c in CAMPAGNE]


def dettaglio_campagna(campaign_id: str):
    """Dizionario completo della campagna con l'id indicato, oppure None."""
    for c in CAMPAGNE:
        if c["id"].lower() == campaign_id.lower():
            return c
    return None


def roi(campaign_id: str):
    """ROI percentuale = (revenue - budget) / budget * 100, arrotondato a 1 decimale."""
    c = dettaglio_campagna(campaign_id)
    if not c:
        return None
    return round((c["revenue_eur"] - c["budget_eur"]) / c["budget_eur"] * 100, 1)


def cpm(campaign_id: str):
    """CPM in euro = budget / impressions * 1000."""
    c = dettaglio_campagna(campaign_id)
    if not c:
        return None
    return round(c["budget_eur"] / c["impressions"] * 1000, 2)


if __name__ == "__main__":
    # Sanity check: stampa un riepilogo ROI/CPM
    for c in CAMPAGNE:
        print(f"{c['id']} {c['cliente']:<12} ROI {roi(c['id']):>6.1f}%  CPM {cpm(c['id']):>6.2f} EUR")
