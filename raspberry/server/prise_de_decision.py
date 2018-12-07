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
    DETECTED_BACk = 8
    FORWARD_LEFT = 9
    FORWARD_RIGHT = 10
    BACKWARD_LEFT = 11
    BACKWARD_RIGHT = 12
'''
class Prise_decision(Thread):

    def prise_decision():
        global Mode
        global DataLidar
        global DataUltrason
        global DataInterface
        global DataOut # les noms sont à voir
        Detection_front = 0
        Detection_back = 0
        Stop_requested = 0
        Forward = 0
        Backward = 0

        #Recuperation donnees
        if (DataInterface.message.value == 5):

            Stop_requested = 1

        if (DataUltrason.message.value == 7 or DataLidar.message.value == 7):

            Detection_avant = 1

        if (DataUltrason.message.value == 8 or DataLidar.message.value == 8):

            Detection_arriere = 1

        if (DataInterface.message.value == 1 or DataInterface.message.value == 9 or DataInterface.message.value == 10):
            
            Forward = 1
        
        if (DataInterface.message.value == 2 or DataInterface.message.value == 11 or DataInterface.message.value == 12):

            Backward = 1

    
        #Utilisation donnes
        
        #Si stop demande, on stop

        if (Stop_requested):
            
            DataOut.message=Message.STOP
            
        #Si detection_avant et on avance, on stop
        elif (Detection_avant and Forward):
            
            DataOut.message=Message.STOP
            
            #Si mode pilote, on indique qu'on passe en autonome
            if (Mode=="PILOTE"):
                
                Mode="AUTONOMOUS"
                
        #Si detection_arriere et on recule, on stop
        elif (Detection_avant and Backward):
            
            DataOut.message=message.STOP
            
            #Si mode pilote, on indique qu'on passe en autonome
            if (Mode=="PILOTE"):
                
                Mode="AUTONOMOUS"
                
        #Si aucun des cas precedents, on transmets juste le message de l'interface
        else:
            DataOut.message=DataInterface.message
#    print("detection avant:", Detection_avant)
#    print("detection arr:" , Detection_arriere)
#    print("demande stop:" , Stop_requested)
#    print("backward:" , Backward)
#    print("forward:" , Forward)
        

'''
#Partie test
DataLidar = Data(ID.LIDAR,Message.DETECTED_BACK)
DataUltrason = Data(ID.ULTRASONIC,Message.DETECTED_FRONT)
DataInterface = Data(ID.INTERFACE,Message.FORWARD)
DataOut = Data(ID.DECISION,Message.FORWARD )

Mode="PILOTE"
prise_decision()
print(DataOut.message)
print(Mode)



'''
