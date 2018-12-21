import test_lidar_detection_thread
import lidar_detection_thread
import prise_decision
import interface
import ultrason
#import can_send
import time
import can
import sys
import os
import struct
import data
import socket
import signal

if __name__ == "__main__":

    
    lidar_instance = test_lidar_detection_thread

    lidar_thread = lidar_instance.LidarDetection()

    lidar_thread.daemon = True
    
    
    lidar_thread.start()

    lidar_thread.join()
