"""Hell/Dunkel-Schalter und gemerkte Anmeldung (Streamlit-Komponente, läuft im Browser).

- schaltet das Streamlit-Farbschema um (localStorage „stActiveTheme-…“) und lädt die Seite neu,
- merkt sich die Anmeldung als Prüfwert (nicht das Passwort) nur für diesen Tab (sessionStorage), damit der
  Neuladen beim Farbwechsel nicht erneut nach dem Passwort fragt.
"""
from __future__ import annotations

import streamlit as st

ANMELDE_KEY = "bosch_speicher_anmeldung"

HTML = '<button class="theme" type="button" title="Hell / Dunkel umschalten" aria-label="Farbschema umschalten">☾</button>'
CSS = """
.theme {width:38px; height:32px; border:1px solid rgba(128,128,128,.35); background:transparent; border-radius:20px;
        cursor:pointer; font-size:15px; line-height:1; color:inherit; display:inline-flex; align-items:center;
        justify-content:center; padding:0; transition:.18s}
.theme:hover {border-color:#005691; color:#005691; box-shadow:0 0 0 3px rgba(0,86,145,.12)}
"""
JS = """
export default function (component) {
  const { data, setStateValue, parentElement } = component;
  const LOGIN = "%LOGIN%";
  const THEME = `stActiveTheme-${window.location.pathname}-v2`;
  const btn = parentElement.querySelector(".theme");
  if (!parentElement.__init) {
    parentElement.__init = true;
    let a = "";
    try { a = window.sessionStorage.getItem(LOGIN) || ""; } catch (e) {}
    setStateValue("anmeldung", a);
    btn.addEventListener("click", () => {
      const dunkel = btn.dataset.dunkel === "1";
      try { window.localStorage.setItem(THEME, JSON.stringify(dunkel ? "Light" : "Dark")); } catch (e) {}
      window.location.reload();
    });
  }
  if (data) {
    btn.dataset.dunkel = data.dunkel ? "1" : "0";
    btn.textContent = data.dunkel ? "☀" : "☾";
    btn.title = data.dunkel ? "Hell darstellen" : "Dunkel darstellen";
    try { if (data.anmeldung) window.sessionStorage.setItem(LOGIN, data.anmeldung); } catch (e) {}
  }
}
""".replace("%LOGIN%", ANMELDE_KEY)

_REG: dict = {}


def _komponente():
    from streamlit.components.v2 import get_bidi_component_manager
    manager = get_bidi_component_manager()
    if _REG.get("manager") is not manager:
        _REG["manager"] = manager
        _REG["render"] = st.components.v2.component("bosch_speicher_browser", html=HTML, css=CSS, js=JS)
    return _REG["render"]


def browser(dunkel: bool, anmeldung: str | None = None, key: str = "bs_browser") -> str | None:
    """Schalter einbinden; gibt den im Tab gemerkten Anmelde-Prüfwert zurück ("" = keiner, None = noch unbekannt)."""
    try:
        erg = _komponente()(key=key, on_anmeldung_change=lambda: None,
                            data={"dunkel": dunkel, "anmeldung": anmeldung})
    except Exception:  # noqa: BLE001 – ohne Komponenten-API läuft die App ohne Schalter weiter
        return None
    return erg.get("anmeldung") if hasattr(erg, "get") else getattr(erg, "anmeldung", None)
