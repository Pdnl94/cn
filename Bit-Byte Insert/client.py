#!/usr/bin/python

import socket
import sys

# Check sysargv
if len(sys.argv) != 3:
	print "Wrong arguments. Shutting down...\nExpected 2 arguments: inserting type (bit, byte) and message.\n"
	sys.exit()

codebook = {'FLAG': '01111110',
			'A': 	'10000001',
			'B': 	'00001110',
			'C': 	'10110011',
			'D': 	'11100110',
			'ESC': 	'01110000'}

def create_message(insert_type, plain_msg):
	new_msg = codebook['FLAG'] # First FLAG

	if insert_type == 'bit': # BIT	
		for i in plain_msg.split(","):
			new_msg += codebook[i]

		i = 7
		number_of_ones = 0
		end_loop = len(new_msg)

		while i < end_loop - 1:

			i += 1
			if new_msg[i] == '1' and number_of_ones < 5:
				number_of_ones += 1
				continue

			if number_of_ones == 5:
				number_of_ones = 0
				new_msg = new_msg[:i] + '0' + new_msg[i:]
				end_loop += 1
				continue

			if new_msg[i] == '0':
				number_of_ones = 0

	else: # BYTE
		for i in plain_msg.split(","):
			if i == 'FLAG' or i == 'ESC':
				new_msg += codebook['ESC']

			new_msg += codebook[i]


	new_msg += codebook['FLAG'] # Last FLAG
	return new_msg

# Create socket and connect
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
connection.connect(server_address)

# Set inserting method, and send to server
insert_type = sys.argv[1]
plain_msg = sys.argv[2]

if insert_type == 'bit': # BIT INSERTING
	print "-- Insert type: 'bit' sent to server successfully."
	connection.sendall('bit ')

elif insert_type == 'byte': # BYTE INSERTING
	print "-- Insert type: 'byte' sent to server successfully."
	connection.sendall('byte')

else: # ERROR HANDLING
	print "-- Inserting type is not correct. Shutting down ...\n"
	sys.exit()

new_msg = create_message(insert_type, plain_msg)

if new_msg != "":
	connection.sendall(new_msg)
	print "-- Message successfully sent to server.\n"
else:
	print "-- Given message was wrong. Shutting down ...\n"
	sys.exit()

connection.close()
