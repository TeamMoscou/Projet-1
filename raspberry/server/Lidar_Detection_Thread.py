# coding: utf-8


from threading import Thread
import os
from rplidar import RPLidar
import time




lidar = RPLidar('/dev/ttyUSB0')

SAFE_DISTANCE=2000
ANGLE_MAX_FRONT=200
ANGLE_MIN_FRONT=160
ANGLE_MAX_BACK=340
ANGLE_MIN_BACK=20
#flags set to 1 when the obstacle is detected
Flag_FRONT=0
Flag_BACK=0

class LidarDetection(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):


        print("Lidar thread in execution")

        global Flag_FRONT
        global Flag_BACK
        
        count_points=0
        count_points_detected_FRONT=0
        count_points_detected_BACK=0
        
        new_scan=True
        angle=0.0
        quality=0
        distance=0.0


        for new_scan, quality, angle, distance in lidar.iter_measurments() :

            print(new_scan, quality, angle, distance)

            if(not(new_scan) and distance!=0) :

                count_points=count_points+1

                if (distance<=SAFE_DISTANCE and angle>=ANGLE_MIN_FRONT and angle<=ANGLE_MAX_FRONT) :
                    count_points_detected_FRONT=count_points_detected_FRONT+1

                elif(distance<=SAFE_DISTANCE and angle>=ANGLE_MAX_BACK or angle<=ANGLE_MIN_BACK):
                    count_points_detected_BACK=count_points_detected_BACK+1
            print("number of points detected in front",count_points_detected_FRONT,"\n")
            print("number of points detected in back",count_points_detected_BACK,"\n")

            if(count_points=360):

               count_points=0

               if(count_points_detected_FRONT>15) :
                  flag_FRONT=1
               else :
                  flag_FRONT=0
               count_points_detected_FRONT=0

               if(count_points_detected_BACK>15) :
                  flag_BACK=1
               else :
                  flag_BACK=0
               count_points_detected_BACK=0

