import threading
import time
import can
import os
import struct
import glob
from glob import *
from data import *

"""US1 = 0x000
US2 = 0x001
flagUltrasonAvant=0
flagUltrasonArriere=0"""

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
        #Nombre de valeur consecutives voulues avant de considerer OK
        NbVal = 5 
        #Membre : 0 :  AvantGauche, 1 : AvantDroite, 2 : Avant centre, 3 : Arriere Gauche, 4 : Arriere Droit, 5 : Arriere Centre 
        compteur=[0,0,0,0,0,0]
        #Verifie si au message precedent c'etait la meme valeur ou pas : Si 1 : Il y avait qq chose au tour precedent, si 0 rien. 
        compteurON=[0,0,0,0,0,0] 
        while True:
            
            msg = self.bus.recv()# Wait until a message is received.
            if msg.arbitration_id == US1:
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                #print("Avant gauche = " + str(distance))
                if distance <= 20:
                    #On verifie si on voyait la meme chose avant (obstacle ici). Si c'est le cas on incremente le compteur. 
                    if compteurON[0] == 1 :
                        compteur[0] = compteur[0] + 1 
                    else : 
                        compteurON[0] = 1
                        compteur[0] = 1
                    #Une fois arrive a un certain nombre de valeurs consecutives ou plus, on considere qu'un obstacle est present 
                    if compteur[0] >= NbVal :
                        flagUltrasonAvantGauche=1
                        print ("Avant gauche detected")   
                else:
                    if compteurON[0] == 0 :
                        compteur[0] = compteur[0] + 1 
                    else : 
                        compteurON[0] = 0
                        compteur[0] = 1
                    #Une fois arrive a un certain nombre de valeurs consecutives ou plus, on considere qu'un obstacle est present 
                    if compteur[0] >= NbVal :
                        flagUltrasonAvantGauche=0     
                    
                distance = int.from_bytes(msg.data[2:4],byteorder='big')
                #print("Avant droit = " + str(distance))
                if distance <= 20:
                    if compteurON[1] == 1 :
                        compteur[1] = compteur[1] + 1 
                    else : 
                        compteurON[1] = 1
                        compteur[1] = 1
                    #Une fois arrive a un certain nombre de valeurs consecutives ou plus, on considere qu'un obstacle est present 
                    if compteur[1] >= NbVal :
                        flagUltrasonAvantDroit=1
                        print("Avant droit detected")
                else:
                    if compteurON[1] == 0 :
                        compteur[1] = compteur[1] + 1 
                    else : 
                        compteurON[1] = 0
                        compteur[1] = 1
                    #Une fois arrive a un certain nombre de valeurs consecutives ou plus, on considere qu'un obstacle est present 
                    if compteur[1] >= NbVal :
                     flagUltrasonAvantDroit=0     
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                #print("Arriere centre = " + str(distance))
                if distance <= 50:
                    if compteurON[5] == 1 :
                        compteur[5] = compteur[5] + 1 
                    else : 
                        compteurON[5] = 1
                        compteur[5] = 1
                    #Une fois arrive a un certain nombre de valeurs consecutives ou plus, on considere qu'un obstacle est present 
                    if compteur[5] >= NbVal :                
                        flagUltrasonArriereCentre=1
                        print("Arriere centre detected")
                else:
                    if compteurON[5] == 0 :
                        compteur[5] = compteur[5] + 1 
                    else : 
                        compteurON[5] = 0
                        compteur[5] = 1
                    #Une fois arrive a un certain nombre de valeurs consecutives ou plus, on considere qu'un obstacle est present 
                    if compteur[5] >= NbVal :
                        flagUltrasonArriereCentre=0     
            elif msg.arbitration_id == US2:
                # ultrason arriere gauche
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                #print("Arriere gauche = " + str(distance))
                if distance <= 20:
                    if compteurON[3] == 1 :
                        compteur[3] = compteur[3] + 1 
                    else : 
                        compteurON[3] = 1
                        compteur[3] = 1
                    #Une fois arrive a un certain nombre de valeurs consecutives ou plus, on considere qu'un obstacle est present 
                    if compteur[3] >= NbVal :
                        flagUltrasonArriereGauche=1
                        print("Arriere gauche detected")
                else:
                    if compteurON[3] == 0 :
                        compteur[3] = compteur[3] + 1 
                    else : 
                        compteurON[3] = 0
                        compteur[3] = 1
                    #Une fois arrive a un certain nombre de valeurs consecutives ou plus, on considere qu'un obstacle est present 
                    if compteur[3] >= NbVal :
                        flagUltrasonArriereGauche=0     
                # ultrason arriere droit
                distance = int.from_bytes(msg.data[2:4], byteorder='big')
                #print("Arriere droit = " + str(distance))
                if distance <= 20:
                    if compteurON[4] == 1 :
                        compteur[4] = compteur[4] + 1 
                    else : 
                        compteurON[4] = 1
                        compteur[4] = 1
                    #Une fois arrive a un certain nombre de valeurs consecutives ou plus, on considere qu'un obstacle est present 
                    if compteur[4] >= NbVal :
                        flagUltrasonArriereDroit=1
                        print("Arriere droit detected")
                else:
                    if compteurON[4] == 0 :
                        compteur[4] = compteur[4] + 1 
                    else : 
                        compteurON[4] = 0
                        compteur[4] = 1
                    #Une fois arrive a un certain nombre de valeurs consecutives ou plus, on considere qu'un obstacle est present 
                    if compteur[4] >= NbVal :
                        flagUltrasonArriereDroit=0     
                # ultrason avant centre
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                #print("Avant centre = " + str(distance))
                if distance <= 50:
                    if compteurON[2] == 1 :
                        compteur[2] = compteur[2] + 1 
                    else : 
                        compteurON[2] = 1
                        compteur[2] = 1
                    #Une fois arrive a un certain nombre de valeurs consecutives ou plus, on considere qu'un obstacle est present 
                    if compteur[2] >= NbVal :
                        flagUltrasonAvantCentre=1
                        print("Avant centre detected") 
                else:
                    if compteurON[2] == 0 :
                        compteur[2] = compteur[2] + 1 
                    else : 
                        compteurON[2] = 0
                        compteur[2] = 1
                    #Une fois arrive a un certain nombre de valeurs consecutives ou plus, on considere qu'un obstacle est present 
                    if compteur[2] >= NbVal :
                        flagUltrasonAvantCentre=0     

            if flagUltrasonAvantDroit==1 or flagUltrasonAvantGauche==1 or flagUltrasonAvantCentre ==1:
                flagUltrasonAvant = 1
            else:
                flagUltrasonAvant = 0
            if flagUltrasonArriereDroit==1 or flagUltrasonArriereGauche==1 or flagUltrasonArriereCentre ==1:
                flagUltrasonArriere = 1
            else:
                flagUltrasonArriere = 0
            if flagUltrasonAvant==1 and flagUltrasonArriere==1:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_BOTH)
            elif flagUltrasonAvant==1:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_FRONT)   
            elif flagUltrasonArriere==1:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_BACK)
            elif flagUltrasonArriere==0 and flagUltrasonAvant==0:
                glob.DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.DETECTED_NULL)
            print("Message ultrason: "+ str(glob.DATA_ULTRASONIC.message))
