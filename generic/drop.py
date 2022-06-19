from typing import Optional, Union

from item import Item
from location import Location


def call(
    person, item: Union[str, Item], location: Optional[Union[str, Location]] = None
):
    person.items.remove(item)
    if item is Item:
        item.location = location

    if location:
        print(f"drop {item} in/on {location}")
    else:
        print(f"drop {item}")
