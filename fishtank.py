#!/usr/bin/python3

# Fishtank master control unit

# We expect Rainbow Swirl or other suitable effect to be running at priority 100

import socket
import time
import subprocess

import emailCheck
# Define those functions first


def flash_lights(server, port, msg):
	x = 0
	# echo '{"color":[0,255,0],"command":"color","priority":1}' | nc localhost 19444
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	sock.connect( (server, port) )
	while x > 3:
		sock.sendall(msg)
		time.sleep(0.5)
		sock.sendall('{"color":[0,0,0],"command":"color","priority":1}') # Black
		time.sleep(0.2)
		x += 1
	# Reset to previous state
	sock.sendall('{"command":"clear","priority":1}')

# Main function

if __name__ == '__main__':

	red = [255,0,0]
	green = [0,255,0]
	blue = [0,0,255]

	#response = subprocess.call(["./emailCheck.py", "-q"])
	response = subprocess.check_output(['./emailCheck.py', '-q'])
	print(response)
	if response == "b'up\n'":
		print("flashing lights!")
		flash_lights('192.168.1.47', '19444', '{"color":[0,255,0],"command":"color","priority":1}')
	else:
		print("no flashing here :( ")
