"""Bosch Speicher – Speicherauswahl Wärmepumpe (Streamlit).

Start lokal:   streamlit run app.py
Server:        deploy/ (Docker + nginx, siehe deploy/ANLEITUNG.md)

Optional mit Passwort: Umgebungsvariable SPEICHER_PASSWORT.
"""
from __future__ import annotations

import hashlib
import hmac
import os

import streamlit as st

st.set_page_config(page_title="Bosch Speicher", page_icon="💧", layout="wide")

from pathlib import Path  # noqa: E402

from speicher.browser import browser  # noqa: E402
from speicher.seite import seite  # noqa: E402

try:
    DUNKEL = st.context.theme.type == "dark"
except Exception:  # noqa: BLE001
    DUNKEL = False
try:
    _ua = st.context.headers.get("User-Agent", "") or ""
except Exception:  # noqa: BLE001
    _ua = ""
MOBIL = any(t in _ua for t in ("iPhone", "iPod", "Android", "Mobile"))

F = dict(seite="#0b1016", kachel="#131b24", linie="rgba(255,255,255,.07)", text="#e8eef4", leise="#8fa1b3",
         akzent="#4fa3e0", akzent_bg="rgba(79,163,224,.12)", gruen="#3ecf6e", gelb="#f2c14e", rot="#ff5a6a") if DUNKEL else \
    dict(seite="#f3f5f8", kachel="#ffffff", linie="rgba(16,24,40,.07)", text="#101828", leise="#667085",
         akzent="#005691", akzent_bg="rgba(0,86,145,.08)", gruen="#12b76a", gelb="#f79009", rot="#e5484d")

st.markdown(f"""<style>
.stApp {{background:{F['seite']}}}
header[data-testid="stHeader"] {{background:transparent}}
.block-container {{padding-top:2.4rem; max-width:min(1600px, 98vw)}}
.superband {{position:fixed; top:0; left:0; right:0; height:4px; z-index:999990;
            background:linear-gradient(90deg,#e20015 0%,#b90276 22%,#50237f 44%,#005691 70%,#008ecf 100%)}}
.marke {{font-weight:800; font-size:22px; letter-spacing:.2px; color:#e20015; line-height:1.1}}
.marke span {{color:{F['text']}}}
.marke small {{display:block; font-size:12px; font-weight:500; color:{F['leise']}; letter-spacing:0; margin-top:2px}}
.g-zeile {{display:flex; justify-content:space-between; font-size:13px; padding:4px 0;
          border-bottom:1px solid {F['linie']}; color:{F['text']}}}
.g-zeile span {{color:{F['leise']}}}
</style><div class="superband"></div>""", unsafe_allow_html=True)


def _passwort() -> str | None:
    for name in ("SPEICHER_PASSWORT",):
        if os.environ.get(name, "").strip():
            return os.environ[name].strip()
        try:
            wert = str(st.secrets[name]).strip()
            if wert:
                return wert
        except Exception:  # noqa: BLE001 – keine Secrets hinterlegt
            pass
    return None


@st.cache_resource
def HTML_SEITE() -> str:
    return (Path(__file__).parent / "speicher.html").read_text(encoding="utf-8")


PASSWORT = _passwort()
PRUEFWERT = hmac.new(PASSWORT.encode(), b"bosch-speicher-anmeldung", hashlib.sha256).hexdigest() if PASSWORT else ""

def _titel_mit_schalter(anmeldung: str | None, key: str) -> str | None:
    k1, k2 = st.columns([8, 1])
    k1.markdown('<div class="marke">BOSCH <span>Speicherauswahl</span><small>Wärmepumpe → Speicher → E-Heizer</small></div>',
                unsafe_allow_html=True)
    with k2:
        return browser(DUNKEL, anmeldung, key=key)


if PASSWORT and not st.session_state.get("sp_angemeldet"):
    gemerkt = _titel_mit_schalter(None, "bs_browser_login")
    if gemerkt and hmac.compare_digest(gemerkt, PRUEFWERT):     # Tab war schon angemeldet (z. B. Farbwechsel)
        st.session_state.sp_angemeldet = True
        st.rerun()
    with st.form("anmelden", border=False):
        eingabe = st.text_input("Passwort", type="password")
        if st.form_submit_button("Anmelden", type="primary", icon=":material/login:"):
            if eingabe and hmac.compare_digest(eingabe, PASSWORT):
                st.session_state.sp_angemeldet = True
                st.rerun()
            st.error("Passwort falsch.")
    st.stop()

# Oberfläche: dieselbe wie speicher.html (Vergleich mit ⚖, Foto beim Überfahren, Drucken, Hell/Dunkel).
# Die native Streamlit-Seite bleibt über ?ansicht=streamlit erreichbar.
if st.query_params.get("ansicht") == "streamlit":
    seite(F, DUNKEL, MOBIL, kopf_rechts=lambda: browser(DUNKEL, PRUEFWERT or None, key="bs_browser"))
else:
    import streamlit.components.v1 as components
    st.markdown("""<style>
    header[data-testid="stHeader"] {display:none}
    .block-container {padding:4px 0 0 0 !important; max-width:100% !important}
    [data-testid="stMainBlockContainer"] {padding:4px 0 0 0 !important}
    .superband {display:none}
    iframe {height:calc(100vh - 10px) !important; width:100% !important; border:0}
    </style>""", unsafe_allow_html=True)
    components.html(HTML_SEITE(), height=900, scrolling=True)
