import threading
import time
import can
import os
import struct
import glob
from glob import *
from data import *

"""US1 = 0x000
US2 = 0x001
flagUltrasonAvant=0
flagUltrasonArriere=0"""

class Ultrason(threading.Thread):
    def __init__(self,bus):
        threading.Thread.__init__(self)
        self.bus = bus

    def run(self):
        flagUltrasonAvant = 0
        flagUltrasonArriere = 0
        flagUltrasonAvantGauche = 0
        flagUltrasonAvantDroit = 0
        flagUltrasonAvantCentre = 0
        flagUltrasonArriereDroit = 0
        flagUltrasonArriereGauche = 0
        flagUltrasonArriereCentre = 0
        while True:
            
            msg = self.bus.recv()# Wait until a message is received.
            if msg.arbitration_id == US1:
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                #print("Avant gauche = " + str(distance))
                if distance <= 30:
                    flagUltrasonAvantGauche=1
                    print ("Avant gauche detecté")   
                else:
                    flagUltrasonAvantGauche=0     
                    
                distance = int.from_bytes(msg.data[2:4],byteorder='big')
                #print("Avant droit = " + str(distance))
                if distance <= 30:
                    flagUltrasonAvantDroit=1
                    print("Avant droit detecté")
                else:
                    flagUltrasonAvantDroit=0     
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                #print("Arriere centre = " + str(distance))
                if distance <= 100:
                    flagUltrasonArriereCentre=1
                    print("Arriere centre detecté")
                else:
                    flagUltrasonArriereCentre=0     
            elif msg.arbitration_id == US2:
                # ultrason arriere gauche
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                #print("Arriere gauche = " + str(distance))
                if distance <= 30:
                    flagUltrasonArriereGauche=1
                    print("Arriere gauche detecté")
                else:
                    flagUltrasonArriereGauche=0     
                # ultrason arriere droit
                distance = int.from_bytes(msg.data[2:4], byteorder='big')
                #print("Arriere droit = " + str(distance))
                if distance <= 30:
                    flagUltrasonArriereDroit=1
                    print("Arriere droit detecté")
                else:
                    flagUltrasonArriereDroit=0     
                # ultrason avant centre
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                #print("Avant centre = " + str(distance))
                if distance <= 100:
                    flagUltrasonAvantCentre=1
                    print("Avant centre detecté") 
                else:
                    flagUltrasonAvantCentre=0     

            if flagUltrasonAvantDroit==1 or flagUltrasonAvantGauche==1 or flagUltrasonAvantCentre ==1:
                flagUltrasonAvant = 1
            else:
                flagUltrasonAvant = 0
            if flagUltrasonArriereDroit==1 or flagUltrasonArriereGauche==1 or flagUltrasonArriereCentre ==1:
                flagUltrasonArriere = 1
            else:
                flagUltrasonArriere = 0
            if flagUltrasonAvant==1 and flagUltrasonArriere==1:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_BOTH)
            elif flagUltrasonAvant==1:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_FRONT)   
            elif flagUltrasonArriere==1:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_BACK)
            elif flagUltrasonArriere==0 and flagUltrasonAvant==0:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_NULL)
            #print("Message ultrason: "+ str(glob.DATA_ULTRASONIC.message))
