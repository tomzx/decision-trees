import generic.drop
import generic.go_to
import generic.pick
import location
from item import Item
from location import Location, Person


def call(person):
    generic.go_to.call(person, location.BathRoom)
    generic.pick.call(person, Item("dental floss", Location("dental kit")))
    print("floss top gum from right to left")
    print("floss bottom gum from right to left")
    generic.drop.call(person, Item("dental floss", Person), Location("garbage bin"))
