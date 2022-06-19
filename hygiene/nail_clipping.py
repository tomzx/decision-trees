import generic.go_to
import generic.pick
import generic.put
import location
from item import Item
from location import Location


def trimNail(nail):
    print(f"trim {nail}")


def call(person):
    generic.go_to.call(person, location.BathRoom)
    generic.pick.call(person, Item("nail clipper", Location("cupboard")))
    print("close toilet seat")
    print("sit down on toilet seat")
    generic.pick.call(person, Item("trash bin", location.Kitchen))
    generic.put.call(person, Item("trash bin", location.Person), location.BathRoom)
    trimNail("left little toe")
    trimNail("left ring toe")
    trimNail("left middle toe")
    trimNail("left long toe")
    trimNail("left big toe")
    trimNail("right little toe")
    trimNail("right ring toe")
    trimNail("right middle toe")
    trimNail("right long toe")
    trimNail("right big toe")
    trimNail("left thumb")
    trimNail("left index finger")
    trimNail("left middle finger")
    trimNail("left ring finger")
    trimNail("left little finger")
    trimNail("right thumb")
    trimNail("right index finger")
    trimNail("right middle finger")
    trimNail("right ring finger")
    trimNail("right little finger")
    generic.pick.call(person, Item("trash bin", location.BathRoom))
    generic.put.call(person, Item("trash bin", location.Person), location.Kitchen)
    generic.put.call(
        person, Item("nail clipper", location.Person), Location("cupboard")
    )
