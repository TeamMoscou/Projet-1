# coding: utf-8
import threading
import can
import time
from glob import *

class Can_send(threading.Thread):

    def __init__(self, bus):
        threading.Thread.__init__(self)
        #We use the bus open by the server class
        self.bus = bus

    def run(self):

        #We fixed a constant speed, change this value to increase or decrease the speed
        self.speed_cmd = 25
        self.move = 0
        self.turn = 0
        self.enable = 0

        while True:
            #Avoid sending to much data threw the CAN
            time.sleep(0.1)

            if (glob.DATA_DECISION.message == Message.FORWARD):
                self.move = 1
                self.turn = 0
                self.enable = 1
                print("Send cmd move forward")
            elif (glob.DATA_DECISION.message == Message.FORWARD_LEFT):
                self.move = 1
                self.turn = -1
                self.enable = 1
                print("Send cmd move forward_left")
            elif (glob.DATA_DECISION.message == Message.FORWARD_RIGHT):
                self.move = 1
                self.turn = 1
                self.enable = 1
                print("Send cmd move forward_right")
            elif (glob.DATA_DECISION.message == Message.BACKWARD):
                self.move = -1
                self.turn = 0
                self.enable = 1
                print("Send cmd move backward")
            elif (glob.DATA_DECISION.message == Message.BACKWARD_LEFT):
                self.move = -1
                self.turn = -1
                self.enable = 1
                print("Send cmd move backward_left")
            elif (glob.DATA_DECISION.message == Message.BACKWARD_RIGHT):
                self.move = -1
                self.turn = 1
                self.enable = 1
                print("Send cmd move backward_right")
            elif (glob.DATA_DECISION.message == Message.LEFT):
                self.move = 0
                self.turn = -1
                self.enable = 1
                print("Send cmd turn left")
            elif (glob.DATA_DECISION.message == Message.RIGHT):
                self.move = 0
                self.turn = 1
                self.enable = 1
                print("Send cmd turn right")
            elif (glob.DATA_DECISION.message == Message.STOP):
                self.move = 0
                self.turn = 0
                self.enable = 0
                print("Send cmd move stop")

            if self.enable:
                cmd_mv = (50 + self.move * self.speed_cmd) | 0x80
                cmd_turn = 50 + self.turn * 20 | 0x80
            else:
                cmd_mv = 0x00
                cmd_turn = 0x00
                #cmd_mv = (50 + self.move * self.speed_cmd) & ~0x80
                #cmd_turn = 50 + self.turn * 20 & 0x80

            #Create message threw the CAN with the compute command
            msg = can.Message(arbitration_id=0x010, data=[cmd_mv, cmd_mv, cmd_turn, 0x00, 0x00, 0x00, 0x00, 0x00], extended_id=False)

            #Message stopping the car
            #msg = can.Message(arbitration_id=0x010,data=[0x00,0x00,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)

            #Simple message example to go forward
            #msg = can.Message(arbitration_id=MCM,data=[0xBC,0xBC,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)

            self.bus.send(msg)
