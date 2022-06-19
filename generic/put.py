from typing import Union

import generic.go_to
from item import Item
from location import Location, Person


def call(person, item: Union[str, Item], location: Union[str, Location] = None):
    if item.location != Person:
        raise RuntimeError(
            f"Item {item} is not on person (is in/on {item.location}), cannot put it in/on {location}..."
        )

    if location is not None:
        generic.go_to.call(person, location)

    person.items.remove(item)
    if item is Item:
        item.location = location

    print(f"put {item} in/on {location}")
