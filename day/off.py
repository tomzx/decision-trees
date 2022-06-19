import eat.dinner
import eat.lunch
import generic.entertainment


def call(person):
    generic.entertainment.call(person)
    eat.lunch.call(person)
    generic.entertainment.call(person)
    eat.dinner.call(person)
    generic.entertainment.call(person)
