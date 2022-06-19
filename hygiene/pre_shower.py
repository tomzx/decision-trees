import dress.undress
import generic.go_to
import generic.pick
import generic.put
import location
from item import Item
from location import BedRoomCloset, Location, Person


def call(person):
    generic.pick.call(person, Item("new underwear", BedRoomCloset))
    generic.go_to.call(person, location.BathRoom)
    generic.put.call(person, Item("new underwear", Person), Location("shelf"))
    dress.undress.call(person, None, Location("bathroom floor"))
    generic.pick.call(person, Item("towel", Location("shower curtain rod")))
    generic.put.call(person, Item("towel", Person), Location("toilet seat"))
