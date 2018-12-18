from data import *
import threading
import socket
import glob
from glob import *
HOST = ''  # Symbolic name meaning all available interfaces
PORT = 6666  # Arbitrary non-privileged port



class Interface(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        self.conn, addr = s.accept()
        print('Connected by', addr)

    def run(self):

        while True:
            if (glob.DATA_ULTRASONIC.message == Message.DETECTED_FRONT or glob.DATA_LIDAR.message == Message.DETECTED_FRONT):
                #message to interface
                message = "OIF:" + str('1')+ ";"  #detection of obstacle in front of the car
                size = self.conn.send(message.encode())
            elif (glob.DATA_ULTRASONIC.message == Message.DETECTED_BACK or glob.DATA_LIDAR.message == Message.DETECTED_BACK):
                #message to interface
                message = "OIB:" + str('1')+ ";"  #detection of obstacle in back of the car
                size = self.conn.send(message.encode())
            elif (glob.DATA_LIDAR.message == Message.DETECTED_BOTH or glob.DATA_ULTRASONIC.message == Message.DETECTED_BOTH):
                #message to interface
                message = "OBB:" + str('1')+ ";"  #detection of obstacle in front and back of the car
                size = self.conn.send(message.encode())
            else :
                message = "NOD:" + str('1')+ ";"  #no obstacle detected
                size = self.conn.send(message.encode())

            data = self.conn.recv(1024) #receve data from socket

            if not data: break

            header = data[0:3]
            payload = data[3:]
            print("header :", header, "payload:", str(payload))

            if (header == b'STE'):  # steer
                if (payload == b'left'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.LEFT)
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'right'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.RIGHT)
                    #print(glob.DATA_INTERFACE.message.value)
            elif (header == b'MOV'):  # move
                if (payload == b'stop'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.STOP)
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'forward'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.FORWARD)
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'backward'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.BACKWARD)
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'backwardright'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.BACKWARD_RIGHT)
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'backwardleft'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.BACKWARD_LEFT)
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'forwardleft'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.FORWARD_LEFT)
                    #print(glob.DATA_INTERFACE.message.value)
                elif (payload == b'forwardright'):
                    glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.FORWARD_RIGHT)
                    #print(glob.DATA_INTERFACE.message.value)
            elif (header == b'AUT'):  # autonomous mode
                glob.DATA_INTERFACE = Data(ID.INTERFACE, Message.BACKWARD)
                #print(glob.DATA_INTERFACE.message.value)
            print("Message interface: "+str(glob.DATA_INTERFACE.message)) 
        conn.close()


'''
glob.DATA_ULTRASONIC = Data(ID.ULTRASONIC, Message.DETECTED_NULL)
inter = Interface()
inter.run()

'''















