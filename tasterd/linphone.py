#!/usr/bin/python3

from time import sleep
import subprocess
from subprocess import PIPE


class linphone:

    #################################################################
    #Konstruktor / Destuktor
    #def __init(self):
        #print("Init")

    def __del__(self):
        self.exit()

    ##############################################################    
    #Kommunikation mit linphonecsh

    def run(self,arg):
        #c = "/usr/bin/linphonecsh"
        args = ['/usr/bin/linphonecsh'] + arg
        r = subprocess.run(args, stdout=PIPE, stderr=PIPE)
        return r.stdout.decode("utf-8"),r.stderr.decode("utf-8")
        
    def run_generic(self,arg):
        c = "/usr/bin/linphonecsh"
        args = ['/usr/bin/linphonecsh','generic'] + arg
        r = subprocess.run(args, stdout=PIPE, stderr=PIPE)
        return r.stdout.decode("utf-8"),r.stderr.decode("utf-8")

    
    ##############################################################    
    #(De-) Initialisieren    
    def ini(self,host,user,pwd):
        try:
            if self.get_register_status() != "registered":
                o,e = self.run(['init'])
                sleep(5)
                arg = ['register', '--host', host, '--username', user, '--password', pwd]
                o,e = self.run(arg)
        except:
            "Exception at initialising linhphone"


    def exit(self):
        o,e = self.run(['exit'])       
       
    ##############################################################        
    #Statusabfragen
    def get_register_status(self):
        o,e = self.run( ['status', 'register'])
        if len(e) != 0:
            return "ERROR" 
        if o.find("registered=0") != -1:
            return "not registered"
        if o.find("registered,") != -1:
            return "registered"
        return "Unknown Status"

        
    def get_call_status(self):
        o,e = self.run_generic(["calls"])
        if len(e) != 0:
            return "ERROR" 
        if o.find("OutgoingEarlyMedia") != -1:
            return "OutgoingEarlyMedia"
        if o.find("StreamsRunning") != -1:
            return "StreamsRunning"
        if o.find("No active call") != -1:
            return "No active call"
        return "Unknown Status"
       
       
    ##############################################################        
    #High Level telefoniefunktionen
    def dial(self,number):
        o,e = self.run(['dial', number])
 
    def hang_up(self):
        o,e = self.run_generic(["terminate all"])
       
    def wait_for_call(self,n):
        for i in range(n):
            sleep(1)
            if self.get_call_status()=="StreamsRunning":
                return
        self.hang_up() #Auflegen wenn keiner ran gegangen ist
    

    
if __name__ == "__main__":      
    print("Linphone test")
     
    phone = linphone()
    phone.ini("192.168.178.1","12345678","Rambo123")
    phone.dial("**611")
    phone.wait_for_call(5)
    
    

