#!/bin/bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --host=0.0.0.0 &

/home/pi/hausautomatisierung/klingel/livecam/mjpeg.sh &

python3  /home/pi/hausautomatisierung/klingel/tasterd/tasterd.py &


