#!/usr/bin/python3

from gpiozero import Button
import os
from time import sleep
from picamera import PiCamera
import http.client, urllib
import requests
import telegram_send
import datetime
import urllib.request
from shutil import copyfile
from python_json_config import ConfigBuilder




class taster():

    #################################################################
    #Konstruktor
    def __init__(self):
        print("Klingel GPIO Daemon")
        self.loadconfig()
        self.RASPI_BUTTON = Button(14)  # an diesen Port ist der Taster angeschlossen
        
        #Einstellungen
        #self.PUSHOVER_USER_KEY = "ue1j2qp7uuinvrcuvmzztojobzv3re"
        #self.PUSHOVER_APP_TOKEN= "asrgueig8omqmoh4zdvvxqt8kevs45"
        #self.MESSAGE = "Es ist jemand an der Tür"  #Diese Nachricht wird gesendet
        #self.PIC_URL = 'http://raspi:8080/?action=snapshot' #URL MJPEG Streamer um Bild abzuholen
        #self.PIC_SOURCE = "streamer"   #Gibt an wie das Bild aufgenomment wird: "streamer" oder "camera"
 
 
    #################################################################
    #Lädt die Config aus dem JSON File
    def loadconfig(self):
        self.settings_available = False
    
        try:
            settings_file = os.environ['KLINGEL_SETTING_FILE']
            print("Reading Settings from: "+settings_file)
        except:
            print("Cannot read environment variable: KLINGEL_SETTING_FILE")
            print("using default: config.json")
            settings_file = 'config.json'

        # create config parser
        builder = ConfigBuilder()

        # parse config
        try:
            self.config = builder.parse_config(settings_file)    
        except: 
            print("Cannot read setting file: " + settings_file)
            return
    
        self.settings_available = True

        
    #################################################################
    #Gibt einen String zurueck der das Datum wiederspiegelt
    def date_time(self):
        now = datetime.datetime.now()
        date_time = now.strftime("%Y_%m_%d_%H_%M_%S_%f")
        return date_time
    
    
    #################################################################
    #Sendet ueber Pushover
    def send_pushover(self,message, img_path):
      r = requests.post("https://api.pushover.net/1/messages.json", data = {
        "token": self.config.PUSHOVER_APP_TOKEN,
        "user": self.config.PUSHOVER_USER_KEY,
        "message": message
      },
      files = {
        "attachment": ("image.jpg", open(img_path, "rb"), "image/jpeg")
      })
      print("Pushover: "+ r.text)

      
    #################################################################
    #Sendet ueber Telegram
    def send_telegram(self,message, img_path):
        telegram_send.send(messages=[message])

        with open(img_path, "rb") as f:
            telegram_send.send(images=[f])

            
    #################################################################
    #Macht ein Bild
    #Uber Type kann eingestellt werden ob dies über den mjpeg streamer
    #Oder über die RaspiKamera gemacht wird
    #TODO: Fehler abfangen wenn z.b. MJPEG Streamer nicht erreicht werden kann
    def capture_pic(self,type,dest):
        if type=="camera":
            camera = PiCamera()
            try:
                camera.capture(dest)  
            except:
                #print("Failed to make image via " + PIC_URL)
                src = self.config.path + "/no_pic.jpg"
            finally:
                camera.close()
        if type == "streamer":
            try:
                urllib.request.urlretrieve(self.config.PIC_URL,dest)
            except:
                print("Failed to make image via " + self.config.PIC_URL)
                src = "no_pic.jpg"
                copyfile(src, dest)
                
    #################################################################
    def run(self):
        while True:
            if self.RASPI_BUTTON.is_pressed:
            #if 1:
                print("Pressed")
                img_path=self.config.image_path +"/"+ self.date_time() + '.jpg'
                self.capture_pic(self.config.PIC_SOURCE,img_path)
                sleep(0.2)
                self.send_pushover(self.config.MESSAGE,img_path)
                self.send_telegram(self.config.MESSAGE,img_path)
                sleep(3) #verhindert Sturmklingeln
            sleep(0.2)

    
    
#################################################################
if __name__ == "__main__":    
    myApp = taster()
    if myApp.settings_available:
        myApp.run()
    else:
        print("Exiting due to wrong settings. Import via:")
        print("export KLINGEL_SETTING_FILE=/home/pi/hausautomatisierung/klingel/config.json")


