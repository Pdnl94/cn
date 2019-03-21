import socket

server_address = ('',10000)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind(server_address)

server.settimeout(1.0)

while True:
	data, client_addr = server.accept()
	with open("recv.txt","wb") as f:
		l = data.recv(1)
		print("RECV: ",l.decode(), client_addr)
		while (l):
			f.write(l)
			l = data.recv(1)
			print("RECV: ",l.decode(), client_addr)
	print("Done")