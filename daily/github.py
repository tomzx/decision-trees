import computer.browse
import generic.go_to
from generic.askBoolean import askBoolean


def call(person):
    # Precondition
    generic.go_to.call(person, "computer")

    if askBoolean("Did I commit something on github today?", "no"):
        return

    # Actions
    print("find a project to work on")
    print("implement change")
    print("git commit")
    print("git push")
    computer.browse.call(person, "github.com")
