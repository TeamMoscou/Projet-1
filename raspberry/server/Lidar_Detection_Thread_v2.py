

# coding: utf-8



#mécanisme de détection plus robuste


from threading import Thread
import os
from rplidar import RPLidar
import time
import math




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

        first_point_FRONT=True
        first_point_BACK=True
        refer_angle_FRONT=-1.0
        refer_angle_BACK=-1.0

        time.sleep(5)
        for new_scan, quality, angle, distance in lidar.iter_measurments() :

            #print(new_scan, quality, angle, distance)

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
                        print("here1")

                    elif (abs(relative_angle-refer_angle_BACK)<4):
                        refer_angle_BACK=relative_angle
                        count_points_detected_BACK=count_points_detected_BACK+1
                        print("here2")
                    elif(abs(relative_angle-refer_angle_BACK)>4 and count_points_detected_BACK<10) :
                        first_point_BACK=True
                        count_points_detected_BACK=0
                        print("here3")

                    else:
                        print("here4")
                        refer_angle_BACK=relative_angle
                        count_points_detected_BACK=count_points_detected_BACK+1

            print("number of points detected in front",count_points_detected_FRONT,"\n")
            print("number of points detected in back",count_points_detected_BACK,"\n")

            if(count_points==320):

               count_points=0

               if(count_points_detected_FRONT>15) :
                  Flag_FRONT=1
               else :
                  Flag_FRONT=0
               count_points_detected_FRONT=0
               first_point_FRONT=True

               if(count_points_detected_BACK>15) :
                  Flag_BACK=1
               else :
                  Flag_BACK=0
               count_points_detected_BACK=0
               first_point_BACK==True

            print("FLAG FRONT     ",Flag_FRONT,"\n")
            print("FLAG  back     ",Flag_BACK,"\n")



if __name__ == "__main__":


        try:
               newDetect=LidarDetection()
               newDetect.start()
               newDetect.join()

        except KeyboardInterrupt:
               print('Stoping.')
               lidar.stop()
               lidar.stop_motor()
               lidar.disconnect()







