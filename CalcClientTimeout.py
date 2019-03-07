import socket
import struct
import time
import random

server_address = ('localhost', 10000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)

packer = struct.Struct('I I 1s')

operator = ['+','-','*','/','%']
for i in range(5):
	num1 = random.randint(1,100)
	op = operator[random.randint(0,4)]
	num2 = random.randint(1,100)

	values = (int(num1), int(num2), op.encode())
	print("Kuldom: ", values)
	packed_data = packer.pack(*values)

	client.sendall(packed_data)
	data = client.recv(20).decode()
	print("Eredmeny: ",data)
	time.sleep(2)
	
client.close()


