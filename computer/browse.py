import generic.go_to
import location

def call(person, url):
    # Precondition
    generic.go_to.call(person, location.Computer)
    # Actions
    print("browse to %s" % url)
