from data import Data
from data import ID
from data import Message
import threading
import socket

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 6666  # Arbitrary non-privileged port

global DATA_INTERFACE  # global variable.
global DATA_ULTRASONIC
global DATA_LIDAR

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
            if (DATA_ULTRASONIC.message.value == 7 or DATA_LIDAR.message.value == 7):
                #message to interface
                message = "OIF:" + str('')+ ";"  #detection of obstacle in front of the car
                size = self.conn.send(message.encode())
            if (DATA_ULTRASONIC.message.value == 8 or DATA_LIDAR.message.value == 8):
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
                    DATA_INTERFACE = Data(ID.INTERFACE, Message.LEFT)
                    print(DATA_INTERFACE.message.value)
                elif (payload == b'right'):
                    DATA_INTERFACE = Data(ID.INTERFACE, Message.RIGHT)
                    print(DATA_INTERFACE.message.value)
            elif (header == b'MOV'):  # move
                if (payload == b'stop'):
                    DATA_INTERFACE = Data(ID.INTERFACE, Message.STOP)
                    print(DATA_INTERFACE.message.value)
                elif (payload == b'forward'):
                    DATA_INTERFACE = Data(ID.INTERFACE, Message.FORWARD)
                    print(DATA_INTERFACE.message.value)
                elif (payload == b'backward'):
                    DATA_INTERFACE = Data(ID.INTERFACE, Message.BACKWARD)
                    print(DATA_INTERFACE.message.value)
            elif (header == b'AUT'):  # autonomous mode
                DATA_INTERFACE = Data(ID.INTERFACE, Message.AUTONOMOUS)
                print(DATA_INTERFACE.message.value)

        conn.close()


'''
inter = Interface()
inter.run()
'''
















