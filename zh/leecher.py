import socket

tracker_address = ('127.0.0.1', 7777)
tracker = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tracker.sendto("leecher".encode(),tracker_address)
seeder, address = tracker.recvfrom(4096)
seeder = seeder.split(';'.encode())
    
seeder_address = (seeder[0],int(seeder[1]))

leecher = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
leecher.connect(seeder_address)

leecher.sendall("request".encode())
msg = leecher.recv(255)
print (msg)

leecher.close()