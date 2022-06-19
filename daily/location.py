from generic.choose import choose
from location import (
    BathRoom,
    BedRoom,
    ComputerRoom,
    Kitchen,
    LivingRoom,
    Location,
    Outside,
)


def call(person):
    location = choose(
        "Where am I?",
        [BedRoom, ComputerRoom, Kitchen, BathRoom, LivingRoom, Outside],
        BedRoom,
    )
    person.location = Location(str(location))
    person.memory.location = location
    person.memory.locations[location] = True
