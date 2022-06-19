import dress.wear
import generic.go_to
from clothes import Clothes
from location import Location


# TODO: Convert to Items
# params: to (put everything until that part, included)
def call(person, to, location: Location):
    location = "bedroom closet" if location is None else location
    generic.go_to.call(person, location)

    # todo: support a more complicated/configurable state machine
    clothes = [
        Clothes.Underwear,
        Clothes.Socks,
        Clothes.Pants,
        Clothes.Shorts,
        Clothes.Shirt,
        Clothes.Shoes,
        Clothes.Coat,
        Clothes.Hat,
        Clothes.Gloves,
    ]

    for cloth in clothes:
        # todo: pick
        dress.wear.call(person, cloth, location)
        if cloth == to:
            break
