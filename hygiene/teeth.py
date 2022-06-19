import generic.pick
import generic.put

from item import Item
from location import Location, Person

def brush(teeth):
	print('brush %s teeth' % teeth)

def call(person):
	generic.pick.call(person, Item('toothbrush', Location('dental kit')))
	generic.pick.call(person, Item('toothpaste', Location('dental kit')))
	print('apply toothpaste to toothbrush')
	generic.put.call(person, Item('toothpaste', Person), Location('dental kit'))
	print('apply water to toothbrush')
	brush('outside top left')
	brush('outside top front')
	brush('outside top right')
	brush('outside bottom left')
	brush('outside bottom front')
	brush('outside bottom right')
	brush('top left molar')
	brush('top right molar')
	brush('bottom left molar')
	brush('bottom right molar')
	brush('inside top left')
	brush('inside top front')
	brush('inside top right')
	brush('inside bottom left')
	brush('inside bottom front')
	brush('inside bottom right')
	print('spit toothpaste')
	print('rinse toothbrush')
	generic.put.call(person, Item('toothbrush', Person), Location('dental kit'))
