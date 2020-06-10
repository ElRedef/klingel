
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, abort
)
import os
import datetime


bp = Blueprint('lists', __name__, url_prefix='/')


#Einstellen wo die Bilder gespeichert sind
#PATH = 'X:\pic'
PATH = '/home/pi/pic'


#Dies wird benoetigt um die Bilder sortieren zu koenne
def get_year(event):
    return event.get('year')

def get_month(event):
    return event.get('month')

def get_day(event):
    return event.get('day')

def get_hour(event):
    return event.get('hour')

def get_min(event):
    return event.get('min')

def get_sec(event):
    return event.get('sec')

#sortiert die Bilder(events)
def sort(e):
    e.sort(key=get_sec,reverse=True)    
    e.sort(key=get_min,reverse=True)    
    e.sort(key=get_hour,reverse=True)    

    e.sort(key=get_day,reverse=True)    
    e.sort(key=get_month,reverse=True)    
    e.sort(key=get_year,reverse=True)   

#Geht durch das angegebene Verzeichnis und sucht alle Bilder
def parse_dir():
    events = []

    for filename in os.listdir(PATH):
        a =filename.split(".") #trennt .jpg am Schluss ab
        b=a[0].split("_")
        try: #Nur machen wenn der Dateiname das 'richtige' Format hat
            event = {'year':b[0],'month':b[1], 'day':b[2], 
                'hour':b[3], 'min':b[4],'sec':b[5],'msec':b[6],
                'filename':filename}
            events.append(event)
        except:
            print("kann Datei nicht oeffnen")
    sort(events)
    return events

###################################
#ab hier flask aufrufe


@bp.route('/list')
def list():
    events = parse_dir()
    return render_template('list.html', events=events)

@bp.route('/piclist')
def piclist():
    events = parse_dir()
    return render_template('pic_list.html', events=events,Heading="Liste aller Bilder")


@bp.route('/letzte', methods=['GET'])
def letzte():
    events = parse_dir()
    try:
        pic=request.args.get('pic')
        print("Das Bild Nr: " + pic + " wurde angefragt")
        pic=int(pic)
        filename = events[pic].get("filename")
    except:
        abort(404)
    return send_from_directory(PATH, filename)


@bp.route('/')
@bp.route('/todaylist')
def todaylist():
    events = parse_dir()
    now = datetime.datetime.now()
    events_heute = []
    for e in events:
        if int(get_day(e)) == now.day:
            events_heute.append(e)
    return render_template('pic_list.html', events=events_heute,Heading="Liste von heute")




@bp.route('/<path:filename>')  
def send_file(filename):  
    return send_from_directory(PATH, filename)


