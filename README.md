# Klingel – Smarte Türklingel für Raspberry Pi

Dieses Projekt bietet eine smarte Türklingel-Lösung mit Weboberfläche, Kamera, Benachrichtigungen und Telefonintegration. Es ist für den Einsatz auf einem Raspberry Pi konzipiert, kann aber auch unter Windows getestet werden.

## Features
- **Web-Interface (Flask):** Anzeige von Bildern, Live-Stream und Einstellungen
- **Taster-Daemon:** Reagiert auf einen physischen Klingelknopf, nimmt Bilder auf, versendet Benachrichtigungen (Pushover, Telegram) und startet Telefonanrufe
- **Livebild:** Integration eines MJPEG-Streamers für die Kamera
- **Klingeltöne:** Auswahl verschiedener Sounds
- **Konfigurierbar:** Einstellungen über JSON-Dateien für verschiedene Umgebungen

## Projektstruktur
```
├── klingel/           # Flask Web-App
│   ├── __init__.py    # App-Initialisierung
│   ├── lists.py       # Bild- und Eventlisten
│   ├── live.py        # Livebild-Routen
│   ├── settings.py    # Einstellungen
│   ├── static/        # CSS-Dateien
│   └── templates/     # HTML-Templates
├── tasterd/           # Taster-Daemon
│   ├── taster.py      # Hauptdaemon
│   ├── linphone.py    # VoIP-Integration
│   └── tasterd.service# Systemd-Unit
├── livecam/           # MJPEG-Streamer
├── sounds/            # Klingeltöne
├── tests/             # Pytest-Tests
├── config.json        # Beispiel-Konfiguration (Platzhalter!)
├── configwin.json     # Beispiel-Konfiguration für Windows
├── klingel.sh         # Startskript für Linux
├── start.ps1          # Startskript für Windows
├── setup.py, setup.cfg# Paketinstallation (optional)
```

## Installation
### Raspberry Pi
1. System vorbereiten:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip linphone python3-gpiozero picamera mjpg-streamer git
   pip3 install flask waitress telegram-send python_json_config
   ```
2. Repository klonen:
   ```bash
   git clone <repo-url>
   cd klingel
   ```
3. Konfiguration anpassen:
   - `config.json` mit eigenen Werten füllen (API-Keys, Pfade, Telefonnummern)
   - Niemals echte Schlüssel auf Github hochladen!
4. Starten:
   ```bash
   ./klingel.sh start
   ```
5. Taster-Daemon als Service einrichten:
   - `tasterd.service` nach `/etc/systemd/system/` kopieren und anpassen
   - Service aktivieren:
     ```bash
     sudo systemctl enable tasterd
     sudo systemctl start tasterd
     ```

### Windows (nur Web-Interface, Debugging)
1. Python und Flask installieren
2. `configwin.json` anpassen
3. Starten:
   ```powershell
   .\start.ps1
   ```

## Konfiguration
- **config.json / configwin.json:**
  - Enthält alle Einstellungen als Platzhalter. Vor dem Einsatz mit echten Werten füllen.
  - Beispiel:
    ```json
    {
      "user": "<USER>",
      "pic_path": "<PIC_PATH>",
      ...
    }
    ```

## Sicherheitshinweise
- Niemals echte API-Keys, Passwörter oder Telefonnummern veröffentlichen!
- Konfigurationsdateien mit Platzhaltern bereitstellen und die echten Dateien in `.gitignore` aufnehmen.

## Lizenz
Dieses Projekt ist privat und dient als Beispiel für eine smarte Türklingel. Lizenz und Nutzung nach Absprache.

## Kontakt
Maintainer: JF

---

**Hinweis:**
Dieses Projekt ist ein Beispiel und kann nach eigenen Anforderungen angepasst und erweitert werden. Für produktiven Einsatz sind zusätzliche Sicherheitsmaßnahmen und Tests erforderlich.
