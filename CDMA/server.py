#!/usr/bin/python

import select
import socket
import sys
import struct
import Queue
import time

chipSeq1 = "0001"
chipSeq2 = "0010"
chipSeq3 = "0100"
chipSeq4 = "1000"

class CDMAServer:
  def __init__(self, msgLen = 8, addr='localhost', port=10001, incomingMsgTimeout=10, outgoingMsgTimeout = 1):
    self.server = self.setupServer(addr, port)
    # Sockets from which we expect to read
    self.inputs = [ self.server ]
    # Sockets to which we expect to write
    self.outputs = []
    self.usernameToChipSeq = {}
    self.vectorLen = msgLen * len(chipSeq1)
    self.initJointTransmissionVector()
    self.initChipSeqs()
    self.incomingMsgTimeout = incomingMsgTimeout
    self.outgoingMsgTimeout = outgoingMsgTimeout
    self.packerForTransmission = struct.Struct('b' * self.vectorLen)

  def setupServer(self, addr, port):
    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the port
    server_address = (addr, port)
    server.bind(server_address)
    
    # Listen for incoming connections
    server.listen(5)
    return server
  
  def initChipSeqs(self):
    self.chipSeqs = Queue.Queue()
    self.chipSeqs.put(chipSeq1)
    self.chipSeqs.put(chipSeq2)
    self.chipSeqs.put(chipSeq3)
    self.chipSeqs.put(chipSeq4)

  def initJointTransmissionVector(self):
    self.jointTransmissionVector = [0] * self.vectorLen # e.g. if vectorLen = 16 --> jointTransmissionVector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

  def doInterference(self, unpackedMsg):
    for idx in range(0, self.vectorLen):
      self.jointTransmissionVector[idx] += unpackedMsg[idx]

  def handleNewConnection(self, sock):
    # A "readable" server socket is ready to accept a connection
    connection, client_address = sock.accept()
    connection.settimeout(1.0)
    data = connection.recv(20)
    username = data.strip()
    print >>sys.stderr, 'new connection from', client_address, "with username", username
    try:
      currentChipSeq = self.chipSeqs.get_nowait()
    except Queue.Empty:
      currentChipSeq = "NNNN" # There are no more chip sequences
    connection.sendall(currentChipSeq)
    self.usernameToChipSeq[username] = currentChipSeq
    self.inputs.append(connection)
    self.outputs.append(connection)

  def handleSocketError(self, err, sock):
    errorcode=err[0]
    if errorcode == 10054: # WSAECONNRESET
        print >>sys.stderr, 'The connection was forcibly closed by', str(sock.getpeername())
        # Stop listening for input on the connection
        if sock in self.outputs:
            self.outputs.remove(sock)
        self.inputs.remove(sock)
    else:
        raise # Re-throwing exception

  def handleClosedConnection(self, sock):
    # Interpret empty result as closed connection
    print >>sys.stderr, 'closing', str(sock.getpeername()), 'after reading no data'
    # Stop listening for input on the connection
    if sock in self.outputs:
        self.outputs.remove(sock)
    self.inputs.remove(sock)
    sock.close()

  def handleDataFromClient(self, sock):
    try:
        data = sock.recv(20)
    except socket.error as err:
        self.handleSocketError(err, sock)
    else:
        if data:
            receiver = data.strip()
            receiverChipSeq = self.usernameToChipSeq[receiver]
            sock.sendall(receiverChipSeq)
            try:
              msg = sock.recv(self.vectorLen)
            except socket.error as err:
              self.handleSocketError(err, sock)
            else:
              if msg:
                unpackedMsg = self.packerForTransmission.unpack(msg)
                self.doInterference(unpackedMsg)
              else:
                self.handleClosedConnection(sock)
        else:
            self.handleClosedConnection(sock)

  def handleInputs(self, readable):
    for sock in readable:
        if sock is self.server:
            self.handleNewConnection(sock)
        else:
            self.handleDataFromClient(sock)

  def handleOutputs(self, writable):
    for sock in writable:
      packedJointTransmissionMsg = self.packerForTransmission.pack(*self.jointTransmissionVector)
      sock.sendall(packedJointTransmissionMsg)

  def handleExceptionalCondition(self, exceptional):
    for sock in exceptional:
      print >>sys.stderr, 'handling exceptional condition for', str(sock.getpeername())
      # Stop listening for input on the connection
      self.inputs.remove(sock)
      if sock in self.outputs:
          self.outputs.remove(sock)
      sock.close()

  def handleConnections(self):
    while self.inputs:
      try:
        startTime = time.time()
        self.initJointTransmissionVector()
        while True:
          readable, writable, exceptional = select.select(self.inputs, [], self.inputs, self.incomingMsgTimeout)
          self.handleInputs(readable)
          self.handleExceptionalCondition(exceptional)
          if (time.time() - startTime) > self.incomingMsgTimeout: # if there is an interrupt the remaining time must be checked
            break
        if self.outputs:
          readable, writable, exceptional = select.select([], self.outputs, self.outputs, self.outgoingMsgTimeout)
          if not (readable or writable or exceptional):
            continue
          self.handleOutputs(writable)
          self.handleExceptionalCondition(exceptional)
      except KeyboardInterrupt:
        print "Close the system"
        for c in self.inputs:
            c.close()
        self.inputs = []

cdmaServer = CDMAServer()
cdmaServer.handleConnections()