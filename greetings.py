"""Saluti di benvenuto, come in un'app di chat: cambiano con l'ora, il giorno e la storia dell'utente.

{nome} = nome (es. Riccardo), {nick} = diminutivo (es. Richi; se manca si usa il nome).
Forma del saluto scelta dall'utente: "m" (bentornato), "f" (bentornata), "n" (neutra).
Ogni frase ha la versione con il nome e quella senza, per chi non l'ha indicato.
"""
import random
from datetime import datetime

FORMS = {"m": "Al maschile (bentornato)", "f": "Al femminile (bentornata)", "n": "Neutro"}


def _g(form, m, f, n):
    return {"m": m, "f": f}.get(form, n)


def _lines(form):
    g = lambda m, f, n: _g(form, m, f, n)  # noqa: E731
    time_greetings = {
        "mattina": ("Buongiorno, {nome}", "Buongiorno"),
        "pomeriggio": ("Buon pomeriggio, {nome}", "Buon pomeriggio"),
        "sera": ("Buonasera, {nome}", "Buonasera"),
        "notte": ("Ancora al lavoro, {nome}?", "Ancora al lavoro?"),
    }
    sublines = [
        ("Che azienda cerchiamo oggi?",) * 2,
        ("Chi vuoi trovare oggi?",) * 2,
        ("Su quale mercato ci concentriamo?",) * 2,
        ("Raccontami il cliente ideale e ci penso io.",) * 2,
        (g("Pronto a trovare nuovi clienti?", "Pronta a trovare nuovi clienti?", "Pronti a trovare nuovi clienti?"),) * 2,
        ("Quale settore esploriamo?",) * 2,
        ("Da dove partiamo oggi?",) * 2,
        ("Dimmi chi cerchi, al resto penso io.",) * 2,
        ("{nick}, oggi chi convinciamo?", "Oggi chi convinciamo?"),
    ]
    morning = [("Caffè pronto? {nome}, allora cominciamo.", "Caffè pronto? Allora cominciamo.")]
    night = [
        (g("{nick}, ancora sveglio?", "{nick}, ancora sveglia?", "{nick}, ancora qui?"), "I clienti dormono, noi no."),
        ("Turno di notte, {nome}?", "Ti faccio compagnia."),
    ]
    night_noname = [
        (g("Ancora sveglio?", "Ancora sveglia?", "Ancora qui?"), "I clienti dormono, noi no."),
        ("Turno di notte?", "Ti faccio compagnia."),
    ]
    welcome_back = g("Bentornato", "Bentornata", "Che bello rivederti")
    returning = [
        (welcome_back + " {nome}! Continuiamo da dove eravamo rimasti?",
         welcome_back + "! Continuiamo da dove eravamo rimasti?"),
        ("Eccoti di ritorno. Nuova ricerca?",) * 2,
        ("{nick}, siamo pronti? Iniziamo.", "Siamo pronti? Iniziamo."),
    ]
    welcome = g("Benvenuto in SalesPilot", "Benvenuta in SalesPilot", "Ciao, ti diamo il benvenuto in SalesPilot")
    first = (welcome + ", {nome}", welcome, "Descrivi il cliente che cerchi e io trovo le aziende giuste.")
    return time_greetings, sublines, morning, night, night_noname, returning, first


MONDAY_LINE = ("Lunedì, eh?", "Coraggio {nome}, si parte.", "Coraggio, si parte.")


def _pick(pair, nome, nick):
    with_name, without_name = pair
    return with_name.format(nome=nome, nick=nick or nome) if nome else without_name


def build_greeting(now, nome="", nick="", has_history=False, form="n", rng=None):
    """Restituisce (saluto, frase). now: ora locale dell'utente."""
    rng = rng or random.Random()
    nome = (nome or "").strip()
    nick = (nick or "").strip() or nome
    time_greetings, sublines, morning, night, night_noname, returning, first = _lines(form)
    if not has_history:
        return (first[0].format(nome=nome) if nome else first[1]), first[2]
    hour = now.hour
    if hour >= 23 or hour < 5:
        if rng.random() < 0.6:
            title, sub = rng.choice(night if nome else night_noname)
            return title.format(nome=nome, nick=nick), sub
        return _pick(time_greetings["notte"], nome, nick), _pick(rng.choice(sublines), nome, nick)
    if now.weekday() == 0 and hour < 12 and rng.random() < 0.5:
        return MONDAY_LINE[0], MONDAY_LINE[1].format(nome=nome) if nome else MONDAY_LINE[2]
    slot = "mattina" if hour < 12 else "pomeriggio" if hour < 18 else "sera"
    title = _pick(time_greetings[slot], nome, nick)
    pool = list(sublines) + (morning if slot == "mattina" else [])
    if rng.random() < 0.3:
        pool = returning
    return title, _pick(rng.choice(pool), nome, nick)


if __name__ == "__main__":
    r = random.Random(1)
    for form in ("m", "f", "n"):
        print(form, build_greeting(datetime(2026, 11, 4, 1), "Giulia", "Giuli", True, form, r),
              build_greeting(datetime(2026, 11, 4, 9), "Giulia", "", False, form, r))
