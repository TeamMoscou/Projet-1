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
        ANGLE_MAX_FRONT = 195
        ANGLE_MIN_FRONT = 165
        arr = np.arange(6) 
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
                    print("1:",arr[0],"\n")
                    print("2:",arr[1],"\n")
                    print("3:",arr[2],"\n")
                    print("4:",arr[3],"\n")
                    print("5:",arr[4],"\n")
                    print("6:",arr[5],"\n")
                    #Front
                    if (distance<=SAFE_DISTANCE and angle>=ANGLE_MIN_FRONT and angle<=ANGLE_MAX_FRONT) :
                        if (first_point_FRONT==True):
                            first_point_FRONT=False
                            refer_angle_FRONT=angle
                            count_points_detected_FRONT=1
                            print("detected 1")
                        elif(abs(angle-refer_angle_FRONT)<4):
                            refer_angle_FRONT=angle
                            count_points_detected_FRONT=count_points_detected_FRONT+1
                            print("detected 2")
                        elif(abs(angle-refer_angle_FRONT)>4 and count_points_detected_FRONT<10) :
                            refer_angle_FRONT = angle
                            first_point_FRONT = True
                            count_points_detected_FRONT = 0
                            print("detected 3")
                        else:
                            refer_angle_FRONT=angle
                            count_points_detected_FRONT=count_points_detected_FRONT+1
                            print("detected 4")

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
