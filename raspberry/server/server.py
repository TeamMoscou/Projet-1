import Lidar_Detection_Thread
import global_variables
import prise_de_decision
import interface
import Ultrason
import can_send
import data
import time
import can
import sys
import os
import struct

DATA_INTERFACE
DATA_LIDAR
DATA_ULTRASONIC
DATA_OUT

if __name__ == "__main__":

    print('Bring up CAN0....')
    os.system("sudo ifconfig can0 down")
    os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)

    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

    lidar_instance = Lidar_Detection_Thread
    interface_instance = interface
    ultrason_instance = Ultrason
    decision_instance = prise_de_decision
    cansend_instance = can_send

    lidar_thread = lidar_instance.LidarDetection()
    interface_thread = interface_instance.Interface()
    ultrason_thread = ultrason_instance.Ultrason(bus)
    decision_thread = decision_instance()
    cansend_thread = cansend_instance(bus)

    lidar_thread.daemon = True
    interface_thread.daemon = True
    ultrason_thread.daemon = True
    decision_thread.daemon = True
    cansend_thread.daemon = True

    lidar_thread.start()
    interface_thread.start()
    ultrason_thread.start()
    decision_thread.start()
    cansend_thread.start()

    lidar_thread.join()
    interface_thread.join()
    ultrason_thread.join()
    decision_thread.join()
    cansend_thread.join()

