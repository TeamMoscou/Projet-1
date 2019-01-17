# coding: utf-8
import can
#import sys
import os
import struct
import data
import socket
from rplidar import RPLidar
import time
import signal

import lidar as lidar_instance
import prise_decision as decision_instance
import interface as interface_instance
import ultrason as ultrason_instance
#import can_send as cansend_instance
import cansend_jo as cansend_instance

#In this file we create all the threads and launch them

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    conn.close()

if __name__ == "__main__":

    #lidar instance
    lidar = RPLidar('/dev/ttyUSB0')

    #connect to the User Interface via socket
    HOST = ''
    PORT = 6666
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.bind((HOST, PORT))
    #s.listen(1)
    #conn, addr = s.accept()

    print('Bring up CAN0....')
    os.system("sudo ifconfig can0 down")
    os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)

    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

    #configure the signal handler to handle Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    #instanciate Threads
    lidar_thread = lidar_instance.LidarDetection(lidar)
    #interface_thread = interface_instance.Interface(conn)
    #interfaceReturn_thread = interface_instance.ReturnInterface(conn)
    ultrason_thread = ultrason_instance.Ultrason(bus)
    decision_thread = decision_instance.Prise_decision()
    cansend_thread = cansend_instance.Can_send(bus)

    #set the Threads as daemon
    lidar_thread.daemon = True
    #interface_thread.daemon = True
    #interfaceReturn_thread.daemon = True
    ultrason_thread.daemon = True
    decision_thread.daemon = True
    cansend_thread.daemon = True

    #start the Threads
    lidar_thread.start()
    #interface_thread.start()
    #interfaceReturn_thread.start()
    ultrason_thread.start()
    decision_thread.start()
    cansend_thread.start()

    #wait until the Threads finish
    lidar_thread.join()
    #interface_thread.join()
    #interfaceReturn_thread.join()
    ultrason_thread.join()
    decision_thread.join()
    cansend_thread.join()


