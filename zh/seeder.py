import socket
import select

seeder_address = ('127.0.0.1', 10000)
target_dir = "files"

seeder = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
seeder.bind(seeder_address)
seeder.listen(0)
seeder.settimeout(1.0)

tracker_address = ('127.0.0.1', 7777)
tracker = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

conns = [seeder]

seeder_msg = "seeder;" + seeder_address[0] + ";" + str(seeder_address[1])
tracker.sendto(seeder_msg.encode(),tracker_address)
print ("sajt")

while True:
    try:
        read, write, exe = select.select(conns,conns,conns,1)
        for v in read:
            if v is seeder:
                ts,addr = seeder.accept()
                print (addr,"connected.")
                conns.append(ts)
            else:
                msg = v.recv(255)
                if "request".encode() in msg:
                    v.sendall("ZH".encode())
                else:
                    conns.remove(v)
                    
    except socket.error as msg:
        print (msg)

seeder.close()