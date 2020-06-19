#!/usr/bin/python3
#https://www.python.org/dev/peps/pep-3143/
#https://pypi.org/project/python-daemon/

from taster import taster
import daemon


print("TasterDaemon")
with daemon.DaemonContext():
        
    myApp = taster()
    myApp.run()


    




