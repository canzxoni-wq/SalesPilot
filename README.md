# SalesPilot

Assistente AI per la ricerca e qualificazione di prospect B2B, con prioritizzazione e esportazione Excel. Prototipo universitario: i risultati AI richiedono verifica indipendente.

## Pubblicazione con GitHub e Render

1. Carica i file di questa cartella nella **radice** del repository GitHub `SalesPilot`, inclusi `render.yaml`, `.gitignore` e la cartella `.streamlit`. **Non caricare `.env`, `.venv` o credenziali.**
2. Su Render crea **New > Blueprint**, collega il repository GitHub e seleziona il blueprint dal file `render.yaml`. Se il piano free non è disponibile nel tuo account, scegli un piano compatibile.
3. Imposta le variabili d'ambiente richieste (Render può chiederle durante la creazione o puoi aggiungerle da **Environment**):
   - `GEMINI_API_KEY`: chiave API di Gemini
   - `SALESPILOT_USERNAME`: nome utente per il login
   - `SALESPILOT_PASSWORD`: password lunga e casuale per il login
   - `GEMINI_MODEL`: facoltativa, predefinita `gemini-2.5-flash`
4. Esegui il deploy e apri l'indirizzo pubblico fornito da Render.

> Il login è basato su una password condivisa e sessione Streamlit: è adatto a una demo privata con utenti fidati, **non** è un sistema di autenticazione enterprise. La pagina di login protegge l'interfaccia, non sostituisce controlli infrastrutturali di accesso. Usa credenziali uniche e HTTPS, non condividere l'indirizzo pubblicamente se contiene dati sensibili.

## Avvio locale

```bash
python -m pip install -r requirements.txt
```

Copia `.env.example` in `.env`, sostituisci i segnaposto con credenziali locali e avvia:

```bash
streamlit run app.py
```

## Limiti del prototipo

- **Demo (senza API)** restituisce esclusivamente aziende fittizie.
- **Gemini (API)** genera proposte di prospect, ma non garantisce ricerche web aggiornate o fonti verificate: il codice attuale non abilita Google Search grounding.
- I servizi suggeriti sono **ipotesi**, non un catalogo validato.
- Verifica manualmente nomi, siti, numeri e priorità prima dell'uso commerciale.
- La chiave API e la password vanno inserite solo nelle variabili d'ambiente di Render o nel `.env` locale, mai su GitHub.
