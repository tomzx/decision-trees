import dress.dress
import dress.undress


def call(person, remove, put):
    dress.undress.call(person, remove)
    dress.dress.call(person, put)
