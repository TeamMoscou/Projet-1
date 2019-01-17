import threading
import time
import numpy as np
import math
from rplidar import RPLidar
from glob import *
from data import *

#In this file we compute data from Lidar
#We decide and inform when there is an obstacle in the front or back partself.
#The autonomous managment is also done here with the avoidance system

class LidarDetection(threading.Thread):

    def __init__(self, lidar):
        threading.Thread.__init__(self)
        #We use the lidar open by the main class
        self.lidar = lidar

    def run(self):

        #To be sure lidar is running
        time.sleep(3)

        print("Lidar thread in execution")

        #Distance chose for the dangerous zone (1000 = 1 meter)
        SAFE_DISTANCE_FRONT = 2000
        SAFE_DISTANCE_BACK = 1000

        #Distance use to manage the autonomous/avoidance system, we saw that after 3.5 meters some errors appear on the lidar data
        MAX_DETECTED_DISTANCE = 3500

        #We separate the lidar detection in diffent areas, we use only front and back areas
        #Zone FRONT between 160 and 200
        ANGLE_FRONT_LEFT = 160
        ANGLE_FRONT_MIDDLE_LEFT = 170
        ANGLE_FRONT_MIDDLE = 180
        ANGLE_FRONT_MIDDLE_RIGHT = 190
        ANGLE_FRONT_RIGHT = 200

        #Zone BACK between 340 and 20
        ANGLE_BACK_RIGHT = 340
        ANGLE_BACK_MIDDLE = 0
        ANGLE_BACK_LEFT = 20

        #Count the number of detection point in the 4 front zones
        count_front = 0 #Used for the 2 zones in the middle (170 to 190)
        count_fright = 0
        count_fleft = 0

        #Count the number of detection in the danger zone for the front and the back
        count_front_danger = 0
        count_back_danger = 0

        #Flags using the number of detection to change their state
        flag_front = False
        flag_fright = False
        flag_fleft = False
        flag_front_danger = False
        flag_back_danger = False

        new_scan = True
        angle = 0.0
        quality = 0
        distance = 0.0

        #Use to compute data after one entire rotation
        previous_angle = 0

        i = 0
        for (new_scan, quality, angle, distance) in self.lidar.iter_measurments():         
            i = (i+1)%2
            #Distance == 0 due to error from the lidar or someting put on the sensor, we don't use those data
            if(distance != 0 and i == 0) :
                #Check detection on one full rotation
                if(angle > previous_angle):
                    previous_angle = angle
                    #Check if there are enough detection, increasing the number is to lower errors but also dectect larger obstacle
                    if(count_front > 2):
                        flag_front = True
                    else :
                        flag_front = False

                    if(count_fright > 1):
                        flag_fright = True
                    else :
                        flag_fright = False

                    if(count_fleft > 1):
                        flag_fleft = True
                    else :
                        flag_fleft = False

                    if(count_front_danger > 2):
                        flag_front_danger = True
                    else :
                        flag_front_danger = False

                    if(count_back_danger > 2):
                        flag_back_danger = True
                    else :
                        flag_back_danger = False
                else:
                    #Mean that one rotation is over so we reset counters
                    previous_angle = 0
                    count_front = 0
                    count_fright = 0
                    count_fleft = 0
                    count_front_danger = 0
                    count_back_danger = 0

                    #Update global variable autonomous/avoidance system
                    if(flag_front):
                        if(flag_fright and flag_fleft):
                            #If there are obstacles in every zones in front of the car we try to get around by the left
                            DATA_LIDAR_AUTONOMOUS.message = Message.FORWARD_LEFT
                        elif(flag_fright):
                            DATA_LIDAR_AUTONOMOUS.message = Message.FORWARD_LEFT
                        elif(flag_fleft):
                            DATA_LIDAR_AUTONOMOUS.message = Message.FORWARD_RIGHT
                        else:
                            #If only an obstacle in the middle we go on the left side
                            DATA_LIDAR_AUTONOMOUS.message = Message.FORWARD_LEFT
                    else:
                        #When the car don't detect anything we go forward
                        DATA_LIDAR_AUTONOMOUS.message = Message.FORWARD

                    #Update global variable for the danger detection zone
                    if(flag_front_danger and flag_back_danger):
                        DATA_LIDAR.message = Message.DETECTED_BOTH
                    elif (flag_front_danger):
                        DATA_LIDAR.message = Message.DETECTED_FRONT
                    elif (flag_back_danger):
                        DATA_LIDAR.message = Message.DETECTED_BACK
                    else:
                        DATA_LIDAR.message = Message.DETECTED_NULL


                    print("Message Lidar detection: "+str(DATA_LIDAR.message))
                    print("Message Lidar autonomous: "+str(DATA_LIDAR_AUTONOMOUS.message))


                #Treatment of the data from Lidar for the front
                if (angle >= ANGLE_FRONT_LEFT and angle <= ANGLE_FRONT_RIGHT):

                    #Danger zone
                    if (distance <= SAFE_DISTANCE_FRONT):
                        count_front_danger = count_front_danger + 1

                    #Detection zone accurate
                    if (distance <= MAX_DETECTED_DISTANCE):
                        if (angle < ANGLE_FRONT_MIDDLE_LEFT):
                            count_fleft = count_fleft + 1
                        elif (angle > ANGLE_FRONT_MIDDLE_LEFT and angle < ANGLE_FRONT_MIDDLE_RIGHT):
                            
                            count_front = count_front + 1
                        else :
                            count_fright = count_fright + 1

                #Treatment of the data from Lidar for the back
                elif (angle >= ANGLE_BACK_RIGHT or angle <= ANGLE_BACK_LEFT) :

                    #Danger zone
                    if (distance <= SAFE_DISTANCE_BACK):
                        count_back_danger = count_back_danger + 1

