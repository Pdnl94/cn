import socket

tracker_address = ('127.0.0.1', 7777)

tracker = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tracker.bind(tracker_address)
tracker.settimeout(1.0)

seeder = ""

while True:
    try:
        msg, address = tracker.recvfrom(4096)
        if "seeder".encode() in msg:
            seeder = msg[7:]
            print (seeder)
        elif "leecher".encode() in msg:
            tracker.sendto(seeder,address)
            pass
        else:
            print ("weird msg")
    except socket.error as msg:
        print (msg)


tracker.close() 