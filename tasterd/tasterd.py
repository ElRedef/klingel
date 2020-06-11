#!/usr/bin/python3

from gpiozero import Button
from time import sleep
from picamera import PiCamera
import http.client, urllib
import requests
import telegram_send
import datetime
import urllib.request

print("GPIO Daemon")

#Einstellungen
PUSHOVER_USER_KEY = "ue1j2qp7uuinvrcuvmzztojobzv3re"
PUSHOVER_APP_TOKEN= "asrgueig8omqmoh4zdvvxqt8kevs45"
PATH = '/home/pi/pic/'  #Da werden die Bilder hin gespeichert
RASPI_BUTTON = Button(14)  # an diesen Port ist der Taster angeschlossen
MESSAGE = "Es ist jemand an der Tür"  #Diese Nachricht wird gesendet
PIC_URL = 'http://raspi:8080/?action=snapshot' #URL MJPEG Streamer um Bild abzuholen
PIC_SOURCE = "streamer"   #Gibt an wie das Bild aufgenomment wird: "streamer" oder "camera"

#Gibt einen String zurueck der das Datum wiederspiegelt
def date_time():
    now = datetime.datetime.now()
    date_time = now.strftime("%Y_%m_%d_%H_%M_%S_%f")
    return date_time

#Sendet ueber Pushover
def send_pushover(message, img_path):
  r = requests.post("https://api.pushover.net/1/messages.json", data = {
    "token": PUSHOVER_APP_TOKEN,
    "user": PUSHOVER_USER_KEY,
    "message": message
  },
  files = {
    "attachment": ("image.jpg", open(img_path, "rb"), "image/jpeg")
  })
  print(r.text)


#Sendet ueber Telegram
def send_telegram(message, img_path):
    telegram_send.send(messages=[message])

    with open(img_path, "rb") as f:
        telegram_send.send(images=[f])

#Macht ein Bild
#Uber Type kann eingestellt werden ob dies über den mjpeg streamer
#Oder über die RaspiKamera gemacht wird
#TODO: Fehler abfangen wenn z.b. MJPEG Streamer nicht erreicht werden kann
def capture_pic(type,dest):

    if type=="camera":
        camera = PiCamera()
        try:
            camera.capture(dest)  
        finally:
            camera.close()
    if type == "streamer":
        urllib.request.urlretrieve(PIC_URL,dest)


while True:
    if RASPI_BUTTON.is_pressed:
    #if 1:
        print("Pressed")
        img_path=PATH + date_time() + '.jpg'
        capture_pic(PIC_SOURCE,img_path)
        send_pushover(MESSAGE,img_path)
        send_telegram(MESSAGE,img_path)
        sleep(2) #verhindert Sturmklingeln
    sleep(0.2)
