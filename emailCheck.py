#!/usr/bin/python3

import sys
import imaplib
import email
import os
import argparse

# Define those functions first

# Count of unread emails
def count_mails(server):
	rv, data = server.search(None, 'ALL')
	if rv != 'OK':
		print("Error getting \# of messages")
		return

	#data contains all the mail id's -- count them
	mails = str(data[0], encoding='UTF-8') # decode from bstring
	total = mails.split()		# split into list based on spaces
	numOfMails = len(total)
	return numOfMails
# End of def

## Body here

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Checks change in number of emails within a mailbox.')
	parser.add_argument('-q','--quiet', help='Only outputs up/down/same', action='store_true')
	parser.add_argument('-m','--mailbox', help='Choose a folder other than inbox', default='INBOX')
	args = parser.parse_args()

	home = os.path.expanduser('~')
	path = home + '/.gpass'
	if os.path.isfile(path):
		with open(path,'r') as file:
			lines=file.readlines()
			username = lines[0]
			password = lines[1]
	else:
		print("~/.gpass not found - please add username and password to file on seperate lines")
		exit()

	firstRun = True

	counter = 0 ## Presume we have no value

	if os.path.isfile('/var/tmp/fishtank'):
		print('File found at /var/tmp/fishtank')
		with open("/var/tmp/fishtank",'r') as file:
			counter = int(file.read())
			firstRun = False
	else:
		print('File not found at /var/tmp/fishtank - we will create it as we finish')


	## Where are we connecting to?
	server = imaplib.IMAP4_SSL('imap.gmail.com')

	try:
		server.login(username,password)
	except imaplib.IMAP4.error:
		print("Login Failed!")
		exit()

	# rv is response code (expect OK), data is returned data

	rv, data = server.select(args.mailbox)
	if rv == 'OK':
		if firstRun == True:
			firstrun = False
			counter = count_mails(server)

		count = count_mails(server)
		server.close()

		if count > counter:
			if args.quiet: print("up")
			else: print("Number of emails in inbox: %i - more than previously" %count)
		elif count == counter:
			if args.quiet: print("same")
			else: print("Same number of emails in inbox: %i" %count)
		else:
			if args.quiet: print ("down")
			else :print("Number of emails in inbox: %i - less than previously" %count)

		# Write out counter value
		if os.path.isfile('/var/tmp/fishtank'):
			with open("/var/tmp/fishtank", 'w') as file:
				file.write(str(count))

	server.logout()

