import dress.undress
import generic.go_to
from clothes import Clothes


def call(person):
    generic.go_to.call(person, "bedroom")
    dress.undress.call(person, Clothes.Socks)
    generic.go_to.call(person, "bed")
    print("lay on horizontal flat surface")
    print("close eyes")
    person.state["eyes"] = "closed"
    print("switch mode to system/unconscious")
    person.state["overall"] = "asleep"
