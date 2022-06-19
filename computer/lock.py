import generic.go_to
import location

def call(person):
    # Precondition
    generic.go_to.call(person, location.Computer)
    # Actions
    print("press windows key")
    print("press l key")
    print("release l key")
    print("release windows key")
