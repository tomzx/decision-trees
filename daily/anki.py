import generic.go_to
import location

def call(person):
    # Precondition
    generic.go_to.call(person, location.Computer)
    # Actions
    print("open anki")
    deckChinese()


def deckChinese():
    print("study deck Chinese")
