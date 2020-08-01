#! /bin/bash

case "$1" in 
    start)
        echo "Starte alles fuer die Klingel"
        logger "Starte alles fuer die Klingel"    
        export FLASK_APP=klingel
        export FLASK_ENV=development
        export KLINGEL_SETTING_FILE=/home/pi/hausautomatisierung/klingel/config.json
        #flask run --host=0.0.0.0 & 
        waitress-serve  --port=5000 --call 'klingel:create_app' &
        /home/pi/hausautomatisierung/klingel/livecam/mjpeg.sh  &
        # /home/pi/hausautomatisierung/klingel/tasterd/taster.py & 
        
        #echo "Registriere Linphone"
        #logger "Registriere Linphone"    
        #sleep 3
        #linphonecsh init
        #sleep 10 
        #linphonecsh register --host 192.168.178.1 --username 12345678 --password Rambo123
        
        #echo "fertig Registriere Linphone"
        #logger "fertig Registriere Linphone"    
        
        
        
        ;;
    stop)
        echo "Stoppe Klingel"
        killall flask 
        killall mjpg_streamer 
        killall python3 
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
        
    
    tasterd)        
        # export KLINGEL_SETTING_FILE=/home/pi/hausautomatisierung/klingel/config.json
        # /home/pi/hausautomatisierung/klingel/tasterd/taster.py & 
        ;;        
        
        
        
    *)
       echo "Benutzt: /etc/init.d/klingel {start|stop|flask|waitress}"
       
       
       ;;
       
esac

exit 0
       




