
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
import os



bp = Blueprint('lists', __name__, url_prefix='/')



#PATH = 'X:\pic'
PATH = '/home/pi/pic'



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


@bp.route('/')
def los():
    return 'Hello Bild2!'


@bp.route('/list')
def list():
    events = parse_dir()
    return render_template('list.html', events=events)


@bp.route('/piclist')
def piclist():
    events = parse_dir()
    return render_template('pic_list.html', events=events)

@bp.route('/<path:filename>')  
def send_file(filename):  
    return send_from_directory(PATH, filename)


