
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
import os



bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/')
def list():
    return render_template('settings.html')





