from typing import Optional

import dress.remove
from clothes import Clothes
from location import Location


# TODO: Convert to Items
# params: to (remove everything until that part, included)
def call(person, to, location: Optional[Location] = None):
    # todo: support a more complicated/configurable state machine
    clothes = [
        Clothes.Gloves,
        Clothes.Hat,
        Clothes.Coat,
        Clothes.Shoes,
        Clothes.Shirt,
        Clothes.Shorts,
        Clothes.Pants,
        Clothes.Socks,
        Clothes.Underwear,
    ]

    for cloth in clothes:
        dress.remove.call(person, cloth, location)
        # todo: drop
        if cloth == to:
            break
