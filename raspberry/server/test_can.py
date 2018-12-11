import can_send
import time
import can
import sys
import os
import struct
import data
import global_variables
from global_variables import *

if __name__ == "__main__":

    
    print('Bring up CAN0....')
    os.system("sudo ifconfig can0 down")
    os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

    cansend_instance = can_send
    cansend_thread = cansend_instance.Can_send(bus)
    cansend_thread.daemon = True
    cansend_thread.start()
    #cansend_thread.join()

    while(1):
        print(1)
        time.sleep(0.2)
        #test_dec = 0
        global_variables.DATA_DECISION = Data(ID.DECISION,Message.FORWARD)
        #test_dec = 1
        time.sleep(0.5)
        global_variables.DATA_DECISION = Data(ID.DECISION,Message.STOP)
    cansend_thread.join()

