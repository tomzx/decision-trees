import generic.pick
import generic.put
import location
from item import Item
from person import Person


def call(person: Person):
    generic.pick.call(person, Item("deodorant", location.BathRoom))
    generic.put.call(person, Item("deodorant", location.Person), location.Person)
