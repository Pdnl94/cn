import socket
import struct

server_address = ('localhost', 10000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)

packer = struct.Struct('I I 1s')

num1 = input("Kerek egy szamot: ")
op = input("Kerek egy operatort: ")
num2 = input("Kerek meg egy szamot: ")

values = (int(num1), int(num2), op.encode())
packed_data = packer.pack(*values)

client.sendall(packed_data)
data = client.recv(20).decode()

print("Eredmeny: ",data)

client.close()


