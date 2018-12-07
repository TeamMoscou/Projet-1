#from threading import Thread
import threading
import data
from data import Data
from data import ID
from data import Message
'''
class ID(Enum):
    LIDAR = 1
    ULTRASONIC = 2
    INTERFACE = 3
    AUTRE = 4

class Message(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    STOP = 5
    AUTONOMOUS = 6
    DETECTED_AVANT = 7
    DETECTED_ARRIERE = 8
'''
class Prise_decision(threading.Thread):

def prise_decision():
    global Mode
    global DataLidar
    global DataUltrason
    global DataInterface
    global DataOut # les noms sont à voir
    if (Mode=="Pilote" or Mode=="Autonomous"):
        if (DataInterface.message.value == 5 or ((DataLidar.message.value == 7 or DataUltrason.message.value == 7) and DataInterface.message.value==1) or ((DataLidar.message.value == 8 or DataUltrason.message.value == 8 )and DataInterface.message.value == 2 )):
            DataOut.message=Message.STOP
            if (Mode=="Pilote"):
                Mode="Autonomous"
        else:
            DataOut.message=DataInterface.message

'''
#Partie test
DataLidar = Data(ID.LIDAR,Message.DETECTED_ARRIERE)
DataUltrason = Data(ID.ULTRASONIC,Message.DETECTED_AVANT)
DataInterface = Data(ID.INTERFACE,Message.FORWARD)
DataOut = Data(ID.AUTRE,Message.FORWARD )

Mode="Pilote"
prise_decision()
print(DataOut.message)
print(Mode)
'''

