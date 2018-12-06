from data import Data
from data import ID
from data import Message

import socket

global DATAINTERFACE #global variable. 

class Interface():
    def __init__(self,conn):
        self.conn = conn
        
    def run(self):

        while True :
            data = self.conn.recv(1024)

            if not data : break
                
            header = data[0:3]
            payload = data[3:]
            print("header :", header, "payload:", str(payload))
            
            if (header == b'STE'): # steer
                if (payload == b'left'):
                    DATAINTERFACE = Data(ID.INTERFACE,Message.LEFT)
                elif (payload == b'right'):
                    DATAINTERFACE = Data(ID.INTERFACE,Message.RIGHT)
            elif (header == b'MOV'):  # move
                if (payload == b'stop'):
                    DATAINTERFACE = Data(ID.INTERFACE,Message.STOP)
                elif (payload == b'forward'):
                    DATAINTERFACE = Data(ID.INTERFACE,Message.FORWARD)
                elif (payload == b'backward'):
                    DATAINTERFACE = Data(ID.INTERFACE,Message.BACKWARD)
            
        conn.close()   
        
'''
message = "STE" + "left"
data_bytes = message.encode("ascii")

inter = Interface(data_bytes)
inter.run()
'''



        
        



    
            
            
            
            
            
            
            
            