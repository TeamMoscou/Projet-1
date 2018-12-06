# coding: utf-8
from enum import Enum

class ID(Enum):
    LIDAR = 1
    ULTRASONIC = 2
    INTERFACE = 3

class Message(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    STOP = 5
    AUTONOMOUS = 6

class Data: 
    def __init__(self, iDEnvoyeur, message):
        if iDEnvoyeur not in (ID.LIDAR, ID.ULTRASONIC, ID.INTERFACE):
            raise ValueError('ID not valid')
        self.iDEnvoyeur = iDEnvoyeur
        if message not in (Message.FORWARD, Message.BACKWARD, Message.LEFT, Message.RIGHT, Message.STOP, Message.AUTONOMOUS):
            raise ValueError('Message not valid')
        self.message = message
    
    
'''
Data = Data(ID.INTERFACE,Message.FORWARD)
print (Data.iDEnvoyeur.value)
print (Data.message.value)

print(ID.LIDAR.value)
print(Message.FORWARD.value)'''