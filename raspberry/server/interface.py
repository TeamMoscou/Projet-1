from data import Data
from data import ID
from data import Message
import threading
import socket

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 6666  # Arbitrary non-privileged port

global DATAINTERFACE  # global variable.


class Interface(threading.Thread):
    def __init__(self):
        Thread.__init__(self)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        self.conn, addr = s.accept()
        print('Connected by', addr)

    def run(self):

        while True:
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
inter = Interface()
inter.run()
'''
















