from typing import Optional, Union

import generic.go_to
from item import Item
from location import Location, Person


def call(person, item: Union[str, Item]):
    generic.go_to.call(person, item.location)

    print(f"pick {item} in/on {item.location}")

    item.location = Person
    person.items.add(item)
