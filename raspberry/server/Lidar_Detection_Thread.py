# coding: utf-8

import threading
import os
from rplidar import RPLidar
import time
from data import Data
from data import ID
from data import Message

from global_variables import *




# the definition of the class thread of the lidar
class LidarDetection(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)     
    
    def run(self):

        print("Lidar thread in execution")

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
        for new_scan, quality, angle, distance in lidar.iter_measurments():
           
            if shutdown_lidar.isSet():
                print("Lidar thread exit")
                wait_ultrason.set()
                lidar.stop()
                lidar.stop_motor()
                lidar.disconnect()
                break
                
                
            else :

                if(not(new_scan) and distance!=0) :

                    count_points=count_points+1

                    #Front
                    if (distance<=SAFE_DISTANCE and angle>=ANGLE_MIN_FRONT and angle<=ANGLE_MAX_FRONT) :
                        if (first_point_FRONT==True):
                            first_point_FRONT=False
                            refer_angle_FRONT=angle
                            count_points_detected_FRONT=1
                        elif ( abs(angle-refer_angle_FRONT)< 4 ):
                            refer_angle_FRONT=angle
                            count_points_detected_FRONT=count_points_detected_FRONT+1
                        elif(abs(angle-refer_angle_FRONT)>4 and count_points_detected_FRONT<10) :
                            first_point_FRONT=True
                            count_points_detected_FRONT=0

                        else:
                            refer_angle_FRONT=angle
                            count_points_detected_FRONT=count_points_detected_FRONT+1



                    #Back        
                    elif(distance<=SAFE_DISTANCE and angle>=ANGLE_MAX_BACK or angle<=ANGLE_MIN_BACK):
                        if(angle>=ANGLE_MAX_BACK) :
                            relative_angle=angle-360.0
                        else :
                            relative_angle=angle

                        if (first_point_BACK==True):
                            first_point_BACK=False
                            refer_angle_BACK=relative_angle
                            count_points_detected_BACK=1

                        elif (abs(relative_angle-refer_angle_BACK)<4):
                            refer_angle_BACK=relative_angle
                            count_points_detected_BACK=count_points_detected_BACK+1
                        elif(abs(relative_angle-refer_angle_BACK)>4 and count_points_detected_BACK<4) :
                            first_point_BACK=True
                            count_points_detected_BACK=0

                        else:
                            refer_angle_BACK=relative_angle
                            count_points_detected_BACK=count_points_detected_BACK+1

                print("number of points detected in front",count_points_detected_FRONT,"\n")
                print("number of points detected in back",count_points_detected_BACK,"\n")

                if(count_points==320):

                   count_points=0

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

                print("FLAG FRONT     ",Flag_FRONT,"\n")
                print("FLAG  back     ",Flag_BACK,"\n")
                
                if(Flag_BACK and Flag_FRONT) :
                    DataLidar=Data(ID.LIDAR,Message.DETECTED_BOTH)
                elif (Flag_FRONT):
                    DataLidar=Data(ID.LIDAR,Message.DETECTED_FRONT)
                elif (Flag_BACK) :
                    DataLidar=Data(ID.LIDAR,Message.DETECTED_BACK)
                else :
                    DataLidar=Data(ID.LIDAR,Message.DETECTED_NULL)
                    
                wait_ultrason.set()
                wait_lidar.clear()
                wait_lidar.wait()
