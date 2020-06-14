#! /bin/bash

case "$1" in 
    start)
        echo "Starte alles fuer die Klingel"
            
            export FLASK_APP=klingel
            export FLASK_ENV=development
            export KLINGEL_SETTING_FILE=/home/pi/hausautomatisierung/klingel/config.json
            flask run --host=0.0.0.0 & 
            /home/pi/hausautomatisierung/klingel/livecam/mjpeg.sh  &
            /home/pi/hausautomatisierung/klingel/tasterd/taster.py & 
        ;;
    stop)
        echo "Stoppe Klingel"
        killall flask 
        killall mjpg_streamer 
        killall python3 

        #und jetzt sich selbst killen
        killall klingel.sh 
        ;;
        
    flask)        
        export FLASK_APP=klingel
        export FLASK_ENV=development
        export KLINGEL_SETTING_FILE=/home/pi/hausautomatisierung/klingel/config.json
        flask run --host=0.0.0.0
        ;;
    
    tasterd)        
        export KLINGEL_SETTING_FILE=/home/pi/hausautomatisierung/klingel/config.json
        /home/pi/hausautomatisierung/klingel/tasterd/taster.py & 
        ;;        
        
        
        
    *)
       echo "Benutzt: /etc/init.d/klingel {start|stop|flask|tasterd}"
       
       
       ;;
       
esac

exit 0
       




