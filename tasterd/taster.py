#!/usr/bin/python3

from gpiozero import Button
import os, signal, sys
from time import sleep
from picamera import PiCamera
import http.client, urllib
import requests
import telegram_send
import datetime
import urllib.request
from shutil import copyfile
from python_json_config import ConfigBuilder
from linphone import linphone




class taster():

    #################################################################
    # Konstruktor
    def __init__(self):
        """
        Initialisiert den Taster-Daemon:
        - Lädt die Konfiguration
        - Initialisiert den GPIO-Button
        - Initialisiert die Telefonfunktion
        """
        print("Klingel GPIO Daemon")
        self.loadconfig()
        self.RASPI_BUTTON = Button(14)  # GPIO-Port für den Taster
        # Initialisiere Linphone mit Konfigurationsdaten
        self.phone = linphone()
        self.phone.ini(self.config.PHONE_HOST, self.config.PHONE_USER, self.config.PHONE_PW)

        
 
 
 
    #################################################################
    # Lädt die Config aus dem JSON File
    def loadconfig(self):
        """
        Lädt die Einstellungen aus der JSON-Konfigurationsdatei.
        Falls die Umgebungsvariable nicht gesetzt ist, wird ein Standardpfad verwendet.
        """
        self.settings_available = False
        try:
            settings_file = os.environ['KLINGEL_SETTING_FILE']
            print(f"Reading Settings from: {settings_file}")
        except:
            print("Cannot read environment variable: KLINGEL_SETTING_FILE")
            print("using default: /home/pi/hausautomatisierung/klingel/config.json")
            settings_file = '/home/pi/hausautomatisierung/klingel/config.json'
        # Konfigurationsparser erstellen
        builder = ConfigBuilder()
        try:
            self.config = builder.parse_config(settings_file)
        except:
            print(f"Cannot read setting file: {settings_file}")
            return
        self.settings_available = True

        
    #################################################################
    # Gibt einen String zurück, der das aktuelle Datum und die Uhrzeit enthält
    def date_time(self):
        """
        Gibt das aktuelle Datum und die Uhrzeit als formatierten String zurück.
        Format: YYYY_MM_DD_HH_MM_SS_microseconds
        """
        now = datetime.datetime.now()
        date_time = now.strftime("%Y_%m_%d_%H_%M_%S_%f")
        return date_time
    
    
    #################################################################
    # Sendet eine Benachrichtigung über Pushover
    def send_pushover(self, message, img_path):
        """
        Sendet eine Nachricht und ein Bild über den Pushover-Dienst.
        """
        r = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": self.config.PUSHOVER_APP_TOKEN,
                "user": self.config.PUSHOVER_USER_KEY,
                "message": message
            },
            files={
                "attachment": ("image.jpg", open(img_path, "rb"), "image/jpeg")
            }
        )
        print("Pushover: " + r.text)

      
    #################################################################
    # Sendet eine Nachricht und ein Bild über Telegram
    def send_telegram(self, message, img_path):
        """
        Sendet eine Textnachricht und ein Bild über Telegram.
        """
        telegram_send.send(messages=[message])
        with open(img_path, "rb") as f:
            telegram_send.send(images=[f])

            
    #################################################################
    # Erstellt ein Bild
    # Über "type" kann eingestellt werden, ob das Bild über die Kamera oder eine URL aufgenommen wird
    # TODO: Fehler abfangen, wenn z.B. die URL nicht erreichbar ist
    def capture_pic(self, type, dest):
        """
        Erstellt ein Bild und speichert es unter "dest".
        Typen:
        - "camera": Aufnahme mit PiCamera
        - "streamer": Download über MJPEG-Streamer-URL
        """
        if type == "camera":
            camera = PiCamera()
            try:
                camera.capture(dest)
            except:
                # Fehler beim Aufnehmen mit Kamera
                src = self.config.path + "/no_pic.jpg"
            finally:
                camera.close()
        if type == "streamer":
            try:
                urllib.request.urlretrieve(self.config.PIC_URL, dest)
            except:
                print("Failed to make image via " + self.config.PIC_URL)
                src = self.config.no_path + "no_pic.jpg"
                copyfile(src, dest)
      
       
                
    #################################################################
    # Hauptschleife: Überwacht den Taster und führt Aktionen aus
    def run(self):
        """
        Endlosschleife, die den GPIO-Taster überwacht.
        Bei Tastendruck werden folgende Aktionen ausgeführt:
        - Sound abspielen
        - Bild aufnehmen
        - (optional) Benachrichtigung versenden
        - Telefonanruf auslösen
        """
        while True:
            if self.RASPI_BUTTON.is_pressed:
                print("Pressed")
                # Klingelton abspielen
                os.system("aplay " + self.config.SOUNDFILE + "&")
                # Bild aufnehmen und speichern
                img_path = self.config.image_path + "/" + self.date_time() + '.jpg'
                self.capture_pic(self.config.PIC_SOURCE, img_path)
                # Benachrichtigungen (optional, auskommentiert)
                #self.send_pushover(self.config.MESSAGE, img_path)
                #self.send_telegram(self.config.MESSAGE, img_path)
                # Telefonstatus prüfen und Anruf auslösen
                status = self.phone.get_register_status()
                print("Linphone status: " + status)
                self.phone.dial(self.config.PHONE_NUMBER)
                self.phone.wait_for_call(self.config.PHONE_CALL_TIME)
                #sleep(3) # verhindert Sturmklingeln
            sleep(0.1)

    
    
#################################################################
# Einstiegspunkt für das Skript
if __name__ == "__main__":
    # Signal-Handler für sauberes Beenden mit Ctrl+C
    def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    print("Taster: Start watching")
    myApp = taster()
    if myApp.settings_available:
        myApp.run()
    else:
        print("Exiting due to wrong settings. Import via:")
        print("export KLINGEL_SETTING_FILE=/home/pi/hausautomatisierung/klingel/config.json")


