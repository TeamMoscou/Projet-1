# coding: utf-8
import threading
import can
import time
import glob
import os
from glob import *


#la valeur retournée par le capteur d'angle des roues en position milieu
theta=1650


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
        delta_cmd_turn = 0
        prev_steer_angle=None

        while True:
            
            msg = bus.recv();# Wait until a message is received.
            
            #steering control
            if msg.arbitration_id == MS:
                          
                 steer_angle = int.from_bytes(msg.data[0:2], byteorder='big')
                 if prev_steer_angle==None :
                        prev_steer_angle=steer_angle
                 elif abs(prev_steer_angle-steer_angle)>15 :
                        continue
                 prev_steer_angle=steer_angle

                 #print("steering angle", steer_angle)
                 delta_angle=  - steer_angle
				 #si delta_angle<0 -> les roues sont déviés vers la gauche -> tourner à droit
				 #si delta_angle>0 -> les roues sont déviés vers la droit ->  tourner à gauche
                 #print("Kp*Delta angle",Kp*delta_angle)
                 delta_cmd_turn=int(Kp*delta_angle)
				 cmd_turn = (50 + delta_cmd_turn) | 0x80
            
                 #print("delta command turn", delta_cmd_turn)
                
                
            self.speed_cmd = 25
            if (glob.DATA_DECISION.message == Message.FORWARD):
                self.move = 1
                #self.turn = 0
                self.enable = 1
                print("send cmd move forward")
            elif (glob.DATA_DECISION.message == Message.FORWARD_LEFT):
                self.move = 1
                #self.turn = -1
                self.enable = 1
                print("send cmd move forward_left")
            elif (glob.DATA_DECISION.message == Message.FORWARD_RIGHT):
                self.move = 1
                #self.turn = 1
                self.enable = 1
                print("send cmd move forward_right")
            elif (glob.DATA_DECISION.message == Message.BACKWARD):
                self.move = -1
                #self.turn = 0
                self.enable = 1
                print("send cmd move backward")
            elif (glob.DATA_DECISION.message == Message.BACKWARD_LEFT):
                self.move = -1
                #self.turn = -1
                self.enable = 1
                print("send cmd move backward_left")
            elif (glob.DATA_DECISION.message == Message.BACKWARD_RIGHT):
                self.move = -1
                #self.turn = 1
                self.enable = 1
                print("send cmd move backward_right")
            elif (glob.DATA_DECISION.message == Message.LEFT):
                self.move = 0
                #self.turn = -1
                self.enable = 1
                print("send cmd turn left")
            elif (glob.DATA_DECISION.message == Message.RIGHT):
                self.move = 0
                #self.turn = 1
                self.enable = 1
                print("send cmd turn right")
            elif (glob.DATA_DECISION.message == Message.STOP):
                self.move = 0
                #self.turn = 0
                self.enable = 0
                print("send cmd move stop")

 #           print("Data decision: ", DATA_DECISION.message)

            if self.enable:
                cmd_mv = (50 + self.move * self.speed_cmd) | 0x80
                #cmd_turn = 50 + self.turn * 20 | 0x80
            else:
                cmd_mv = 0x00
                #cmd_turn = 0x00
                #cmd_mv = (50 + self.move * self.speed_cmd) & ~0x80
                #cmd_turn = 50 + self.turn * 20 & 0x80

#            print("mv:", cmd_mv, "turn:", cmd_turn)
            msg = can.Message(arbitration_id=0x010, data=[cmd_mv, cmd_mv, cmd_turn, 0x00, 0x00, 0x00, 0x00, 0x00], extended_id=False)
              
            #msg = can.Message(arbitration_id=0x010,data=[0x00,0x00,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
            # msg = can.Message(arbitration_id=MCM,data=[0xBC,0xBC,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
            #print(msg)
            self.bus.send(msg)
