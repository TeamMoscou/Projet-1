# coding: utf-8
from enum import Enum

class ID(Enum):
    LIDAR = 1
    ULTRASONIC = 2
    INTERFACE = 3
    DECISION = 4

class Message(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    STOP = 5
    AUTONOMOUS = 6
    DETECTED_FRONT = 7
    DETECTED_BACK = 8
    FORWARD_LEFT = 9
    FORWARD_RIGHT = 10
    BACKWARD_LEFT = 11
    BACKWARD_RIGHT = 12
 

    def list():
        return list(map(lambda c: c.value, Message))

class Data: 
    def __init__(self, iDEnvoyeur, message):
        if iDEnvoyeur not in (ID.LIDAR, ID.ULTRASONIC, ID.INTERFACE, ID.DECISION):
            raise ValueError('ID not valid')
        self.iDEnvoyeur = iDEnvoyeur
        if message not in (Message.FORWARD,Message.BACKWARD,Message.LEFT,Message.RIGHT,Message.STOP,Message.AUTONOMOUS,Message.DETECTED_FRONT,Message.DETECTED_BACK,Message.FORWARD_RIGHT,Message.FORWARD_LEFT,Message.BACKWARD_LEFT,Message.BACKWARD_RIGHT ):
            raise ValueError('Message not valid')
        self.message = message
    

'''   
Data = Data(ID.INTERFACE,Message.FORWARD)
print (Data.iDEnvoyeur.value)
print (Data.message.value)

print(ID.LIDAR.value)
print(Message.FORWARD.value)
'''
