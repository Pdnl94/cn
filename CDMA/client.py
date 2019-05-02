#!/usr/bin/python

import sys
import socket
import struct

def CDMA_coding(chipSequence, bitSequence):
	result = ""

	for b in bitSequence:
		if b == "1":
			for ch in chipSequence:
				result += ch
		else:
			for ch in chipSequence:
				if ch == "1":
					result += "-1"
				else:
					result += "0"

	return result

def send_msg(connection, msg):
	if(len(msg) >= 2 and sys.argv[1] != msg[0]):
		print "<" + sys.argv[1] + "> " + msg

		# Get chipSequence of receiver
		connection.send(msg[0])
		receiverChipSequence = connection.recv(4)
		print receiverChipSequence

		# Send CDMA crypted message to server
		connection.send(CDMA_coding(receiverChipSequence, msg[1:9]))
		packed_data = connection.recv(32)

# Begins here
if(len(sys.argv) == 2):

	# Create connection with server
	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server_addr = ('localhost', 10001)
	connection.connect(server_addr)

	# Send ID to server
	connection.send(sys.argv[1])
	chipSequence = connection.recv(4)
	print "My chipSequence: " + chipSequence

	# Send messages
	if(sys.argv[1] == "A"):
		send_msg(connection, "C10010011")

	print "Close the client"
	connection.close()
else:
	print "Error: bad arg list, expected number: 1"
