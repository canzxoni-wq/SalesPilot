import io
import json
import os
import re
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="SalesPilot | AI Sales Agent", page_icon="🔎", layout="wide")
st.markdown("""<style>.block-container{max-width:1100px;padding-top:2rem}h1{letter-spacing:-.04em}.stChatMessage{border-radius:14px}</style>""", unsafe_allow_html=True)

USERNAME = os.getenv("SALESPILOT_USERNAME") or os.getenv("CXI_USERNAME", "")
PASSWORD = os.getenv("SALESPILOT_PASSWORD") or os.getenv("CXI_PASSWORD", "")
API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not USERNAME or not PASSWORD or PASSWORD == "CAMBIA_QUESTA_PASSWORD":
    st.error("Configura SALESPILOT_USERNAME e SALESPILOT_PASSWORD nelle variabili d’ambiente di Render.")
    st.stop()

if not st.session_state.get("authenticated", False):
    st.title("SalesPilot · Accesso")
    st.caption("Accesso alla versione beta")
    with st.form("login"):
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Accedi", use_container_width=True)
    if submitted:
        import hmac
        if hmac.compare_digest(user, USERNAME) and hmac.compare_digest(password, PASSWORD):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Credenziali non valide")
    st.stop()

with st.sidebar:
    st.header("SalesPilot · Beta")
    mode = st.radio("Modalità", ["Demo (senza API)", "Gemini (API)"], index=0)
    st.caption("Le informazioni sui servizi CXI sono provvisorie fino alla ricezione dei documenti aziendali.")
    if st.button("Nuova conversazione"):
        st.session_state.messages = []
        st.rerun()
    if st.button("Esci"):
        st.session_state.clear()
        st.rerun()

st.title("SalesPilot")
st.caption("Ricerca prospect B2B · prioritizzazione · suggerimenti commerciali")
st.info("⚠️ Prototipo universitario. Verifica sempre aziende, numeri, contatti e fonti prima dell'uso commerciale.")

if "messages" not in st.session_state:
    st.session_state.messages = []

COLUMNS = ["Azienda", "Settore", "Area", "Dimensione", "Priorità", "Punteggio", "Servizio suggerito", "Interlocutore (ruolo)", "Motivazione", "Fonte URL", "Stato verifica"]

def demo_results(query):
    return [
        {"Azienda": "ESEMPIO — Alfa Industriale", "Settore": "Manifatturiero", "Area": "Piemonte", "Dimensione": "Non verificata", "Priorità": "Alta", "Punteggio": 82, "Servizio suggerito": "Analisi customer journey (ipotesi)", "Interlocutore (ruolo)": "Direzione commerciale", "Motivazione": "Esempio di opportunità, non basato su dati reali", "Fonte URL": "", "Stato verifica": "FITTIZIO"},
        {"Azienda": "ESEMPIO — Beta Components", "Settore": "Automotive", "Area": "Lombardia", "Dimensione": "Non verificata", "Priorità": "Media", "Punteggio": 64, "Servizio suggerito": "Ottimizzazione esperienza clienti (ipotesi)", "Interlocutore (ruolo)": "Responsabile customer service", "Motivazione": "Esempio illustrativo", "Fonte URL": "", "Stato verifica": "FITTIZIO"},
        {"Azienda": "ESEMPIO — Gamma Solutions", "Settore": "Servizi", "Area": "Italia", "Dimensione": "Non verificata", "Priorità": "Bassa", "Punteggio": 41, "Servizio suggerito": "Analisi VOC (ipotesi)", "Interlocutore (ruolo)": "Responsabile marketing", "Motivazione": "Esempio illustrativo", "Fonte URL": "", "Stato verifica": "FITTIZIO"},
    ]

def extract_json(text):
    clean = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I)
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", clean, re.S)
        if match:
            return json.loads(match.group(0))
        raise ValueError("La risposta AI non contiene JSON valido")

def gemini_results(query):
    if not API_KEY:
        raise ValueError("Manca GEMINI_API_KEY nelle variabili d’ambiente di Render")
    prompt = f'''Sei un assistente di pre-vendita B2B per un progetto universitario di CXI. Il catalogo ufficiale CXI NON è disponibile: ogni servizio suggerito va etichettato come IPOTESI.
Richiesta utente: {query}
Cerca di identificare aziende reali che soddisfino i criteri; non inventare nomi, dati, URL, persone o numeri. Se un dato non è confermato scrivi "Non verificato". Non attribuire contatti nominativi senza fonti. Se non hai accesso a fonti attendibili restituisci una lista vuota e spiega il limite.
Per ogni azienda assegna un punteggio indicativo 0-100, priorità Alta/Media/Bassa, una motivazione, un ruolo di interlocutore (non nominativo), e URL della fonte solo se realmente disponibile. Il punteggio è una valutazione ipotetica, non un fatto.
Rispondi ESCLUSIVAMENTE in JSON con oggetto: {{"sintesi":"...", "aziende":[{{"Azienda":"...", "Settore":"...", "Area":"...", "Dimensione":"...", "Priorità":"...", "Punteggio":0, "Servizio suggerito":"... (ipotesi)", "Interlocutore (ruolo)":"...", "Motivazione":"...", "Fonte URL":"...", "Stato verifica":"Da verificare"}}]}}.'''
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2}}
  
    response = requests.post(url, params={"key": API_KEY}, json=payload, timeout=100)
    if not response.ok:
        raise RuntimeError(f"Gemini API HTTP {response.status_code}. Controlla la chiave API, il modello e i limiti di utilizzo.")
    data = response.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini non ha restituito risultati")
    parts = candidates[0].get("content", {}).get("parts", [])
    raw = "\n".join(p.get("text", "") for p in parts if "text" in p)
    result = extract_json(raw)
    rows = result.get("aziende", [])
    if not isinstance(rows, list):
        raise ValueError("Formato risultati non valido")
    # Grounding metadata may supply source links even if the generated JSON does not.
    metadata = candidates[0].get("groundingMetadata", {})
    source_links = [x.get("web", {}).get("uri") for x in metadata.get("groundingChunks", []) if x.get("web", {}).get("uri")]
    return str(result.get("sintesi", "Risultati preliminari: verificare ogni dato.")), rows, source_links

def excel_bytes(rows):
    df = pd.DataFrame(rows).reindex(columns=COLUMNS, fill_value="")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Prospect", index=False)
    return output.getvalue()

for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])
        if msg.get("rows") is not None:
            st.dataframe(pd.DataFrame(msg["rows"]).reindex(columns=COLUMNS, fill_value=""), use_container_width=True, hide_index=True)
            st.download_button("📥 Scarica Excel", data=excel_bytes(msg["rows"]), file_name=f"salespilot_prospect_{idx}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key=f"export_{idx}")
            if msg.get("sources"):
                with st.expander("Fonti segnalate da Google Search (da verificare)"):
                    for link in msg["sources"]:
                        st.write(link)

query = st.chat_input("Es. Trova 10 aziende automotive in Piemonte con almeno 200 dipendenti...")
if query:
    st.session_state.messages.append({"role": "user", "text": query})
    try:
        if mode.startswith("Demo"):
            summary = "**Modalità demo:** risultati interamente fittizi per provare l'interfaccia. Non rispondono necessariamente ai filtri inseriti."
            rows, sources = demo_results(query), []
        else:
            with st.spinner("Gemini sta elaborando la richiesta..."):
                summary, rows, sources = gemini_results(query)
            summary += "\n\n⚠️ I dati e le fonti non sono stati validati da CXI."
        st.session_state.messages.append({"role": "assistant", "text": summary, "rows": rows, "sources": sources})
    except Exception as exc:
        st.session_state.messages.append({"role": "assistant", "text": f"⚠️ Errore: {exc}"})
    st.rerun()
