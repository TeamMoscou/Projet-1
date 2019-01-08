# coding: utf-8
import threading
import can
import time
import glob
import os
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
        cmd_mv = 50
        cmd_turn = 50
        delta_angle=0.0
        while True:
            
           
            self.speed_cmd = 25
            if (glob.DATA_DECISION.message == Message.FORWARD):
                self.move = 1
                theta=1650; #l'angle de consigne pour dresser les roues
                self.enable = 1
                print("send cmd move forward")
                
            elif (glob.DATA_DECISION.message == Message.FORWARD_LEFT):
                self.move = 1
                theta=2096; #l'angle de consigne pour tourner à gauche
                self.enable = 1
                print("send cmd move forward_left")
                
            elif (glob.DATA_DECISION.message == Message.FORWARD_RIGHT):
                self.move = 1
                theta=1292; #l'angle de consigne pour tourner à droite
                self.enable = 1
                print("send cmd move forward_right")
            elif (glob.DATA_DECISION.message == Message.BACKWARD):
                self.move = -1
                theta=1650; #l'angle de consigne pour dresser les roues
                self.enable = 1
                print("send cmd move backward")
                
            elif (glob.DATA_DECISION.message == Message.BACKWARD_LEFT):
                self.move = -1
                theta=2096; #l'angle de consigne pour tourner à gauche
                self.enable = 1
                print("send cmd move backward_left")
                
            elif (glob.DATA_DECISION.message == Message.BACKWARD_RIGHT):
                self.move = -1
                theta=1292; #l'angle de consigne pour tourner à droite
                self.enable = 1
                print("send cmd move backward_right")
                
            elif (glob.DATA_DECISION.message == Message.LEFT):
                self.move = 0
                theta=2096;#l'angle de consigne pour tourner à gauche
                self.enable = 1
                print("send cmd turn left")
                
            elif (glob.DATA_DECISION.message == Message.RIGHT):
                self.move = 0
                theta=1292; #l'angle de consigne pour tourner à droite
                self.enable = 1
                print("send cmd turn right")
                
            elif (glob.DATA_DECISION.message == Message.STOP):
                self.move = 0
                theta=1650; #l'angle de consigne pour dresser les roues
                self.enable = 0
                print("send cmd move stop")

            print("Data decision: ", glob.DATA_DECISION.message)
            
            delta_angle=20 ;#pour rentrer au moins une fois
            delta_cmd_turn = 0
            prev_current_angle=None

            if (abs(delta_angle)>=5):
                while abs(delta_angle)>=5: #boucle de regulation de l'angle de rotation des roues avec theta comme consigne 
                    print("le while")
                    msg = self.bus.recv();# Wait until a message is received.
                    
                    if msg.arbitration_id == glob.MS:
                        print("if message arbitration")
                        #récuperer l'angle actuelle
                        current_angle = int.from_bytes(msg.data[0:2], byteorder='big')
                        
                        #une sorte de filtrage pour éliminer des points bruités 
                        """
                        if prev_current_angle==None :
                                prev_current_angle=current_angle
                        elif abs(prev_current_angle-current_angle)>15 :
                                continue
                        prev_current_angle=current_angle
                        """
                        #print("steering angle", current_angle)
                         
                        delta_angle=  theta- current_angle
                        #si delta_angle<0 ==> les roues sont déviés vers la gauche ==> il faut tourner à droit
                        #si delta_angle>0 ==> les roues sont déviés vers la droit ==> il faut  tourner à gauche
                        #print("Kp*Delta angle",Kp*delta_angle)
                        delta_cmd_turn=int(glob.Kp*delta_angle)
                        if(delta_cmd_turn>=20):
                            delta_cmd_turn=20
                        elif delta_cmd_turn<=-20 :
                            delta_cmd_turn=-20
                        cmd_turn = (50 + delta_cmd_turn) | 0x80
                        print(delta_angle)
                        print("delta command turn", delta_cmd_turn)
                        
                    
                    if self.enable:
                        cmd_mv = (50 + self.move * self.speed_cmd) | 0x80
                    else:
                        cmd_mv = (50 + self.move * self.speed_cmd) & ~0x80

                    print("mv:", cmd_mv, "turn:", cmd_turn)
                    msg = can.Message(arbitration_id=0x010, data=[cmd_mv, cmd_mv, cmd_turn, 0x00, 0x00, 0x00, 0x00, 0x00], extended_id=False)
                    self.bus.send(msg)
            else:     
                print("le else")
                #envoyer la trame CAN correspondante
                if self.enable:
                        cmd_mv = (50 + self.move * self.speed_cmd) | 0x80
                else:
                        cmd_mv = (50 + self.move * self.speed_cmd) & ~0x80

                #print("mv:", cmd_mv, "turn:", cmd_turn)
                msg = can.Message(arbitration_id=0x010, data=[cmd_mv, cmd_mv,0x00, 0x00, 0x00, 0x00, 0x00, 0x00], extended_id=False)
                self.bus.send(msg)
