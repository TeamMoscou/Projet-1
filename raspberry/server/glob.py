# coding: utf-8
import threading
import socket
#from rplidar import RPLidar
from data import *




#gain proportionnel du regulateur de position des roues.
Kp=-0.2
#à rajouter dans le fichier glob
MS=0x100


#---------------------Lidar Variables----------------------#
#lidar = RPLidar('/dev/ttyUSB0')
#SAFE_DISTANCE = 2000
#ANGLE_MAX_FRONT = 200
#ANGLE_MIN_FRONT = 160
#ANGLE_MAX_BACK = 340
#ANGLE_MIN_BACK = 20
# flags set to 1 when the obstacle is detected
#Flag_FRONT = 0
#Flag_BACK = 0

#wait_lidar=threading.Event()
#wait_lidar.set()
#shutdown_lidar=threading.Event()
#shutdown_lidar.clear()


DATA_LIDAR = Data(ID.LIDAR,Message.STOP)
DATA_LIDAR_AUTONOMOUS = Data(ID.LIDAR, Message.STOP)

#--------------------------------------------------------------------------





#---------------------Ultrasonic Variables----------------------#

US1 = 0x000
US2 = 0x001

flagUltrasonAvant=0
flagUltrasonArriere=0

#wait_ultrason=threading.Event()
#wait_ultrason.clear()
#shutdown_ultrason=threading.Event()
#shutdown_ultrason.clear()

#global DATA_ULTRASONIC
DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.STOP)
#----------------------------------------------------------------------


#-------------------Interface Variables----------------------#
#wait_interface=threading.Event()
#wait_interface.clear()
#shutdown_interface=threading.Event()
#shutdown_interface.clear()

HOST = ''  ;# Symbolic name meaning all available interfaces
PORT = 6666  ;# Arbitrary non-privileged 



DATA_INTERFACE=Data(ID.INTERFACE,Message.FORWARD)
#---------------------------------------------------------------------------




#---------------------Decision Variables----------------------#

#wait_decision=threading.Event()
#wait_decision.clear()

#shutdown_decision=threading.Event()
#shutdown_decision.clear()

#global DATA_DECISION
DATA_DECISION=Data(ID.DECISION,Message.STOP)
#--------------------------------------------------------------#




#-------------- Can_send variables-----------------------#

#wait_can=threading.Event()
#wait_can.clear()
#shutdown_can=threading.Event()
#shutdown_can.clear()
#---------------------------------------------------------#

MODE="PILOTE"


