import generic.go_to
import location

def call(person):
    # Precondition
    generic.go_to.call(person, location.Computer)
    # Actions
    print("press any key on the keyboard")
    print("release pressed key on the keyboard")
