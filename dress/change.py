import dress.dress
import dress.undress
from location import Location


def call(person, remove, put, location: Location):
    dress.undress.call(person, remove)
    dress.dress.call(person, put, location)
