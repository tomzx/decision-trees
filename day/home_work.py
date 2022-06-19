import eat.dinner
import eat.lunch
import generic.go_to
import generic.work
import plan.home_work
from generic.askBoolean import askBoolean


def call(person):
    plan.home_work.call(person)
    print("record day plan video")

    generic.go_to.call(person, "computer")
    generic.work.call(person, [])

    eat.lunch.call(person)

    generic.go_to.call(person, "computer")
    generic.work.call(person, [])

    eat.dinner.call(person)

    generic.go_to.call(person, "computer")
    generic.work.call(person, [])

    print("record day completion video")
