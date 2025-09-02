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


## Installation & Setup

### Raspberry Pi
1. **System vorbereiten:**
   ```bash
   sudo raspi-config
   # Passwort ändern, WLAN einrichten, Hostname setzen, Kamera aktivieren, Dateisystem erweitern
   sudo apt-get update
   sudo apt-get dist-upgrade
   sudo apt-get install python3 python3-pip linphone python3-gpiozero picamera mjpg-streamer git
   sudo apt remove python-rpi.gpio
   pip3 install flask waitress picamera gpiozero telegram-send python_json_config pigpio
   mkdir /home/pi/pic
   ```
2. **Samba einrichten (optional):**
   Siehe: https://www.elektronik-kompendium.de/sites/raspberry-pi/2007071.htm
3. **MJPEG Streamer installieren:**
   [MJPEG-Streamer Guide](https://github.com/cncjs/cncjs/wiki/Setup-Guide:-Raspberry-Pi-%7C-MJPEG-Streamer-Install-&-Setup-&-FFMpeg-Recording)
4. **Repository klonen:**
   ```bash
   git clone <repo-url>
   cd klingel
   ```
5. **Konfiguration anpassen:**
   - `config.json` mit eigenen Werten füllen (API-Keys, Pfade, Telefonnummern)
   - Niemals echte Schlüssel auf Github hochladen!
6. **Starten:**
   ```bash
   ./klingel.sh start
   ```
7. **Taster-Daemon als Service einrichten:**
   - `tasterd.service` nach `/etc/systemd/system/` kopieren und anpassen
   - Service aktivieren:
     ```bash
     sudo systemctl enable tasterd
     sudo systemctl start tasterd
     ```
8. **Startup (optional):**
   In `/etc/rc.local` eintragen:
   ```bash
   logger -i -t klingel -- Starte die Klingel
   runuser -l pi -c '/home/pi/hausautomatisierung/klingel/klingel.sh start'
   sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 5000
   ```

### Windows (nur Web-Interface, Debugging)
1. Python und Flask installieren
2. `configwin.json` anpassen
3. Starten:
   ```powershell
   .\start.ps1
   ```

## Shell-Kommandos & Tipps

- Service starten/stoppen:
  ```bash
  sudo systemctl enable tasterd
  sudo systemctl start tasterd
  sudo systemctl status tasterd
  ```
- Logs ansehen:
  ```bash
  journalctl -u tasterd
  cat /var/log/messages | grep "Klingel"
  cat /var/log/messages | grep "MJPG"
  ```
- Flask ausprobieren:
  ```bash
  ./klingel.sh flask
  ```
- Tasterdaemon direkt testen:
  ```bash
  python3 taster.py
  ```
- Sound testen:
  ```bash
  aplay -l   # Soundkarten anzeigen
  alsamixer
  alsactl store
  aplay /home/pi/hausautomatisierung/klingel/sounds/Doorbell.wav
  ```
- Telegram konfigurieren:
  ```bash
  telegram-send --configure
  # Token von BotFather holen
  # Siehe: https://pypi.org/project/telegram-send/#usage
  ```
- Paket lokal installierbar machen:
  ```bash
  pip install -e .
  ```

## Dateien & Verzeichnisse

**Wichtige Unterverzeichnisse:**
- `klingel/`: Flask Web-App
- `livecam/`: MJPEG-Streamer
- `sounds/`: Klingeltöne
- `tasterd/`: Tasterdaemon
- `tests/`: Unit Tests

**Wichtige Dateien:**
- `config.json`: Konfiguration für Raspberry Pi
- `configwin.json`: Konfiguration für Windows
- `klingel.sh`: Start-/Stoppskript für Linux
- `start.ps1`: Startskript für Windows
- `tasterd.service`: Systemd-Unit für Tasterdaemon
- `linphone.py`: Python-Wrapper für Linphone
- `taster.py`: Hauptdaemon

## TODO
- tasterd: Exception abfangen, wenn Bild-URL falsch oder Flask nicht läuft
- flask: Adresse für Video in JSON File konfigurierbar machen
- klingel.sh: auch tasterd bedienbar machen

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
