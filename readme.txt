
################################################################################
#
#  SHELL KOMMANDOS
#
################################################################################


#Service starten bzw Stoppen
sudo systemctl enable klingel
sudo systemctl start klingel

#Logs anschauen des Tasterdaemon
journalctl -u tasterd

#Logs Startup und klingel
cat /var/log/messages | grep "Klingel"
cat /var/log/messages | grep "MJPG"


#flask ausprobieren
./klingel.sh flask

#tasterdaemon so ausprobieren
python3 taster.py


#sound
aplay -l   # anzeigen welche soundkarten vorhanden sind
alsamixer
alsactl store
aplay /home/pi/hausautomatisierung/klingel/sounds/Doorbell.wav


################################################################################
#
#  DATEIEN
#
################################################################################


tasterd.service    Unit Datei fuer Systemd. Gehört in /etc/systemd/system/




################################################################################
#
#  STARTUP
#
################################################################################

In /etc/rc.local folgendes hinzufuegen, dies startet die webapplikation und den mjpeg streamer
logger -i -t klingel -- Starte die Klingel
runuser -l pi -c '/home/pi/hausautomatisierung/klingel/klingel.sh start'

Zusätzlich muss der tasterd mit systemctl gestartet werden
tasterd.service in /etc/systemd/system/ kopieren
und mit 
'sudo systemctl enable klingel'
enablen



################################################################################
#
#  Installation
#
################################################################################

sudo raspi-config
  - Passwort aendern
  - Evtl: WLAN einrichten
  - hostname
  - Kamera aktivieren
  - Dateisystem erweitern
  - ...
sudo apt-get update
sudo apt-get dist-upgrade





Samba einrichten
https://www.elektronik-kompendium.de/sites/raspberry-pi/2007071.htm
 
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install linphone
sudo apt-get install git
sudo apt remove python-rpi.gpio
sudo apt install python3-gpiozero


MJPEG Streamer installieren
https://github.com/cncjs/cncjs/wiki/Setup-Guide:-Raspberry-Pi-%7C-MJPEG-Streamer-Install-&-Setup-&-FFMpeg-Recording

git auschecken
git clone ssh://johannes@192.168.178.2/volume1/git_repos/hausautomatisierung.git


nano ~/.bashrc
 und dort
 alias python='/usr/bin/python3'
 alias pip=pip3
an und abmelden

pip install flask
    waitress
    picamera
    gpiozero
    telegram_send
    python_json_config
    pigpio
    
    
 
mkdir /home/pi/pic
 
# mit folgendem Befehl kann die gewünschte Soundkarte ermittelt werden:
aplay -l

mcedit /usr/share/alsa/alsa.conf
# in folgenden Zeilen die 0 gegen die ID der ermittelten Soundkarte tauschen und speichern:
defaults.ctl.card 0
defaults.pcm.card 0
 
  

################################################################################
#
#  TODO
#
################################################################################
tasterd: Exception abfangen wenn URL für Bild falsch bzw. flask nicht läuft? Hostname nicht bekannt?
flask: Livebild adresse konfigurierbar
tasterd: fehler abfangen wenn telegram nicht funktioniert

