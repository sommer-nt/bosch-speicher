# Betrieb auf eigenem Server: speicher.sommer-nt.de

Die App läuft als Docker-Container und ist nur lokal auf **127.0.0.1:8505** erreichbar. nginx leitet
`speicher.sommer-nt.de` dorthin, certbot holt das HTTPS-Zertifikat. Bosch Flow (8504) und climate (8503)
bleiben unberührt.

**1. DNS:** CNAME `speicher` → `danisox.ddns.net`. Prüfen: `dig +short speicher.sommer-nt.de`.

**2. Code holen und starten**

Das Repository ist **privat**. Der Server liest es über einen eigenen **Deploy Key** (nur lesen):

```bash
ssh-keygen -t ed25519 -f ~/.ssh/bosch_speicher -N "" -C "webmin bosch-speicher"
cat ~/.ssh/bosch_speicher.pub          # Zeile kopieren
```

GitHub → `sommer-nt/bosch-speicher` → **Settings → Deploy keys → Add deploy key**: Zeile einfügen,
„Allow write access“ **nicht** anhaken. Dann auf dem Server:

```bash
cat >> ~/.ssh/config <<'EOT'
Host github-speicher
    HostName github.com
    User git
    IdentityFile ~/.ssh/bosch_speicher
    IdentitiesOnly yes
EOT
chmod 600 ~/.ssh/config

cd ~
git clone git@github-speicher:sommer-nt/bosch-speicher.git
cd bosch-speicher/deploy
cp .env.beispiel .env && nano .env          # Passwort setzen, APP_PORT=8505
docker compose -p speicher up -d --build
curl http://127.0.0.1:8505/_stcore/health   # → ok
```

**3. nginx und HTTPS**
```bash
sudo cp nginx-speicher.sommer-nt.de.conf /etc/nginx/sites-available/speicher.sommer-nt.de
sudo ln -s /etc/nginx/sites-available/speicher.sommer-nt.de /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d speicher.sommer-nt.de
```

Fertig: **https://speicher.sommer-nt.de** (zuerst die Passwortseite).

## Im Betrieb

| Aufgabe | Befehl (im Ordner `~/bosch-speicher/deploy`) |
|---|---|
| Neue Version einspielen | `git pull && docker compose -p speicher up -d --build` |
| Logs ansehen | `docker compose -p speicher logs -f app` |
| Status | `docker compose -p speicher ps` |
| Stoppen | `docker compose -p speicher down` |

## Fehlersuche

- **Seite weiß / lädt endlos:** WebSocket-Zeilen in der nginx-Konfiguration prüfen.
- **502 Bad Gateway:** Container läuft nicht → `docker compose -p speicher ps` und `logs -f app`.
- **Port belegt:** in `.env` einen freien `APP_PORT` wählen und `proxy_pass` in der nginx-Datei anpassen.
