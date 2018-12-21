import threading
import os
from rplidar import RPLidar
import time
import glob
import numpy as np
from glob import *
from data import Data
from data import ID
from data import Message
#from global_variables import *
# the definition of the class thread of the lidar

#lidar = RPLidar('/dev/ttyUSB0')
class LidarDetection(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.lidar = RPLidar('/dev/ttyUSB0')

    def run(self):

        SAFE_DISTANCE = 2000
        
        ANGLE_FRONT_LEFT = 160
        #Zone FRONT LEFT (160 - 170)
        ANGLE_FRONT_MIDDLE_LEFT = 170
        #Zone FRONT MIDDLE LEFT (170 - 180)
        ANGLE_FRONT_MIDDLE = 180
        #Zone FRONT MIDDLE RIGHT (180 - 190)
        ANGLE_FRONT_MIDDLE_RIGHT = 190
        #Zone FRONT RIGHT (190 - 200)
        ANGLE_FRONT_RIGHT = 200
        #Zone FRONT LEFT (160 - 170)
        #ANGLE_RIGHT_FRONT = 250
        #Zone FRONT LEFT (160 - 170)
        #ANGLE_RIGHT_BACK = 300
        #Zone FRONT LEFT (160 - 170)
        ANGLE_BACK_RIGHT = 340
        #Zone FRONT LEFT (160 - 170)
        ANGLE_BACK_MIDDLE = 0
        #Zone FRONT LEFT (160 - 170)
        ANGLE_BACK_LEFT = 20
        #Zone FRONT LEFT (160 - 170)
        #ANGLE_LEFT_FRONT = 250
        #Zone FRONT LEFT (160 - 170)
        #ANGLE_LEFT_BACK = 300
        #Zone FRONT LEFT (160 - 170)
        
        detected_zone = {}
        detected_zone["FRONT_LEFT"] = 0
        detected_zone["FRONT_MIDDLE_LEFT"] = 0
        detected_zone["FRONT_MIDDLE_RIGHT"] = 0
        detected_zone["FRONT_RIGHT"] = 0
        
        
        Flag_DISTANCE = np.array([1000,1000,1000,1000])

        ANGLE_MAX_BACK = 340
        ANGLE_MIN_BACK = 20
        Flag_FRONT = 0
        Flag_BACK = 0
        print("Lidar thread in execution")
        left = 0
        right = 0

        count_points = 0
        count_points_detected_FRONT = 0
        count_points_detected_BACK = 0

        new_scan = True
        angle = 0.0
        quality = 0
        distance = 0.0
        
        first_point_FRONT=True
        first_point_BACK=True
        refer_angle_FRONT=-1.0
        refer_angle_BACK=-1.0

        time.sleep(1)
        for new_scan, quality, angle, distance in self.lidar.iter_measurments():
                detected_zone["FRONT_LEFT"] = 0
                detected_zone["FRONT_MIDDLE_LEFT"] = 0
                detected_zone["FRONT_MIDDLE_RIGHT"] = 0
                detected_zone["FRONT_RIGHT"] = 0
                if(not(new_scan) and distance!=0) :
                    count_points=count_points+1
                    #Front
                    if (distance<=SAFE_DISTANCE and angle>=ANGLE_FRONT_LEFT and angle<=ANGLE_FRONT_RIGHT) :
                        if (angle < ANGLE_FRONT_MIDDLE_LEFT):
                            detected_zone["FRONT_LEFT"] = 1
                        if (angle > ANGLE_FRONT_MIDDLE_LEFT and angle < ANGLE_FRONT_MIDDLE):
                            detected_zone["FRONT_MIDDLE_LEFT"] = 1
                        if (angle > ANGLE_FRONT_MIDDLE and angle < ANGLE_FRONT_MIDDLE_RIGHT):
                            detected_zone["FRONT_MIDDLE_RIGHT"] = 1
                        if (angle > ANGLE_FRONT_MIDDLE_RIGHT and angle < ANGLE_FRONT_RIGHT):
                            detected_zone["FRONT_RIGHT"] = 1
                        print("Detected zone :",detected_zone)
                        #Flag_ZONE = np.array([0,0,0,0,0])s
                        #print("shortest distance :",index_distance)        
                        
                if(count_points==320):
                   count_points=0
                   #left = ANGLE_MIN_FRONT - 
                   if(count_points_detected_FRONT>4) :
                      Flag_FRONT=1
                   else :
                      Flag_FRONT=0
                   count_points_detected_FRONT=0
                   first_point_FRONT=True

                   if(count_points_detected_BACK>4) :
                      Flag_BACK=1
                   else :
                      Flag_BACK=0
                   count_points_detected_BACK=0
                   first_point_BACK==True

                #print("FLAG FRONT     ",Flag_FRONT,"\n")
                #print("FLAG  back     ",Flag_BACK,"\n")
                
                if(Flag_BACK and Flag_FRONT) :
                    glob.DATA_LIDAR=Data(ID.LIDAR,Message.DETECTED_BOTH)
                elif (Flag_FRONT):
                    glob.DATA_LIDAR=Data(ID.LIDAR,Message.DETECTED_FRONT)
                elif (Flag_BACK) :
                    glob.DATA_LIDAR=Data(ID.LIDAR,Message.DETECTED_BACK)
                else :
                    glob.DATA_LIDAR=Data(ID.LIDAR,Message.DETECTED_NULL)
                #print("Message Lidar: "+str(glob.DATA_LIDAR.message))



