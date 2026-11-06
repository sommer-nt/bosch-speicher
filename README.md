# Bosch Speicher

Speicherauswahl Wärmepumpe: **Wärmepumpe wählen → zugelassene Speicher** (Puffer, WW, WW bivalent, Kombi)
→ Detailansicht mit TTNr, Preis (UVP), Maßbild, Maßen und Anschlüssen, Produktfoto, Installationsanleitung,
freigegebenen Wärmepumpen und **passenden E-Heizern samt TTNr**. Suche über Speichername oder TTNr,
Vergleich von zwei Speichern.

Es gibt zwei Versionen mit identischer Auswahl-Logik:

| | `speicher.html` | Python / Streamlit |
|---|---|---|
| Start | Datei im Browser öffnen, läuft offline (Daten und Bilder eingebettet) | `streamlit run app.py` |
| Betrieb | per Mail/Datei weitergeben | eigener Server, siehe `deploy/ANLEITUNG.md` |

## Datenquellen

- Speichermatrix und E-Heizer-Liste (Excel, Matthias Spies)
- Bosch-Gesamtkatalog 03/2026, Ergänzungskatalog Speicher 07/2026, Ergänzungskatalog Elektro 07/2026
- Installationsanleitung 6721110844 (WP 290/370-2 KLP 1), Folien zu den E-Heizern der Generation -7

Angezeigt werden in der ersten Ausbaustufe nur Wärmepumpenspeicher (Speicher aus der WP-Matrix).

## Daten aktualisieren

```bash
pip install -r requirements-dev.txt
python tools/katalog_import.py Speicher_..._Gesamtkatalog.pdf EK_Speicher_..._Ergaenzungskatalog.pdf BO_..._Elektrosortiment.pdf
python tools/speicher_import.py Speichermatrix_TT.MM.JJJJ.xlsx
python -m pytest -q
```

Der Import schreibt `speicher/daten/speicher.json` und bettet Daten und Bilder in `speicher.html` ein.
Ergänzungen ohne Codeänderung: `speicher/daten/speicher_im.json` (Daten aus Installationsanleitungen),
`speicher/daten/speicher_eheizer_ergaenzung.json` (E-Heizer), `speicher/daten/speicher_stammdaten.csv` (SAP).

---

Werkzeug zur Vorplanung, nicht offiziell freigegeben. Entwickelt von Daniel Sommer · HC/SDE3-PSD.
