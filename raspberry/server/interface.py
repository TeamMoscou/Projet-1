from data import *
import threading
import socket
import glob
import time
from glob import *
HOST = ''  # Symbolic name meaning all available interfaces
PORT = 6666  # Arbitrary non-privileged port
        
class ReturnInterface(threading.Thread):
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.conn = conn
    def run(self):
        while True: 
            time.sleep(0.1)
            if (glob.DATA_ULTRASONIC.message == Message.DETECTED_FRONT or glob.DATA_LIDAR.message == Message.DETECTED_FRONT):
                #message to interface
                message = "OIF:" + str('')+ ";"  #detection of obstacle in front of the car
                size = self.conn.send(message.encode())
            elif (glob.DATA_ULTRASONIC.message == Message.DETECTED_BACK or glob.DATA_LIDAR.message == Message.DETECTED_BACK):
                #message to interface
                message = "OIB:" + str('')+ ";"  #detection of obstacle in back of the car
                size = self.conn.send(message.encode())
            elif (glob.DATA_LIDAR.message == Message.DETECTED_BOTH or glob.DATA_ULTRASONIC.message == Message.DETECTED_BOTH):
                #message to interface
                message = "OBB:" + str('')+ ";"  #detection of obstacle in front and back of the car
                size = self.conn.send(message.encode())
            elif (glob.MODE == "AUTONOMOUS"): 
                message = "AUT:" + str('')+ ";"  #autonomouse mode
            else :
                message = "NOD:" + str('')+ ";"  #no obstacle detected
                size = self.conn.send(message.encode())

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

            if (header == b'STE'):  # steer
                if (payload == b'left'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.LEFT)
                    glob.MODE = "PILOTE"
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'right'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.RIGHT)
                    glob.MODE = "PILOTE"
                    #print(glob.DATA_INTERFACE.message.value)
            elif (header == b'MOV'):  # move
                if (payload == b'stop'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.STOP)
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'forward'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.FORWARD)
                    glob.MODE = "PILOTE"
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'backward'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.BACKWARD)
                    glob.MODE = "PILOTE"
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'backwardright'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.BACKWARD_RIGHT)
                    glob.MODE = "PILOTE"
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'backwardleft'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.BACKWARD_LEFT)
                    glob.MODE = "PILOTE"
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'forwardleft'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.FORWARD_LEFT)
                    glob.MODE = "PILOTE"
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'forwardright'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.FORWARD_RIGHT)
                    glob.MODE = "PILOTE"
                    #print(glob.DATA_INTERFACE.message.value)
            elif (header == b'AUT'):  # autonomous mode
                glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.FORWARD)
                glob.MODE = "AUTONOMOUS"
                #print(glob.DATA_INTERFACE.message.value)
            print("Message interface: "+str(glob.DATA_INTERFACE.message)) 


'''
glob.DATA_ULTRASONIC = Data(ID.ULTRASONIC, Message.DETECTED_NULL)
inter = Interface()
inter.run()

'''















