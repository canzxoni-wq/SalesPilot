import io
import json
import os
import re
import hmac
from datetime import datetime

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="SalesPilot | AI Sales Agent", page_icon="🔎", layout="wide")
st.markdown("""<style>.block-container{max-width:1250px;padding-top:1.7rem}h1{letter-spacing:-.035em}</style>""", unsafe_allow_html=True)

USERNAME = os.getenv("SALESPILOT_USERNAME") or os.getenv("CXI_USERNAME", "")
PASSWORD = os.getenv("SALESPILOT_PASSWORD") or os.getenv("CXI_PASSWORD", "")
API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MAX_HISTORY = 10

SHEETS = {
    "1. New Names": ["Azienda", "Sede", "Fatturato", "Altri dati chiave", "Fonte"],
    "2. Priorità": ["Priorità", "Azienda", "Cluster", "Cambiamento", "Accessibilità", "Volume", "Totale"],
    "3. Info aziende": ["Azienda", "Cosa sapere"],
    "4. Buyer Persona": ["Ruolo", "Peso nella decisione", "Cosa gli interessa", "Primo messaggio utile"],
    "5. Servizi CXI": ["Azienda", "Servizio principale", "Servizio secondario", "Aggancio al fatto"],
}
KEYS = ["new_names", "priorita", "informazioni", "buyer_persona", "servizi_cxi"]
TITLES = ["Lista New Names", "Clusterizzazione e priorità", "Informazioni chiave sulle aziende", "Interlocutori e Buyer Persona", "Servizi CXI pertinenti"]

if not USERNAME or not PASSWORD or PASSWORD == "CAMBIA_QUESTA_PASSWORD":
    st.error("Configura SALESPILOT_USERNAME e SALESPILOT_PASSWORD nelle variabili d'ambiente di Render.")
    st.stop()

if not st.session_state.get("authenticated", False):
    st.title("SalesPilot · Accesso")
    with st.form("login"):
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Accedi", use_container_width=True)
    if submitted:
        if hmac.compare_digest(user, USERNAME) and hmac.compare_digest(password, PASSWORD):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Credenziali non valide")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = []
if "selected_id" not in st.session_state:
    st.session_state.selected_id = None


def clean_rows(value, columns):
    if not isinstance(value, list):
        return []
    rows = []
    for item in value:
        if not isinstance(item, dict):
            continue
        row = {}
        for col in columns:
            val = item.get(col, "")
            row[col] = "" if val is None else val if isinstance(val, (int, float, str)) else str(val)
        rows.append(row)
    return rows


def normalize_result(result):
    if not isinstance(result, dict):
        raise ValueError("Gemini non ha restituito un oggetto JSON.")
    tables = {}
    for (sheet, cols), key in zip(SHEETS.items(), KEYS):
        tables[key] = clean_rows(result.get(key, []), cols)
    # Totale e graduatoria sono calcolati dal codice, non inventati dal modello.
    for row in tables["priorita"]:
        scores = []
        for key in ("Cambiamento", "Accessibilità", "Volume"):
            try:
                score = int(row[key])
                if score not in (1, 2, 3):
                    raise ValueError()
                scores.append(score)
                row[key] = score
            except (TypeError, ValueError):
                scores.append(None)
                row[key] = "Non verificato"
        row["Totale"] = sum(scores) if all(s is not None for s in scores) else "Non verificato"
    tables["priorita"].sort(key=lambda r: r["Totale"] if isinstance(r["Totale"], int) else -1, reverse=True)
    for i, row in enumerate(tables["priorita"], start=1):
        row["Priorità"] = i
    return str(result.get("sintesi", "")), tables


def demo_results():
    names = ["ESEMPIO — Alfa Industriale", "ESEMPIO — Beta Components", "ESEMPIO — Gamma Solutions"]
    return normalize_result({
        "sintesi": "**Modalità demo:** aziende e informazioni interamente fittizie. La demo mostra il formato delle cinque tabelle, non verifica i criteri della ricerca.",
        "new_names": [{"Azienda": n, "Sede": "Non verificato", "Fatturato": "Non verificato", "Altri dati chiave": "Dato illustrativo", "Fonte": "DEMO — nessuna fonte"} for n in names],
        "priorita": [{"Azienda": n, "Cluster": "Esempio", "Cambiamento": 3-i, "Accessibilità": 2, "Volume": 2} for i, n in enumerate(names)],
        "informazioni": [{"Azienda": n, "Cosa sapere": "Informazione illustrativa, non reale."} for n in names],
        "buyer_persona": [{"Ruolo": "Responsabile Customer Experience", "Peso nella decisione": "Possibile decisore", "Cosa gli interessa": "Esperienza cliente", "Primo messaggio utile": "Esempio di messaggio commerciale"}],
        "servizi_cxi": [{"Azienda": n, "Servizio principale": "Consulting X (ipotesi)", "Servizio secondario": "Operations X (ipotesi)", "Aggancio al fatto": "Esempio fittizio"} for n in names],
    })


def extract_json(text):
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.S)
        if match:
            return json.loads(match.group(0))
        raise ValueError("La risposta AI non contiene JSON valido. Riprova.")


def gemini_results(query):
    if not API_KEY:
        raise ValueError("Manca GEMINI_API_KEY nelle variabili d'ambiente di Render")
    example = {"sintesi": "Breve sintesi e limiti della ricerca", **{
        key: [{col: "..." for col in cols}] for key, cols in zip(KEYS, SHEETS.values())
    }}
    prompt = f"""Sei un assistente di pre-vendita B2B per CXI. Devi rispondere alla richiesta indipendente qui sotto.
RICHIESTA: {query}

Produci ESCLUSIVAMENTE un oggetto JSON valido con ESATTAMENTE le cinque liste e le colonne indicate in questo schema illustrativo:
{json.dumps(example, ensure_ascii=False)}

REGOLE OBBLIGATORIE:
- Le cinque tabelle seguono gli Use Case CXI. Restituisci aziende reali SOLO se supportate da informazioni attendibili; non inventare aziende, fatturati, URL, numeri, nomi o fatti.
- Non hai necessariamente accesso a ricerca web in tempo reale. Se non puoi verificare un dato, scrivi 'Non verificato'; se non puoi verificare le aziende, lascia le liste aziendali vuote e spiega il limite nella sintesi.
- new_names: 'Fatturato' SEMPRE presente, con anno di riferimento se noto. 'Fonte' deve essere un URL reale e pertinente soltanto se noto con sufficiente certezza; altrimenti 'Non verificato'. Inserisci clienti, sedi, dipendenti e altre misure settoriali in 'Altri dati chiave'.
- priorita: esattamente le stesse aziende di new_names; 'Cambiamento', 'Accessibilità', 'Volume' sono valutazioni COMMERCIALI IPOTETICHE da 1 a 3. Il codice calcolerà 'Totale' e 'Priorità'. Non inventare evidenze per giustificare punteggi.
- informazioni: esattamente le stesse aziende; 'Cosa sapere' contiene solo fatti verificabili, distinguendo chiaramente ipotesi.
- buyer_persona: ruoli aziendali pertinenti al settore, NON nomi inventati. Indica ruolo, influenza nella decisione, interessi e messaggio commerciale iniziale.
- servizi_cxi: esattamente le stesse aziende; usa soltanto categorie Consulting X, Operations X, Digital X, ESG X. Poiché non hai il catalogo ufficiale, etichetta ogni proposta come '(ipotesi)'. L'aggancio al fatto deve riferirsi a un dato effettivamente disponibile; altrimenti 'Da verificare'.
- Non sostituire il JSON con tabelle Markdown o testo extra.
"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}}
    response = requests.post(url, params={"key": API_KEY}, json=payload, timeout=110)
    if not response.ok:
        raise RuntimeError(f"Gemini API HTTP {response.status_code}. Controlla modello, chiave API e limiti di utilizzo.")
    data = response.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini non ha restituito risultati.")
    parts = candidates[0].get("content", {}).get("parts", [])
    raw = "\n".join(part.get("text", "") for part in parts if "text" in part)
    return normalize_result(extract_json(raw))


def excel_bytes(tables):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for (sheet_name, columns), key in zip(SHEETS.items(), KEYS):
            df = pd.DataFrame(tables.get(key, [])).reindex(columns=columns, fill_value="")
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            ws = writer.sheets[sheet_name]
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions
            from openpyxl.styles import Font, PatternFill, Alignment
            for cell in ws[1]:
                cell.fill = PatternFill("solid", fgColor="123A5D")
                cell.font = Font(color="FFFFFF", bold=True)
                cell.alignment = Alignment(wrap_text=True)
            for col_idx, column in enumerate(columns, 1):
                letter = ws.cell(1, col_idx).column_letter
                ws.column_dimensions[letter].width = min(54, max(17, len(column) + 5))
            for row in ws.iter_rows(min_row=2):
                for cell in row:
                    cell.alignment = Alignment(vertical="top", wrap_text=True)
    return output.getvalue()


def show_result(item):
    st.caption(f"Ricerca del {item['date']} · {item['mode']}")
    st.markdown(f"**Richiesta:** {item['query']}")
    if item.get("error"):
        st.error(item["error"])
        return
    st.markdown(item.get("summary", ""))
    for idx, ((_, columns), key, title) in enumerate(zip(SHEETS.items(), KEYS, TITLES), 1):
        st.subheader(f"{idx}. {title}")
        df = pd.DataFrame(item["tables"].get(key, [])).reindex(columns=columns, fill_value="")
        st.dataframe(df, use_container_width=True, hide_index=True)
        if df.empty:
            st.caption("Nessun dato verificabile disponibile per questa sezione.")
    st.download_button("📥 Scarica Excel delle 5 tabelle", data=excel_bytes(item["tables"]),
                       file_name=f"salespilot_ricerca_{item['id']}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       key=f"export_{item['id']}")

with st.sidebar:
    st.header("SalesPilot · Beta")
    mode = st.radio("Modalità", ["Demo (senza API)", "Gemini (API)"], index=1)
    if st.button("➕ Nuova ricerca", use_container_width=True):
        st.session_state.selected_id = None
        st.rerun()
    st.divider()
    st.subheader("Cronologia ricerche")
    st.caption(f"Ultime {MAX_HISTORY} ricerche della sessione")
    for item in reversed(st.session_state.history):
        label = f"{item['date']} · {item['query'][:38]}"
        if st.button(label, key=f"history_{item['id']}", use_container_width=True):
            st.session_state.selected_id = item["id"]
            st.rerun()
    if st.session_state.history and st.button("🗑️ Cancella cronologia", use_container_width=True):
        st.session_state.history = []
        st.session_state.selected_id = None
        st.rerun()
    st.divider()
    if st.button("Esci", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.title("SalesPilot")
st.caption("Ricerca prospect B2B · prioritizzazione · suggerimenti commerciali")
st.info("Prototipo universitario: verifica aziende, fatturati, contatti e fonti prima dell'uso commerciale.")

selected = next((x for x in st.session_state.history if x["id"] == st.session_state.selected_id), None)
if selected:
    show_result(selected)
else:
    st.markdown("Inserisci una nuova richiesta. Ogni ricerca è indipendente dalle precedenti.")

query = st.chat_input("Es. Trova 5 gruppi di concessionarie auto in Piemonte o Lombardia con fatturato >300 milioni...")
if query and query.strip():
    uid = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    item = {"id": uid, "date": datetime.now().strftime("%d/%m/%Y %H:%M"), "query": query.strip(), "mode": mode}
    try:
        if mode.startswith("Demo"):
            item["summary"], item["tables"] = demo_results()
        else:
            with st.spinner("Gemini sta elaborando la ricerca..."):
                item["summary"], item["tables"] = gemini_results(query.strip())
    except Exception as exc:
        item["error"] = f"Ricerca non completata: {exc}"
    st.session_state.history.append(item)
    st.session_state.history = st.session_state.history[-MAX_HISTORY:]
    st.session_state.selected_id = uid
    st.rerun()
