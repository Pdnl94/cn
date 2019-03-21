import socket

server_address = ('localhost',10000)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

with open("input.txt","rb") as f:
	l = f.read(1)
	while (l):
		client.sendto(l, server_address)
		print("Send:",l.decode())
		l = f.read(1)
client.sendto("".encode(), server_address)
client.close()
print("Done")