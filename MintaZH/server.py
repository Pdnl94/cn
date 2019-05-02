#!/usr/bin/python

import sys
import socket
import struct
import select

def calculateResult(lhs, rhs, operator):
  result = 0

  if operator == '+':
    result = lhs + rhs

  elif operator == '-':
    result = lhs - rhs

  elif operator == '*':
    result = lhs * rhs

  elif operator == '/':
    result = lhs / rhs

  return result

# Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10001)
server.setblocking(1)
server.bind(server_address)
server.listen(1)

# Create UDP socket
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_serveraddr  = ('localhost', 10002)

# Accept client requests
inputs = [server]
outputs = []

while inputs:
  try:
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    for sock in readable:
      if sock is server:
        connection, client_address = sock.accept()
        inputs.append(connection)

      else:
        packed_data = sock.recv(200)
        unpacker = struct.Struct('i i c')
        unpacked_data = unpacker.unpack(packed_data)
        inputs.remove(connection)

        print "Calculated result sent to UDP server"
        udp_server.sendto(str(calculateResult(unpacked_data[0], unpacked_data[1], unpacked_data[2])), udp_serveraddr)

  except KeyboardInterrupt:
    print "\nTCP Server is interrupted by user"
    exit()

server.close()