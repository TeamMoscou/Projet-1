import Lidar_Detection_Thread
import prise_de_decision
import interface
import Ultrason
import can_send
import time
import can
import sys
import os
import struct
import data

MODE
DATA_LIDAR
DATA_ULTRASONIC
DATA_INTERFACE
DATA_OUT

if __name__ == "__main__":

    print('Bring up CAN0....')
    os.system("sudo ifconfig can0 down")
    os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)

    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

    cansend_instance = can_send
    cansend_thread = cansend_instance(bus)
    cansend_thread.daemon = True
    cansend_thread.start()
    cansend_thread.join()

    while(1):
        time.sleep(0.1)
        DATA_OUT = (DECISION,BACKWARD)
        time.sleep(1)
        DATA_OUT = (DECISION, STOP)
        time.sleep(5)

