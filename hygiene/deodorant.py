import generic.go_to

import location
from item import Item
from person import Person

def call(person):
	generic.pick.call(person, Item("deodorant", location.BathRoom))
	generic.put.call(person, Item("deodorant", location.Person), location.Person)
