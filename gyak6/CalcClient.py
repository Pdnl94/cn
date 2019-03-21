import socket
import struct

server_address_udp = ('localhost',10000)
server_address_tcp = ('localhost',10001)
client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_tcp.connect(server_address_tcp)



packer = struct.Struct('I I 1s')

num1 = input("Kerek egy szamot:") #python2  raw_input()
op = input("Kerek egy operatort:")
num2 = input("Kerek egy masik szamot:")

values = ( int(num1), int(num2), op.encode() )

#packed_data = packer.pack(int(num1), int(num2), op.encode())
packed_data = packer.pack(*values)

# udp
client_udp.sendto(packed_data, server_address_udp)
r, _ = client_udp.recvfrom(20)
res = r.decode()
print("Eredmeny UDP: ",res)

# tcp
client_tcp.send(packed_data)
r = client_tcp.recv(20)
res = r.decode()
print("Eredmeny TCP: ",res)



client_tcp.close()
client_udp.close()


