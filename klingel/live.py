
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
import os



bp = Blueprint('live', __name__, url_prefix='/live')


@bp.route('/')
@bp.route('/live')
def list():
    return render_template('live.html')


@bp.route('/live_raw')
def live_raw():
    return render_template('live_raw.html')


