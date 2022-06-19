import computer.browse
import generic.go_to

def call(person):
	# Precondition
	generic.go_to.call(person, 'computer')
	# Actions
	print('check slack')
	computer.browse.call(person, 'https://mail.google.com/mail/u/0/#inbox')
	print('check irc')
