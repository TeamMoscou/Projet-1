import lidar_detection_thread
import global_variables
import prise_decision
import interface
import ultrason
import can_send
import time
import can
import sys
import os
import struct
import data

if __name__ == "__main__":

    print('Bring up CAN0....')
    os.system("sudo ifconfig can0 down")
    os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)

    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

    lidar_instance = lidar_detection_thread
    interface_instance = interface
    ultrason_instance = ultrason
    decision_instance = prise_decision
    cansend_instance = can_send

    lidar_thread = lidar_instance.LidarDetection()
    interface_thread = interface_instance.Interface()
    ultrason_thread = ultrason_instance.Ultrason(bus)
    decision_thread = decision_instance.Prise_decision()
    cansend_thread = cansend_instance.Can_send(bus)

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

