from flask import Flask
from flask import send_from_directory
from flask import render_template
import datetime
import os


PATH = '/home/pi/pic/'
app = Flask(__name__, static_folder=PATH) 


def date_time():
    now = datetime.datetime.now()
    date_time = now.strftime("%Y_%m_%d_%H_%M_%S_%f")
    return date_time


def parse_dir():
    events = []

    for filename in os.listdir(PATH):
        a =filename.split(".") #trennt .jpg am Schluss ab
        b=a[0].split("_")
        try:
            event = {'year':b[0],'month':b[1], 'day':b[2], 
                'hour':b[3], 'min':b[4],'sec':b[5],'msec':b[6],
                'filename':filename}
            events.append(event)
        except:
            print("kann Datei nicht öffnen")
    return events


@app.route('/')
def los():
    return 'Hello Bild!'


@app.route('/list')
def list():
    events = parse_dir()
    return render_template('list.html', events=events)

@app.route('/piclist')
def piclist():
    events = parse_dir()
    return render_template('pic_list.html', events=events)

@app.route('/<path:filename>')  
def send_file(filename):  
    return send_from_directory(app.static_folder, filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0')