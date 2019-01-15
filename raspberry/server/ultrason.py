import threading
import time
import can
import os
import struct
from glob import *
from data import *


class Ultrason(threading.Thread):
    def __init__(self,bus):
        threading.Thread.__init__(self)
        self.bus = bus

    def run(self):
        flagUltrasonAvant = 0
        flagUltrasonArriere = 0
        flagUltrasonAvantGauche = 0
        flagUltrasonAvantDroit = 0
        flagUltrasonAvantCentre = 0
        flagUltrasonArriereDroit = 0
        flagUltrasonArriereGauche = 0
        flagUltrasonArriereCentre = 0
        
        #Number of consecutive values wanted before considering obstale is detection
        NbVal = 5 
        
        #Membres : 0 :  ForwardLeft, 1 : ForwardRight, 2 : ForwardCentre, 3 : BackwardLeft, 4 : BackwardRight, 5 : BackwardCentre 
        compteur=[0,0,0,0,0,0]
        #Check if the previous message has the same value or not : If 1: There was something in the previous round, 0 if nothing. 
        compteurON=[0,0,0,0,0,0] 
        
        while True:
            msg = self.bus.recv()# Wait until a message is received.
            
            if msg.arbitration_id == US1:
                
                #Ultrasonic ForwardLeft
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                if distance <= 20:
                    #We check if we saw the same thing before (obstacle here). If so, increment the counter. 
                    if compteurON[0] == 1 :
                        compteur[0] = compteur[0] + 1 
                    else : 
                        compteurON[0] = 1
                        compteur[0] = 1
                    #Once the number of consecutive values  exceeds NBVal an obstacle is considered
                    if compteur[0] >= NbVal :
                        flagUltrasonAvantGauche=1
                        
                else:
                    if compteurON[0] == 0 :
                        compteur[0] = compteur[0] + 1 
                    else : 
                        compteurON[0] = 0
                        compteur[0] = 1
                    #Once the number of consecutive values  exceeds NBVal an obstacle is considered
                    if compteur[0] >= NbVal :
                        flagUltrasonAvantGauche=0     
                    
                #Ultrasonic ForwardRight
                distance = int.from_bytes(msg.data[2:4],byteorder='big')
                if distance <= 20:
                    #We check if we saw the same thing before (obstacle here). If so, increment the counter. 
                    if compteurON[1] == 1 :
                        compteur[1] = compteur[1] + 1 
                    else : 
                        compteurON[1] = 1
                        compteur[1] = 1
                    #Once the number of consecutive values  exceeds NBVal an obstacle is considered
                    if compteur[1] >= NbVal :
                        flagUltrasonAvantDroit=1
                        print("Avant droit detected")
                else:
                    if compteurON[1] == 0 :
                        compteur[1] = compteur[1] + 1 
                    else : 
                        compteurON[1] = 0
                        compteur[1] = 1
                    #Once the number of consecutive values  exceeds NBVal an obstacle is considered
                    if compteur[1] >= NbVal :
                        flagUltrasonAvantDroit=0  
                        
                #Ultrasonic BackwardCentre 
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                if distance <= 50:
                    #We check if we saw the same thing before (obstacle here). If so, increment the counter. 
                    if compteurON[5] == 1 :
                        compteur[5] = compteur[5] + 1 
                    else : 
                        compteurON[5] = 1
                        compteur[5] = 1
                    #Once the number of consecutive values  exceeds NBVal an obstacle is considered
                    if compteur[5] >= NbVal :                
                        flagUltrasonArriereCentre=1
                        
                else:
                    if compteurON[5] == 0 :
                        compteur[5] = compteur[5] + 1 
                    else : 
                        compteurON[5] = 0
                        compteur[5] = 1
                    #Once the number of consecutive values  exceeds NBVal an obstacle is considered
                    if compteur[5] >= NbVal :
                        flagUltrasonArriereCentre=0   
                        Une fois arrive a un certain nombre de valeurs consecutives ou plus, on considere qu'un obstacle est present 
                        
            elif msg.arbitration_id == US2:
                
                #Ultrasonic BackwardLeft
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                if distance <= 20:
                    #We check if we saw the same thing before (obstacle here). If so, increment the counter. 
                    if compteurON[3] == 1 :
                        compteur[3] = compteur[3] + 1 
                    else : 
                        compteurON[3] = 1
                        compteur[3] = 1
                    #Once the number of consecutive values  exceeds NBVal an obstacle is considered
                    if compteur[3] >= NbVal :
                        flagUltrasonArriereGauche=1
                        print("Arriere gauche detected")
                else:
                    if compteurON[3] == 0 :
                        compteur[3] = compteur[3] + 1 
                    else : 
                        compteurON[3] = 0
                        compteur[3] = 1
                    #Once the number of consecutive values  exceeds NBVal an obstacle is considered
                    if compteur[3] >= NbVal :
                        flagUltrasonArriereGauche=0 
                        
                #Ultrasonic BackwardRight
                distance = int.from_bytes(msg.data[2:4], byteorder='big')
                if distance <= 20:
                    #We check if we saw the same thing before (obstacle here). If so, increment the counter. 
                    if compteurON[4] == 1 :
                        compteur[4] = compteur[4] + 1 
                    else : 
                        compteurON[4] = 1
                        compteur[4] = 1
                    #Once the number of consecutive values  exceeds NBVal an obstacle is considered
                    if compteur[4] >= NbVal :
                        flagUltrasonArriereDroit=1
                        print("Arriere droit detected")
                else:
                    if compteurON[4] == 0 :
                        compteur[4] = compteur[4] + 1 
                    else : 
                        compteurON[4] = 0
                        compteur[4] = 1
                    #Once the number of consecutive values  exceeds NBVal an obstacle is considered
                    if compteur[4] >= NbVal :
                        flagUltrasonArriereDroit=0   
                        
                #Ultrasonic ForwardCentre
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                if distance <= 50:
                    #We check if we saw the same thing before (obstacle here). If so, increment the counter. 
                    if compteurON[2] == 1 :
                        compteur[2] = compteur[2] + 1 
                    else : 
                        compteurON[2] = 1
                        compteur[2] = 1
                    #Once the number of consecutive values  exceeds NBVal an obstacle is considered
                    if compteur[2] >= NbVal :
                        flagUltrasonAvantCentre=1
                        
                else:
                    if compteurON[2] == 0 :
                        compteur[2] = compteur[2] + 1 
                    else : 
                        compteurON[2] = 0
                        compteur[2] = 1
                    #Once the number of consecutive values  exceeds NBVal an obstacle is considered
                    if compteur[2] >= NbVal :
                        flagUltrasonAvantCentre=0     
                        
                        
            #if one of the Forward Ultrasonic detect, we consider that there is an at the front 
            if flagUltrasonAvantDroit==1 or flagUltrasonAvantGauche==1 or flagUltrasonAvantCentre ==1:
                flagUltrasonAvant = 1
            #else no one of the Forward Ultrasonic detect, we consider that there is no obstacle at the front                 
            else:
                flagUltrasonAvant = 0
                
            #if one of the Backward Ultrasonic detect, we consider that there is an at the front 
            if flagUltrasonArriereDroit==1 or flagUltrasonArriereGauche==1 or flagUltrasonArriereCentre ==1:
                flagUltrasonArriere = 1
            #else no one of the Backward Ultrasonic detect, we consider that there is no obstacle at the front                 
            else:
                flagUltrasonArriere = 0
                
            #set the Ultrasonic Massage to the approproate Value 
            if flagUltrasonAvant==1 and flagUltrasonArriere==1:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_BOTH)
            elif flagUltrasonAvant==1:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_FRONT)   
            elif flagUltrasonArriere==1:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_BACK)
            elif flagUltrasonArriere==0 and flagUltrasonAvant==0:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_NULL)
            #print("Message ultrason: "+ str(glob.DATA_ULTRASONIC.message))
