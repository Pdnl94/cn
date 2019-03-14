import socket

server_address = ('',10000)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_address)
server.listen(5)

while True:
	client, client_addr = server.accept()
	with open("recv.txt","wb") as f:
		l = client.recv(1)
		print("RECV: ",l.decode())
		while (l):
			f.write(l)
			l = client.recv(1)
			print("RECV: ",l.decode())
		client.close()
	print("Done")