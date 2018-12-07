#!/usr/bin/python3
#
#Modification de test.py avec trucs de server.py 
#pour tester les ultrasons
#
#

from threading import Thread
import time
import can
import os
import struct

US1 = 0x000
US2 = 0x001
flagUltrasonAvant=0
flagUltrasonArriere=0

class Ultrason(Thread):
    def __init__(self, bus):
        Thread.__init__(self)
        self.bus = bus

    def run(self):
        while True:
            msg = self.bus.recv()# Wait until a message is received.
            arretUltrason=0
            if msg.arbitration_id == US1:
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                print("Avant gauche = " + str(distance))
                if distance <= 30:
                    flagUltrasonAvant=1;	 
                distance = int.from_bytes(msg.data[2:4],byteorder='big')
                print("Avant droit = " + str(distance))
                if distance <= 30:
                    flagUltrasonAvant=1;
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                print("Arriere centre = " + str(distance))
                if distance <= 50:
                    flagUltrasonArriere=1;
            elif msg.arbitration_id == US2:
                # ultrason arriere gauche
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                print("Arriere gauche = " + str(distance))
                if distance <= 30:
                    flagUltrasonArriere=1;
                # ultrason arriere droit
                distance = int.from_bytes(msg.data[2:4], byteorder='big')
                print("Arriere droit = " + str(distance))
                if distance <= 30:
                    flagUltrasonArriere=1;
                # ultrason avant centre
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                print("Avant centre = " + str(distance))
                if distance <= 50:
                    flagUltrasonAvant=1;
