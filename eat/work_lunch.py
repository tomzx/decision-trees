import eat.eat
import eat.lunch
import generic.go_to
import generic.pick
import generic.put
from generic.askBoolean import askBoolean
from item import Item
from location import Location, Work


def call(person):
    if person.memory.recall("will_eat") == "lunch":
        eat.lunch.call(person)
    else:
        print("decide what/where to eat")
        generic.go_to.call(person, "restaurant")
        print("order")
        generic.pick.call(person, Item("order", Location("restaurant")))
        generic.go_to.call(person, Work)
        generic.go_to.call(person, "dinning room")
        generic.put.call(person, Item("order", Location("dinning table")))
        eat.eat.call(person)
        print("throw away garbage")
