#!/usr/bin/python3

# Automated pulling of all cisco configs
# Created Feb 2019
# Tim Bowers, PCMS Group

## Connect to Primary firewall and get copy of the config
## Connect to Secondary firewall and get copy of the config
## Return state of copies, possibly return line highlighting for changes

import getpass
import time
import pexpect
import datetime
from time import sleep
import sys
import subprocess
import difflib

## We can't use pxssh because it tries to change the prompt which doesn't work

now = datetime.datetime.now()
date = now.strftime("%Y-%b-%d")

## For each ip, hostname pair - pull the configs

print ("Enter ssh password")
password = getpass.getpass()
print ("Enter enable password")
enable_password = getpass.getpass()
print ("Enter destination IP")


f = open("sites.txt", "r")

for line in f:
        host1 = line.split(",")[0]
        hostname = line.split(",")[1]
        hostname1 = hostname.rstrip()

        print ('Running config pull on %s named %s copying to %s' % (destination,host1,hostname1))

        child1 = pexpect.spawn('/usr/bin/ssh networks@%s' % (host1))
        try:
                child1.expect('assword:')
                child1.sendline(password)
                child1.expect('>')
                print ("Logged in successfully")
                child1.sendline('en')
                child1.expect('assword:')
                child1.sendline(enable_password)
                child1.expect('#')
                child1.sendline("copy start tftp://%s/%s-%s.txt" %(destination,hostname1,date))
                child1.expect(']?')
                child1.sendline()
                child1.expect(']?')
                child1.sendline()
                sleep(1)
                child1.expect('#')
                child1.sendline('exit')
                print ("Copy finished, terminating in 5 seconds")
                sleep(5)
                child1.sendline('exit')
                child1.close()

        except pexpect.TIMEOUT :
                print('Timed out connecting to %s - %s' % (host1,hostname1))

        except pexpect.EOF :
                print('EOF Recieved, connecting to %s - %s' % (host1,hostname1))

print ("Finished copying files")
