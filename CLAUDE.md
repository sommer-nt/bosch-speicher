# Hinweise für die Entwicklung mit KI-Assistenz

## Git
- Arbeitszweig ist `main`. Änderungen direkt auf `main` committen und pushen. Vor dem Arbeiten `git pull`.
- Commits immer als `Daniel Sommer <98900287+sommer-nt@users.noreply.github.com>`.
- Keine Co-Authored-By-, Session- oder „Generated with“-Zeilen in Commits; keine Modellnamen in Commits.
- Niemals Passwörter, `.env`, `secrets.toml`, Original-Kataloge (PDF) oder die Excel-Matrix einchecken.

## Projekt
- Bosch Speicher: `speicher.html` (offline) und Streamlit (`app.py`, `speicher/`). Beide Versionen rechnen
  identisch – Änderungen an der Auswahl-Logik in `speicher/logik.py` **und** im `<script id="logik">` von
  `speicher.html` nachziehen; `tests/test_speicher.py` vergleicht beide.
- Daten nur über `tools/katalog_import.py` und `tools/speicher_import.py` erzeugen, nicht von Hand in
  `speicher.json` ändern.
- Betrieb: eigener Ubuntu-Server mit Docker und nginx, siehe `deploy/ANLEITUNG.md` (speicher.sommer-nt.de).
- Vor jedem Push: `python -m pytest -q` muss grün sein.
