from threading import Thread
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


class Prise_decision(Thread):

    def prise_decision():
        global MODE
        global DATA_LIDAR
        global DATA_ULTRASONIC
        global DATA_INTERFACE
        global DATA_OUT  # les noms sont à voir
        Detection_front = 0
        Detection_back = 0
        Stop_requested = 0
        Forward = 0
        Backward = 0

        # Recuperation donnees
        if (DATA_INTERFACE.message == Message.STOP):
            Stop_requested = 1

        if (DATA_ULTRASONIC.message == Message.DETECTED_FRONT or DATA_LIDAR.message == Message.DETECTED_FRONT or DATA_LIDAR.message == Message.DETECTED_BOTH or DATA_ULTRASONIC.message == Message.DETECTED_BOTH):
            Detection_front = 1

        if (DATA_ULTRASONIC.message == Message.DETECTED_BACK or DATA_LIDAR.message == Message.DETECTED_BACK or DATA_LIDAR.message == Message.DETECTED_BOTH or DATA_ULTRASONIC.message == Message.DETECTED_BOTH):
            Detection_back = 1

        if (
                DATA_INTERFACE.message == Message.FORWARD or DATA_INTERFACE.message == Message.FORWARD_RIGHT or DATA_INTERFACE.message == Message.FORWARD_LEFT):
            Forward = 1

        if (
                DATA_INTERFACE.message == Message.BACKWARD or DATA_INTERFACE.message == Message.BACKWARD_RIGHT or DATA_INTERFACE.message == Message.BACKWARD_LEFT):
            Backward = 1

        # Utilisation donnes

        # Si stop demande, on stop

        if (Stop_requested):

            DATA_OUT.message = Message.STOP

        # Si detection_avant et on avance, on stop
        elif (Detection_front and Forward):

            DATA_OUT.message = Message.STOP

            # Si mode pilote, on indique qu'on passe en autonome
            if (MODE == "PILOTE"):
                MODE = "AUTONOMOUS"

        # Si detection_arriere et on recule, on stop
        elif (Detection_back and Backward):

            DATA_OUT.message = message.STOP

            # Si mode pilote, on indique qu'on passe en autonome
            if (MODE == "PILOTE"):
                MODE = "AUTONOMOUS"

        # Si aucun des cas precedents, on transmets juste le message de l'interface
        else:
            DATA_OUT.message = DATAINTERFACE.message
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


