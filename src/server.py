# coding: utf-8

import socket
import time

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('localhost', 2345))

while True:
        socket.listen(5)
        client, address = socket.accept()
        print ("{} connected".format( address ))
        i =0
        while True:
                
                time.sleep(0.01)
                output = '&theta: '+ str(i) +' Dist: 03606.00 Q: 47'
                
                client.sendall(output.encode('utf-8'))
                i = (i+1)%360

print ("Close")
client.close()
stock.close()
