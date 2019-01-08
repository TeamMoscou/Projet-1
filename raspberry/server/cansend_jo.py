# coding: utf-8
import threading
import can
import time
import glob
from glob import *

class Can_send(threading.Thread):
    def __init__(self, bus):
        threading.Thread.__init__(self)
        self.bus = bus
        glob.DATA_DECISION = Data(ID.DECISION, Message.STOP)  
        #global test_dec

    def run(self):
        self.speed_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0
        while True:
            time.sleep(0.1)
            self.speed_cmd = 25
            if (glob.DATA_DECISION.message == Message.FORWARD):
                self.move = 1
                self.turn = 0
                self.enable = 1
                print("send cmd move forward")
            elif (glob.DATA_DECISION.message == Message.FORWARD_LEFT):
                self.move = 1
                self.turn = -1
                self.enable = 1
                print("send cmd move forward_left")
            elif (glob.DATA_DECISION.message == Message.FORWARD_RIGHT):
                self.move = 1
                self.turn = 1
                self.enable = 1
                print("send cmd move forward_right")
            elif (glob.DATA_DECISION.message == Message.BACKWARD):
                self.move = -1
                self.turn = 0
                self.enable = 1
                print("send cmd move backward")
            elif (glob.DATA_DECISION.message == Message.BACKWARD_LEFT):
                self.move = -1
                self.turn = -1
                self.enable = 1
                print("send cmd move backward_left")
            elif (glob.DATA_DECISION.message == Message.BACKWARD_RIGHT):
                self.move = -1
                self.turn = 1
                self.enable = 1
                print("send cmd move backward_right")
            elif (glob.DATA_DECISION.message == Message.LEFT):
                self.move = 0
                self.turn = -1
                self.enable = 1
                print("send cmd turn left")
            elif (glob.DATA_DECISION.message == Message.RIGHT):
                self.move = 0
                self.turn = 1
                self.enable = 1
                print("send cmd turn right")
            elif (glob.DATA_DECISION.message == Message.STOP):
                self.move = 0
                self.turn = 0
                self.enable = 0
                print("send cmd move stop")

 #print("Data decision: ", DATA_DECISION.message)

            if self.enable:
                cmd_mv = (50 + self.move * self.speed_cmd) | 0x80
                cmd_turn = 50 + self.turn * 20 | 0x80
            else:
                cmd_mv = 0x00
                cmd_turn = 0x00
                #cmd_mv = (50 + self.move * self.speed_cmd) & ~0x80
                #cmd_turn = 50 + self.turn * 20 & 0x80

#            print("mv:", cmd_mv, "turn:", cmd_turn)
            msg = can.Message(arbitration_id=0x010, data=[cmd_mv, cmd_mv, cmd_turn, 0x00, 0x00, 0x00, 0x00, 0x00], extended_id=False)
              
            #msg = can.Message(arbitration_id=0x010,data=[0x00,0x00,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
            # msg = can.Message(arbitration_id=MCM,data=[0xBC,0xBC,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
            #print(msg)
            self.bus.send(msg)
