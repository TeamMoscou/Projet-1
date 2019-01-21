import time
import can
import os
import struct
import tourner

#File testing functions of tourner.py

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
    tourner.tourner_Droit(bus,45)


except KeyboardInterrupt:
    bus.send(arret)
    os.system("sudo /sbin/ip link set can0 down")
print('\n\rKeyboard interrtupt')
