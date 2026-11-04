"""Interruttori delle funzioni aggiunte il 4 novembre 2026.

Per togliere una funzione basta mettere False accanto al suo nome e ricaricare questo file:
l'app torna a comportarsi come prima per quella parte. Per tornare in blocco alla versione
precedente c'è il tag git "versione-4-novembre" (e lo zip con gli stessi file).
"""

FEATURES = {
    # Scelta del modello "Sales" / "Head Hunter" con la legenda che spiega le differenze.
    # Head Hunter: fino a 3 persone per azienda (LinkedIn/email solo se pubblicati) e bozza del messaggio.
    # Spento: si usa sempre Sales e il selettore non compare.
    "modelli_sales_headhunter": True,
    # Telefono, email e sito dell'azienda presi dal sito ufficiale (entrambi i modelli).
    "contatti_azienda": True,
    # 1 · Validazione per singola azienda (pertinente, dati corretti, ruolo, servizio).
    "validazione_aziende": True,
    # 2 · Statistiche con i target della House of Quality ed export Excel.
    "statistiche_hoq": True,
    # 3 · Bozza del primo messaggio per ogni azienda, rivolta alla persona trovata (solo Head Hunter).
    "bozza_messaggio": True,
    # 4 · Stato del lead (da contattare, contattata, ...) e pagina "Lead".
    "stato_lead": True,
    # 5 · Avviso "già trovata" ed elenco dei clienti CXI da escludere.
    "doppioni_e_esclusi": True,
    # 6 · "Trova altre aziende simili" ed "Escludi" sulla singola azienda.
    "continua_ricerca": True,
    # 7 · Ricerche sul web in parallelo (fatturati, contatti, sedi): stessi risultati, meno attesa.
    "ricerche_parallele": True,
}


def on(name):
    return FEATURES.get(name, False)
