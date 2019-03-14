import socket
import struct
import select
import queue

server_address = ('', 10000)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(server_address)
server.listen(1)

#server.settimeout(1.0)

inputs = [server]
timeout = 1

msg_q = queue.Queue()
username = {}

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
				user = client.recv(20).decode()
				username[client] = user.strip()
				msg_q.put("["+user+"] is LOGIN")
			else:
				data = s.recv(200)
				if data:
					msg_q.put(data.decode())
				else:
					msg_q.put("["+user+"] is LOGOUT")
					if s in writeable:
						writeable.remove(s)
					print("Kliens kilepett")
					inputs.remove(s)
					s.close()
	
		while not msg_q.empty():
			try:
				next_msg = msg_q.get_nowait()
			except Queue.empty():
				break
			else:
				for s in writeable:
					s.sendall(next_msg.encode())
					print("SEND ", username[s], next_msg)
	except socket.timeout:
		pass
	except socket.error as m:
		print(m)
	except KeyboardInterrupt:
		inputs.remove(server)
		for c in inputs:
			c.close()
		server.close()