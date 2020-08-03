
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, Response
)
import os

from camera.camera import Camera


bp = Blueprint('live', __name__, url_prefix='/live')


@bp.route('/')
@bp.route('/live')
def list():
    return render_template('live.html')


#https://blog.miguelgrinberg.com/post/video-streaming-with-flask
#https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@bp.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

