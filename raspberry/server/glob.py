# coding: utf-8
from data import *

#File containing all global variables of the project, each variable is initialize at STOP

#---------------------Lidar Variables----------------------#

DATA_LIDAR = Data(ID.LIDAR,Message.STOP)
DATA_LIDAR_AUTONOMOUS = Data(ID.LIDAR, Message.STOP)


#---------------------Ultrasonic Variables----------------------#

US1 = 0x000
US2 = 0x001

DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.STOP)


#-------------------Interface Variables----------------------#

# Symbolic name meaning all available interfaces
HOST = ''
# Arbitrary non-privileged
PORT = 6666

DATA_INTERFACE=Data(ID.INTERFACE,Message.STOP)


#---------------------Decision Variables----------------------#

DATA_DECISION=Data(ID.DECISION,Message.STOP)
MODE="PILOTE"

#---------------------Wheels Variables----------------------#
#gain proportionnel du regulateur de position des roues.
Kp=-0.2
#à rajouter dans le fichier glob
MS=0x100
