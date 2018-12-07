# coding: utf-8

import threading
import os
from rplidar import RPLidar
import time

lidar = RPLidar('/dev/ttyUSB0')
SAFE_DISTANCE = 2000
ANGLE_MAX_FRONT = 200
ANGLE_MIN_FRONT = 160
ANGLE_MAX_BACK = 340
ANGLE_MIN_BACK = 20
# flags set to 1 when the obstacle is detected
Flag_FRONT = 0
Flag_BACK = 0


# the definition of the class thread of the lidar
class LidarDetection(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
    def stop(self):
        self._stop.set()
    def run(self):

        print("Lidar thread in execution")

        global Flag_FRONT
        global Flag_BACK
        count_points = 0
        count_points_detected_FRONT = 0
        count_points_detected_BACK = 0

        new_scan = True
        angle = 0.0
        quality = 0
        distance = 0.0

        time.sleep(5)
        for new_scan, quality, angle, distance in lidar.iter_measurments():
            if self._stop.is_set():
                print('wait,shuting down')
                break
                
            else :

                if (not (new_scan) and distance != 0):
                    count_points = count_points + 1

                    if (distance <= SAFE_DISTANCE and angle >= ANGLE_MIN_FRONT and angle <= ANGLE_MAX_FRONT):
                        count_points_detected_FRONT = count_points_detected_FRONT + 1

                    elif (distance <= SAFE_DISTANCE and angle >= ANGLE_MAX_BACK or angle <= ANGLE_MIN_BACK):
                        count_points_detected_BACK = count_points_detected_BACK + 1
                print("number of points detected in front", count_points_detected_FRONT, "\n")
                print("number of points detected in back", count_points_detected_BACK, "\n")

                if (count_points == 320):

                    count_points = 0

                    if (count_points_detected_FRONT > 15):
                        Flag_FRONT = 1
                    else:
                        Flag_FRONT = 0
                    count_points_detected_FRONT = 0

                    if (count_points_detected_BACK > 15):
                        Flag_BACK = 1
                    else:
                        Flag_BACK = 0
                    count_points_detected_BACK = 0
                print("FLAG FRONT     ", Flag_FRONT, "\n")
                print("FLAG  back     ", Flag_BACK, "\n")

