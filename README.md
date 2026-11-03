# SalesPilot

Assistente AI per la ricerca e qualificazione di prospect B2B per CXI, con prioritizzazione, suggerimento dei servizi ed esportazione Excel. Prototipo universitario (caso 28, Ingegneria della Qualità, Politecnico di Torino): i risultati AI richiedono verifica indipendente.

L'agent (ricerca, prioritizzazione, servizi CXI, arricchimenti) è basato sul repository [SalesPilot](https://github.com/canzxoni-wq/SalesPilot) di canzxoni-wq. Questa versione aggiunge gli account individuali e l'archivio permanente su Supabase.

## Accesso e archivio

L'app funziona in due modalità, scelte automaticamente dalle variabili d'ambiente.

| Modalità | Variabili | Accesso | Cronologia |
| --- | --- | --- | --- |
| Account individuali (consigliata) | `SUPABASE_URL`, `SUPABASE_ANON_KEY` | Email e password, un account per Account Manager | Archivio permanente, visibile solo all'utente che ha fatto la ricerca |
| Accesso condiviso | `SALESPILOT_USERNAME`, `SALESPILOT_PASSWORD` | Credenziali uniche per tutti | Solo per la sessione aperta |

Se sono configurate le variabili Supabase, prevale la modalità con account individuali.

- Ogni utente vede, valuta e cancella solo le proprie ricerche: la separazione è garantita dalla Row Level Security del database, non solo dall'interfaccia.
- Le ricerche non vengono cancellate in automatico (EC15: retention ≥ 90 giorni). La barra laterale mostra le ultime 20; le altre restano nell'archivio.
- "Cancella cronologia" chiede conferma e cancella solo le ricerche dell'utente loggato.
- L'app usa la chiave pubblica (anon/publishable) e il token dell'utente. La chiave `service_role` non serve e non va configurata.

## Informativa privacy e Termini d'uso

I testi sono in `legal.py` e sono consultabili nell'app agli indirizzi `/?pagina=privacy` e `/?pagina=termini`, anche senza accesso. Per registrarsi bisogna spuntare la casella di presa visione dell'informativa e accettazione dei termini; la versione accettata e la data vengono salvate nei metadati dell'utente su Supabase. Quando i testi cambiano, aggiornare `LEGAL_VERSION` in `legal.py`.

## Configurazione di Supabase

1. Crea un progetto su supabase.com.
2. Nel **SQL Editor** esegui il file `supabase/schema.sql`: crea la tabella `salespilot_searches`, le regole di sicurezza e la vista `salespilot_feedback_stats`.
3. In **Authentication → URL Configuration** imposta **Site URL** all'indirizzo pubblico dell'app su Render e aggiungi in **Redirect URLs** lo stesso indirizzo seguito da `/**` (es. `https://salespilot.onrender.com/**`). Dopo il clic sul link di conferma, l'utente torna all'app e vede il messaggio "account verificato".
4. Copia **Project URL** e chiave **anon/publishable** (Project Settings → API Keys).

## Pubblicazione su Render

1. Su Render crea **New → Blueprint**, collega questo repository e usa il file `render.yaml`.
2. Imposta le variabili d'ambiente (sezione **Environment**):
   - `GEMINI_API_KEY`: chiave API di Gemini
   - `TAVILY_API_KEY`: chiave della ricerca web Tavily
   - `SUPABASE_URL` e `SUPABASE_ANON_KEY`: per gli account individuali
   - in alternativa `SALESPILOT_USERNAME` e `SALESPILOT_PASSWORD`: per l'accesso condiviso
   - `PRIVACY_CONTROLLER` e `PRIVACY_CONTACT_EMAIL`: titolare del trattamento ed email di contatto mostrati nell'Informativa privacy
   - `APP_URL`: facoltativa, indirizzo pubblico dell'app (altrimenti viene ricavato in automatico)
   - `GEMINI_MODEL`: facoltativa, predefinita `gemini-3.1-flash-lite`
3. Esegui il deploy e apri l'indirizzo pubblico fornito da Render.

## Avvio locale

```bash
python -m pip install -r requirements.txt
cp env.example .env   # poi inserisci le tue chiavi
streamlit run app.py
```

## Limiti del prototipo

- Le aziende sono proposte da Gemini a partire dalle fonti Tavily: verifica nomi, siti, numeri e priorità prima dell'uso commerciale.
- I servizi suggeriti sono ipotesi commerciali, non un catalogo validato.
- I contatti nominativi provengono da fonti professionali pubbliche: prima dell'uso commerciale verifica la base giuridica e gli obblighi privacy applicabili.
- Le chiavi vanno inserite solo nelle variabili d'ambiente di Render o nel `.env` locale, mai su GitHub.
