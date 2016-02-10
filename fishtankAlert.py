#!/usr/bin/python3

import sys
import imaplib
import email
import pathlib

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




username = sys.argv[1]
password = sys.argv[2]

firstRun = 1

#try:
#	f = open('/var/tmp/fishtank','r')
#	counter = f.read()
#	f.close()
#except:


counter = 0 ## Presume we have no value

if path.is_file('/var/tmp/fishtank'):
	with open("/var/tmp/fishtank") as file:
		counter = file.read()

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
	if firstRun == 1:
		firstrun = 0
		counter = count_mails(server)

	count = count_mails(server)
	server.close()

	if count > counter
		print("Number of emails in inbox: %i - more than previously" %count)
	else:
		print("Number of emails in inbox: %i - less than previously" %count)

	# Write out counter value
	try:
		f = open('/var/tmp/fishtank','w')
		f.write(counter)
		f.close()
	except:
		print("Failed to write to /var/tmp/fishtank - check permissions")
server.logout()

