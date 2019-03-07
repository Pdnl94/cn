import socket
import struct

server_address = ('', 10000)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(server_address)
server.listen(1)

server.settimeout(1.0)

unpack = struct.Struct('I I 1s')

while True:
	try:
		client, client_addr = server.accept()
		client.setblocking(1)
		
		data = client.recv(unpack.size)
		unpacked_data = unpack.unpack(data)
		print("Kaptam: ", unpacked_data)
		
		x = eval(str(unpacked_data[0]) + unpacked_data[2].decode() + str(unpacked_data[1]))
		
		client.sendall(str(x).encode())
		client.close()
	except socket.timeout:
		pass
	except socket.error as m:
		print(m)		