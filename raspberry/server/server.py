import Lidar_Detection_Thread
import prise_de_decision
#import interface
import Ultrason
import time
import can
import sys
import os
import struct

if __name__ == "__main__":

    print('Bring up CAN0....')
    os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)

    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        print('Cannot find PiCAN board.')
        exit()

    lidar_instance = Lidar_Detection_Thread
    #interface_instance = interface
    ultrason_instance = Ultrason
    #decision_instance = prise_de_decision

    lidar_thread = lidar_instance.LidarDetection()
    #interface_thread = interface_instance.Interface()
    ultrason_thread = ultrason_instance.Ultrason(bus)
    #decision_thread = decision_instance

    lidar_thread.start()
    #interface_thread.start()
    ultrason_thread.start()
    #decision_thread.start()


    try:
        time.sleep(.1)
    except KeyboardInterrupt:
        lidar_thread._stop.clear()
        # interface_thread._stop.clear()
        ultrason_thread._stop.clear()
        # decison_thread._stop.clear()

    lidar_thread.join()
    # interface_thread._stop.clear()
    ultrason_thread.join()
    # decision_thread.join()

