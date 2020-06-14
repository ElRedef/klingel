#!/usr/bin/python3

from gpiozero import Button
from time import sleep
from picamera import PiCamera
import http.client, urllib
import requests
import telegram_send
import datetime
import urllib.request
from shutil import copyfile




class taster():


    def __init__(self):
        print("Klingel GPIO Daemon")

        #Einstellungen
        self.PUSHOVER_USER_KEY = "ue1j2qp7uuinvrcuvmzztojobzv3re"
        self.PUSHOVER_APP_TOKEN= "asrgueig8omqmoh4zdvvxqt8kevs45"
        self.PATH = '/home/pi/pic/'  #Da werden die Bilder hin gespeichert
        self.RASPI_BUTTON = Button(14)  # an diesen Port ist der Taster angeschlossen
        self.MESSAGE = "Es ist jemand an der Tür"  #Diese Nachricht wird gesendet
        self.PIC_URL = 'http://raspi:8080/?action=snapshot' #URL MJPEG Streamer um Bild abzuholen
        self.PIC_SOURCE = "streamer"   #Gibt an wie das Bild aufgenomment wird: "streamer" oder "camera"



    #Gibt einen String zurueck der das Datum wiederspiegelt
    def date_time(self):
        now = datetime.datetime.now()
        date_time = now.strftime("%Y_%m_%d_%H_%M_%S_%f")
        return date_time

    #Sendet ueber Pushover
    def send_pushover(self,message, img_path):
      r = requests.post("https://api.pushover.net/1/messages.json", data = {
        "token": self.PUSHOVER_APP_TOKEN,
        "user": self.PUSHOVER_USER_KEY,
        "message": message
      },
      files = {
        "attachment": ("image.jpg", open(img_path, "rb"), "image/jpeg")
      })
      print(r.text)


    #Sendet ueber Telegram
    def send_telegram(self,message, img_path):
        telegram_send.send(messages=[message])

        with open(img_path, "rb") as f:
            telegram_send.send(images=[f])

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
                src = "no_pic.jpg"
            finally:
                camera.close()
        if type == "streamer":
            try:
                urllib.request.urlretrieve(self.PIC_URL,dest)
            except:
                print("Failed to make image via " + self.PIC_URL)
                src = "no_pic.jpg"
                copyfile(src, dest)
                

    def run(self):
        while True:
            if self.RASPI_BUTTON.is_pressed:
            #if 1:
                print("Pressed")
                img_path=self.PATH + self.date_time() + '.jpg'
                self.capture_pic(self.PIC_SOURCE,img_path)
                sleep(0.2)
                self.send_pushover(self.MESSAGE,img_path)
                self.send_telegram(self.MESSAGE,img_path)
                sleep(2) #verhindert Sturmklingeln
            sleep(0.2)

    
if __name__ == "__main__":    
    myApp = taster()
    myApp.run()


