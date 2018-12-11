import threading
import time
import can
import os
import struct
import server
from data import Data
from data import ID
from data import Message

US1 = 0x000
US2 = 0x001
flagUltrasonAvant=0
flagUltrasonArriere=0

class Ultrason(threading.Thread):
    def __init__(self,bus):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.bus = bus

    def stop(self):
        self._stop.set()

    def run(self):
        while True:
            msg = self.bus.recv()# Wait until a message is received.
            arretUltrason=0
            if msg.arbitration_id == US1:
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                print("Avant gauche = " + str(distance))
                if distance <= 30:
                    flagUltrasonAvant=1;
                    DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_AVANT)
                    print(dataUltrason.message.value)
                distance = int.from_bytes(msg.data[2:4],byteorder='big')
                print("Avant droit = " + str(distance))
                if distance <= 30:
                    flagUltrasonAvant=1;
                    DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_AVANT)
                    print(dataUltrason.message.value)
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                print("Arriere centre = " + str(distance))
                if distance <= 100:
                    flagUltrasonArriere=1;
                    DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_ARRIERE)
                    print(dataUltrason.message.value)
            elif msg.arbitration_id == US2:
                # ultrason arriere gauche
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                print("Arriere gauche = " + str(distance))
                if distance <= 30:
                    flagUltrasonArriere=1;
                    DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_ARRIERE)
                    print(dataUltrason.message.value)
                # ultrason arriere droit
                distance = int.from_bytes(msg.data[2:4], byteorder='big')
                print("Arriere droit = " + str(distance))
                if distance <= 30:
                    flagUltrasonArriere=1;
                    DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_ARRIERE)
                    print(dataUltrason.message.value)
                # ultrason avant centre
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                print("Avant centre = " + str(distance))
                if distance <= 100:
                    flagUltrasonAvant=1;
                    DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_AVANT)
                    print(dataUltrason.message.value)
