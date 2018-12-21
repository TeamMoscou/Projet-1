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
        #Zone FRONT_LEFT (160 - 170)
        ANGLE_FRONT_MIDDLE_LEFT = 170
        #Zone FRONT_MIDDLE_LEFT (170 - 180)
        ANGLE_FRONT_MIDDLE = 180
        #Zone FRONT_MIDDLE_RIGHT (180 - 190)
        ANGLE_FRONT_MIDDLE_RIGHT = 190
        #Zone FRONT_RIGHT (190 - 200)
        ANGLE_FRONT_RIGHT = 200
        #Zone RIGHT_FRONT (200 - 255)
        ANGLE_RIGHT_MIDDLE = 255
        #Zone RIGHT_BACK (255 - 310)
        ANGLE_BACK_RIGHT = 310
        #Zone BACK_RIGHT (310 - 360)
        ANGLE_BACK_MIDDLE = 0
        #Zone BACK_LEFT (0 - 50)
        ANGLE_BACK_LEFT = 50
        #Zone LEFT_BACK (50 - 105)
        ANGLE_LEFT_MIDDLE = 105
        #Zone LEFT_FRONT (105 - 160)
        
        detected_zone = {}
        detected_zone["FRONT_LEFT"] = 0
        detected_zone["FRONT_MIDDLE_LEFT"] = 0
        detected_zone["FRONT_MIDDLE_RIGHT"] = 0
        detected_zone["FRONT_RIGHT"] = 0
        detected_zone["RIGHT_FRONT"] = 0
        detected_zone["RIGHT_BACK"] = 0
        detected_zone["BACK_RIGHT"] = 0
        detected_zone["BACK_LEFT"] = 0
        detected_zone["LEFT_BACK"] = 0
        detected_zone["LEFT_FRONT"] = 0      
        
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
                if(not(new_scan) and distance!=0) :
                    count_points=count_points+1
                    #Front
                    if (angle>=ANGLE_FRONT_LEFT and angle<=ANGLE_FRONT_RIGHT) :
                        if (angle < ANGLE_FRONT_MIDDLE_LEFT):
                            if (distance<=3500):
                                detected_zone["FRONT_LEFT"] = 1
                            else:
                                detected_zone["FRONT_LEFT"] = 0
                        if (angle > ANGLE_FRONT_MIDDLE_LEFT and angle < ANGLE_FRONT_MIDDLE):
                            if (distance<=3500):
                                detected_zone["FRONT_MIDDLE_LEFT"] = 1
                            else:
                                detected_zone["FRONT_MIDDLE_LEFT"] = 0
                        if (angle > ANGLE_FRONT_MIDDLE and angle < ANGLE_FRONT_MIDDLE_RIGHT):
                            if (distance<=3500):
                                detected_zone["FRONT_MIDDLE_RIGHT"] = 1
                            else:
                                detected_zone["FRONT_MIDDLE_RIGHT"] = 0
                        if (angle > ANGLE_FRONT_MIDDLE_RIGHT and angle < ANGLE_FRONT_RIGHT):
                            if (distance<=3500):
                                detected_zone["FRONT_RIGHT"] = 1
                            else:
                                detected_zone["FRONT_RIGHT"] = 0
                    else: 
                        if (angle > ANGLE_FRONT_RIGHT and angle < ANGLE_RIGHT_MIDDLE):
                            if (distance<=3500):
                                detected_zone["RIGHT_FRONT"] = 1
                            else:
                                detected_zone["RIGHT_FRONT"] = 0
                        if (angle > ANGLE_RIGHT_MIDDLE and angle < ANGLE_BACK_RIGHT):
                            if (distance<=3500):
                                detected_zone["RIGHT_BACK"] = 1
                            else:
                                detected_zone["RIGHT_BACK"] = 0
                        if (angle > ANGLE_BACK_RIGHT and angle < ANGLE_BACK_MIDDLE):
                            if (distance<=3500):
                                detected_zone["BACK_RIGHT"] = 1
                            else:
                                detected_zone["BACK_RIGHT"] = 0
                        if (angle > ANGLE_BACK_MIDDLE and angle < ANGLE_BACK_LEFT):
                            if (distance<=3500):
                                detected_zone["BACK_LEFT"] = 1
                            else:
                                detected_zone["BACK_LEFT"] = 0 
                        if (angle > ANGLE_BACK_LEFT and angle < ANGLE_LEFT_MIDDLE):
                            if (distance<=3500):
                                detected_zone["LEFT_BACK"] = 1
                            else:
                                detected_zone["LEFT_BACK"] = 0
                        if (angle > ANGLE_LEFT_MIDDLE and angle < ANGLE_FRONT_LEFT):
                            if (distance<=3500):
                                detected_zone["LEFT_FRONT"] = 1
                            else:
                                detected_zone["LEFT_FRONT"] = 0                       
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



