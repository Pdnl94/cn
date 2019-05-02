#!/usr/bin/python

import sys
import socket

# Create UDP socket
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10002)
udp_server.bind(server_address)

while True:
	data, address = udp_server.recvfrom(200)
	print "Result received from TCP server: " + data
	