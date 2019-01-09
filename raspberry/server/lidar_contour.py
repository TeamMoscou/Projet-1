import threading
import os
from rplidar import RPLidar
import time
import glob
import numpy as np
import math
from glob import *
from data import *
#from global_variables import *
# the definition of the class thread of the lidar


#lidar = RPLidar('/dev/ttyUSB0')
class LidarDetection(threading.Thread):

    def __init__(self,lidar):
        threading.Thread.__init__(self)
        self.lidar = lidar

    def run(self):

        print("Lidar thread in execution")
        
        SAFE_DISTANCE_FRONT = 2000
        SAFE_DISTANCE_BACK = 1000
        #Distance with few errors
        MAX_DETECTED_DISTANCE = 3500
        
        ANGLE_FRONT_LEFT = 160
        #Zone FRONT_LEFT (160 - 170)
        ANGLE_FRONT_MIDDLE_LEFT = 170
        #Zone FRONT_MIDDLE (170 - 180)
        ANGLE_FRONT_MIDDLE = 180
        #Zone FRONT_MIDDLE (180 - 190)
        ANGLE_FRONT_MIDDLE_RIGHT = 190
        #Zone FRONT_RIGHT (190 - 200)
        ANGLE_FRONT_RIGHT = 200
        #Zone RIGHT_FRONT (200 - 255)
        ANGLE_RIGHT_MIDDLE = 255
        #Zone RIGHT_BACK (255 - 330)
        ANGLE_BACK_RIGHT = 340
        #Zone BACK_RIGHT (340 - 360)
        ANGLE_BACK_MIDDLE = 0
        #Zone BACK_LEFT (0 - 20)
        ANGLE_BACK_LEFT = 20
        #Zone LEFT_BACK (20 - 105)
        ANGLE_LEFT_MIDDLE = 105
        #Zone LEFT_FRONT (105 - 160)
    


        count_front = 0
        #front_right
        count_fright = 0 
        #front_left
        count_fleft = 0
        count_front_danger = 0
        count_back_danger = 0
        
        flag_front = False
        flag_fright = False
        flag_fleft = False
        flag_front_danger = False
        flag_back_danger = False

        new_scan = True
        angle = 0.0
        quality = 0
        distance = 0.0

        previous_angle = 0
        i = 0
        time.sleep(1)

        for new_scan, quality, angle, distance in self.lidar.iter_measurments():
            i = (i+1)%2    
            if(distance != 0 and i == 0) :
                
                #Check detection on one full rotation
                if(angle > previous_angle):
                    previous_angle = angle
                    #Check if there are enough detection
                    if(count_front > 1):
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
                     #UPDATE global variable autonomous
                    if(flag_front):
                        if(flag_fright and flag_fleft):
                            glob.DATA_LIDAR_AUTONOMOUS = Data(ID.LIDAR,Message.FORWARD_LEFT)
                        elif(flag_fright):
                            glob.DATA_LIDAR_AUTONOMOUS = Data(ID.LIDAR,Message.FORWARD_LEFT)
                        elif(flag_fleft):
                            glob.DATA_LIDAR_AUTONOMOUS = Data(ID.LIDAR,Message.FORWARD_RIGHT)
                        else:
                            glob.DATA_LIDAR_AUTONOMOUS = Data(ID.LIDAR,Message.FORWARD_LEFT)
                    else:
                        glob.DATA_LIDAR_AUTONOMOUS = Data(ID.LIDAR,Message.FORWARD)

                    #UPDATE global variable detection
                    if(flag_front_danger and flag_back_danger):
                        glob.DATA_LIDAR = Data(ID.LIDAR,Message.DETECTED_BOTH)
                        #glob.DATA_LIDAR_AUTONOMOUS = Data(ID.LIDAR,Message.STOP)
                    elif (flag_front_danger):
                        glob.DATA_LIDAR = Data(ID.LIDAR,Message.DETECTED_FRONT)
                        #glob.DATA_LIDAR_AUTONOMOUS = Data(ID.LIDAR,Message.STOP)
                    elif (flag_back_danger):
                        glob.DATA_LIDAR = Data(ID.LIDAR,Message.DETECTED_BACK)
                    else:
                        glob.DATA_LIDAR = Data(ID.LIDAR,Message.DETECTED_NULL)
                    print("Message Lidar detection: "+str(glob.DATA_LIDAR.message))
                    #print("Message Lidar autonomous: "+str(glob.DATA_LIDAR_AUTONOMOUS.message))
                    previous_angle = 0
                    count_front = 0
                    count_fright = 0
                    count_fleft = 0
                    count_front_danger = 0
                    count_back_danger = 0
                    

                #FRONT
                if (angle>=ANGLE_FRONT_LEFT and angle<=ANGLE_FRONT_RIGHT) :
                    
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

                #BACK
                elif (angle >= ANGLE_BACK_RIGHT or angle <= ANGLE_BACK_LEFT) :

                    #Danger zone
                    if (distance <= SAFE_DISTANCE_BACK):
                        count_back_danger = count_back_danger + 1 



