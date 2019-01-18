import threading
import time
from data import *
import glob

class Prise_decision(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        #Init des variables locales


    def run(self):
        #To be sure that each module has started
        time.sleep(2)
        Stop_requested = 0
        Detection_front = 0
        Detection_back = 0 
        Forward = 0
        Backward = 0
        
        while True:
            #We consider checking variables 10 times per second is enough
            time.sleep(0.1)

            #Reading global variables and change the state of them
            if (glob.DATA_INTERFACE.message == Message.STOP):
                Stop_requested = 1
            else:
                Stop_requested = 0    

            #Ultrasonic or Lidar detect something in front of the car
            if (glob.DATA_ULTRASONIC.message == Message.DETECTED_FRONT or glob.DATA_LIDAR.message == Message.DETECTED_FRONT or glob.DATA_LIDAR.message == Message.DETECTED_BOTH or glob.DATA_ULTRASONIC.message == Message.DETECTED_BOTH):
                Detection_front = 1
            else:
                Detection_front = 0

            #Ultrasonic or Lidar detect something at the back of the car
            if (glob.DATA_ULTRASONIC.message == Message.DETECTED_BACK or glob.DATA_LIDAR.message == Message.DETECTED_BACK or glob.DATA_LIDAR.message == Message.DETECTED_BOTH or glob.DATA_ULTRASONIC.message == Message.DETECTED_BOTH):
                Detection_back = 1
            else: 
                Detection_back = 0    

            #Command forward sent by the interface or the autonomous mode
            if (glob.DATA_INTERFACE.message == Message.FORWARD or glob.DATA_INTERFACE.message == Message.FORWARD_RIGHT or glob.DATA_INTERFACE.message == Message.FORWARD_LEFT or glob.MODE == "AUTONOMOUS"):
                Forward = 1
            else:
                Forward = 0    

            #Command backward sent by the interface
            if (glob.DATA_INTERFACE.message == Message.BACKWARD or glob.DATA_INTERFACE.message == Message.BACKWARD_RIGHT or glob.DATA_INTERFACE.message == Message.BACKWARD_LEFT):
                Backward = 1
            else:
                Backward = 0    
            
            print(" Detection_front ", Detection_front, " Forward ",Forward, " Detection_back ",Detection_back," Backward ",Backward)
            #Generating decision message
            #If stop is requested by the interface we just stop
            if (glob.MODE == "AUTONOMOUS"):
                glob.DATA_DECISION.message = glob.DATA_LIDAR_AUTONOMOUS.message
            
            elif (Stop_requested):
                glob.DATA_DECISION.message = Message.STOP

            #If we want to go forward but there is something we stop
            elif (Detection_front and Forward ):
                glob.DATA_DECISION.message = Message.STOP

            #If we want to go backward but there is something we stop
            elif (Detection_back and Backward):
                glob.DATA_DECISION.message = Message.STOP

            #If we are in an other situation we send the message of the interface or the autonomous depending on the mode
            else:
                
                glob.DATA_DECISION.message = glob.DATA_INTERFACE.message
            print("MODE: ",glob.MODE)   

            print("Message PriseD: "+str(glob.DATA_DECISION.message))
