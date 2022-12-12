
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
import os
import sys
import getpass



bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/')
def list():
    ver = sys.version
    path = current_app.config['PIC_PATH']
    user = getpass.getuser()

    conf = current_app.config
    conf = [] #AAAACHTUNG: DANN WIRD AUCH DER SECRET KEY ANGEZEIGT
    
    return render_template('settings.html', ver=ver, path = path, user=user,config=conf)

@bp.route('/ver')
def ver():
    return sys.version


# a simple page that says hello
@bp.route('/hello')
def hello():
    return 'Hello, Pytest!'