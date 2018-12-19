import time
import can
import os
import struct
import Turn90

OM1 = 0x101

toutDroit = can.Message(arbitration_id=0x010,data=[0xbc,0xbc,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
tournerDroit = can.Message(arbitration_id=0x010,data=[0xc4,0xa0,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
tournerGauche = can.Message(arbitration_id=0x010,data=[0xa0,0xc4,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
arret = can.Message(arbitration_id=0x010,data=[0x00,0x00,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)

print('Bring up CAN0....')
os.system("sudo ifconfig can0 down")
os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
time.sleep(0.1)

print('Press CTL-C to exit')

try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
	print('Cannot find PiCAN board.')
	exit()

# Main loop
try:
    #msg = can.Message(arbitration_id=0x010,data=[0xc4,0xa0,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
    #bus.send(msg)
    #time.sleep(10.5)
    #msg = can.Message(arbitration_id=0x010,data=[0x00,0x00,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
    '''while True:
        msg = bus.recv()
        if msg.arbitration_id == OM1:
            yaw = struct.unpack('>f',msg.data[0:4])
            angle = int(yaw[0])
            print("angle 0 : " + str(angle))
            break
    bus.send(tournerDroit)
    while True:
        msg = bus.recv()
        if msg.arbitration_id == OM1:
            yaw = struct.unpack('>f',msg.data[0:4])
            print("angle : " + str(int(yaw[0])))
            if (int(yaw[0])) > angleObj and  (int(yaw[0])) < angleObj : break 
    bus.send(arret)'''      
    Turn90.tourner_Droit(bus,0)
    bus.send(toutDroit)
    time.sleep(2)
    bus.send(arret)
    Turn90.tourner_Gauche(bus,90)

except KeyboardInterrupt:
	#Catch keyboard interrupt
    #msg = can.Message(arbitration_id=0x010,data=[0x00,0x00,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
    bus.send(arret)
    os.system("sudo /sbin/ip link set can0 down")
print('\n\rKeyboard interrtupt')
