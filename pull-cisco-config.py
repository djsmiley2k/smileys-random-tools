#!/usr/bin/python3

# Pull Cisco config when given ip, username, password
# Created Feb 2019
# Tim Bowers, djsmiley2k@gmail.com

## Connect via ssh
## Save config back via scp

import getpass
import time
import pexpect
import datetime
from time import sleep
import argparse
import sys

## We can't use pxssh because it tries to change the prompt which doesn't work

parser = argparse.ArgumentParser()
parser.add_argument('-ho', "--host", help="host ip to connect to")
parser.add_argument('-hn', "--hostname", help="hostname of the device - used for saving the file")
parser.add_argument('-u', "--user", help="Username to use when connecting")
parser.add_argument('-d', "--destination", help="Destination IP for tftp copy")

args = parser.parse_args()

if not args.host:
        host=input("IP of the device: ")
        if not host:
                print("Please set an IP to continue")
                sys.exit(2)
else:
        host = args.host

if not args.hostname:
        hostname=input("Hostname of device: ")
        if not hostname:
                print("Please set a hostname to continue")
                sys.exit(2)
else:
        hostname =  args.hostname

if not args.user:
        user=input("Username: ")
        if not user:
                print("Please set a username to continue")
                sys.exit(2)
else:
        user = args.user

if not args.destination:
        destination=input("TFTP Destination: ")
        if not destination:
                print("Please set a destination for tftp copy to continue")
                sys.exit(2)
else:
        destination = args.destination

now = datetime.datetime.now()
date = now.strftime("%Y-%b-%d")

print ("Connecting to %s@%s, file will be saved with name: %s-%s.txt, press ctrl+C to cancel" % (user,host,hostname,date))

sleep(3)

print ("Enter ssh password")
password = getpass.getpass()

print ("Enter enable password")
enable_password = getpass.getpass()

child = pexpect.spawn('/usr/bin/ssh %s@%s' % (user,host))
print ("Connecting via SSH")
child.expect('assword:')
child.sendline(password)
child.expect('>')
print ("Logged in successfully")
child.sendline('en')
child.expect('assword:')
child.sendline(enable_password)
child.expect('#')
child.sendline("copy start tftp://%s/%s-%s.txt" %(destination,hostname,date))
child.expect(']?')
child.sendline()
child.expect(']?')
child.sendline()
sleep(1)
child.expect('#')
child.sendline('exit')
print ("Copy finished, terminating in 5 seconds")
sleep(5)
child.sendline('exit')
exit(0)
