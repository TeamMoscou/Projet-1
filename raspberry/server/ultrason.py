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
        while True:
            
            msg = self.bus.recv()# Wait until a message is received.
            if msg.arbitration_id == US1 or  msg.arbitration_id == US2:
                flagUltrasonAvant=0
                flagUltrasonArriere=0
            if msg.arbitration_id == US1:
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                #print("Avant gauche = " + str(distance))
                if distance <= 30:
                    flagUltrasonAvant=1        
                distance = int.from_bytes(msg.data[2:4],byteorder='big')
                #print("Avant droit = " + str(distance))
                if distance <= 30:
                    flagUltrasonAvant=1
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                #print("Arriere centre = " + str(distance))
                if distance <= 100:
                    flagUltrasonArriere=1
            elif msg.arbitration_id == US2:
                # ultrason arriere gauche
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                #print("Arriere gauche = " + str(distance))
                if distance <= 30:
                    flagUltrasonArriere=1
                # ultrason arriere droit
                distance = int.from_bytes(msg.data[2:4], byteorder='big')
                #print("Arriere droit = " + str(distance))
                if distance <= 30:
                    flagUltrasonArriere=1
                # ultrason avant centre
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                #print("Avant centre = " + str(distance))
                if distance <= 100:
                    flagUltrasonAvant=1
            if flagUltrasonAvant==1 and flagUltrasonArriere==1:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_BOTH)
            elif flagUltrasonAvant==1:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_FRONT)   
            elif flagUltrasonArriere==1:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_BACK)
            elif flagUltrasonArriere==0 and flagUltrasonAvant==0:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_NULL)
            #print("Message ultrason: "+ str(glob.DATA_ULTRASONIC.message))
