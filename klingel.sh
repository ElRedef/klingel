#! /bin/bash

case "$1" in 
    start)
        echo "Starte alles fuer die Klingel"
            
            export FLASK_APP=klingel
            export FLASK_ENV=development
            flask run --host=0.0.0.0 
            /home/pi/hausautomatisierung/klingel/livecam/mjpeg.sh 
            python3  /home/pi/hausautomatisierung/klingel/tasterd/tasterd.py 
        
        ;;
    stop)
        echo "Stoppe Klingel"
        
        killall klingel.sh
        killall flask
        killall mjpg_streamer
        killall python3
        
        
        ;;
    *)
       echo "Benutzt: /etc/init.d/klingel {start|stop}"
       
       
       ;;
       
esac

exit 0
       




