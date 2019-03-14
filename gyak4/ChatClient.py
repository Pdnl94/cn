import socket
import sys
from input_timeout import readInput

username = sys.argv[1]

def prompt(nl):
	if nl:
		print("")
	print ("<"+username+">")
	
server_address = ('localhost',10000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)
client.sendall(username.encode())
client.settimeout(1.0)
prompt(False)

while True:
	try:
		data = client. recv(200)
		if not data:
			print ("Server down")
			break
		else:
			print(data.decode())
			prompt(False)
	except socket.timeout:
		pass
	except socket.error as m:
		print(m)
	
	try:
		msg = readInput().strip()
		if msg == 'exit':
			break
		elif msg != '':
			client.sendall(("["+username+"]: "+msg).encode())
			prompt(True)
	except socket.timeout:
		pass
	except socket.error as m:
		print(m)

client.close()