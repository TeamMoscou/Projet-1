# coding: utf-8
from data import *

#File containing all global variables of the project, each variable is initialize at STOP

#---------------------Lidar Variables----------------------#

global DATA_LIDAR
DATA_LIDAR = Data(ID.LIDAR,Message.STOP)

global DATA_LIDAR_AUTONOMOUS
DATA_LIDAR_AUTONOMOUS = Data(ID.LIDAR, Message.STOP)


#---------------------Ultrasonic Variables----------------------#

global US1
US1 = 0x000
global US2
US2 = 0x001

global DATA_ULTRASONIC
DATA_ULTRASONIC=Data(ID.ULTRASONIC,Message.STOP)


#-------------------Interface Variables----------------------#

# Symbolic name meaning all available interfaces
global HOST
HOST = ''
# Arbitrary non-privileged
global PORT
PORT = 6666

global DATA_INTERFACE
DATA_INTERFACE=Data(ID.INTERFACE,Message.STOP)


#---------------------Decision Variables----------------------#

global DATA_DECISION
DATA_DECISION=Data(ID.DECISION,Message.STOP)
global MODE
MODE = "PILOTE"

#---------------------Wheels Variables----------------------#
#Proportional-Only Controller Gain for controlling steering wheels
global Kp
Kp=-0.2
#CAN ID for MotorSensor Frame
global MS
MS=0x100
