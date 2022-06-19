import computer.browse
import generic.go_to
import location

def call(person):
    # Precondition
    generic.go_to.call(person, location.Computer)
    # Actions
    print("check slack")
    computer.browse.call(person, "https://mail.google.com/mail/u/0/#inbox")
    print("check irc")
