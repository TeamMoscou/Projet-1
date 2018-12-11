import threading
import glob
from glob import * 
import data
from data import *

'''
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
'''


class Prise_decision(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        
        Detection_front = 0
        Detection_back = 0
        Stop_requested = 0
        Forward = 0
        Backward = 0

        # Recuperation donnees
        if (glob.DATA_INTERFACE.message == Message.STOP):
            Stop_requested = 1

        if (glob.DATA_ULTRASONIC.message == Message.DETECTED_FRONT or glob.DATA_LIDAR.message == Message.DETECTED_FRONT or glob.DATA_LIDAR.message == Message.DETECTED_BOTH or glob.DATA_ULTRASONIC.message == Message.DETECTED_BOTH):
            Detection_front = 1

        if (glob.DATA_ULTRASONIC.message == Message.DETECTED_BACK or glob.DATA_LIDAR.message == Message.DETECTED_BACK or glob.DATA_LIDAR.message == Message.DETECTED_BOTH or glob.DATA_ULTRASONIC.message == Message.DETECTED_BOTH):
            Detection_back = 1

        if (glob.DATA_INTERFACE.message == Message.FORWARD or glob.DATA_INTERFACE.message == Message.FORWARD_RIGHT or glob.DATA_INTERFACE.message == Message.FORWARD_LEFT):
            Forward = 1

        if (glob.DATA_INTERFACE.message == Message.BACKWARD or glob.DATA_INTERFACE.message == Message.BACKWARD_RIGHT or glob.DATA_INTERFACE.message == Message.BACKWARD_LEFT):
            Backward = 1

        # Utilisation donnes

        # Si stop demande, on stop

        if (Stop_requested):

            glob.DATA_DECISION.message = Message.STOP

        # Si detection_avant et on avance, on stop
        elif (Detection_front and Forward):

            glob.DATA_DECISION.message = Message.STOP

            # Si mode pilote, on indique qu'on passe en autonome
            if (MODE == "PILOTE"):
                MODE = "AUTONOMOUS"

        # Si detection_arriere et on recule, on stop
        elif (Detection_back and Backward):

            glob.DATA_DECISION.message = message.STOP

            # Si mode pilote, on indique qu'on passe en autonome
            if (MODE == "PILOTE"):
                MODE = "AUTONOMOUS"

        # Si aucun des cas precedents, on transmets juste le message de l'interface
        else:
            glob.DATA_DECISION.message = glob.DATA_INTERFACE.message
        # print("detection avant:", Detection_front)
        # print("detection arr:" , Detection_back)
        # print("demande stop:" , Stop_requested)
        # print("backward:" , Backward)
        # print("forward:" , Forward)


'''
#Partie test
DataLidar = Data(ID.LIDAR,Message.DETECTED_FRONT)
DataUltrason = Data(ID.ULTRASONIC,Message.DETECTED_FRONT)
DataInterface = Data(ID.INTERFACE,Message.FORWARD)
DataOut = Data(ID.DECISION,Message.FORWARD )

Mode="PILOTE"
prise_decision()
print(DataOut.message)
print(Mode)

'''


