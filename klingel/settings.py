
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
import os
import sys



bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/')
def list():
    ver = sys.version
    path = current_app.config['PIC_PATH']
    return render_template('settings.html', ver=ver, path = path, config=current_app.config)

@bp.route('/ver')
def ver():
    return sys.version


