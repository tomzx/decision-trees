import computer.browse
import generic.go_to
import location

def call(person):
    # Precondition
    generic.go_to.call(person, location.Computer)
    # Actions
    computer.browse.call(person, "https://www.youtube.com/")
    computer.browse.call(person, "https://news.ycombinator.com/best")
    print("check slack")
    print("irc")
