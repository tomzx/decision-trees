import computer.sleep
import computer.wake_up
import dress.change
import dress.dress
import dress.pick_clothes
import dress.undress
import eat.dinner
import eat.lunch
import eat.work_lunch
import generic.go_to
import generic.work
import location
from clothes import Clothes
from generic.choose import choose
from item import Item
from location import Home, Location, Work


def call(person):
    print("get ready for work")
    person.memory.remember(
        "will_eat",
        choose(
            "Do I make myself a lunch or eat outside?",
            ["lunch", "eat outside"],
            "lunch",
        ),
    )
    computer.sleep.call(person)
    dress.pick_clothes.call(person)
    generic.go_to.call(person, location.ComputerRoom)
    generic.go_to.call(person, "work computer")
    generic.work.call(person, [])
    print("stand up (1000-1015)")
    generic.go_to.call(person, "work computer")
    generic.work.call(person, [])
    eat.work_lunch.call(person)
    generic.go_to.call(person, "work computer")
    generic.work.call(person, [])
    generic.go_to.call(person, Home)
    dress.change.call(person, Clothes.Pants, Clothes.Shorts, location.BedRoomCloset)
    computer.wake_up.call(person)
    eat.dinner.call(person)
