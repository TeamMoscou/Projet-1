# coding: utf-8
import threading
import socket
import time
from data import *
import glob

#Thread sending information to the User Interface
class ReturnInterface(threading.Thread):

    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        while True:
            time.sleep(0.1)
            if (glob.DATA_ULTRASONIC.message == Message.DETECTED_FRONT or glob.DATA_LIDAR.message == Message.DETECTED_FRONT):
                #send message to interface: detection of obstacle in front of the car
                message = "OIF:" + str('')+ ";"  
                size = self.conn.send(message.encode())
            elif (glob.DATA_ULTRASONIC.message == Message.DETECTED_BACK or glob.DATA_LIDAR.message == Message.DETECTED_BACK):
                #send message to interface: detection of obstacle in back of the car
                message = "OIB:" + str('')+ ";"  
                size = self.conn.send(message.encode())
            elif (glob.DATA_LIDAR.message == Message.DETECTED_BOTH or glob.DATA_ULTRASONIC.message == Message.DETECTED_BOTH):
                #send message to interface: detection of obstacle in front and back of the car
                message = "OBB:" + str('')+ ";"  
                size = self.conn.send(message.encode())
            elif (glob.MODE == "AUTONOMOUS"):
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

        while True:
            data = self.conn.recv(1024) #receve data from socket

            if not data: break

            header = data[0:3]
            payload = data[3:]
            print("header :", header, "payload:", str(payload))

            if (header == b'STE'):  # steering maneuvres
                # steering left
                if (payload == b'left'):
                    glob.DATA_INTERFACE.message = Message.LEFT
                    glob.MODE = "PILOTE"
                # steering right
                elif (payload == b'right'):
                    glob.DATA_INTERFACE.message = Message.RIGHT
                    glob.MODE = "PILOTE"
                    
            elif (header == b'MOV'):  # moving maneuvres
                # stopping
                if (payload == b'stop'):
                    glob.DATA_INTERFACE.message = Message.STOP
                # moving Forward
                elif (payload == b'forward'):
                    glob.DATA_INTERFACE.message = Message.FORWARD
                    glob.MODE = "PILOTE"
                # moving Backward
                elif (payload == b'backward'):
                    glob.DATA_INTERFACE.message = Message.BACKWARD
                    glob.MODE = "PILOTE"
                # moving Backward Right
                elif (payload == b'backwardright'):
                    glob.DATA_INTERFACE.message = Message.BACKWARD_RIGHT
                    glob.MODE = "PILOTE"
                # moving Backward Left
                elif (payload == b'backwardleft'):
                    glob.DATA_INTERFACE.message = Message.BACKWARD_LEFT
                    glob.MODE = "PILOTE"
                # moving Forward Forward Left
                elif (payload == b'forwardleft'):
                    glob.DATA_INTERFACE.message = Message.FORWARD_LEFT
                    glob.MODE = "PILOTE"
                # moving Forward Right
                elif (payload == b'forwardright'):
                    glob.DATA_INTERFACE.message = Message.FORWARD_RIGHT
                    glob.MODE = "PILOTE"
               
            elif (header == b'AUT'):  # autonomous mode button
                glob.DATA_INTERFACE.message = Message.FORWARD
       
                glob.MODE = "AUTONOMOUS"
            print("MODE_Interface_glob: ",glob.MODE)
            print("Message interface: "+str(glob.DATA_INTERFACE.message))
