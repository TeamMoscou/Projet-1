import time
import can
import os
import struct


#Not use in the project, functionnality to turn on itself using only motor wheels
OM1 = 0x101

toutDroit = can.Message(arbitration_id=0x010,data=[0xbc,0xbc,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
tournerDroit = can.Message(arbitration_id=0x010,data=[0xc4,0xa0,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
tournerGauche = can.Message(arbitration_id=0x010,data=[0xa0,0xc4,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
arret = can.Message(arbitration_id=0x010,data=[0x00,0x00,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
tournerMouvDroit = can.Message(arbitration_id=0x010,data=[0xbc,0xbc,0xbc, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
    
def tourner_Droit(bus,angleTournage):
    while True:
        msg = bus.recv()
        if msg.arbitration_id == OM1:
            yaw = struct.unpack('>f',msg.data[0:4])
            angle = int(yaw[0])
            print("angle 0 : " + str(angle))
            break
    angleObj = angle - angleTournage
    print("angle Obj : " + str(angleObj))
    if angleObj < -180:
        angleObj = 360 + angleObj
    print("angle Obj : " + str(angleObj))
    bus.send(tournerDroit)
    while True:
        msg = bus.recv()
        if msg.arbitration_id == OM1:
            yaw = struct.unpack('>f',msg.data[0:4])
            print("angle : " + str(int(yaw[0])))
            if (int(yaw[0])) >= angleObj-3 and  (int(yaw[0])) <= angleObj+3 : break 
            #if (int(yaw[0])) >= angleObj and  (int(yaw[0])) > 0 : break 
            #if (int(yaw[0])) <= angleObj and  (int(yaw[0])) < 0 : break 
    bus.send(arret) 

def tourner_mouv_Droit(bus,angleTournage):
    while True:
        msg = bus.recv()
        if msg.arbitration_id == OM1:
            yaw = struct.unpack('>f',msg.data[0:4])
            angle = int(yaw[0])
            print("angle 0 : " + str(angle))
            break
    angleObj = angle - angleTournage
    print("angle Obj : " + str(angleObj))
    if angleObj < -180:
        angleObj = 360 + angleObj
    print("angle Obj : " + str(angleObj))
    bus.send(tournerMouvDroit)
    while True:
        msg = bus.recv()
        if msg.arbitration_id == OM1:
            yaw = struct.unpack('>f',msg.data[0:4])
            print("angle : " + str(int(yaw[0])))
            if (int(yaw[0])) >= angleObj-3 and  (int(yaw[0])) <= angleObj+3 : break 
    bus.send(arret) 

def tourner_Gauche(bus,angleTournage):
    while True:
        msg = bus.recv()
        if msg.arbitration_id == OM1:
            yaw = struct.unpack('>f',msg.data[0:4])
            angle = int(yaw[0])
            print("angle 0 : " + str(angle))
            break
    angleObj = angle + angleTournage
    print("angle Obj : " + str(angleObj))
    if angleObj > 180:
        angleObj = -360 + angleObj
    print("angle Obj : " + str(angleObj))
    bus.send(tournerGauche)
    while True:
        msg = bus.recv()
        if msg.arbitration_id == OM1:
            yaw = struct.unpack('>f',msg.data[0:4])
            print("angle : " + str(int(yaw[0])))
            if (int(yaw[0])) >= angleObj-3 and  (int(yaw[0])) <= angleObj+3 : break 
    bus.send(arret) 
