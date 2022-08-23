#!/usr/bin/python3

# Start process to run a command via a telnet session and listen for the output
# Created Apr 2020
# Tim Bowers

import getpass
import time
import pexpect
import datetime
from time import sleep
import argparse
import string
import sys

def check_device(user, host, password, command):

        ## We can't use pxssh because it tries to change the prompt which doesn't work

        #print ("Connecting to %s@%s, checking for backup file from %s" % (user,host,date))

        # sleep(3)
        child = pexpect.spawn('/usr/bin/telnet %s' % (host))
        # child.logfile = open("/home/tim/cpbackup.log", "w")
        #print ("Connecting via SSH")
        child.expect('login:')
        child.sendline(user)
        child.expect('password:')
        child.sendline(password)
        print ("Logged in successfully")
        print (child.before.decode())
        child.sendline(command)
        sleep(1)
        child.interact()


if __name__ == '__main__':

        parser = argparse.ArgumentParser()
        parser.add_argument('-ho', "--host", help="host ip to connect to")
        parser.add_argument('-u', "--user", help="Username to use when connecting")
        parser.add_argument('-pw', "--password", help="Telnet Password")
        parser.add_argument('-c', "--command", help="Command to execute")


        args = parser.parse_args()

        if not args.host:
                host=input("IP of device: ")
                if not host:
                        print("Please set an IP to continue")
                        sys.exit(2)
        else:
                host = args.host

        if not args.user:
                user=input("Username: ")
                if not user:
                        print("Please set a username to continue")
                        sys.exit(2)
        else:
                user = args.user

        if not args.password:
                print ("Enter password")
                password = getpass.getpass()
                if not password:
                        print("Without a password, we cannot connect")
                        sys.exit(2)
        else:
                password = args.password


        if not args.command:
                command=input("command: ")
                if not command:
                        print("Please set a command to continue")
                        sys.exit(2)
        else:
                command = args.command



        results = check_device(user, host, password, command)
        print(results)
