import socket

server_address = ('localhost',10000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(server_address)

with open("input.txt","rb") as f:
	l = f.read(1)
	while (l):
		client.sendall(l)
		print("Send:",l.decode())
		l = f.read(1)
client.sendall("".encode())
client.close()
print("Done")