import generic.go_to
import generic.pick
import generic.put
from item import Item
from location import Location


def call(person):
    generic.go_to.call(person, "bedroom closet")
    generic.pick.call(person, Item("laundry basket", Location("floor")))
    generic.go_to.call(person, "laundry room")
    generic.put.call(person, Item("laundry basket", Location("floor")))
    generic.pick.call(person, Item("clothes", Location("laundry basket")))
    generic.go_to.call(person, "laundry room")
    generic.pick.call(person, Item("detergent", Location("cupboard")))
    generic.pick.call(person, Item("dryer sheet", Location("cupboard")))
    generic.go_to.call(person, "laundry room")
    generic.put.call(person, Item("dryer sheet", Location("dryer")))
    generic.put.call(person, Item("clothes", Location("washer")))
    generic.put.call(person, Item("detergent", Location("washer")))
    generic.pick.call(person, Item("clothes", Location("washer")))
    generic.put.call(person, Item("clothes", Location("dryer")))
    generic.pick.call(person, Item("clothes", Location("dryer")))
    generic.go_to.call(person, "bedroom")
    generic.put.call(person, Item("clothes", Location("bed")))
    print("fold clothes")
    generic.pick.call(person, Item("clothes", Location("bed")))
    generic.go_to.call(person, "bedroom closet")
    generic.put.call(person, Item("clothes", Location("storage space")))
    generic.go_to.call(person, "laundry room")
    generic.pick.call(person, Item("laundry basket", Location("floor")))
    generic.go_to.call(person, "bedroom closet")
    generic.put.call(person, Item("laundry basket", Location("floor")))
