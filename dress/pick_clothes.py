import dress.dress
import dress.undress
from clothes import Clothes
from generic.askBoolean import askBoolean


def call(person):
    if askBoolean("Is it cold outside?"):
        dress.dress.call(
            person, Clothes.Gloves
        )  # todo: there might be a clearer way to say we put on a coat, hat and gloves
    else:
        dress.dress.call(person, Clothes.Shoes)
