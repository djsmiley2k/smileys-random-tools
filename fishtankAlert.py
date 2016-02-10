#!/usr/bin/python3

import sys
import imaplib
import getpass
import email
import datetime

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

server = imaplib.IMAP4_SSL('imap.gmail.com')

try:
	server.login(username,password)
except imaplib.IMAP4.error:
	print("Login Failed!")
	exit

# rv is response code (expect OK), data is returned data

rv, data = server.select("INBOX")
if rv == 'OK':
	count = count_mails(server)
	server.close()
	try:
		print("Number of emails in inbox: %i" %count)
	except:
		print("failed to get number of emails")

server.logout()
