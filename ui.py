"""Aspetto grafico di SalesPilot: colori, stili e piccoli blocchi HTML.

Per cambiare i colori modifica SOLO il dizionario THEME (e primaryColor in
.streamlit/config.toml con lo stesso valore di THEME["primary"]).
Tutti i testi provenienti da AI o fonti web passano da esc() prima di finire
nell'HTML, per evitare che contenuti esterni inseriscano codice nella pagina.
"""
import html
import os
import re
from urllib.parse import urlparse

LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo-icon.png")

LIGHT = {
    "primary": "#087F8C",       # pulsanti, link, barre dei punteggi
    "primary_dark": "#05606A",  # hover dei pulsanti, testo dei chip
    "on_primary": "#FFFFFF",    # testo sopra il colore primario
    "primary_text": "#087F8C",  # link e parola "Pilot" su fondo chiaro
    "deep": "#0B3A44",          # pannello di accesso, badge della classifica
    "deep_text": "#CFE3E6",     # testo secondario sul colore deep
    "accent_light": "#7FD6DE",  # icone sul colore deep
    "ink": "#102A33",           # testo principale
    "muted": "#4A5F66",         # testo secondario (contrasto AA su bianco)
    "bg": "#F6F7F7",            # sfondo della pagina
    "surface": "#FFFFFF",       # schede e barra laterale
    "border": "#DCE4E6",        # bordi
    "soft": "#E6F3F4",          # sfondo di chip ed elemento selezionato
    "track": "#E1E7E8",         # binario delle barre e badge spento
    "warn_bg": "#FFF6E5",
    "warn_ink": "#6B4A00",
}
# Modalità scura: stessi ruoli, colori adatti a uno sfondo scuro (contrasto AA).
DARK = {
    "primary": "#2AA7B5",
    "primary_dark": "#5CC3CE",
    "on_primary": "#06222A",
    "primary_text": "#6FD3DC",
    "deep": "#0B3A44",
    "deep_text": "#B9D3D8",
    "accent_light": "#7FD6DE",
    "ink": "#E6EEF0",
    "muted": "#9FB1B6",
    "bg": "#0F1416",
    "surface": "#161D20",
    "border": "#2A3538",
    "soft": "#183238",
    "track": "#2A3538",
    "warn_bg": "#3A2E14",
    "warn_ink": "#F0C66B",
}
# Nel codice i colori sono variabili CSS: chiaro e scuro si scambiano subito quando l'utente
# cambia tema dal menu ⋮, senza ricaricare la pagina (vedi THEME_WATCH_JS).
THEME = {k: f"var(--sp-{k.replace('_', '-')})" for k in LIGHT}


def theme_vars_css():
    light = "".join(f"--sp-{k.replace('_', '-')}: {v};" for k, v in LIGHT.items())
    dark = "".join(f"--sp-{k.replace('_', '-')}: {v};" for k, v in DARK.items())
    return f":root {{ {light} }} html[data-sp-theme=\"dark\"] {{ {dark} }}"


# Legge il colore di sfondo dell'app (che Streamlit cambia con il tema) e segna la pagina come chiara o scura.
THEME_WATCH_JS = """<script>
(function () {
  function apply() {
    var app = document.querySelector('.stApp') || document.body;
    var m = (getComputedStyle(app).backgroundColor || '').match(/\\d+/g);
    var dark = m && (0.299 * m[0] + 0.587 * m[1] + 0.114 * m[2]) < 128;
    document.documentElement.setAttribute('data-sp-theme', dark ? 'dark' : 'light');
  }
  apply();
  if (!window.__spThemeWatch) { window.__spThemeWatch = setInterval(apply, 400); }
})();
</script>"""


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
{theme_vars_css()}
/* Lo sfondo della pagina lo decide Streamlit (config.toml): serve allo script del tema per capire chiaro/scuro. */
.block-container {{ max-width: 1180px; padding-top: 3.5rem; }}
/* Nasconde solo menu e Deploy: il pulsante per riaprire la barra laterale resta visibile. */
/* Il menu ⋮ di Streamlit è nascosto: il tema si sceglie dal selettore nella barra laterale,
   che usa il menu "dietro le quinte" (vedi theme_switch_js). */
footer, [data-testid="stAppDeployButton"], [data-testid="stMainMenu"] {{ display: none; }}
[data-testid="stMainMenuPopover"] {{ opacity: 0 !important; pointer-events: none !important; }}
header[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapsedControl"] {{ visibility: visible; display: flex; }}
h1, h2, h3 {{ color: {t['ink']}; letter-spacing: -0.015em; }}
a, a:visited {{ color: {t['primary_text']}; }}
button[kind^="primary"], button[kind^="primary"] p {{ color: {t['on_primary']} !important; font-weight: 600; }}
button[kind^="primary"] {{ background: {t['primary']} !important; border-color: {t['primary']} !important; }}
button[kind^="primary"]:hover {{ background: {t['primary_dark']} !important; border-color: {t['primary_dark']} !important; }}
[data-testid="stSidebar"] {{ background: {t['surface']}; border-right: 1px solid {t['border']}; }}
[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{ display: flex; flex-direction: column; }}
[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{ display: flex; flex-direction: column; height: 100vh; }}
/* La riga con il pulsante per chiudere la barra non occupa spazio: il logo parte dall'alto. */
[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {{ position: absolute; top: 0; right: 0; height: auto;
  padding: 0.75rem 0.75rem 0 0; z-index: 2; }}
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{ padding-top: 1.25rem; padding-bottom: 1rem; flex: 1;
  display: flex; flex-direction: column; min-height: 0; }}
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div {{ flex: 1; display: flex; flex-direction: column; }}
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div > [data-testid="stVerticalBlock"] {{ flex: 1; }}
/* Il blocco principale della barra occupa tutta l'altezza: l'account resta in fondo, come nelle app di chat. */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{ gap: 2px; }}
/* Voci di navigazione e cronologia: righe a tutta larghezza, testo a sinistra su una riga */
[data-testid="stSidebar"] .stButton button[kind="tertiary"] {{ width: 100%; min-height: 36px; padding: 6px 10px; border-radius: 8px;
  justify-content: flex-start; color: {t['ink']}; font-weight: 500; }}
[data-testid="stSidebar"] .stButton button[kind="tertiary"]:hover {{ background: {t['soft']}; color: {t['ink']}; }}
[data-testid="stSidebar"] .stButton button[kind="tertiary"] > div,
[data-testid="stSidebar"] .stButton button[kind="tertiary"] [data-testid="stMarkdownContainer"] {{ min-width: 0; width: 100%; justify-content: flex-start; text-align: left; }}
[data-testid="stSidebar"] .stButton button[kind="tertiary"] p {{ white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: left; margin: 0; font-size: 14px; }}
[data-testid="stSidebar"] .stButton button[kind="tertiary"] [data-testid="stIconMaterial"] {{ color: {t['muted']}; font-size: 20px; }}
[data-testid="stSidebar"] .stTextInput input {{ min-height: 36px; }}
[data-testid="stSidebar"] .stPopover button {{ min-height: 36px; border-color: transparent; background: transparent; }}
.sp-sidebar-spacer {{ min-height: 16px; }}
[data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.sp-sidebar-spacer) {{ flex: 1; }}
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button {{ padding: 4px 6px; min-height: 34px; font-size: 13px; }}
[data-testid="stSidebar"] [data-testid="stButtonGroup"] > div {{ flex-wrap: nowrap; }}
[data-testid="stLayoutWrapper"]:has(> .st-key-account_box) {{ margin-top: auto; }}
.st-key-account_box {{ border-top: 1px solid {t['border']}; padding-top: 10px; }}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{ margin-bottom: 0 !important; }}
.sp-label {{ display: block; font-size: 12px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: {t['muted']};
  padding: 14px 10px 2px; line-height: 1.4; }}
.sp-group {{ display: block; font-size: 12px; font-weight: 600; color: {t['muted']}; padding: 8px 10px 2px; line-height: 1.4; }}
.sp-steps {{ list-style: none; margin: 4px 0 0; padding: 0; display: flex; flex-direction: column; gap: 6px; font-size: 14px; }}
.sp-steps li {{ display: flex; align-items: center; gap: 8px; color: {t['muted']}; }}
.sp-steps li.done {{ color: {t['ink']}; }}
.sp-steps li.now {{ color: {t['ink']}; font-weight: 600; }}
.sp-dot {{ width: 8px; height: 8px; border-radius: 50%; background: {t['primary']}; animation: sp-pulse 1s ease-in-out infinite; }}
@keyframes sp-pulse {{ 0%, 100% {{ opacity: 0.35; }} 50% {{ opacity: 1; }} }}
.sp-user {{ display: flex; align-items: center; gap: 10px; min-width: 0; }}
.sp-avatar {{ flex: none; width: 32px; height: 32px; border-radius: 50%; background: {t['deep']}; color: #FFFFFF; font-size: 12px; font-weight: 700;
  display: flex; align-items: center; justify-content: center; }}
.sp-user-text {{ display: flex; flex-direction: column; min-width: 0; line-height: 1.25; }}
.sp-user-text strong {{ font-size: 13px; color: {t['ink']}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.sp-user-text span {{ font-size: 12px; color: {t['muted']}; }}
.stTabs [data-baseweb="tab-panel"] {{ padding-top: 1rem; }}
.st-key-continue_box {{ margin-top: 1rem; }}
.sp-table-wrap {{ margin-bottom: 1rem; overflow-x: auto; border: 1px solid {t['border']}; border-radius: 12px; background: {t['surface']}; }}
.sp-table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
.sp-table th {{ text-align: left; padding: 10px 12px; background: {t['bg']}; color: {t['muted']}; font-size: 13px; font-weight: 600;
  border-bottom: 1px solid {t['border']}; white-space: nowrap; }}
.sp-table td {{ padding: 10px 12px; border-bottom: 1px solid {t['border']}; vertical-align: top; color: {t['ink']}; line-height: 1.45;
  min-width: 120px; max-width: 420px; overflow-wrap: anywhere; }}
.sp-table tr:last-child td {{ border-bottom: 0; }}
.sp-dim {{ color: {t['muted']}; }}
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"],
.stDownloadButton button[kind="primary"] {{ background: {t['primary']}; border-color: {t['primary']}; color: {t['on_primary']}; min-height: 46px; font-weight: 600; }}
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
.sp-track {{ height: 8px; border-radius: 4px; background: {t['track']}; }}
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
            f'<rect width="48" height="48" rx="12" style="fill:{bg}"></rect>'
            f'<rect x="12" y="13" width="24" height="6" rx="3" style="fill:{top}"></rect>'
            f'<rect x="12" y="21" width="17" height="6" rx="3" style="fill:{bars}" fill-opacity="0.7"></rect>'
            f'<rect x="12" y="29" width="10" height="6" rx="3" style="fill:{bars}" fill-opacity="0.4"></rect></svg>')


def _wordmark(sales_color, pilot_color, size=19):
    return (f'<span style="font-size:{size}px;letter-spacing:-0.02em"><span style="font-weight:700;color:{sales_color}">'
            f'Sales</span><span style="font-weight:600;color:{pilot_color}">Pilot</span></span>')


def brand_header():
    return (f'<div class="sp-brand" style="padding:0 6px">{logo_icon(36)}{_wordmark(THEME["ink"], THEME["primary_text"], 21)}</div>')


def user_card(title, subtitle="Account Manager"):
    title = str(title or "")
    initials = "".join(w[0] for w in title.split()[:2]).upper() if " " in title else title[:2].upper()
    return (f'<div class="sp-user"><span class="sp-avatar">{esc(initials or "SP")}</span>'
            f'<span class="sp-user-text"><strong>{esc(title)}</strong><span>{esc(subtitle)}</span></span></div>')


def _cell(value):
    text = str(value if value is not None else "")
    url = safe_url(text)
    if url:
        label = urlparse(url).netloc.replace("www.", "") or "link"
        return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a>'
    return esc(text) if text.strip() else '<span class="sp-dim">–</span>'


def theme_switch_js(want):
    """Applica il tema scelto (System/Light/Dark) usando il selettore nativo di Streamlit, nascosto."""
    want = want if want in ("System", "Light", "Dark") else "System"
    return """<script>
(function () {
  var want = "%s";
  function current() {
    try { return JSON.parse(localStorage.getItem('stActiveTheme-/-v2') || '"System"'); } catch (e) { return 'System'; }
  }
  if (current() === want) { return; }
  var tries = 0;
  (function attempt() {
    var menu = document.querySelector('[data-testid="stMainMenu"] button');
    if (!menu) { if (tries++ < 30) { setTimeout(attempt, 150); } return; }
    menu.click();
    setTimeout(function () {
      var option = document.querySelector('[data-testid="stMainMenuItem-theme-' + want + '"]');
      if (option) { option.click(); }
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      setTimeout(function () {
        if (document.querySelector('[data-testid="stMainMenuPopover"]')) { menu.click(); }
      }, 120);
    }, 120);
  })();
})();
</script>""" % want


def steps_list(steps, running=True):
    """Fasi della ricerca: completate con ✓, quella in corso con un punto che pulsa."""
    items = []
    for i, text in enumerate(steps):
        last = i == len(steps) - 1
        if last and running:
            items.append(f'<li class="now"><span class="sp-dot"></span>{esc(text)}…</li>')
        else:
            items.append(f'<li class="done">✓ {esc(text)}</li>')
    return f'<ul class="sp-steps">{"".join(items)}</ul>'


HIDE_STALE_CSS = ("<style>[data-testid=\"stMain\"] [data-stale=\"true\"] { display: none !important; }</style>")


def html_table(rows, columns):
    """Tabella con testo a capo: ogni colonna è leggibile per intero."""
    head = "".join(f"<th>{esc(c)}</th>" for c in columns)
    body = "".join("<tr>" + "".join(f"<td>{_cell(r.get(c))}</td>" for c in columns) + "</tr>" for r in rows)
    return (f'<div class="sp-table-wrap"><table class="sp-table"><thead><tr>{head}</tr></thead>'
            f'<tbody>{body}</tbody></table></div>')


def login_panel():
    return f"""<div class="sp-login-panel">
<div class="sp-brand" style="gap:16px">{logo_icon(68, bg=THEME['primary'], top='#FFFFFF')}{_wordmark('#FFFFFF', THEME['accent_light'], 40)}</div>
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
    bg = THEME["deep"] if top else THEME["track"]
    fg = "#FFFFFF" if top else THEME["ink"]
    sub = THEME["deep_text"] if top else THEME["muted"]
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
