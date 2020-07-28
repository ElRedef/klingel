
################################################################################
#
#  SHELL KOMMANDOS
#
################################################################################


#Service starten bzw Stoppen
sudo systemctl enable klingel
sudo systemctl start klingel

#Logs anschauen des Tasterdaemon
journalctl -u tasterd

#Logs Startup und klingel
cat /var/log/messages | grep "Klingel"
cat /var/log/messages | grep "MJPG"



################################################################################
#
#  DATEIEN
#
################################################################################


tasterd.service    Unit Datei fuer Systemd. Gehört in /etc/systemd/system/




################################################################################
#
#  STARTUP
#
################################################################################

In /etc/rc.local folgendes hinzufuegen, dies startet die webapplikation und den mjpeg streamer
logger -i -t klingel -- Starte die Klingel
runuser -l pi -c '/home/pi/hausautomatisierung/klingel/klingel.sh start'

Zusätzlich muss der tasterd mit systemctl gestartet werden
tasterd.service in /etc/systemd/system/ kopieren
und mit 
sudo systemctl enable klingel
enablen
