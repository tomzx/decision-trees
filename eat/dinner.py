import eat.eat
import eat.wash_dishes
import generic.go_to


def call(person):
    generic.go_to.call(person, "kitchen")
    print("decide what to eat")
    print("prepare meal")
    generic.go_to.call(person, "dinning room")
    eat.eat.call(person)
    eat.wash_dishes.call(person)
