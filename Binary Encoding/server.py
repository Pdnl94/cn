#!/usr/bin/python

import socket
import struct

# Functions
def handle_binary_encoding(connection, encoding, code):
  if encoding[:14] == "DiffManchester":
    perform_DiffManchester_encoding(connection, code)

  elif encoding[:5] == "NRZ-L":
    perform_NRZL_encoding(connection, code)

  elif encoding[:10] == "Manchester":
    perform_Manchester_encoding(connection, code)

  elif encoding[:2] == "RZ":
    perform_RZ_encoding(connection, code)

  else:
    print "Encoding is not correct."

def perform_DiffManchester_encoding(connection, code):
  print "Start DiffManchester encoding..."

  lastByte = '0'

  for i in code:
    if i == '1':
      if lastByte == '0':
        connection.sendall('011')
        lastByte = '1'
      else:
        connection.sendall('100')
        lastByte = '0'

    else:
      if lastByte == '0':
        connection.sendall('100')
        lastByte = '0'
      else:
        connection.sendall('011')
        lastByte = '1'

def perform_NRZL_encoding(connection, code):
  print "Start NRZ-L encoding..."

  for i in code:
      if i == '1':
        connection.sendall('111')
      else:
        connection.sendall('000')

def perform_Manchester_encoding(connection, code):
  print "Start Manchester encoding..."

  for i in code:
    if i == '1':
      connection.sendall('100')
    else:
      connection.sendall('011')

def perform_RZ_encoding(connection, code):
  print "Start RZ encoding..."

  for i in code:
    if i == '1':
      connection.sendall('100')
    else:
      connection.sendall('000')

# Create socket, start listening
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.settimeout(10)

server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(1)

# Accept client messages
while True:
  try:
    connection, client_address = sock.accept()
    print "----\nClient connected."

    data = connection.recv(30)

    unpacker = struct.Struct('14s 16s')
    unpacked_data = unpacker.unpack(data)
    print "Received data:", unpacked_data[0], unpacked_data[1]

    handle_binary_encoding(connection, unpacked_data[0], unpacked_data[1].rstrip('\x00'))
    print "Result sent to client.\n----"

  except socket.timeout:
    print "Timed out, no more responses ..."
    break

  except KeyboardInterrupt:
    print "\nServer shut down."
    break

sock.close()
