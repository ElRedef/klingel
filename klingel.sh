#! /bin/bash

case "$1" in 
    start)
        echo "Starte alles fuer die Klingel"
        logger "Starte alles fuer die Klingel"    
        export FLASK_APP=klingel
        export FLASK_ENV=development
        export KLINGEL_SETTING_FILE=/home/pi/hausautomatisierung/klingel/config.json
        waitress-serve  --port=5000 --call 'klingel:create_app' &
        /home/pi/hausautomatisierung/klingel/livecam/mjpeg.sh  &
        ;;

    stop)
        echo "Stoppe Klingel"
        killall flask 
        killall mjpg_streamer 
        killall python3 
        killall waitress-serve
        linphonecsh unregister

        #und jetzt sich selbst killen
        killall klingel.sh 
        ;;
  
  
    flask)        
        export FLASK_APP=klingel
        export FLASK_ENV=development
        export KLINGEL_SETTING_FILE=/home/pi/hausautomatisierung/klingel/config.json
        flask run --host=0.0.0.0
        ;;
        
     waitress)        
        export FLASK_APP=klingel
        export FLASK_ENV=development
        export KLINGEL_SETTING_FILE=/home/pi/hausautomatisierung/klingel/config.json
        waitress-serve  --port=5000 --call 'klingel:create_app' &
        ;;
      
        
    mjpeg)
        /home/pi/hausautomatisierung/klingel/livecam/mjpeg.sh  &
        ;;
        
    *)
       echo "Benutzt: /etc/init.d/klingel {start|stop|flask|waitress|mjpeg}"
       
       
       ;;
       
esac

exit 0
       




