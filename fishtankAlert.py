#!/usr/bin/python3

import sys
import imaplib
import email
import os

# Define those functions first

# Count of unread emails
def count_mails(server):
	rv, data = server.search(None, 'ALL')
	if rv != 'OK':
		print("Error getting \# of messages")
		return

	#data contains all the mail id's -- count them
	for mail in data:
		mails = str(mail, encoding='UTF-8') # decode from bstring
		total = mails.split()		# split into list based on spaces
		numOfMails = len(total)
		return numOfMails
# End of def

## Body here

if __name__ == '__main__':

	username = sys.argv[1]
	password = sys.argv[2]

	firstRun = True

	#try:
	#	f = open('/var/tmp/fishtank','r')
	#	counter = f.read()
	#	f.close()
	#except:


	counter = 0 ## Presume we have no value

	if os.path.isfile('/var/tmp/fishtank'):
		print('File found at /var/tmp/fishtank')
		with open("/var/tmp/fishtank",'r') as file:
			counter = int(file.read())
			firstRun = False
	else:
		print('File not found at /var/tmp/fishtank')


	## Where are we connerting to?
	server = imaplib.IMAP4_SSL('imap.gmail.com')

	try:
		server.login(username,password)
	except imaplib.IMAP4.error:
		print("Login Failed!")
		exit

	# rv is response code (expect OK), data is returned data

	rv, data = server.select("INBOX")
	if rv == 'OK':
		if firstRun == True:
			firstrun = False
			counter = count_mails(server)

		count = count_mails(server)
		server.close()

		if count > counter:
			print("Number of emails in inbox: %i - more than previously" %count)
		elif count == counter:
			print("Same number of emails in inbox: %i" %count)
		else:
			print("Number of emails in inbox: %i - less than previously" %count)

		# Write out counter value
		if os.path.isfile('/var/tmp/fishtank'):
			with open("/var/tmp/fishtank", 'w') as file:
				file.write(str(count))

		#try:
		#	f = open('/var/tmp/fishtank','w')
		#	f.write(counter)
		#	f.close()
		#except:
		#	print("Failed to write to /var/tmp/fishtank - check permissions")

	server.logout()

