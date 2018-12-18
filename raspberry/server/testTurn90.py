import time
import can
import os
import struct

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
    msg = can.Message(arbitration_id=0x010,data=[0xc2,0xa2,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
    bus.send(msg)
    time.sleep(20)
    msg = can.Message(arbitration_id=0x010,data=[0x00,0x00,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
    bus.send(msg)

except KeyboardInterrupt:
	#Catch keyboard interrupt
    msg = can.Message(arbitration_id=0x010,data=[0x00,0x00,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
    bus.send(msg)
    os.system("sudo /sbin/ip link set can0 down")
print('\n\rKeyboard interrtupt')
