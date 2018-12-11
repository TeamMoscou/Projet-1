from data import Data
from data import ID
from data import Message
import threading
import socket

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 6666  # Arbitrary non-privileged port

global DATAINTERFACE  # global variable.
global DATALIDAR
global DATAULTRASONIC

class Interface(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        self.conn, addr = s.accept()
        print('Connected by', addr)

    def stop(self):
        self._stop.set()

    def run(self):

        while True:
            if (DATAULTRASONIC.message.value == 7 or DATALIDAR.message.value == 7):
                #message to interface
                message = "OIF:" + str('')+ ";"  #detection of obstacle in front of the car
                size = self.conn.send(message.encode())

            if (DATAULTRASONIC.message.value == 8 or DATALIDAR.message.value == 8):
                #message to interface
                message = "OIB:" + str('')+ ";"  #detection of obstacle in back of the car
                size = self.conn.send(message.encode())
            
            
            data = self.conn.recv(1024)
            if not data: break

            header = data[0:3]
            payload = data[3:]
            print("header :", header, "payload:", str(payload))

            if (header == b'STE'):  # steer
                if (payload == b'left'):
                    DATAINTERFACE = Data(ID.INTERFACE, Message.LEFT)
                    print(DATAINTERFACE.message.value)
                elif (payload == b'right'):
                    DATAINTERFACE = Data(ID.INTERFACE, Message.RIGHT)
                    print(DATAINTERFACE.message.value)
            elif (header == b'MOV'):  # move
                if (payload == b'stop'):
                    DATAINTERFACE = Data(ID.INTERFACE, Message.STOP)
                    print(DATAINTERFACE.message.value)
                elif (payload == b'forward'):
                    DATAINTERFACE = Data(ID.INTERFACE, Message.FORWARD)
                    print(DATAINTERFACE.message.value)
                elif (payload == b'backward'):
                    DATAINTERFACE = Data(ID.INTERFACE, Message.BACKWARD)
                    print(DATAINTERFACE.message.value)
            elif (header == b'AUT'):  # autonomous mode
                DATAINTERFACE = Data(ID.INTERFACE, Message.AUTONOMOUS)
                print(DATAINTERFACE.message.value)

            
        conn.close()


'''
#Partie test
DATALIDAR = Data(ID.LIDAR,Message.DETECTED_BACK)
DATAULTRASONIC = Data(ID.ULTRASONIC,Message.DETECTED_BACK)
inter = Interface()
inter.run()
'''
















