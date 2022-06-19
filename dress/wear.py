import generic.pick
import generic.put
from item import Item
from location import Location, Person


def call(person, cloth, location: Location):
    if cloth not in person.clothes:
        person.clothes.add(cloth)
        generic.pick.call(person, Item(cloth, location))
        generic.put.call(person, Item(cloth, Person), Person)
