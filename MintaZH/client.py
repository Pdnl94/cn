#!/usr/bin/python

import sys
import socket
import struct

# Create TCP socket, and  connect
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10001)
connection.connect(server_address)

# Send message
values = (123, 2, '*')
packer = struct.Struct('i i c')
packed_data = packer.pack(*values)

connection.sendall(packed_data)

connection.close()