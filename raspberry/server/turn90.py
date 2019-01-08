import threading
import time
import can
import os
import struct
import glob
from glob import *
from data import *

toutDroit = can.Message(arbitration_id=0x010,data=[0xbc,0xbc,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
tournerDroit = can.Message(arbitration_id=0x010,data=[0xc2,0xa2,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
tournerGauche = can.Message(arbitration_id=0x010,data=[0xa2,0xc2,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
arret = can.Message(arbitration_id=0x010,data=[0x00,0x00,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)

class Turn90(threading.Thread):
    def __init__(self,bus):
        threading.Thread.__init__(self,bus)
        self.bus = bus

    def run(self):
        bus.send(toutDroit)
        if(detected):
            bus.send(tournerDroit)
            time.sleep(20)
            bus.send(arret)
            bus.send(toutDroit)
            time.sleep(2)
            bus.send(arret)
            bus.send(tournerGauche)
            time.sleep(20)
            bus.send(arret)
            bus.send(toutDroit)
            time.sleep(2)
            bus.send(tournerGauche)
            time.sleep(20)
            bus.send(arret)
            bus.send(toutDroit)
            time.sleep(2)
            bus.send(tournerDroit)
            time.sleep(20)
            bus.send(arret)
        elif():
            bus.send(tournerGauche)
            time.sleep(20)
            bus.send(arret)
        else
            bus.send(arret)
                
        
