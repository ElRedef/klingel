
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
import os



bp = Blueprint('last', __name__, url_prefix='/last')


@bp.route('/')
@bp.route('/last')
def list():
    return "last"





