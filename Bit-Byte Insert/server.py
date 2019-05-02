#!/usr/bin/python

import socket

TIME_OUT = 10000

codebook = {'FLAG': '01111110',
			'A': 	'10000001',
			'B': 	'00001110',
			'C': 	'10110011',
			'D': 	'11100110',
			'ESC': 	'01110000'}

def get_key_by_value(value):

	for key, tmp_val in codebook.items():
		if value == tmp_val:
			return key

def unlock_message(insert_type, locked_message):
	unlocked_message = ""

	if insert_type == 'bit': # BIT

		tmp_message = ""
		number_of_ones = 0
		for i in range(8, len(locked_message) - 8):

			if locked_message[i] == '1' and number_of_ones < 5:
				tmp_message += '1'
				number_of_ones += 1
				continue

			if number_of_ones == 5:
				number_of_ones = 0
				continue

			if locked_message[i] == '0':
				tmp_message += '0'
				number_of_ones = 0

		for i in range(0, len(tmp_message) - 7, 8):
			key = get_key_by_value(tmp_message[i:i + 8])
			unlocked_message += key + ','

	else: # BYTE

		ESC_need_to_be_removed = True

		for i in range(8, len(locked_message) - 8, 8):
			key = get_key_by_value(locked_message[i:i + 8])

			if key == 'ESC' and ESC_need_to_be_removed == False:
				unlocked_message += key + ','
				ESC_need_to_be_removed = True
				continue

			elif key == 'ESC': #ESC need to be removed is True
				ESC_need_to_be_removed = False
				continue
			else:
				unlocked_message += key + ','
				ESC_need_to_be_removed = True

	return unlocked_message[:-1]

# Create socket, start listening
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.settimeout(TIME_OUT)

server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(1)

while True:
  try:
    connection, client_address = sock.accept()
    print "----\nClient connected."

    insert_type = connection.recv(4).rstrip()
    print "Inserting type: " + insert_type

    locked_message = connection.recv(1000)
    print "Message received from client:\n" + locked_message + "\n"

    unlocked_message = unlock_message(insert_type, locked_message)
    print "The original message is: " + unlocked_message

  except socket.timeout:
    print "Timed out, no more responses ..."
    break

  except KeyboardInterrupt:
    print "\nServer shut down."
    break

sock.close()
