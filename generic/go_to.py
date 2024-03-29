from typing import Union

from location import Location, Person


def call(person, location: Union[str, Location]):
    if type(location) is str:
        location = Location(location)

    # We don't need to go anywhere if the location is ourselves
    # TODO: Support going to a different person
    if location == Person:
        return

    prior_location = person.location
    if prior_location == location:
        return

    # Use this to diagnose what is know/not known in terms of locations
    # if location not in person.memory.locations.memory:
    # 	raise RuntimeError(f"Person currently doesn't know how to get to {location} (only knows about {person.memory.locations}")

    person.location = location
    person.memory.location = location
    person.memory.locations[location] = True
    print(f"go to/in {location} (was at/in {prior_location})")
