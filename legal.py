"""Testi di Informativa privacy e Termini d'uso di SalesPilot.

Aggiornare LEGAL_VERSION ogni volta che i testi cambiano in modo sostanziale:
la versione accettata viene salvata nel profilo dell'utente alla registrazione.
"""
import os

LEGAL_VERSION = "2026-11-04"
LEGAL_DATE = "4 novembre 2026"


def _controller():
    name = os.getenv("PRIVACY_CONTROLLER", "").strip() or (
        "il gruppo di progetto SalesPilot (corso di Ingegneria della Qualità, Politecnico di Torino)")
    email = os.getenv("PRIVACY_CONTACT_EMAIL", "").strip()
    contact = f"[{email}](mailto:{email})" if email else "il referente del gruppo di progetto"
    return name, contact


def privacy_text():
    name, contact = _controller()
    return f"""
# Informativa privacy

*Versione del {LEGAL_DATE} · ai sensi degli artt. 13 e 14 del Regolamento (UE) 2016/679 (GDPR)*

SalesPilot è un **prototipo universitario** che aiuta a individuare potenziali clienti B2B. Questa informativa spiega quali dati personali tratta, perché e quali sono i tuoi diritti.

## 1. Titolare del trattamento
Il titolare è {name}. Per qualsiasi richiesta sulla privacy puoi scrivere a {contact}.

## 2. Quali dati trattiamo
- **Dati dell'account:** nome, eventuale diminutivo, forma di saluto preferita (maschile, femminile o neutra), indirizzo email e password. La password è conservata solo in forma cifrata dal fornitore di autenticazione e nessuno del gruppo può leggerla.
- **Dati di utilizzo:** il testo delle ricerche, i risultati generati, i feedback a stelle, la data e la durata di ogni ricerca.
- **Dati tecnici:** dati di connessione (ad esempio indirizzo IP) registrati dai fornitori di hosting e autenticazione per sicurezza e funzionamento del servizio.
- **Dati di terzi nei risultati:** i risultati possono contenere nome, ruolo, link professionale (ad esempio il profilo LinkedIn) ed email professionale di referenti aziendali, solo se pubblicati in fonti accessibili a tutti (vedi punto 7), oltre ai recapiti generici delle aziende.

## 3. Perché li trattiamo e su quale base giuridica
| Finalità | Base giuridica |
| --- | --- |
| Creare e gestire il tuo account, eseguire le ricerche, conservare la tua cronologia | Esecuzione del servizio che richiedi (art. 6.1.b GDPR) |
| Sicurezza del servizio e prevenzione degli abusi | Legittimo interesse del titolare (art. 6.1.f GDPR) |
| Analisi statistica, in forma aggregata, della qualità dei risultati per il progetto universitario | Legittimo interesse del titolare (art. 6.1.f GDPR) |

Non usiamo i dati per pubblicità, non li vendiamo e non prendiamo decisioni automatizzate che producano effetti giuridici su di te.

## 4. A chi vengono comunicati
I dati sono trattati da fornitori tecnici che agiscono come responsabili o titolari autonomi del trattamento:
- **Supabase:** database e autenticazione (account, ricerche, feedback);
- **Render:** hosting dell'applicazione;
- **Google (Gemini API):** elaborazione del testo delle ricerche per generare i risultati;
- **Tavily:** ricerca web a partire dal testo delle ricerche.

Alcuni fornitori possono trattare i dati **fuori dallo Spazio Economico Europeo**. In questi casi il trasferimento avviene sulla base delle garanzie previste dai fornitori stessi, ad esempio le clausole contrattuali standard della Commissione europea.

**Importante:** il testo delle ricerche viene inviato a Google e a Tavily. Con i piani gratuiti, Google può utilizzare i contenuti inviati per migliorare i propri servizi. **Non inserire nelle ricerche dati personali o informazioni riservate.**

## 5. Per quanto tempo li conserviamo
- Le ricerche restano nella tua cronologia finché non le cancelli con **Cancella cronologia**, e comunque non oltre la conclusione del progetto universitario, al termine della quale l'archivio viene eliminato.
- L'account resta attivo finché non ne chiedi la cancellazione o fino alla conclusione del progetto.
- I dati tecnici sono conservati dai fornitori per i tempi indicati nelle rispettive informative.

## 6. I tuoi diritti
Puoi chiedere in qualsiasi momento l'accesso ai tuoi dati, la rettifica, la cancellazione (incluso l'account), la limitazione del trattamento, la portabilità e opporti al trattamento basato sul legittimo interesse (artt. 15-22 GDPR). Per esercitarli scrivi a {contact}. Le ricerche puoi cancellarle anche da solo, direttamente dall'app.

Se ritieni che il trattamento violi il GDPR puoi proporre reclamo al **Garante per la protezione dei dati personali** ([www.garanteprivacy.it](https://www.garanteprivacy.it)).

## 7. Dati di referenti aziendali nei risultati
I risultati possono indicare nome, ruolo e link professionale di persone che ricoprono ruoli in aziende, ricavati da fonti pubblicamente accessibili (siti aziendali, profili professionali), allo scopo di individuare l'interlocutore pertinente in un contesto B2B. Sono mostrati solo i dati minimi necessari, ciascuno con la sua fonte: nessun recapito privato e nessuna email ricostruita o indovinata. Le pagine di LinkedIn non vengono lette: viene riportato solo il link al profilo quando compare nei risultati di ricerca. Le persone interessate possono chiedere in qualsiasi momento la cancellazione o opporsi al trattamento scrivendo a {contact}. Chi usa SalesPilot deve verificare la base giuridica e gli obblighi privacy prima di contattare queste persone per finalità commerciali.

## 8. Obbligatorietà
Email e password sono necessarie per creare l'account: senza di esse non è possibile usare il servizio.

## 9. Modifiche
Questa informativa può essere aggiornata. La versione in vigore è sempre disponibile in questa pagina, con la data dell'ultimo aggiornamento.
"""


def terms_text():
    name, contact = _controller()
    return f"""
# Termini d'uso

*Versione del {LEGAL_DATE}*

## 1. Che cos'è SalesPilot
SalesPilot è un **prototipo sviluppato per un progetto universitario** da {name}. Non è un servizio commerciale, non è prestato a pagamento e può essere modificato, sospeso o chiuso in qualsiasi momento senza preavviso.

## 2. Account
- Per usare SalesPilot serve un account personale. Le credenziali sono personali: non condividerle con altri.
- Sei responsabile delle attività svolte con il tuo account. Se sospetti un accesso non autorizzato, avvisa {contact}.
- Possiamo sospendere o cancellare gli account usati in violazione di questi termini.

## 3. Natura dei risultati
- I risultati sono **generati da sistemi di intelligenza artificiale** a partire da fonti web e possono essere incompleti, non aggiornati o errati.
- Aziende, fatturati, priorità, contatti e servizi suggeriti sono **proposte da verificare**, non dati certificati. Le stime sono indicate come tali.
- Prima di qualsiasi uso commerciale devi verificare in modo indipendente le informazioni e le fonti.

## 4. Uso consentito
È vietato usare SalesPilot per:
- inserire nelle ricerche dati personali di terzi, dati particolari (art. 9 GDPR) o informazioni riservate;
- contattare persone in violazione della normativa privacy o delle regole sul marketing diretto;
- attività illecite, invio di spam, raccolta massiva di dati o tentativi di aggirare le misure di sicurezza;
- sovraccaricare deliberatamente il servizio o le API utilizzate.

## 5. Proprietà intellettuale
Il codice e i contenuti dell'app appartengono ai rispettivi autori. I marchi e i nomi delle aziende citati nei risultati appartengono ai legittimi titolari e sono usati solo a fini informativi.

## 6. Limitazione di responsabilità
SalesPilot è fornito "così com'è", senza garanzie di disponibilità, accuratezza o idoneità a uno scopo specifico. Nei limiti consentiti dalla legge, gli autori non rispondono di decisioni prese o danni derivanti dall'uso dei risultati.

## 7. Privacy
Il trattamento dei dati personali è descritto nell'**Informativa privacy**, che fa parte di questi termini.

## 8. Modifiche e legge applicabile
Questi termini possono essere aggiornati; la versione in vigore è sempre disponibile in questa pagina. Si applica la legge italiana.
"""
