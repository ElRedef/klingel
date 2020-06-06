


print("GPIO Test")


from gpiozero import Button
from time import sleep
from picamera import PiCamera
import http.client, urllib
import requests
import telegram_send
import datetime



USER_KEY = "ue1j2qp7uuinvrcuvmzztojobzv3re"
APP_TOKEN= "asrgueig8omqmoh4zdvvxqt8kevs45"
PATH = '/home/pi/pic/'


def date_time():
    now = datetime.datetime.now()
    date_time = now.strftime("%Y_%m_%d_%H_%M_%S_%f")
    return date_time

def send_pushover(message, img_path):
  r = requests.post("https://api.pushover.net/1/messages.json", data = {
    "token": APP_TOKEN,
    "user": USER_KEY,
    "message": message
  },
  files = {
    "attachment": ("image.jpg", open(img_path, "rb"), "image/jpeg")
  })
  print(r.text)


def send_telegram(message, img_path):
    telegram_send.send(messages=[message])

    with open(img_path, "rb") as f:
        telegram_send.send(images=[f])

        
button = Button(14)
camera = PiCamera()


while True:
    if button.is_pressed:
#    if 1:
        print("Pressed")
        img_path=PATH + date_time() + '.jpg'
        camera.capture(img_path)   
        m = "Es ist jemand an der Tür"
        send_pushover(m,img_path)
        send_telegram(m,img_path)
    sleep(0.2)
