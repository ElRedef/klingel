#!/usr/bin/python3

from taster import taster
import daemon


print("TasterDaemon")
with daemon.DaemonContext():
        
    myApp = taster()
    myApp.run()


    




