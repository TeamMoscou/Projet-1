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
        ANGLE_MAX_FRONT = 200
        ANGLE_MIN_FRONT = 160
        k = 6
        arr = np.arange(k)
        Flag_ZONE = np.arange(k-1)
        Flag_ZONE = [[0]*5 for i in range(k-1)]
        ANGLE_DIFF = ANGLE_MAX_FRONT - ANGLE_MIN_FRONT

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
                    ANGLE_DIFF_INIT=ANGLE_DIFF/5
                    arr[0]=ANGLE_MIN_FRONT
                    arr[1]=arr[0]+ANGLE_DIFF_INIT
                    arr[2]=arr[1]+ANGLE_DIFF_INIT
                    arr[3]=arr[2]+ANGLE_DIFF_INIT
                    arr[4]=arr[3]+ANGLE_DIFF_INIT
                    arr[5]=arr[4]+ANGLE_DIFF_INIT 
#                    print("1:",arr[0],"\n")
#                    print("2:",arr[1],"\n")
#                    print("3:",arr[2],"\n")
#                    print("4:",arr[3],"\n")
#                    print("5:",arr[4],"\n")
#                    print("6:",arr[5],"\n")
                    #Front
                    if (distance<=SAFE_DISTANCE and angle>=ANGLE_MIN_FRONT and angle<=ANGLE_MAX_FRONT) :
                        if (arr[0]<angle and angle < arr[1]):
                            print("OBS Z1 dist : %d",distance)
                            Flag_ZONE[0][0] = True
                            Flag_ZONE[0][1] = distance
                        elif (arr[1]<angle and angle < arr[2]):
                            print("OBS Z2 dist : %d",distance)
                            Flag_ZONE[1][0] = True
                            Flag_ZONE[1][1] = distance
                        elif (arr[2]<angle and angle < arr[3]):
                            print("OBS Z3 dist : %d",distance)
                            Flag_ZONE[2][0] = True
                            Flag_ZONE[2][1] = distance
                        elif (arr[3]<angle and angle < arr[4]):
                            print("OBS Z4 dist : %d",distance)
                            Flag_ZONE[3][0] = True
                            Flag_ZONE[3][1] = distance
                        elif (arr[4]<angle and angle < arr[5]):
                            print("OBS Z5 dist : %d",distance)
                            Flag_ZONE[4][0] = True
                            Flag_ZONE[4][1] = distance
                        else:
                            index = numpy.where(Flag_ZONE == True)
                            print("where?:"index)

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
