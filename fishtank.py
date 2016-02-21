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
	while x < 5:
		#result = sock.recv(4096)
		sock.sendall(msg)
		#print(result)
		time.sleep(0.8)
		blank = '{"color":[0,0,0],"command":"color","priority":1}\n' # Black
		sock.sendall(blank.encode('utf8'))
		time.sleep(0.3)
		x += 1
	# Reset to previous state
	time.sleep(0.5)
	clear = '{"command":"clear","priority":1}\n'
	sock.sendall(clear.encode('utf8'))

# Main function

if __name__ == '__main__':

	red = [255,0,0]
	green = [0,255,0]
	blue = [0,0,255]

	#response = subprocess.call(["./emailCheck.py", "-q"])
	response = subprocess.check_output(['./emailCheck.py', '-q'])
	if response == b'up\n':
		message = '{"color":[0,255,0],"command":"color","priority":1}\n'
		flash_lights('192.168.1.47', 19444, message.encode('utf8'))
