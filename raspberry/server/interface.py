# coding: utf-8
import threading
import socket
import time
from glob import *
from data import *

#Thread sending information to the User Interface
class ReturnInterface(threading.Thread):

    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        while True:
            time.sleep(0.1)
            if (DATA_ULTRASONIC.message == Message.DETECTED_FRONT or DATA_LIDAR.message == Message.DETECTED_FRONT):
                #send message to interface: detection of obstacle in front of the car
                message = "OIF:" + str('')+ ";"  
                size = self.conn.send(message.encode())
            elif (DATA_ULTRASONIC.message == Message.DETECTED_BACK or DATA_LIDAR.message == Message.DETECTED_BACK):
                #send message to interface: detection of obstacle in back of the car
                message = "OIB:" + str('')+ ";"  
                size = self.conn.send(message.encode())
            elif (DATA_LIDAR.message == Message.DETECTED_BOTH or DATA_ULTRASONIC.message == Message.DETECTED_BOTH):
                #send message to interface: detection of obstacle in front and back of the car
                message = "OBB:" + str('')+ ";"  
                size = self.conn.send(message.encode())
            elif (MODE == "AUTONOMOUS"):
                message = "AUT:" + str('')+ ";"  #autonomouse mode
            else :
                #send message to interface: no obstacle detected
                message = "NOD:" + str('')+ ";"  
                size = self.conn.send(message.encode())

                
#Thread receiving driver's maneuvers
class Interface(threading.Thread):

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        global MODE
        while True:
            data = self.conn.recv(1024) #receve data from socket

            if not data: break

            header = data[0:3]
            payload = data[3:]
            print("header :", header, "payload:", str(payload))

            if (header == b'STE'):  # steering maneuvres
                # steering left
                if (payload == b'left'):
                    DATA_INTERFACE.message = Message.LEFT
                    MODE = "PILOTE"
                # steering right
                elif (payload == b'right'):
                    DATA_INTERFACE.message = Message.RIGHT
                    MODE = "PILOTE"
                    
            elif (header == b'MOV'):  # moving maneuvres
                # stopping
                if (payload == b'stop'):
                    DATA_INTERFACE.message = Message.STOP
                # moving Forward
                elif (payload == b'forward'):
                    DATA_INTERFACE.message = Message.FORWARD
                    MODE = "PILOTE"
                # moving Backward
                elif (payload == b'backward'):
                    DATA_INTERFACE.message = Message.BACKWARD
                    MODE = "PILOTE"
                # moving Backward Right
                elif (payload == b'backwardright'):
                    DATA_INTERFACE.message = Message.BACKWARD_RIGHT
                    MODE = "PILOTE"
                # moving Backward Left
                elif (payload == b'backwardleft'):
                    DATA_INTERFACE.message = Message.BACKWARD_LEFT
                    MODE = "PILOTE"
                # moving Forward Forward Left
                elif (payload == b'forwardleft'):
                    DATA_INTERFACE.message = Message.FORWARD_LEFT
                    MODE = "PILOTE"
                # moving Forward Right
                elif (payload == b'forwardright'):
                    DATA_INTERFACE.message = Message.FORWARD_RIGHT
                    MODE = "PILOTE"
               
            elif (header == b'AUT'):  # autonomous mode button
                DATA_INTERFACE.message = Message.FORWARD
              
                MODE = "AUTONOMOUS"
            print("MODE_Interface: ",MODE)
            print("Message interface: "+str(DATA_INTERFACE.message))
