import socket
import struct
import select

server_address = ('', 10000)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(server_address)
server.listen(1)

#server.settimeout(1.0)

unpack = struct.Struct('I I 1s')

inputs = [server]
timeout = 1

while True:
	try:
		readable, writeable, excp = select.select(inputs,inputs,inputs,timeout)
		
		if not (readable or writeable or excp):
			continue
		for s in readable:
			if s is server:
				client, client_addr = s.accept()
				client.setblocking(1)
				inputs.append(client)
			else:
				data = s.recv(unpack.size)
				if data:
					unpacked_data = unpack.unpack(data)
					print("Kaptam: ", unpacked_data)
					
					x = eval(str(unpacked_data[0]) + unpacked_data[2].decode() + str(unpacked_data[1]))
			
					s.sendall(str(x).encode())
				else:
					s.close()
					print("Kliens kilepett")
					inputs.remove(s)
	except socket.timeout:
		pass
	except socket.error as m:
		print(m)
	except KeyboardInterrupt:
		inputs.remove(server)
		for c in inputs:
			c.close()
		server.close()