#!/usr/bin/python

import socket
import struct
import sys

# Create socket and connect
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
connection.connect(server_address)

# Set the values, and send to server
values = (sys.argv[1], sys.argv[2])

packer = struct.Struct('14s 16s')
packed_data = packer.pack(*values)

connection.sendall(packed_data)
print "Data sent to server."

# Receive result from server
result = ""
for i in range(0, len(sys.argv[2])):
  partial_result = connection.recv(3)
  result += "(" + partial_result[0] + partial_result[1] + partial_result[2] + "), "

print "Result received: " + result[:-2]

connection.close()
