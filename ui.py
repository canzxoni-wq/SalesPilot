"""Aspetto grafico di SalesPilot: colori, stili e piccoli blocchi HTML.

Per cambiare i colori modifica SOLO il dizionario THEME (e primaryColor in
.streamlit/config.toml con lo stesso valore di THEME["primary"]).
Tutti i testi provenienti da AI o fonti web passano da esc() prima di finire
nell'HTML, per evitare che contenuti esterni inseriscano codice nella pagina.
"""
import html
import re
from urllib.parse import urlparse

THEME = {
    "primary": "#087F8C",       # pulsanti, link, barre dei punteggi
    "primary_dark": "#05606A",  # hover dei pulsanti
    "deep": "#0B3A44",          # pannello di accesso, badge della classifica
    "deep_text": "#CFE3E6",     # testo secondario sul colore deep
    "accent_light": "#7FD6DE",  # icone sul colore deep
    "ink": "#102A33",           # testo principale
    "muted": "#4A5F66",         # testo secondario (contrasto AA su bianco)
    "bg": "#F6F7F7",            # sfondo della pagina
    "surface": "#FFFFFF",       # schede e barra laterale
    "border": "#DCE4E6",        # bordi
    "soft": "#E6F3F4",          # sfondo di chip ed elemento selezionato
    "warn_bg": "#FFF6E5",
    "warn_ink": "#6B4A00",
}


def esc(value):
    return html.escape(str(value if value is not None else ""), quote=True)


def safe_url(url):
    url = str(url or "").strip()
    parsed = urlparse(url)
    return url if parsed.scheme in ("http", "https") and parsed.netloc else ""


def selected_history_css(key):
    """Evidenzia nella barra laterale la ricerca aperta."""
    return (f"<style>.st-key-{key} button {{ background: {THEME['soft']} !important; "
            f"font-weight: 600; }}</style>")


def global_css():
    t = THEME
    return f"""<style>
.stApp {{ background: {t['bg']}; }}
.block-container {{ max-width: 1180px; padding-top: 3.5rem; }}
/* Nasconde solo menu e Deploy: il pulsante per riaprire la barra laterale resta visibile. */
#MainMenu, footer, [data-testid="stMainMenu"], [data-testid="stAppDeployButton"] {{ display: none; }}
header[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapsedControl"] {{ visibility: visible; display: flex; }}
h1, h2, h3 {{ color: {t['ink']}; letter-spacing: -0.015em; }}
[data-testid="stSidebar"] {{ background: {t['surface']}; border-right: 1px solid {t['border']}; }}
[data-testid="stSidebar"] .stButton button {{ justify-content: flex-start; text-align: left; border-color: transparent; background: transparent;
  width: 100%; min-height: 38px; padding: 6px 10px; }}
[data-testid="stSidebar"] .stButton button > div,
[data-testid="stSidebar"] .stButton button [data-testid="stMarkdownContainer"] {{ min-width: 0; max-width: 100%; width: 100%; justify-content: flex-start; text-align: left; }}
[data-testid="stSidebar"] .stButton button[kind="primary"] > div,
[data-testid="stSidebar"] .stButton button[kind="primary"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] .stButton button[kind="primary"] p {{ justify-content: center; text-align: center; }}
[data-testid="stSidebar"] .stButton button p {{ white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: left; margin: 0; }}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{ gap: 0.35rem; }}
[data-testid="stSidebar"] .stTextInput input {{ min-height: 38px; }}
[data-testid="stSidebar"] .stButton button:hover {{ background: {t['soft']}; border-color: transparent; color: {t['ink']}; }}
[data-testid="stSidebar"] .stButton button[kind="primary"] {{ justify-content: center; background: {t['primary']}; color: #FFFFFF; }}
[data-testid="stSidebar"] .stButton button[kind="primary"]:hover {{ background: {t['primary_dark']}; color: #FFFFFF; }}
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"],
.stDownloadButton button[kind="primary"] {{ background: {t['primary']}; border-color: {t['primary']}; color: #FFFFFF; min-height: 46px; font-weight: 600; }}
.stButton button[kind="primary"]:hover, .stFormSubmitButton button[kind="primary"]:hover {{ background: {t['primary_dark']}; border-color: {t['primary_dark']}; }}
[data-testid="stVerticalBlockBorderWrapper"] {{ background: {t['surface']}; border-radius: 14px; }}
[data-testid="stMetric"] {{ padding: 2px 4px; }}
[data-testid="stMetricLabel"] p {{ color: {t['muted']}; font-size: 0.85rem; }}
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid {t['border']}; }}
.stTabs [data-baseweb="tab"] {{ min-height: 44px; padding: 0 14px; font-weight: 600; }}
.stTabs [aria-selected="true"] {{ color: {t['ink']}; }}
.stTabs [data-baseweb="tab-highlight"] {{ background: {t['primary']}; height: 3px; }}
.sp-brand {{ display: flex; align-items: center; gap: 10px; margin: 0 0 16px; }}
.sp-brand-mark {{ width: 34px; height: 34px; border-radius: 9px; background: {t['deep']}; display: flex; align-items: center; justify-content: center; }}
.sp-brand-name {{ font-size: 19px; font-weight: 700; color: {t['ink']}; }}
.sp-label {{ font-size: 12px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: {t['muted']}; margin: 6px 0 2px; }}
.sp-muted {{ color: {t['muted']}; font-size: 14px; }}
.sp-rank {{ width: 56px; height: 56px; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
.sp-rank span {{ font-size: 11px; font-weight: 600; }}
.sp-rank strong {{ font-size: 22px; line-height: 1; }}
.sp-company {{ font-size: 20px; font-weight: 700; color: {t['ink']}; margin: 0; }}
.sp-company-meta {{ font-size: 14px; color: {t['muted']}; }}
.sp-chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 8px 0 4px; }}
.sp-chip {{ padding: 4px 10px; border-radius: 999px; background: {t['soft']}; color: {t['primary_dark']}; font-size: 13px; font-weight: 600; }}
.sp-chip-warn {{ background: {t['warn_bg']}; color: {t['warn_ink']}; }}
.sp-score-head {{ display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 8px; }}
.sp-score-head span {{ font-size: 13px; font-weight: 600; color: {t['muted']}; }}
.sp-score-head strong {{ font-size: 22px; color: {t['ink']}; }}
.sp-bars {{ display: grid; grid-template-columns: 96px minmax(0, 1fr) 14px; gap: 6px 8px; align-items: center; font-size: 13px; color: {t['ink']}; }}
.sp-track {{ height: 8px; border-radius: 4px; background: #E1E7E8; }}
.sp-fill {{ height: 8px; border-radius: 4px; background: {t['primary']}; }}
.sp-login-panel {{ background: {t['deep']}; color: #FFFFFF; border-radius: 16px; padding: 44px 40px; min-height: 560px; box-sizing: border-box; }}
.sp-login-panel h1 {{ color: #FFFFFF; font-size: 36px; line-height: 1.12; margin: 28px 0 12px; }}
.sp-login-panel p {{ color: {t['deep_text']}; font-size: 16px; line-height: 1.55; }}
.sp-login-panel ul {{ list-style: none; padding: 0; margin: 28px 0 0; display: flex; flex-direction: column; gap: 16px; }}
.sp-login-panel li strong {{ display: block; color: #FFFFFF; }}
.sp-login-panel li span {{ color: {t['deep_text']}; }}
</style>"""


def logo_icon(size=34, bg=None, top=None, bars="#FFFFFF"):
    """Logo SalesPilot (proposta F · Classifica): tre barre in ordine di priorità."""
    bg = bg or THEME["deep"]
    top = top or THEME["accent_light"]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 48 48" role="img" aria-label="Logo SalesPilot">'
            f'<rect width="48" height="48" rx="12" fill="{bg}"></rect>'
            f'<rect x="12" y="13" width="24" height="6" rx="3" fill="{top}"></rect>'
            f'<rect x="12" y="21" width="17" height="6" rx="3" fill="{bars}" fill-opacity="0.7"></rect>'
            f'<rect x="12" y="29" width="10" height="6" rx="3" fill="{bars}" fill-opacity="0.4"></rect></svg>')


def _wordmark(sales_color, pilot_color, size=19):
    return (f'<span style="font-size:{size}px;letter-spacing:-0.02em"><span style="font-weight:700;color:{sales_color}">'
            f'Sales</span><span style="font-weight:600;color:{pilot_color}">Pilot</span></span>')


def brand_header():
    return (f'<div class="sp-brand">{logo_icon(34)}{_wordmark(THEME["ink"], THEME["primary"])}</div>')


def login_panel():
    return f"""<div class="sp-login-panel">
<div class="sp-brand">{logo_icon(40, bg=THEME['primary'], top='#FFFFFF')}{_wordmark('#FFFFFF', THEME['accent_light'], 22)}</div>
<h1>Dal target ai clienti da contattare, con le fonti.</h1>
<p>Descrivi il tipo di azienda che cerchi. SalesPilot trova i new names, li ordina per priorità e suggerisce i servizi CXI più adatti.</p>
<ul>
<li><strong>New names verificabili</strong><span>Ogni azienda ha la fonte da cui è stata presa.</span></li>
<li><strong>Priorità spiegata</strong><span>Cambiamento, accessibilità e volume, con il motivo di ogni punteggio.</span></li>
<li><strong>Archivio personale</strong><span>Le tue ricerche sono visibili solo a te.</span></li>
</ul>
<p style="margin-top:36px;font-size:13px">Prototipo universitario · Politecnico di Torino</p>
</div>"""


def rank_badge(position):
    top = position <= 2
    bg = THEME["deep"] if top else "#E1E7E8"
    fg = "#FFFFFF" if top else THEME["ink"]
    sub = "#9CC3C9" if top else THEME["muted"]
    return (f'<div class="sp-rank" style="background:{bg};color:{fg}">'
            f'<span style="color:{sub}">N.</span><strong>{int(position)}</strong></div>')


def company_head(name, meta):
    meta_html = f' <span class="sp-company-meta">· {esc(meta)}</span>' if meta else ""
    return f'<p class="sp-company">{esc(name)}{meta_html}</p>'


def chips(items):
    """items: lista di (testo, avviso: bool)."""
    parts = [f'<span class="sp-chip{" sp-chip-warn" if warn else ""}">{esc(text)}</span>'
             for text, warn in items if str(text).strip()]
    return f'<div class="sp-chips">{"".join(parts)}</div>' if parts else ""


def score_panel(scores, total):
    """scores: lista di (etichetta, valore 1-3 o None)."""
    rows = []
    for label, value in scores:
        width = f"{round(value / 3 * 100)}%" if isinstance(value, int) else "0%"
        shown = value if isinstance(value, int) else "–"
        rows.append(f'<span>{esc(label)}</span><span class="sp-track"><span class="sp-fill" '
                    f'style="display:block;width:{width}"></span></span><span>{esc(shown)}</span>')
    total_html = f'{esc(total)}<span style="font-size:14px;color:{THEME["muted"]}">/9</span>' \
        if isinstance(total, int) else "–"
    return (f'<div class="sp-score-head"><span>Punteggio CXI</span><strong>{total_html}</strong></div>'
            f'<div class="sp-bars">{"".join(rows)}</div>')


def is_missing(value):
    return str(value or "").strip().casefold() in (
        "", "non verificato", "non individuato", "dato non disponibile", "n/d", "...", "da verificare")


def looks_estimated(value):
    return bool(re.match(r"\s*stima", str(value or ""), re.I))
